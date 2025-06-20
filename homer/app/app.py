from flask import Flask, render_template, Response, abort
import yaml
import os

from widgets.alertmanager import fetch_alerts, group_alerts
from widgets.prometheus import fetch_metrics

app = Flask(__name__)

def load_config():
    config_path = "config.yaml"
    if not os.path.exists(config_path):
        config_path = "config.yaml.template"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


config = load_config()

@app.route("/static/styles.css")
def serve_styles():
    return Response(
        render_template(
            "styles.css.j2",
            theme=config["theme"],
            pages=config.get("pages", {})  # ← added so styles.css.j2 can use {% for page in pages.values() %}
        ),
        mimetype="text/css"
    )

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_page(path):
    full_path = f"/{path}" if path else "/"
    page = config["pages"].get(full_path)
    if page is None:
        abort(404)

    return render_template(
        "page.html",
        title=config["title"],
        subtitle=config["subtitle"],
        menu=config["menu"],
        logo=config.get("logo"),
        theme=config["theme"],
        layout=page,
        fetch_alerts=fetch_alerts,
        group_alerts=group_alerts,
        fetch_metrics=fetch_metrics,
    )

if __name__ == "__main__":
    app.run(debug=True, port=5050)
