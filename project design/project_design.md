# Heart Disease Analysis - Project Design

## 1. Overview

This document provides a detailed technical design for the Heart Disease Analysis project, building upon the requirements and the high-level design established in the previous phases. It covers the specifics of data handling, database schema, data preparation, visualization implementation, and web integration.

## 2. Data Handling and Database Design

### 2.1 Data Sources

The project utilizes a dataset containing various attributes related to heart disease. These attributes typically include:

*   **Demographics**: Age, Sex, etc.
*   **Medical History**: Chest Pain Type, Resting Blood Pressure, Cholesterol, Fasting Blood Sugar, Resting Electrocardiographic Results, Exercise Induced Angina, ST Depression, Slope of the Peak Exercise ST Segment, Number of Major Vessels, Thalassemia.
*   **Clinical Indicators**: Maximum Heart Rate Achieved.

### 2.2 Database Schema (`database/01_schema.sql`)

While a specific schema was not provided, a typical relational database schema for this project would include a `Patients` table and potentially a `MedicalRecords` table. A simplified `HeartDiseaseData` table might look like this:

```sql
CREATE TABLE HeartDiseaseData (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    age INT,
    sex INT, -- 0 = female, 1 = male
    chest_pain_type INT, -- 0-3
    resting_bp INT,
    cholesterol INT,
    fasting_bs INT, -- 0 = false, 1 = true
    resting_ecg INT, -- 0-2
    max_hr INT,
    exercise_angina INT, -- 0 = no, 1 = yes
    st_depression DECIMAL(3,1),
    st_slope INT, -- 0-2
    num_major_vessels INT, -- 0-3
    thalassemia INT, -- 0-3
    target INT -- 0 = no heart disease, 1 = heart disease
);
```

### 2.3 SQL Operations (`database/02_sql_operations.sql`)

SQL operations would involve:

*   **Data Insertion**: Loading raw data into the `HeartDiseaseData` table.
*   **Data Cleaning**: SQL queries to identify and handle inconsistencies or missing values (though Python scripts are preferred for complex cleaning).
*   **Data Aggregation**: Creating aggregated views for dashboard summaries (e.g., average cholesterol by age group, prevalence by region).
*   **Data Extraction**: Queries to extract specific subsets of data for visualization tools.

## 3. Data Preparation (`data_prep/data_preparation.py`)

The data preparation pipeline is crucial for transforming raw data into a clean, structured format suitable for analysis and visualization. This typically involves:

1.  **Loading Data**: Reading the raw dataset (e.g., from CSV files in `data/` or directly from the database).
2.  **Handling Missing Values**: Imputing missing values using strategies like mean, median, mode, or more advanced techniques.
3.  **Categorical Encoding**: Converting categorical features (e.g., `sex`, `chest_pain_type`) into numerical representations if not already done.
4.  **Feature Scaling**: Normalizing or standardizing numerical features to ensure consistent scales.
5.  **Feature Engineering**: Creating new, more informative features (e.g., BMI from height and weight, age groups).
6.  **Data Transformation**: Pivoting, melting, or aggregating data to prepare it for specific visualizations.
7.  **Saving Prepared Data**: Storing the cleaned and prepared data, often as CSV files, for use by visualization tools.

## 4. Visualization Implementation

### 4.1 Tableau Dashboards

The project aims to create interactive dashboards in Tableau for three distinct personas:

*   **Clinician Dashboard (`dashboard_clinician.html`)**: Focuses on individual patient profiles, detailed medical history, and correlations between clinical indicators and heart disease risk. Key visualizations might include scatter plots of cholesterol vs. blood pressure, bar charts of chest pain types, and trend lines for risk factors over time.
*   **Policy Dashboard (`dashboard_policy.html`)**: Provides a high-level overview of heart disease prevalence across different demographics and geographical regions. Visualizations could include choropleth maps, demographic breakdowns (age, sex), and correlation matrices of lifestyle factors.
*   **Personal Dashboard (`dashboard_personal.html`)**: A simplified view for individuals to monitor their own risk factors against healthy benchmarks. This would feature gauges for blood pressure and cholesterol, simple bar charts for lifestyle habits, and clear indicators of risk levels.

### 4.2 Data Story (`story.html`)

A data story will be created to guide users through a narrative of key insights, connecting different dashboards and visualizations to present a cohesive understanding of heart disease risk factors and prevention strategies.

### 4.3 Plotly + Flask Alternative (`visualizations/build_dashboards.py`)

As an open-source alternative to Tableau, Plotly will be used within Python to generate interactive web-based visualizations. The `build_dashboards.py` script will contain functions to create various chart types (e.g., bar, line, scatter, pie) using Plotly Express or Plotly Graph Objects. These charts will then be rendered into HTML and embedded into Flask templates.

## 5. Web Integration (`app.py`, `templates/`, `static/`)

The web integration component makes the dashboards and stories accessible via a web browser.

### 5.1 Flask Application (`app.py`)

*   **Routing**: Defines routes for different dashboards and the data story (e.g., `/clinician`, `/policy`, `/personal`, `/story`).
*   **Data Loading**: Loads prepared data (e.g., from CSVs or directly from the database) to pass to the visualization rendering functions.
*   **Rendering**: Renders Jinja2 templates, injecting the generated Plotly charts or static HTML exports from Tableau.

### 5.2 Templates (`templates/`)

HTML files (e.g., `dashboard_clinician.html`, `dashboard_policy.html`, `dashboard_personal.html`, `story.html`) will serve as the structure for the web pages. These templates will include placeholders for embedding the visualizations and will incorporate navigation elements.

### 5.3 Static Files (`static/`)

This directory will contain CSS files for styling the web application (e.g., responsive design, layout) and JavaScript files for any additional client-side interactivity or dynamic content loading.

## 6. Performance Testing

Performance testing will focus on the efficiency and responsiveness of the dashboards and the web application.

*   **Data Rendering**: Measuring the time taken to render visualizations, especially with large datasets.
*   **Filter Utilization**: Assessing the responsiveness of filters and interactive elements.
*   **Calculation Fields**: Evaluating the impact of complex calculations on dashboard performance.
*   **Number of Visualizations/Graphs**: Monitoring performance as the number of visualizations on a single dashboard increases.

## 7. Project Structure (Relevant for Design)

| Folder           | Purpose                                                                                             |
| :--------------- | :-------------------------------------------------------------------------------------------------- |
| `data/`          | Stores raw datasets and cleaned/aggregated CSV extracts.                                            |
| `database/`      | Contains SQL schema (`01_schema.sql`) and SQL operations (`02_sql_operations.sql`).                 |
| `data_prep/`     | Houses Python scripts for data generation (`00_gen_data.py`) and data preparation (`data_preparation.py`). |
| `visualizations/`| Contains Python script for chart definitions (`build_dashboards.py`) and static HTML exports of dashboards. |
| `flask_app/`     | (Implied from `app.py`, `templates/`, `static/`) Web integration components: Flask routes, Jinja templates, CSS. |
| `docs/`          | Project documentation files (e.g., `Documentation.md`, `Development_Procedure.md`, `Video_Script.md`). |
