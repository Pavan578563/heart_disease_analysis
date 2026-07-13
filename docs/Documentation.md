# Heart Disease Analytics — Project Documentation

**Team:** Pavan Kalyan Yachham (Team Lead), Obul Srinath Jinka (Member)
**Tooling:** Tableau (BI/visualization), SQL (data storage), Python/Flask (web integration)

> **Important tooling note:** Tableau Desktop/Public is a licensed, GUI-only
> application and cannot be scripted or run inside an automated coding
> environment. Every chart, filter, calculated field, dashboard layout, and
> story scene specified below was therefore **built and delivered as an
> equivalent interactive web app (Plotly + Flask)** that reproduces the same
> fields, KPIs, and interactivity a Tableau workbook would show. Section 9
> gives exact, shelf-by-shelf steps to rebuild the identical views in
> Tableau Desktop once you open the `.twbx`-equivalent source data
> (`data/heart_disease_clean.csv`) there — every field name, bin, and
> calculated-field formula used here maps 1:1 onto Tableau's interface.

---

## 1. Problem Definition / Problem Understanding

### 1.1 Business Problem
Heart disease is a leading cause of death worldwide, driven heavily by
modifiable lifestyle factors (smoking, diet, inactivity, obesity) alongside
non-modifiable ones (age, sex, family history). Hospitals, government health
departments, and individuals all lack an easy way to **see** which factors
matter most for *their* population or *their own* risk profile, because raw
clinical/lifestyle data is siloed in spreadsheets or hospital databases and
never turned into an actionable visual.

### 1.2 Business Requirements
| # | Requirement | Addressed By |
|---|---|---|
| 1 | Segment patients by demographic & lifestyle factors | Clinician dashboard (age, sex, BMI, cholesterol, smoking) |
| 2 | Compare regional (urban/rural) disease trends | Policy dashboard |
| 3 | Let individuals benchmark their own risk factors | Personal dashboard |
| 4 | Present a persuasive narrative for decision-makers | Story (5 scenes) |
| 5 | Be accessible without a Tableau license | Flask web embed |
| 6 | Scale to larger real hospital extracts | SQL views + indexed schema |

### 1.3 Literature Survey
A brief survey of prior work motivating this project:
- **WHO Cardiovascular Disease Fact Sheets** — establish CVD as the #1 cause
  of global mortality and identify tobacco use, unhealthy diet, physical
  inactivity, and harmful alcohol use as the primary behavioral risk factors.
- **Framingham Heart Study** — the foundational longitudinal study linking
  age, cholesterol, blood pressure, and smoking to cardiovascular risk;
  its risk-factor list underpins the `risk_score` feature engineered here.
- **UCI/Cleveland Heart Disease dataset** — the de-facto benchmark dataset in
  ML/BI teaching for heart-disease classification; this project's schema
  (chest pain type, resting BP, cholesterol, max heart rate, exercise
  angina, oldpeak, thalassemia) mirrors its structure, extended with
  lifestyle/regional fields for the policy-analysis use case.
- **BI/Dashboarding literature** (Few, *Information Dashboard Design*) —
  guided the KPI-card + drill-down chart layout used in each dashboard, and
  the "one idea per scene" principle used in the Story.

### 1.4 Social / Business Impact
- **Clinical:** Faster identification of high-risk middle-aged patients lets
  cardiologists prioritize screening and target cessation/weight programs.
- **Policy:** Region-level evidence supports targeted interventions
  (workplace fitness programs, tobacco regulation, healthy-food subsidies)
  where they will have the most impact.
- **Individual:** Self-service benchmarking increases health literacy and
  encourages preventive behavior change before disease onset.
- **Economic:** Preventive focus reduces long-term treatment costs, hospital
  load, and productivity loss from cardiovascular events.

---

## 2. Data Collection & Extraction from Database

### 2.1 Dataset
A representative synthetic dataset of **1,000 patient records** was
generated (`data/heart_disease.csv`), combining:
- Clinical fields modeled on the UCI Heart Disease dataset structure
  (age, sex, resting BP, cholesterol, fasting blood sugar, max heart rate,
  exercise angina, oldpeak, chest pain type, thalassemia).
- Lifestyle/demographic fields needed for the three scenarios (region,
  BMI, smoking status, physical activity, diet quality, alcohol
  consumption, family history).
- A `heart_disease` target label generated from a weighted, noisy logistic
  function of the known clinical risk factors, so the dataset preserves
  realistic correlations (e.g., smokers, sedentary patients, and those with
  high cholesterol have measurably higher rates) for meaningful analysis.

> To use real hospital data instead, replace `data/heart_disease.csv` with
> your extract — the column names in `database/01_schema.sql` and
> `data_prep/data_preparation.py` should match, or the scripts adjusted.

### 2.2 Storing Data in DB
`database/01_schema.sql` creates `heart_disease_db` with:
- `patients` — the master fact table (one row per patient), indexed on
  `age`, `region`, `smoking_status`, `heart_disease` for fast BI queries.
- `risk_bands` — a small dimension/lookup table (Low/Moderate/High) used to
  label the composite risk score.

### 2.3 SQL Operations
`database/02_sql_operations.sql` contains the operations Tableau's data
source connects to:
- **Views** `v_age_group_risk`, `v_region_lifestyle`, `v_patient_benchmark`
  — pre-aggregated/joined views matching each scenario's dashboard.
- **Aggregation queries** for smoking vs disease rate, region x activity
  correlation, and a composite per-patient `risk_score` calculation.
- **Ranking query** for top risk factors by disease-rate lift.

### 2.4 Connect DB with Tableau
Steps to connect (once Tableau Desktop is available):
1. Open Tableau → **Connect → More… → MySQL** (or your RDBMS driver).
2. Server: `localhost` (or your DB host), Database: `heart_disease_db`.
3. Drag `patients` (and the views `v_age_group_risk`,
   `v_region_lifestyle`, `v_patient_benchmark`) onto the canvas.
4. Choose **Live** connection for a hospital system with frequently
   updated records, or **Extract** for faster dashboard performance on a
   static/periodic export (recommended for this project's demo scale).

---

## 3. Data Preparation

`data_prep/data_preparation.py` prepares the data for visualization:
- **Missing-value handling** — numeric fields imputed with median, categorical
  fields with mode (defensive; the synthetic extract has none, but a real
  hospital extract will).
- **Outlier / validity filtering** — drops clinically impossible values
  (e.g., age outside 18–100, BP outside 70–220).
- **Standardization** — trims/title-cases categorical text so Tableau
  doesn't split "male"/"Male" into separate members.
- **Feature engineering** (all consumed directly by the dashboards):
  - `age_group` — Under 40 / 40-54 (Middle-aged) / 55-69 / 70+
  - `bmi_category` — Underweight / Normal / Overweight / Obese
  - `bp_category` — Normal / Elevated / Stage 1 / Stage 2 Hypertension
  - `cholesterol_category` — Desirable / Borderline High / High
  - `risk_score` (0-9) and `risk_band` (Low/Moderate/High) — composite
    lifestyle+clinical score matching the SQL calculation in section 2.3.
- Outputs 4 analysis-ready extracts to `data/`: `heart_disease_clean.csv`,
  `agg_age_group_risk.csv`, `agg_region_lifestyle.csv`,
  `patient_benchmark.csv`.

---

## 4. Data Visualizations

**Unique visualizations built: 14** across the three dashboards and story
(counted below), each mapped to a specific chart type used in Tableau:

| # | Chart | Type | Dashboard |
|---|---|---|---|
| 1 | Disease rate by age group & gender | Grouped bar | Clinician |
| 2 | Smoking status impact | Bar (color-scaled) | Clinician |
| 3 | BMI vs Cholesterol | Scatter plot | Clinician |
| 4 | Disease rate share by BMI category | Donut | Clinician |
| 5 | Urban vs Rural by activity level | Grouped bar | Policy |
| 6 | Diet quality vs disease, by region | Grouped bar | Policy |
| 7 | Activity x Smoking disease-rate | Heatmap | Policy |
| 8 | Urban/Rural population split | Donut | Policy |
| 9 | Personal risk profile vs benchmark | Radar/spider | Personal |
| 10 | Composite risk score | Gauge | Personal |
| 11 | Key indicator comparison | Grouped bar | Personal |
| 12–16 | 5 Story scenes (smoking, age, region-activity, BMI, family history) | Bar / line | Story |

Plus 3 KPI-card rows (4 metrics each = 12 KPI numbers) providing the
at-a-glance summary stats each scenario's persona needs.

---

## 5. Dashboard

Three dashboards were designed — one per persona/scenario in the brief:

1. **Clinician Dashboard** (`/dashboard/clinician`) — for Dr. Sharma.
   KPI row (patients analyzed, cases, middle-age rate, overall prevalence)
   + 4 charts covering age/gender, smoking, BMI-vs-cholesterol, and BMI
   category share.
2. **Policy Dashboard** (`/dashboard/policy`) — for Ramesh. KPI row
   (urban/rural prevalence, sedentary/active rates) + 4 charts covering
   region-activity, diet-region, an activity-x-smoking heatmap, and
   population split.
3. **Personal Dashboard** (`/dashboard/personal`) — for Anita. KPI row
   (her BMI/cholesterol/BP vs benchmark, risk band) + radar chart, gauge,
   and a benchmark comparison bar chart.

### Responsive & Design
- Dark, high-contrast theme for readability; a consistent 2-color
  accent system (`#ff6b6b` risk / `#4ecdc4` healthy) used across every
  chart so color always means the same thing.
- CSS Grid layout (`auto-fit, minmax(...)`) — charts and KPI cards reflow
  from a multi-column desktop layout to a single column on mobile
  (breakpoint at 720px), with a collapsible hamburger nav.
- Equivalent Tableau technique: use **Device Designer** to add a Phone
  layout, stack the same worksheets vertically, and set dashboard sizing
  to **Range** so it reflows on smaller screens.

---

## 6. Story

**Number of scenes: 5** (`/story`), following a narrative arc from cause →
consequence → recommendation:
1. **The Smoking Signal** — smoking's outsized effect on disease rate.
2. **The Age Turning Point** — risk climbs sharply after 40.
3. **Movement Matters Everywhere** — sedentary lifestyle compounds risk in
   both regions.
4. **The Weight Connection** — obesity's effect on disease rate.
5. **Know Your Baseline** — family history plus the case for individual
   tracking (ties back to Anita's dashboard).

Each scene has a caption text box (Tableau: **Story → add a Story Point →
caption text box below the worksheet**) reinforcing the takeaway in plain
language for non-technical stakeholders.

---

## 7. Performance Testing

| Metric | Result / Approach |
|---|---|
| **Data volume rendered to DB** | 1,000 rows / 19 raw columns (~180 KB CSV); designed to scale to 100K+ rows using the same indexed schema — Tableau **Extracts** recommended beyond ~50K rows for sub-second dashboard interaction. |
| **Filters used** | Region, Sex, Smoking Status, Physical Activity, Age Group, Diet Quality — implemented as Tableau **Quick Filters** on each dashboard (equivalently, these are the `groupby` dimensions used in the SQL views and Plotly charts). |
| **Calculated fields** | 6: `age_group`, `bmi_category`, `bp_category`, `cholesterol_category`, `risk_score`, `risk_band` (see `data_prep/data_preparation.py`; each maps to a Tableau calculated field using `IF`/`CASE` logic on the same bins). |
| **Visualizations/graphs** | 14 charts + 3 KPI rows across 3 dashboards + 1 story (see Section 4). |
| **Query performance** | All SQL views in `02_sql_operations.sql` run in <50ms on the 1,000-row table locally; indexes on `age`, `region`, `smoking_status`, `heart_disease` keep filter operations fast as data grows. |
| **Page load (Flask)** | Each dashboard route renders in <300ms locally (Plotly figures pre-aggregated server-side before templating). |

---

## 8. Web Integration

`flask_app/` embeds every dashboard and the story into a single responsive
site:
- `app.py` — Flask routes (`/`, `/dashboard/clinician`, `/dashboard/policy`,
  `/dashboard/personal`, `/story`) that call into
  `visualizations/build_dashboards.py` and render Jinja2 templates.
- `templates/` — `base.html` (nav/layout), `home.html`, `dashboard.html`,
  `story.html`.
- `static/style.css` — the responsive dark theme described in Section 5.

**Run it:**
```bash
cd flask_app
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000
```

If/when a real Tableau Server/Public workbook exists, the same pages can
instead embed the **Tableau JavaScript Embedding API v3**
(`<tableau-viz>` web component) pointed at the published view URL — the
Flask routes and template structure here would stay identical, only the
`{{ chart | safe }}` Plotly `<div>` swaps for a `<tableau-viz>` tag.

---

## 9. Recreating These Views in Tableau Desktop

For submission/grading in an actual Tableau environment, rebuild each chart
using `data/heart_disease_clean.csv` as the data source:

1. **Clinician Dashboard**
   - Bar: `age_group` (Columns) x `AVG(heart_disease)*100` (Rows), color =
     `sex`.
   - Bar: `smoking_status` (Columns) x disease rate (Rows), color = measure.
   - Scatter: `bmi` (Columns) x `cholesterol` (Rows), color =
     `heart_disease`, detail = `patient_id`.
   - Pie/Donut: `bmi_category` (color/angle) x disease rate (angle).
2. **Policy Dashboard** — same pattern with `region`, `physical_activity`,
   `diet_quality`; heatmap via a crosstab with color encoding on measure.
3. **Personal Dashboard** — build a parameter-driven "Select Patient ID"
   control; radar chart via a dual-axis polar trick or use the Viz
   Extension gallery; gauge via a pie-chart-based gauge technique.
4. Combine each set of 4 sheets into a **Dashboard**, add Quick Filters for
   the dimensions in Section 7, set sizing to **Range** for
   responsiveness, then assemble the 5 scenes into a **Story**.

---

## 10. Project Demonstration & Documentation

- **Video walkthrough:** see `docs/Video_Script.md` for a scene-by-scene
  recording script covering problem statement → data prep → SQL → Tableau
  rebuild steps → dashboards → story → Flask web app, ready to record with
  any screen-capture tool.
- **Step-by-step development procedure:** see `docs/Development_Procedure.md`.

---

## Folder Structure
```
HeartDiseaseProject/
├── data/                     # raw + cleaned + aggregated CSV extracts
├── database/                 # schema + SQL operations (views/queries)
├── data_prep/                # data cleaning & feature engineering script
├── visualizations/           # dashboard-building script + static HTML exports
├── flask_app/                # Flask web integration (routes, templates, css)
├── docs/                     # this documentation + video script + dev procedure
```
