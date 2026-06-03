import pandas as pd
df = pd.DataFrame({
    "Name": ["A", "B", "C", "D"],
    "Marks": [50, 80, 30, 90]
})
print(df)
df["Status"] = df["Marks"].apply(lambda x: "Pass" if x >= 50 else "Fail")
print(df)
passed_students = df[df["Status"] == "Pass"]
print(passed_students)
average_marks = passed_students["Marks"].mean()
print(average_marks)