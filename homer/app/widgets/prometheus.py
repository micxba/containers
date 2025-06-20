import requests
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any

SPARKLINE_CHARS = '▁▂▃▄▅▆▇█'


def _format_value(val: float) -> str:
    if abs(val) >= 10:
        return f"{val:.1f}"
    return f"{val:.2f}"


def _apply_multiplier(val: float, multiplier: Any) -> float:
    try:
        mult = float(multiplier)
        if mult > 0:
            return val * mult
        elif mult < 0:
            return val / abs(mult)
    except (ValueError, TypeError):
        pass
    return val


def _normalize_sparkline(values: List[float], rules: List[Dict[str, str]]) -> str:
    if not values:
        return ""

    min_val = min(values)
    max_val = max(values)
    span = max_val - min_val or 1e-9
    buckets = len(SPARKLINE_CHARS) - 1

    spark = ""
    for v in values:
        char = SPARKLINE_CHARS[round((v - min_val) / span * buckets)]
        color = None
        for rule in sorted(rules, key=lambda r: r["gt"]):
            if v > rule["gt"]:
                color = rule["color"]
        if color:
            spark += f'<span class="color-{color}">{char}</span>'
        else:
            spark += char
    # print([(round(v, 1), color) for v in values])

    return spark



def _execute_scalar(url: str, query: str) -> float:
    resp = requests.get(f"{url}/api/v1/query", params={"query": query}, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "success":
        raise RuntimeError("query failed")
    result = data.get("data", {}).get("result")
    if not result:
        raise RuntimeError("no data")
    return float(result[0]["value"][1])


def _execute_sparkline(url: str, query: str, width: int, range_str: str) -> List[float]:
    now = int(time.time())
    unit_map = {"s": 1, "m": 60, "h": 3600}
    try:
        dur = int(range_str[:-1]) * unit_map[range_str[-1]]
    except Exception:
        raise ValueError("Invalid range format, expected e.g. '10m'")

    step = max(dur // width, 1)
    params = {
        "query": query,
        "start": now - dur,
        "end": now,
        "step": step,
    }
    resp = requests.get(f"{url}/api/v1/query_range", params=params, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "success":
        raise RuntimeError("query_range failed")
    result = data.get("data", {}).get("result")
    if not result:
        raise RuntimeError("no data")
    return [float(val[1]) for val in result[0]["values"]]


async def _gather_queries(url: str, queries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    loop = asyncio.get_event_loop()
    results = []

    with ThreadPoolExecutor() as pool:
        tasks = []
        for q in queries:
            query_str = q["query"].replace("$cluster", q.get("cluster", ""))
            mode = q.get("mode", "scalar")
            if mode == "sparkline":
                sparkline_cfg = q.get("sparkline", {})
                width = int(sparkline_cfg.get("width", 16))
                range_str = sparkline_cfg.get("range", "10m")
                task = loop.run_in_executor(pool, _execute_sparkline, url, query_str, width, range_str)
            else:
                task = loop.run_in_executor(pool, _execute_scalar, url, query_str)
            tasks.append(task)

        values = await asyncio.gather(*tasks, return_exceptions=True)

    for q, v in zip(queries, values):
        entry = {
            "key": q.get("key", q.get("query")),
            "unit": q.get("unit"),
            "mode": q.get("mode", "scalar"),
        }
        if isinstance(v, Exception):
            entry["error"] = str(v)
        else:
            if entry["mode"] == "sparkline":
                adjusted = [_apply_multiplier(x, q.get("unitMultiplier")) for x in v]
                rules = q.get("sparkline", {}).get("colorRules", [])
                entry["sparkline"] = _normalize_sparkline(adjusted, rules)          

                # Evaluate colorRules based on latest value
                color = None
                last = adjusted[-1] if adjusted else 0
                for rule in q.get("sparkline", {}).get("colorRules", []):
                    if "gt" in rule and last > rule["gt"]:
                        color = rule.get("color")
                if color:
                    entry["color"] = color
            else:
                adjusted = _apply_multiplier(v, q.get("unitMultiplier"))
                entry["value"] = _format_value(adjusted)

        results.append(entry)

    return results


def fetch_metrics(config: Dict[str, Any]) -> Dict[str, Any]:
    url = config.get("url")
    qcfg = config.get("query")
    if not url or not qcfg:
        return {"results": [], "error": "missing url or query"}

    queries = [qcfg] if isinstance(qcfg, dict) else qcfg if isinstance(qcfg, list) else [{"key": qcfg, "query": qcfg}]
    try:
        results = asyncio.run(_gather_queries(url, queries))
        return {"results": results}
    except Exception as e:
        return {"results": [], "error": str(e)}
