import numpy as np, pandas as pd
np.random.seed(42)

n = 1000
regions = ['Urban', 'Rural']
region_w = [0.62, 0.38]

age = np.random.normal(52, 12, n).clip(20, 90).astype(int)
sex = np.random.choice(['Male', 'Female'], n, p=[0.55, 0.45])
region = np.random.choice(regions, n, p=region_w)

# lifestyle
smoking = np.random.choice(['Never', 'Former', 'Current'], n, p=[0.5, 0.25, 0.25])
activity = np.random.choice(['Sedentary', 'Moderate', 'Active'], n, p=[0.4, 0.35, 0.25])
diet = np.random.choice(['Poor', 'Average', 'Good'], n, p=[0.3, 0.45, 0.25])
alcohol = np.random.choice(['None', 'Moderate', 'Heavy'], n, p=[0.5, 0.35, 0.15])

bmi = np.random.normal(26, 4.5, n).clip(15, 45)
family_history = np.random.choice(['Yes', 'No'], n, p=[0.3, 0.7])

# clinical
resting_bp = (110 + (age - 40) * 0.5 + (bmi - 25) * 1.2 + np.random.normal(0, 10, n)).clip(90, 200).astype(int)
cholesterol = (180 + (age - 40) * 0.8 + (bmi - 25) * 2.5 + np.where(diet=='Poor', 20, 0) + np.random.normal(0, 25, n)).clip(120, 400).astype(int)
fasting_bs = np.where(np.random.rand(n) < 0.15 + (bmi > 30) * 0.1, 1, 0)
max_hr = (208 - 0.7 * age + np.where(activity=='Active', 10, np.where(activity=='Sedentary', -8, 0)) + np.random.normal(0, 10, n)).clip(70, 210).astype(int)
exercise_angina = np.random.choice(['Yes', 'No'], n, p=[0.32, 0.68])
oldpeak = np.random.exponential(1.0, n).clip(0, 6.2).round(1)
chest_pain = np.random.choice(['Typical Angina', 'Atypical Angina', 'Non-anginal', 'Asymptomatic'], n, p=[0.15, 0.2, 0.25, 0.4])
thal = np.random.choice(['Normal', 'Fixed Defect', 'Reversible Defect'], n, p=[0.55, 0.15, 0.3])

# risk score -> target
risk = (
    (age > 55).astype(int) * 1.2 +
    (sex == 'Male').astype(int) * 0.8 +
    (smoking == 'Current').astype(int) * 1.5 +
    (smoking == 'Former').astype(int) * 0.6 +
    (activity == 'Sedentary').astype(int) * 1.0 +
    (diet == 'Poor').astype(int) * 0.8 +
    (bmi > 30).astype(int) * 1.1 +
    (cholesterol > 240).astype(int) * 1.3 +
    (resting_bp > 140).astype(int) * 1.2 +
    (fasting_bs == 1).astype(int) * 0.7 +
    (family_history == 'Yes').astype(int) * 1.0 +
    (exercise_angina == 'Yes').astype(int) * 1.4 +
    (oldpeak > 2).astype(int) * 1.0 +
    (alcohol == 'Heavy').astype(int) * 0.5 +
    np.random.normal(0, 1.5, n)
)
prob = 1 / (1 + np.exp(-(risk - 6)))
target = (np.random.rand(n) < prob).astype(int)

df = pd.DataFrame({
    'patient_id': [f'P{i+1:05d}' for i in range(n)],
    'age': age,
    'sex': sex,
    'region': region,
    'bmi': bmi.round(1),
    'smoking_status': smoking,
    'physical_activity': activity,
    'diet_quality': diet,
    'alcohol_consumption': alcohol,
    'family_history': family_history,
    'resting_bp': resting_bp,
    'cholesterol': cholesterol,
    'fasting_blood_sugar': fasting_bs,
    'max_heart_rate': max_hr,
    'exercise_angina': exercise_angina,
    'oldpeak': oldpeak,
    'chest_pain_type': chest_pain,
    'thalassemia': thal,
    'heart_disease': target
})

df.to_csv('data/heart_disease.csv', index=False)
print(df.shape)
print(df['heart_disease'].value_counts())
print(df.head())
