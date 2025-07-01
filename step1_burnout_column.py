import pandas as pd
base_path= "/Users/hdpriyo/Desktop/Paper/marge_file.csv"
ACCEPTED_CONDITION_COLUMNS=['sum_click', 'score', 'final_result', 'is_banked']

final_merge=pd.read_csv(base_path)

final_merge["burnout"]=0
# 1. Low activity on studentVle (below 25th percentile)
condition_column = 'sum_click'
mask = final_merge[condition_column] <= final_merge[condition_column].quantile(0.25)
final_merge.loc[mask, 'burnout'] = 1

#2. Missed or failed most assessments	
condition_column = 'score'
mask = final_merge[condition_column] <= 30
final_merge.loc[mask, 'burnout'] = 1

# 3.Final result in studentInfo = Withdrawn or Fail	
condition_column = 'final_result'
mask = final_merge[condition_column].isin(['Withdrawn', 'Fail'])
final_merge.loc[mask, 'burnout'] = 1

# 4. Consistent drop in engagement over time
#    Replace 'col1' with the actual column name you want to use for the condition.
#    condition_column1 = 'score'
condition_column2='is_banked'

#.  Create a boolean mask to identify the rows
#mask1= final_merge[condition_column1] <= 30
mask2= final_merge[condition_column2]==1
#final_mask= mask1 & mask2
#final_merge.loc[final_mask, 'burnout'] = 1
final_merge.loc[mask2, 'burnout'] = 1


final_merge.to_csv("Final_dataset.csv", index=False)
