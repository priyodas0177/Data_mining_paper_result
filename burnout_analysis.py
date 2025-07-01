import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('base_path= "/Users/hdpriyo/Desktop/Paper/burnout_prediction_dataset.csv')
print("✅ Dataset loaded.")

# Step 1: Fix imd_band (replace invalid values with appropriate range)
invalid_imd_values = [
    '11-Oct', '12-Oct', '13-Oct', '14-Oct', '15-Oct',
    '16-Oct', '17-Oct', '18-Oct', '19-Oct', '20-Oct'
]
df['imd_band'] = df['imd_band'].replace(invalid_imd_values, '20-30%')
valid_imd = [
    '0-10%', '10-20%', '20-30%', '30-40%', '40-50%',
    '50-60%', '60-70%', '70-80%', '80-90%', '90-100%'
]
df['imd_band'] = df['imd_band'].where(df['imd_band'].isin(valid_imd))
df['imd_band'] = df['imd_band'].fillna(df['imd_band'].mode()[0])
print(f"✅ Cleaned 'imd_band'. Filled missing/invalid with mode: {df['imd_band'].mode()[0]}")

# Step 2: Fill remaining missing values with suitable values
for col in ['id_assessment', 'date_submitted', 'is_banked', 'score',
            'date_registration', 'date_unregistration', 'id_site', 'date', 'sum_click']:
    if df[col].isnull().sum() > 0:
        median_val = df[col].median()
        df[col].fillna(median_val, inplace=True)
        print(f"✅ Filled missing values in '{col}' with median: {median_val}")

# Step 3: Convert date fields
course_start = pd.to_datetime('2013-01-01')
df['date_registration_dt'] = course_start + pd.to_timedelta(df['date_registration'], unit='D')
df['date_dt'] = course_start + pd.to_timedelta(df['date'], unit='D')
print("✅ Converted date columns.")

# Step 4: Feature 1 – Clicks per week
df['weeks_active'] = ((df['date_dt'] - df['date_registration_dt']).dt.days // 7).clip(lower=1)
df['clicks_per_week'] = df['sum_click'] / df['weeks_active']
avg_clicks = df.groupby('id_student')['clicks_per_week'].mean().reset_index(name='avg_clicks_per_week')
print("✅ Calculated clicks per week.")

# Step 5: Feature 2 – Missed/failed assessments
df['score_filled'] = df['score'].fillna(0)
df['failed_or_missed'] = df['score_filled'].apply(lambda x: 1 if x == 0 else 0)
failed_counts = df.groupby('id_student')['failed_or_missed'].sum().reset_index(name='total_failed_or_missed')
print("✅ Counted failed or missed assessments.")

# Step 6: Feature 3 – Engagement duration
last_activity = df.groupby('id_student')['date_dt'].max().reset_index(name='last_activity_dt')
reg_dates = df[['id_student', 'date_registration_dt']].drop_duplicates('id_student')
engagement = pd.merge(last_activity, reg_dates, on='id_student')
engagement['engagement_duration_days'] = (engagement['last_activity_dt'] - engagement['date_registration_dt']).dt.days
print("✅ Calculated engagement duration.")

# Step 7: Feature 4 – Demographics
demo_cols = [
    'id_student', 'gender', 'region', 'highest_education', 'imd_band',
    'age_band', 'num_of_prev_attempts', 'studied_credits', 'disability',
    'final_result', 'burnout'
]
demographics = df[demo_cols].drop_duplicates('id_student')
print("✅ Extracted demographics.")

# Step 8: Merge all features
final_df = demographics.merge(avg_clicks, on='id_student') \
                       .merge(failed_counts, on='id_student') \
                       .merge(engagement[['id_student', 'engagement_duration_days']], on='id_student')
print("✅ Merged all features.")

# Step 9: Encode categorical variables
final_df['gender_flag'] = final_df['gender'].apply(lambda x: 1 if x == 'M' else 0)
final_df = pd.get_dummies(final_df, columns=['age_band', 'highest_education'], prefix=['age', 'edu'])
final_df['imd_band'] = final_df['imd_band'].astype('category')
print("✅ Encoded gender and selected categorical variables.")

# Step 10: Final Check – Ensure no missing values
if final_df.isnull().sum().sum() == 0:
    print("✅ Final dataset has NO missing values.")
else:
    print(f" Warning: {final_df.isnull().sum().sum()} missing values still present.")

# Step 11: Save final dataset
#final_df.to_csv('C:/Users/Asus/Downloads/Final_dataset_cleanedf.csv', index=False)
#print("✅ Final cleaned dataset saved as 'Final_dataset_cleaned.csv'.")
