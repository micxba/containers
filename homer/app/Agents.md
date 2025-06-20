# 🧭 Agents Guide for Sith Network Dashboard

This document provides a structured overview of how the **Sith Network Dashboard** is organized, how it should render pages and widgets, and where specific logic should live. This ensures consistency for both humans and AI agents (e.g., GitHub Copilot or Codex) extending or modifying this project.

---

## 🗂️ Project Structure

```
├── app.py                         # Main Flask application, routes and YAML page loading
├── config.yaml                   # Configuration file defining site layout, theme, pages, and widgets
├── requirements.txt             # Python dependencies (e.g., Flask, pyecharts, requests)
├── static/
│   ├── background.jpg           # Optional background image
│   ├── background.png           # Optional alternative background
│   ├── fonts/                   # Custom fonts (e.g., ImperialCode)
│   └── logo.png                 # Logo displayed on the dashboard
├── templates/
│   ├── base.html                # Main base layout template (includes logo, title, subtitle)
│   ├── page.html                # Dynamic page renderer; iterates over rows and cells
│   ├── <widget>_widget.html    # One per widget type (e.g., prometheus_widget.html, alertmanager_widget.html)
│   └── styles.css.j2           # CSS styles (rendered dynamically from theme in config.yaml)
└── widgets/
    ├── <widget>.py             # One Python module per widget (e.g., prometheus.py, alertmanager.py)
```

---

## 🧱 Layout Philosophy

The layout is **data-driven** and controlled entirely by `config.yaml`.

Each page is composed of rows and columns:

```yaml
pages:
  /:
    columns: 3
    rows:
      - span: 3
        widget: freetext
        name: Welcome
        configuration: |
          <h2>Welcome to Sith Network</h2>
          <p>This is your personalized control hub.</p>

      - span: 1
        widget: alertmanager
        name: Alert Summary
        configuration:
          url: https://alertmanager.sith.network
          group_by: job

      - span: 1
        widget: freetext
        name: Filler 1
        configuration: |
          <p>Placeholder text</p>

      - span: 1
        widget: freetext
        name: Filler 2
        configuration: |
          <p>Placeholder text</p>

      - span: 1
        widget: prometheus
        name: Memory Usage
        configuration:
          url: https://prometheus.sith.network
          query: 'sum(node_memory_MemTotal_bytes{} - node_memory_MemAvailable_bytes{}) / sum(node_memory_MemTotal_bytes{}) * 100'
          unit: percent
          visualization: gauge
          size: 250px

      - span: 1
        widget: prometheus
        name: CPU Usage
        configuration:
          title: "CPU Usage"
          chart_type: "line"
          prometheus_query: 'avg(rate(node_cpu_seconds_total{mode!="idle"}[5m])) * 100'
          url: https://prometheus.sith.network
          width: "100%"
          height: "400px"

      - span: 1
        widget: prometheus
        name: Disk Usage
        configuration:
          url: https://prometheus.sith.network
          query: 'sum(node_filesystem_size_bytes{fstype!~"tmpfs|overlay"} - node_filesystem_free_bytes{fstype!~"tmpfs|overlay"}) / sum(node_filesystem_size_bytes{fstype!~"tmpfs|overlay"}) * 100'
          unit: percent
          visualization: bar
          size: 250px
```

- `columns`: Total number of columns on the page.
- Each `row` defines a `span` (how many columns it takes).
- Each row must fill all columns (e.g., three `span: 1` blocks or one `span: 3` block).

---

## 🧩 Widget Design Rules

Each widget type **must** have:

1. A Python module in `widgets/<name>.py` implementing a function:
   ```python
   def render_chart(config) -> dict:
       return {"html": "<div>...</div>", "error": "optional error string"}
   ```

2. A Jinja2 template in `templates/<name>_widget.html` that:
   - Calls the widget’s render function (e.g. `render_chart(row.configuration)`)
   - Displays the returned HTML or a meaningful error message

Example `prometheus_widget.html`:
```html
{% set result = render_chart(row.configuration) %}
{% if result.error %}
  <div class="widget-placeholder">Error loading widget: {{ result.error }}</div>
{% else %}
  {{ result.html|safe }}
{% endif %}
```

---

## 🎨 Theming and Style

- Styling is defined in `styles.css.j2`, using values from `config.yaml > theme`
- Fonts, colors, logo, and background are configurable
- Glass-style (“liquid”) effect is preferred: light blur, soft shadows, no hover effects

Example theme block:
```yaml
theme:
  title_font_family: "ImperialCode2"
  title_font_file: "/static/fonts/ImperialCode2.ttf"
  general_content_font: "'Segoe UI', sans-serif"
  accent_color: "#FF4757"
  background_color: "#f5f5f5"
```

---

## ✅ Design Constraints

- All **widget-specific logic** must be fully contained within:
  - `widgets/<name>.py`
  - `templates/<name>_widget.html`

> ❌ No widget-specific logic should exist in `app.py` or `page.html`.

- This makes widgets portable and modular.
- `app.py` dynamically discovers widget templates and simply renders pages defined in `config.yaml`.

---

## 🚦 Rendering Flow Summary

1. `app.py` loads `config.yaml`, determines which page to render
2. `page.html` uses the `rows` and `columns` to layout the grid
3. For each widget in a cell:
   - Looks up the `<widget>_widget.html` template
   - That template calls `widgets/<widget>.py` to render content
4. Resulting HTML is inserted into the page
5. CSS and fonts are applied via `styles.css.j2`

---

## 🤖 Guidance for Codex

- Never add widget-specific logic to `app.py`, only modify `widgets/<name>.py` and `templates/<name>_widget.html`
- To add a new widget:
  1. Create `widgets/<newwidget>.py` with a `render_chart(config)` or `render_widget(config)`
  2. Create `templates/<newwidget>_widget.html` that calls the function
  3. Add widget entry in `config.yaml` under `pages[...]`
- Always ensure `config.yaml` layout fills all columns per row

---

## 🔍 Example Widget Entry

```yaml
- span: 1
  widget: prometheus
  name: Uptime
  configuration:
    url: http://prometheus:9090
    query: up{job="api"}
    chart_type: line
    title: API Uptime
```

---

Let me know if you’d like to:

- Document how `freetext` widgets work
- Add a template for embedding external content (like Grafana, status pages, etc.)
- Include widget development test tips (e.g., printing HTML to console)
