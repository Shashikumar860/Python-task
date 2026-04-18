import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

temps = np.array([28, 30, 32, 35, 33, 31, 29])
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

df = pd.DataFrame({
    "Day": days,
    "Temperature": temps
})

plt.figure(figsize=(15, 8))

# Line graph
plt.subplot(2, 3, 1)
plt.plot(df["Day"], df["Temperature"], marker='o')
plt.title("Daily Temperature Trend")

# Bar chart
plt.subplot(2, 3, 2)
plt.bar(df["Day"], df["Temperature"])
plt.title("Day-wise Temperature")

# Pie chart
plt.subplot(2, 3, 3)
labels = np.where(df["Temperature"] > 30, "High", "Low")
counts = pd.Series(labels).value_counts()
plt.pie(counts, labels=counts.index, autopct='%1.1f%%')
plt.title("High vs Low Temperature")

# Histogram
plt.subplot(2, 3, 4)
plt.hist(df["Temperature"])
plt.title("Temperature Distribution")

# Scatter plot
plt.subplot(2, 3, 5)
plt.scatter(df.index, df["Temperature"])
plt.title("Index vs Temperature")

plt.tight_layout()
plt.show()