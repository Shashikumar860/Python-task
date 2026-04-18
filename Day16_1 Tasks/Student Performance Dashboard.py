import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

marks = np.array([45, 67, 89, 56, 72, 91, 38])
students = ["A", "B", "C", "D", "E", "F", "G"]

df = pd.DataFrame({
    "Student": students,
    "Marks": marks
})

plt.figure(figsize=(15, 8))

# Line graph
plt.subplot(2, 3, 1) #2 column, 3 rows, 1 position
plt.plot(df["Student"], df["Marks"], marker='o')
plt.title("Marks Trend")

# Bar chart
plt.subplot(2, 3, 2) #2 column, 3 rows, 2 position
plt.bar(df["Student"], df["Marks"])
plt.title("Student vs Marks")

# Pie chart
plt.subplot(2, 3, 3)  #2 column, 3 rows, 3 position
result = np.where(df["Marks"] > 50, "Pass", "Fail")
counts = pd.Series(result).value_counts()
plt.pie(counts, labels=counts.index, autopct='%1.1f%%')
plt.title("Pass vs Fail")

# Histogram
plt.subplot(2, 3, 4)  #2 column, 3 rows, 4 position
plt.hist(df["Marks"])
plt.title("Marks Distribution")

# Scatter plot
plt.subplot(2, 3, 5) #2 column, 3 rows, 5 position
plt.scatter(df.index, df["Marks"])
plt.title("Index vs Marks")

plt.tight_layout()
plt.show()