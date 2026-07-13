# Project Demonstration Video — Recording Script

> Note: An actual video file could not be recorded in this environment.
> This is a ready-to-use script/storyboard — record your screen following
> these beats with any tool (OBS Studio, Loom, PowerPoint screen record).
> Target length: 6-8 minutes.

## Scene-by-Scene Script

**0:00 – 0:40 | Intro**
"Hi, I'm [name], presenting our Heart Disease Analytics project. Heart
disease is a leading global cause of mortality, and this project uses data
visualization and BI techniques to help cardiologists, policymakers, and
individuals understand and act on the key risk factors."

**0:40 – 1:30 | Problem & Requirements**
Show `docs/Documentation.md` Section 1. Explain the three personas: Dr.
Sharma (clinician), Ramesh (policy), Anita (individual), and the business
requirements each one drives.

**1:30 – 2:30 | Data & Database**
Show `data/heart_disease.csv`, then `database/01_schema.sql` and
`02_sql_operations.sql`. Explain the `patients` table, indexes, and the
three analytical views feeding the dashboards.

**2:30 – 3:30 | Data Preparation**
Run `data_prep/data_preparation.py` on screen. Point out the missing-value
handling, outlier filtering, and the 6 engineered fields (age_group,
bmi_category, bp_category, cholesterol_category, risk_score, risk_band).

**3:30 – 5:30 | Dashboards Walkthrough**
Launch the Flask app (`python app.py`) and click through:
- Clinician dashboard — narrate the age/gender, smoking, BMI-cholesterol
  scatter, and BMI-category charts.
- Policy dashboard — narrate urban/rural comparison, diet-region chart,
  activity x smoking heatmap.
- Personal dashboard — narrate Anita's radar chart, risk gauge, and
  benchmark comparison.
- Resize the browser window to show the responsive mobile layout.

**5:30 – 6:30 | Story**
Open `/story` and scroll through the 5 scenes, reading each caption aloud
and connecting it back to a policy or clinical recommendation.

**6:30 – 7:15 | Performance & Web Integration**
Briefly show the SQL views running, mention filter/calculated-field/chart
counts (Documentation.md §7), and highlight the Flask routes/templates
structure powering the web embed.

**7:15 – 8:00 | Closing**
Summarize the impact: earlier risk detection, better-targeted policy, and
individual empowerment — and thank the audience.

## Recording Checklist
- [ ] Screen resolution set to 1920x1080 for clarity
- [ ] Flask app running locally (`python app.py`) before recording starts
- [ ] Browser zoom at 100% so charts aren't cropped
- [ ] Audio levels checked
- [ ] Export as MP4, upload alongside this documentation
