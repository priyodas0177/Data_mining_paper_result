import pandas as pd
from os.path import join

base_path= "/Users/hdpriyo/Desktop/Paper/dataset"


Student_info=pd.read_csv(join(base_path, "studentInfo.csv"))
Student_assessment= pd.read_csv(join(base_path, "studentAssessment.csv"))
Student_registration= pd.read_csv(join(base_path, "studentRegistration.csv"))
student_vle=pd.read_csv(join(base_path, "studentVle.csv"))

merge1= pd.merge (Student_info, Student_assessment, on="id_student", how="left" )
merge2= pd.merge (merge1, Student_registration, on=["id_student", "code_module", "code_presentation"], how="left")
final_merge= pd.merge (merge2,student_vle, on=["id_student", "code_module", "code_presentation"], how="left")
final_merge.to_csv("marge_file.csv", index=False)