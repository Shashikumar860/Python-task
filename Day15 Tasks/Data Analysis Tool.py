import numpy as np
import pandas as pd

# 1. Generate marks using NumPy
marks = np.random.randint(0, 90, size=5)  # 10 students (0–100)

# Student names
names = [f"Student{i+1}" for i in range(5)]

# 2. Convert into Pandas DataFrame
df = pd.DataFrame({
    "Name": names,
    "Marks": marks
})

# 3. Filter passing students (marks >= 50)
passing_students = df[df["Marks"] >= 50]

# 4. Calculate mean using NumPy
average_marks = np.mean(df["Marks"])

# 5. Use loop to print results
print("All Students:")
for index, row in df.iterrows():
    print(f"{row['Name']} - {row['Marks']}")

print("\nPassing Students:")
for index, row in passing_students.iterrows():
    print(f"{row['Name']} - {row['Marks']}")

print(f"\nAverage Marks: {average_marks:.2f}")