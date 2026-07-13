"""
Builds the interactive dashboards for the Heart Disease project.

NOTE ON TOOLING: Tableau Desktop is a licensed, GUI-only application and
cannot run inside this automated environment. These dashboards are built
with Plotly (Python) to reproduce, chart-for-chart, what each Tableau
dashboard specified in the project brief would show (same fields, same
filters, same KPIs). They are exported as standalone interactive HTML and
also embedded into the Flask app. Section "Recreating in Tableau" in
docs/Documentation.md gives the exact shelf-by-shelf steps to rebuild the
same views in Tableau Desktop/Public once a license/seat is available.
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "heart_disease_clean.csv")
OUT = os.path.dirname(__file__)

df = pd.read_csv(DATA)
COLORS = {"bg": "#0f1720", "card": "#182335", "accent": "#ff6b6b", "accent2": "#4ecdc4",
          "text": "#e8edf4", "grid": "#2a3a52"}

TEMPLATE_LAYOUT = dict(
    paper_bgcolor=COLORS["bg"], plot_bgcolor=COLORS["bg"],
    font=dict(color=COLORS["text"], family="Segoe UI, Arial"),
    margin=dict(l=40, r=20, t=50, b=40),
)

def style(fig, title):
    fig.update_layout(title=dict(text=title, font=dict(size=16)), **TEMPLATE_LAYOUT)
    fig.update_xaxes(gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"])
    fig.update_yaxes(gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"])
    return fig

def to_div(fig):
    return fig.to_html(full_html=False, include_plotlyjs=False, config={"displaylogo": False})


# =====================================================================
# SCENARIO 1 — Dr. Sharma: lifestyle factors driving disease in
# middle-aged patients (Age / Gender / BMI / Cholesterol / Smoking)
# =====================================================================
def scenario1():
    divs = []

    # KPI numbers
    total = len(df)
    cases = df.heart_disease.sum()
    mid = df[df.age_group == "40-54 (Middle-aged)"]
    mid_rate = 100 * mid.heart_disease.mean()
    divs.append(f"""
    <div class='kpi-row'>
      <div class='kpi'><div class='kpi-val'>{total:,}</div><div class='kpi-lbl'>Patients Analyzed</div></div>
      <div class='kpi'><div class='kpi-val'>{cases:,}</div><div class='kpi-lbl'>Confirmed Cases</div></div>
      <div class='kpi'><div class='kpi-val'>{mid_rate:.1f}%</div><div class='kpi-lbl'>Middle-Aged (40-54) Disease Rate</div></div>
      <div class='kpi'><div class='kpi-val'>{100*cases/total:.1f}%</div><div class='kpi-lbl'>Overall Prevalence</div></div>
    </div>""")

    # Disease rate by age group & gender
    g = df.groupby(["age_group", "sex"], observed=True).heart_disease.mean().reset_index()
    g["rate_pct"] = g.heart_disease * 100
    fig1 = px.bar(g, x="age_group", y="rate_pct", color="sex", barmode="group",
                  color_discrete_map={"Male": COLORS["accent"], "Female": COLORS["accent2"]},
                  labels={"rate_pct": "Disease Rate (%)", "age_group": "Age Group"})
    style(fig1, "Heart Disease Rate by Age Group & Gender")
    divs.append(to_div(fig1))

    # Smoking status impact
    s = df.groupby("smoking_status", observed=True).heart_disease.mean().reset_index()
    s["rate_pct"] = s.heart_disease * 100
    s = s.sort_values("rate_pct", ascending=False)
    fig2 = px.bar(s, x="smoking_status", y="rate_pct", color="rate_pct",
                  color_continuous_scale=["#4ecdc4", "#ff6b6b"],
                  labels={"rate_pct": "Disease Rate (%)", "smoking_status": "Smoking Status"})
    style(fig2, "Impact of Smoking Habits on Disease Rate")
    divs.append(to_div(fig2))

    # BMI vs Cholesterol scatter colored by disease, sized by age
    fig3 = px.scatter(df, x="bmi", y="cholesterol", color=df.heart_disease.map({0: "No Disease", 1: "Disease"}),
                       color_discrete_map={"No Disease": COLORS["accent2"], "Disease": COLORS["accent"]},
                       opacity=0.6, labels={"bmi": "BMI", "cholesterol": "Cholesterol (mg/dl)", "color": "Status"})
    style(fig3, "BMI vs Cholesterol (colored by diagnosis)")
    divs.append(to_div(fig3))

    # BMI category breakdown
    b = df.groupby("bmi_category", observed=True).heart_disease.mean().reset_index()
    b["rate_pct"] = b.heart_disease * 100
    fig4 = px.pie(b, names="bmi_category", values="rate_pct", hole=0.5,
                  color_discrete_sequence=px.colors.sequential.RdBu)
    style(fig4, "Relative Disease Rate Share by BMI Category")
    divs.append(to_div(fig4))

    return divs


# =====================================================================
# SCENARIO 2 — Ramesh: regional (urban vs rural) prevalence &
# sedentary-lifestyle correlation for policy design
# =====================================================================
def scenario2():
    divs = []
    total_urban = df[df.region == "Urban"].heart_disease.mean() * 100
    total_rural = df[df.region == "Rural"].heart_disease.mean() * 100
    divs.append(f"""
    <div class='kpi-row'>
      <div class='kpi'><div class='kpi-val'>{total_urban:.1f}%</div><div class='kpi-lbl'>Urban Prevalence</div></div>
      <div class='kpi'><div class='kpi-val'>{total_rural:.1f}%</div><div class='kpi-lbl'>Rural Prevalence</div></div>
      <div class='kpi'><div class='kpi-val'>{100*df[df.physical_activity=="Sedentary"].heart_disease.mean():.1f}%</div><div class='kpi-lbl'>Sedentary Group Rate</div></div>
      <div class='kpi'><div class='kpi-val'>{100*df[df.physical_activity=="Active"].heart_disease.mean():.1f}%</div><div class='kpi-lbl'>Active Group Rate</div></div>
    </div>""")

    r = df.groupby(["region", "physical_activity"], observed=True).heart_disease.mean().reset_index()
    r["rate_pct"] = r.heart_disease * 100
    fig1 = px.bar(r, x="region", y="rate_pct", color="physical_activity", barmode="group",
                  color_discrete_sequence=["#ff6b6b", "#f7b733", "#4ecdc4"],
                  labels={"rate_pct": "Disease Rate (%)"})
    style(fig1, "Urban vs Rural Disease Rate by Activity Level")
    divs.append(to_div(fig1))

    d = df.groupby(["region", "diet_quality"], observed=True).heart_disease.mean().reset_index()
    d["rate_pct"] = d.heart_disease * 100
    fig2 = px.bar(d, x="diet_quality", y="rate_pct", color="region", barmode="group",
                  color_discrete_map={"Urban": COLORS["accent"], "Rural": COLORS["accent2"]},
                  labels={"rate_pct": "Disease Rate (%)"})
    style(fig2, "Diet Quality vs Disease Rate, by Region")
    divs.append(to_div(fig2))

    # Heatmap: activity x smoking, disease rate
    h = df.groupby(["physical_activity", "smoking_status"], observed=True).heart_disease.mean().reset_index()
    h["rate_pct"] = h.heart_disease * 100
    pivot = h.pivot(index="physical_activity", columns="smoking_status", values="rate_pct")
    fig3 = go.Figure(data=go.Heatmap(z=pivot.values, x=pivot.columns, y=pivot.index,
                                      colorscale="RdYlBu_r", text=pivot.round(1).values,
                                      texttemplate="%{text}%"))
    style(fig3, "Disease Rate Heatmap: Physical Activity x Smoking")
    divs.append(to_div(fig3))

    # Region population share
    fig4 = px.pie(df, names="region", hole=0.5, color="region",
                  color_discrete_map={"Urban": COLORS["accent"], "Rural": COLORS["accent2"]})
    style(fig4, "Patient Population Split — Urban vs Rural")
    divs.append(to_div(fig4))

    return divs


# =====================================================================
# SCENARIO 3 — Anita: personal risk dashboard vs healthy benchmarks
# =====================================================================
def scenario3():
    divs = []
    # Simulate "Anita" as a sample patient (45yo female, family history yes)
    candidates = df[(df.age.between(43, 47)) & (df.sex == "Female") & (df.family_history == "Yes")]
    anita = candidates.iloc[0] if len(candidates) else df.iloc[0]
    bench_bmi = df.bmi.mean()
    bench_chol = df.cholesterol.mean()
    bench_bp = df.resting_bp.mean()

    divs.append(f"""
    <div class='kpi-row'>
      <div class='kpi'><div class='kpi-val'>{anita.bmi:.1f}</div><div class='kpi-lbl'>Anita's BMI (Benchmark {bench_bmi:.1f})</div></div>
      <div class='kpi'><div class='kpi-val'>{anita.cholesterol:.0f}</div><div class='kpi-lbl'>Cholesterol mg/dl (Benchmark {bench_chol:.0f})</div></div>
      <div class='kpi'><div class='kpi-val'>{anita.resting_bp:.0f}</div><div class='kpi-lbl'>Resting BP (Benchmark {bench_bp:.1f})</div></div>
      <div class='kpi'><div class='kpi-val'>{anita.risk_band}</div><div class='kpi-lbl'>Overall Risk Band</div></div>
    </div>""")

    categories = ["BMI", "Cholesterol", "Resting BP", "Max Heart Rate", "Risk Score"]
    anita_vals = [anita.bmi, anita.cholesterol/4, anita.resting_bp/2, anita.max_heart_rate/2, anita.risk_score*10]
    bench_vals = [bench_bmi, bench_chol/4, bench_bp/2, df.max_heart_rate.mean()/2, df.risk_score.mean()*10]
    fig1 = go.Figure()
    fig1.add_trace(go.Scatterpolar(r=anita_vals+[anita_vals[0]], theta=categories+[categories[0]],
                                    fill="toself", name="Anita", line_color=COLORS["accent"]))
    fig1.add_trace(go.Scatterpolar(r=bench_vals+[bench_vals[0]], theta=categories+[categories[0]],
                                    fill="toself", name="Healthy Benchmark", line_color=COLORS["accent2"], opacity=0.6))
    fig1.update_layout(polar=dict(bgcolor=COLORS["bg"], radialaxis=dict(gridcolor=COLORS["grid"])), **TEMPLATE_LAYOUT)
    fig1.update_layout(title="Personal Risk Profile vs Healthy Benchmark")
    divs.append(to_div(fig1))

    # Gauge-style indicator for risk score
    fig2 = go.Figure(go.Indicator(
        mode="gauge+number", value=int(anita.risk_score),
        title={"text": "Composite Risk Score (0-9)"},
        gauge={"axis": {"range": [0, 9]}, "bar": {"color": COLORS["accent"]},
               "steps": [{"range": [0, 3], "color": "#2e7d5b"},
                         {"range": [3, 7], "color": "#c99a2e"},
                         {"range": [7, 9], "color": "#8b2e2e"}]}))
    fig2.update_layout(**TEMPLATE_LAYOUT)
    divs.append(to_div(fig2))

    # Actionable comparison bars
    comp = pd.DataFrame({
        "Metric": ["BMI", "Cholesterol", "Resting BP"],
        "Anita": [anita.bmi, anita.cholesterol, anita.resting_bp],
        "Healthy Benchmark": [bench_bmi, bench_chol, bench_bp]
    }).melt(id_vars="Metric", var_name="Who", value_name="Value")
    fig3 = px.bar(comp, x="Metric", y="Value", color="Who", barmode="group",
                  color_discrete_map={"Anita": COLORS["accent"], "Healthy Benchmark": COLORS["accent2"]})
    style(fig3, "Anita vs Healthy Benchmark — Key Indicators")
    divs.append(to_div(fig3))

    return divs


# =====================================================================
# STORY — sequential narrative scenes (mirrors a Tableau Story)
# =====================================================================
def story_scenes():
    scenes = []
    s = df.groupby("smoking_status", observed=True).heart_disease.mean().reset_index()
    s["rate_pct"] = s.heart_disease*100
    fig = px.bar(s.sort_values("rate_pct"), x="rate_pct", y="smoking_status", orientation="h",
                 color="rate_pct", color_continuous_scale=["#4ecdc4", "#ff6b6b"])
    style(fig, "Scene 1: Smoking Is a Major Driver of Heart Disease")
    scenes.append(("Scene 1 — The Smoking Signal",
                    "Current smokers show a markedly higher heart-disease rate than never-smokers, "
                    "confirming smoking cessation as a top preventive lever.", to_div(fig)))

    g = df.groupby("age_group", observed=True).heart_disease.mean().reset_index()
    g["rate_pct"] = g.heart_disease*100
    fig = px.line(g, x="age_group", y="rate_pct", markers=True)
    fig.update_traces(line_color=COLORS["accent"])
    style(fig, "Scene 2: Risk Climbs Sharply After 40")
    scenes.append(("Scene 2 — The Age Turning Point",
                    "Disease prevalence rises steeply from the 40-54 bracket onward — the exact "
                    "window where preventive screening has the most leverage.", to_div(fig)))

    r = df.groupby(["region", "physical_activity"], observed=True).heart_disease.mean().reset_index()
    r["rate_pct"] = r.heart_disease*100
    fig = px.bar(r, x="physical_activity", y="rate_pct", color="region", barmode="group",
                 color_discrete_map={"Urban": COLORS["accent"], "Rural": COLORS["accent2"]})
    style(fig, "Scene 3: Sedentary Lifestyles Compound Regional Risk")
    scenes.append(("Scene 3 — Movement Matters Everywhere",
                    "Sedentary patients carry the highest risk in both urban and rural populations, "
                    "supporting workplace fitness and activity-promotion policy.", to_div(fig)))

    b = df.groupby("bmi_category", observed=True).heart_disease.mean().reset_index()
    b["rate_pct"] = b.heart_disease*100
    fig = px.bar(b.sort_values("rate_pct"), x="bmi_category", y="rate_pct", color="rate_pct",
                 color_continuous_scale=["#4ecdc4", "#ff6b6b"])
    style(fig, "Scene 4: Weight Management Reduces Risk")
    scenes.append(("Scene 4 — The Weight Connection",
                    "Obese patients show the steepest disease rate, reinforcing weight-management "
                    "guidance as a practical, individual-level intervention.", to_div(fig)))

    fh = df.groupby("family_history", observed=True).heart_disease.mean().reset_index()
    fh["rate_pct"] = fh.heart_disease*100
    fig = px.bar(fh, x="family_history", y="rate_pct", color="family_history",
                 color_discrete_map={"Yes": COLORS["accent"], "No": COLORS["accent2"]})
    style(fig, "Scene 5: Genetics Still Matter — But Lifestyle Is Actionable")
    scenes.append(("Scene 5 — Know Your Baseline",
                    "Family history raises baseline risk, which is exactly why people like Anita "
                    "benefit most from proactively tracking modifiable factors.", to_div(fig)))

    return scenes


if __name__ == "__main__":
    print("Scenario 1 charts:", len(scenario1()))
    print("Scenario 2 charts:", len(scenario2()))
    print("Scenario 3 charts:", len(scenario3()))
    print("Story scenes:", len(story_scenes()))
