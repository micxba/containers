import requests
from collections import defaultdict

def fetch_alerts(url):
    try:
        response = requests.get(f"{url}/api/v2/alerts", timeout=3)
        response.raise_for_status()
        return {"alerts": response.json()}
    except Exception as e:
        return {"alerts": [], "error": str(e)}

def group_alerts(alerts, group_by="severity"):
    grouped = defaultdict(list)
    for alert in alerts:
        key = alert.get("labels", {}).get(group_by, "unknown")
        grouped[key].append(alert)
    return dict(grouped)
