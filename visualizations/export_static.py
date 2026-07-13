"""Export standalone static HTML versions of each dashboard/story (no Flask server needed)."""
import sys, os
from build_dashboards import scenario1, scenario2, scenario3, story_scenes

PAGE_TMPL = """<!DOCTYPE html><html><head><meta charset="utf-8">
<title>{title}</title>
<script src="https://cdn.plot.ly/plotly-2.29.1.min.js"></script>
<style>
body{{background:#0f1720;color:#e8edf4;font-family:Segoe UI,Arial;margin:0;padding:24px;}}
h1{{margin-bottom:2px}} p.sub{{color:#9fb0c3;margin-top:0}}
.kpi-row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:20px 0}}
.kpi{{background:#182335;border:1px solid #2a3a52;border-radius:12px;padding:18px;text-align:center}}
.kpi-val{{font-size:1.7rem;font-weight:700;color:#ff6b6b}}
.kpi-lbl{{color:#9fb0c3;font-size:.82rem;margin-top:4px}}
.chart-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:18px}}
.chart-card{{background:#182335;border:1px solid #2a3a52;border-radius:14px;padding:10px}}
.scene{{margin-bottom:40px}} .scene-caption{{color:#9fb0c3;max-width:700px}}
</style></head><body>
<h1>{title}</h1><p class="sub">{subtitle}</p>
{body}
</body></html>"""

def save(name, title, subtitle, body):
    html = PAGE_TMPL.format(title=title, subtitle=subtitle, body=body)
    path = os.path.join(os.path.dirname(__file__), name)
    with open(path, "w") as f:
        f.write(html)
    print("wrote", path)

# Scenario dashboards
for fname, title, sub, fn in [
    ("dashboard_clinician.html", "Clinician Dashboard — Dr. Sharma", "Lifestyle risk factors in middle-aged patients", scenario1),
    ("dashboard_policy.html", "Policy Dashboard — Government Health Dept.", "Urban vs Rural prevalence & sedentary lifestyle correlation", scenario2),
    ("dashboard_personal.html", "Personal Risk Dashboard — Anita", "Your indicators vs healthy benchmarks", scenario3),
]:
    divs = fn()
    body = divs[0] + "<div class='chart-grid'>" + "".join(f"<div class='chart-card'>{d}</div>" for d in divs[1:]) + "</div>"
    save(fname, title, sub, body)

# Story
scenes = story_scenes()
body = ""
for name, caption, chart in scenes:
    body += f"<div class='scene'><h2>{name}</h2><p class='scene-caption'>{caption}</p><div class='chart-card'>{chart}</div></div>"
save("story.html", "The Story Behind the Numbers", "Five scenes tracing the biggest drivers of heart disease", body)
