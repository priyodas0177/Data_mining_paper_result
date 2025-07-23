# we are create a conferece paper using data mining rool

We're building a system to predict which students might be at risk of academic burnout. 

🎯 Step-by-Step Usage Plan:
# Step 1: Merge the Datasets:
• Merge studentInfo, studentAssessment, and studentVle using id_student and code_module + code_presentation.
• This gives a full view of a student’s background, engagement, and outcome.

# Step 2: Define Burnout Proxy Labels
Since “burnout” isn't labeled, we define it like this:
i. Low activity on studentVle (below 25th percentile)	-> Yes
ii. Missed or failed most assessments	-> Yes
iii. Final result in studentInfo = Withdrawn or Fail ->  Yes
iv. Consistent drop in engagement over time	-> Yes
v. You can define a binary column: burnout_risk = 1 for "At Risk", 0 for "Not at Risk".
vi. Otherwise	❌ Not at risk -> 

# Step 3: Feature Engineering
Create features like:
• Avg LMS activity/week (from studentVle.csv)
• Total number of missed/failed assessments
• Time gap between registration and last activity
• Demographic flags (from studentInfo.csv) like age group, education level

# Step 4: Build Model
Use Random Forest, XGBoost, or Logistic Regression to classify burnout_risk.
