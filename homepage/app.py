import os
import yaml
import requests
from flask import Flask, render_template

app = Flask(__name__)

BOOKMARKS_PATH = os.environ.get("BOOKMARKS_PATH", "/config/bookmarks.yaml")
WIDGETS_PATH = os.environ.get("WIDGETS_PATH", "/config/widgets.yaml")

PROMETHEUS_URL = os.environ.get("PROMETHEUS_URL")  # Optional global override

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def fetch_prometheus_data(widget):
    try:
        url = widget.get("url", PROMETHEUS_URL)
        query = widget.get("query")
        if not url or not query:
            return None
        response = requests.get(f"{url}/api/v1/query", params={"query": query})
        result = response.json()
        if result["status"] == "success":
            return result["data"]["result"]
    except Exception as e:
        print(f"Error fetching Prometheus data: {e}")
    return None

@app.route("/")
def index():
    bookmarks = load_yaml(BOOKMARKS_PATH)
    widgets_config = load_yaml(WIDGETS_PATH)
    widgets = []

    for widget in widgets_config.get("widgets", []):
        widget_data = fetch_prometheus_data(widget)
        widgets.append({"title": widget.get("title"), "data": widget_data})

    return render_template("index.html", bookmarks=bookmarks, widgets=widgets)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)