# Heart Disease Analytics Project (Tableau / BI)

Analyzing heart disease risk factors for three personas — a cardiologist,
a government health-policy analyst, and an individual patient — through
interactive dashboards and a data story.

**Read `docs/Documentation.md` first** — it walks through every required
project activity (problem understanding, data collection, SQL, data prep,
visualizations, dashboards, story, performance testing, web integration,
documentation) in order, and explains the one important tooling
substitution below.

## ⚠️ About the Tableau deliverable
Tableau Desktop is licensed, GUI-only software and cannot run inside an
automated code environment. Instead of a `.twbx` file that most people here
couldn't open without a paid license anyway, this deliverable is a fully
working **Plotly + Flask web app** that reproduces every chart, filter,
KPI, and story scene the brief asks for — runnable by anyone with Python,
no Tableau license required. `docs/Documentation.md` §9 gives exact steps
to rebuild the same views in Tableau Desktop if/when you have a seat.

## Quick Start
```bash
cd flask_app
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000
```
No server? Just open the pre-built static files directly in a browser:
`visualizations/dashboard_clinician.html`, `dashboard_policy.html`,
`dashboard_personal.html`, `story.html`.

## Folder Guide
| Folder | Contents |
|---|---|
| `data/` | Raw dataset + cleaned/aggregated CSV extracts |
| `database/` | SQL schema (`01_schema.sql`) + views/queries (`02_sql_operations.sql`) |
| `data_prep/` | `00_gen_data.py` (dataset generator), `data_preparation.py` (cleaning/features) |
| `visualizations/` | `build_dashboards.py` (chart definitions), static HTML exports |
| `flask_app/` | Web integration — Flask routes, Jinja templates, CSS |
| `docs/` | `Documentation.md`, `Development_Procedure.md`, `Video_Script.md` |

## Full Rebuild From Scratch
```bash
python data_prep/00_gen_data.py                 # 1. generate dataset
mysql -u root -p < database/01_schema.sql        # 2. create DB (optional, needs MySQL)
mysql -u root -p < database/02_sql_operations.sql
python data_prep/data_preparation.py             # 3. clean & engineer features
python visualizations/build_dashboards.py        # 4. verify chart builders
python visualizations/export_static.py           # 5. export standalone HTML
cd flask_app && pip install -r requirements.txt && python app.py   # 6. run web app
```
