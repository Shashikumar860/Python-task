import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


salaries = np.array([25000, 30000, 28000, 40000, 50000, 35000])
departments = ["HR", "IT", "HR", "IT", "Sales", "Sales"]

df = pd.DataFrame({
    "Department": departments,
    "Salary": salaries
})

plt.figure(figsize=(15, 8))

# Line graph
plt.subplot(2, 3, 1)
plt.plot(df["Salary"], marker='o')
plt.title("Salary Trend")

# Bar chart (average salary per department)
plt.subplot(2, 3, 2)
dept_avg = df.groupby("Department")["Salary"].mean()
plt.bar(dept_avg.index, dept_avg.values)
plt.title("Avg Salary by Department")

# Pie chart
plt.subplot(2, 3, 3)
dept_count = df["Department"].value_counts()
plt.pie(dept_count, labels=dept_count.index, autopct='%1.1f%%')
plt.title("Department Distribution")

# Histogram
plt.subplot(2, 3, 4)
plt.hist(df["Salary"])
plt.title("Salary Distribution")

# Scatter plot
plt.subplot(2, 3, 5)
plt.scatter(df.index, df["Salary"])
plt.title("Index vs Salary")

plt.tight_layout()
plt.show()