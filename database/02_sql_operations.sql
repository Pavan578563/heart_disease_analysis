-- =====================================================================
-- SQL Operations performed on heart_disease_db
-- These views are what Tableau connects to (Data Source = live/extract
-- connection to `heart_disease_db`, tables + views below).
-- =====================================================================
USE heart_disease_db;

-- 1. Age-group segmentation (used in Dr. Sharma's dashboard - Scenario 1)
CREATE OR REPLACE VIEW v_age_group_risk AS
SELECT
    CASE
        WHEN age < 40 THEN 'Under 40'
        WHEN age BETWEEN 40 AND 54 THEN '40-54 (Middle-aged)'
        WHEN age BETWEEN 55 AND 69 THEN '55-69'
        ELSE '70+'
    END AS age_group,
    sex,
    smoking_status,
    ROUND(AVG(bmi), 1)          AS avg_bmi,
    ROUND(AVG(cholesterol), 0)  AS avg_cholesterol,
    COUNT(*)                    AS total_patients,
    SUM(heart_disease)          AS disease_cases,
    ROUND(100.0 * SUM(heart_disease) / COUNT(*), 2) AS disease_rate_pct
FROM patients
GROUP BY age_group, sex, smoking_status;

-- 2. Region-wise prevalence and lifestyle comparison (Ramesh - Scenario 2)
CREATE OR REPLACE VIEW v_region_lifestyle AS
SELECT
    region,
    physical_activity,
    diet_quality,
    COUNT(*)                    AS total_patients,
    SUM(heart_disease)          AS disease_cases,
    ROUND(100.0 * SUM(heart_disease) / COUNT(*), 2) AS disease_rate_pct,
    ROUND(AVG(resting_bp), 1)   AS avg_bp,
    ROUND(AVG(cholesterol), 0)  AS avg_cholesterol
FROM patients
GROUP BY region, physical_activity, diet_quality;

-- 3. Individual risk-factor benchmark view (Anita - Scenario 3)
CREATE OR REPLACE VIEW v_patient_benchmark AS
SELECT
    patient_id, age, sex, bmi, cholesterol, resting_bp,
    physical_activity, diet_quality, family_history,
    (SELECT ROUND(AVG(bmi),1)         FROM patients) AS benchmark_bmi,
    (SELECT ROUND(AVG(cholesterol),0) FROM patients) AS benchmark_cholesterol,
    (SELECT ROUND(AVG(resting_bp),1)  FROM patients) AS benchmark_bp,
    heart_disease
FROM patients;

-- 4. Correlation helper - smoking vs disease
SELECT smoking_status,
       COUNT(*) AS n,
       SUM(heart_disease) AS cases,
       ROUND(100.0*SUM(heart_disease)/COUNT(*),2) AS rate_pct
FROM patients GROUP BY smoking_status ORDER BY rate_pct DESC;

-- 5. Correlation helper - sedentary lifestyle vs disease (rural vs urban)
SELECT region, physical_activity,
       COUNT(*) AS n,
       ROUND(100.0*SUM(heart_disease)/COUNT(*),2) AS rate_pct
FROM patients
GROUP BY region, physical_activity
ORDER BY region, rate_pct DESC;

-- 6. Composite numeric risk score per patient (feeds risk_bands lookup)
SELECT patient_id,
   (CASE WHEN age>55 THEN 1 ELSE 0 END +
    CASE WHEN sex='Male' THEN 1 ELSE 0 END +
    CASE WHEN smoking_status='Current' THEN 2 WHEN smoking_status='Former' THEN 1 ELSE 0 END +
    CASE WHEN physical_activity='Sedentary' THEN 1 ELSE 0 END +
    CASE WHEN bmi>30 THEN 1 ELSE 0 END +
    CASE WHEN cholesterol>240 THEN 1 ELSE 0 END +
    CASE WHEN resting_bp>140 THEN 1 ELSE 0 END +
    CASE WHEN family_history='Yes' THEN 1 ELSE 0 END +
    CASE WHEN exercise_angina='Yes' THEN 1 ELSE 0 END
   ) AS risk_score
FROM patients;

-- 7. Top risk factors ranked by disease-rate lift vs baseline
SELECT 'Smoking-Current' AS factor,
       ROUND(100.0*SUM(CASE WHEN smoking_status='Current' THEN heart_disease END)/
             SUM(CASE WHEN smoking_status='Current' THEN 1 END),2) AS rate_pct FROM patients
UNION ALL
SELECT 'Sedentary', ROUND(100.0*SUM(CASE WHEN physical_activity='Sedentary' THEN heart_disease END)/
             SUM(CASE WHEN physical_activity='Sedentary' THEN 1 END),2) FROM patients
UNION ALL
SELECT 'High-Cholesterol(>240)', ROUND(100.0*SUM(CASE WHEN cholesterol>240 THEN heart_disease END)/
             SUM(CASE WHEN cholesterol>240 THEN 1 END),2) FROM patients
UNION ALL
SELECT 'Obesity(BMI>30)', ROUND(100.0*SUM(CASE WHEN bmi>30 THEN heart_disease END)/
             SUM(CASE WHEN bmi>30 THEN 1 END),2) FROM patients
UNION ALL
SELECT 'Family-History', ROUND(100.0*SUM(CASE WHEN family_history='Yes' THEN heart_disease END)/
             SUM(CASE WHEN family_history='Yes' THEN 1 END),2) FROM patients
ORDER BY rate_pct DESC;
