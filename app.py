"""
Flask Web Integration for the Heart Disease Analytics Project.

Embeds the dashboards (Scenario 1: Clinician view, Scenario 2: Policy view,
Scenario 3: Personal view) and the Story into a single responsive web app,
fulfilling the "Dashboard and Story embed with UI With Flask" requirement.

Run:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "visualizations"))

from flask import Flask, render_template
from build_dashboards import scenario1, scenario2, scenario3, story_scenes

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard/clinician")
def clinician():
    divs = scenario1()
    return render_template("dashboard.html",
                            title="Clinician Dashboard — Dr. Sharma",
                            subtitle="Lifestyle risk factors in middle-aged patients",
                            kpi=divs[0], charts=divs[1:])


@app.route("/dashboard/policy")
def policy():
    divs = scenario2()
    return render_template("dashboard.html",
                            title="Policy Dashboard — Government Health Dept.",
                            subtitle="Urban vs Rural prevalence & sedentary lifestyle correlation",
                            kpi=divs[0], charts=divs[1:])


@app.route("/dashboard/personal")
def personal():
    divs = scenario3()
    return render_template("dashboard.html",
                            title="Personal Risk Dashboard — Anita",
                            subtitle="Your indicators vs healthy benchmarks",
                            kpi=divs[0], charts=divs[1:])


@app.route("/story")
def story():
    scenes = story_scenes()
    return render_template("story.html", scenes=scenes)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
