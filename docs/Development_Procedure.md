# Step-by-Step Project Development Procedure

1. **Problem Understanding**
   - Defined the business problem, requirements, literature survey, and
     social/business impact (see `Documentation.md`, Section 1).

2. **Data Collection**
   - Generated/collected a 1,000-record patient dataset combining clinical
     fields (UCI Heart Disease-style) and lifestyle/regional fields needed
     for the three project scenarios. File: `data/heart_disease.csv`.
   - Script: `gen_data.py` (project root).

3. **Database Setup**
   - Ran `database/01_schema.sql` to create `heart_disease_db`, the
     `patients` table, and the `risk_bands` lookup table, with indexes on
     the columns dashboards filter by most.
   - Loaded the CSV into `patients` (via `LOAD DATA INFILE` or any ETL
     tool / pandas `to_sql`).
   - Ran `database/02_sql_operations.sql` to create the analysis views
     (`v_age_group_risk`, `v_region_lifestyle`, `v_patient_benchmark`) and
     validated the correlation/ranking queries.

4. **Connect Database to Tableau**
   - Connected Tableau Desktop to `heart_disease_db` using the MySQL
     connector, pulled in `patients` and the three views, and set the
     connection to Extract for performance (see `Documentation.md` §2.4).

5. **Data Preparation**
   - Ran `data_prep/data_preparation.py` to clean, validate, and engineer
     features (`age_group`, `bmi_category`, `bp_category`,
     `cholesterol_category`, `risk_score`, `risk_band`).
   - Verified 0 missing values remained; exported 4 analysis-ready CSVs to
     `data/`.

6. **Visualization Design**
   - Designed 14 unique charts + 3 KPI rows across the three
     scenario dashboards and the 5-scene story (see `Documentation.md` §4).
   - Built and validated them with `visualizations/build_dashboards.py`
     (Plotly), then exported standalone static HTML with
     `visualizations/export_static.py`.

7. **Dashboard Assembly**
   - Grouped the charts per persona into 3 dashboards with KPI headers,
     using a consistent color system and responsive grid layout.

8. **Story Assembly**
   - Sequenced 5 scenes with captions building a cause → consequence →
     recommendation narrative.

9. **Performance Testing**
   - Measured SQL view execution time, confirmed index usage, counted
     filters/calculated fields/visualizations, and timed Flask page loads
     (see `Documentation.md` §7).

10. **Web Integration**
    - Built the Flask app (`flask_app/app.py`) with routes for home, each
      dashboard, and the story; embedded charts via Jinja2 templates and a
      shared responsive stylesheet (`flask_app/static/style.css`).
    - Tested all 5 routes return HTTP 200 and render correctly.

11. **Documentation & Demonstration**
    - Wrote `Documentation.md` (full project write-up covering every
      required activity) and `Video_Script.md` (recording script for the
      end-to-end demonstration video).

## How to Reproduce End-to-End
```bash
# 1. Generate data
python gen_data.py

# 2. (Optional) load into MySQL
mysql -u root -p < database/01_schema.sql
mysql -u root -p < database/02_sql_operations.sql

# 3. Clean & engineer features
cd data_prep && python data_preparation.py && cd ..

# 4. Build & preview dashboards
cd visualizations && python build_dashboards.py && python export_static.py && cd ..

# 5. Run the web app
cd flask_app && pip install -r requirements.txt && python app.py
# visit http://127.0.0.1:5000
```
