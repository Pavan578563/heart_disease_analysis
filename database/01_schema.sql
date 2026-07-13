-- =====================================================================
-- Heart Disease Analytics Project
-- Database Schema (MySQL / compatible with PostgreSQL with minor tweaks)
-- =====================================================================

DROP DATABASE IF EXISTS heart_disease_db;
CREATE DATABASE heart_disease_db;
USE heart_disease_db;

-- ---------------------------------------------------------------------
-- Master table: one row per patient record (as extracted from CSV)
-- ---------------------------------------------------------------------
CREATE TABLE patients (
    patient_id            VARCHAR(10)  PRIMARY KEY,
    age                    INT          NOT NULL,
    sex                    VARCHAR(10)  NOT NULL,
    region                 VARCHAR(10)  NOT NULL,        -- Urban / Rural
    bmi                    DECIMAL(4,1) NOT NULL,
    smoking_status         VARCHAR(15)  NOT NULL,        -- Never/Former/Current
    physical_activity      VARCHAR(15)  NOT NULL,        -- Sedentary/Moderate/Active
    diet_quality            VARCHAR(10)  NOT NULL,        -- Poor/Average/Good
    alcohol_consumption     VARCHAR(10)  NOT NULL,        -- None/Moderate/Heavy
    family_history          VARCHAR(3)   NOT NULL,        -- Yes/No
    resting_bp              INT          NOT NULL,
    cholesterol              INT          NOT NULL,
    fasting_blood_sugar      TINYINT      NOT NULL,        -- 0/1
    max_heart_rate           INT          NOT NULL,
    exercise_angina          VARCHAR(3)   NOT NULL,
    oldpeak                  DECIMAL(3,1) NOT NULL,
    chest_pain_type          VARCHAR(20)  NOT NULL,
    thalassemia               VARCHAR(20)  NOT NULL,
    heart_disease             TINYINT      NOT NULL,        -- 0 = No, 1 = Yes
    created_at                TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- Lookup / dimension table used by BI tools (Tableau) for friendlier labels
CREATE TABLE risk_bands (
    band_id      INT PRIMARY KEY,
    band_name    VARCHAR(20),
    min_score    INT,
    max_score    INT
);

INSERT INTO risk_bands VALUES
 (1, 'Low',      0, 3),
 (2, 'Moderate', 4, 7),
 (3, 'High',     8, 15);

-- ---------------------------------------------------------------------
-- Indexes to speed up the aggregations Tableau will issue live
-- ---------------------------------------------------------------------
CREATE INDEX idx_age        ON patients(age);
CREATE INDEX idx_region     ON patients(region);
CREATE INDEX idx_smoking    ON patients(smoking_status);
CREATE INDEX idx_disease    ON patients(heart_disease);

-- ---------------------------------------------------------------------
-- Load data (adjust path; use LOAD DATA LOCAL INFILE or your ETL tool)
-- ---------------------------------------------------------------------
-- LOAD DATA LOCAL INFILE 'data/heart_disease.csv'
-- INTO TABLE patients
-- FIELDS TERMINATED BY ',' ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;
