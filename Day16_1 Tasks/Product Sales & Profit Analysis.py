import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

sales = np.array([200, 300, 250, 400, 350])
profit = np.array([50, 70, 60, 90, 80])
products = ["A", "B", "C", "D", "E"]

df = pd.DataFrame({
    "Product": products,
    "Sales": sales,
    "Profit": profit
})

plt.figure(figsize=(15, 8))

# Line graph
plt.subplot(2, 3, 1)
plt.plot(df["Product"], df["Sales"], marker='o')
plt.title("Sales Trend")

# Bar chart
plt.subplot(2, 3, 2)
plt.bar(df["Product"], df["Sales"])
plt.title("Product vs Sales")

# Pie chart
plt.subplot(2, 3, 3)
plt.pie(df["Sales"], labels=df["Product"], autopct='%1.1f%%')
plt.title("Sales Contribution")

# Histogram
plt.subplot(2, 3, 4)
plt.hist(df["Profit"])
plt.title("Profit Distribution")

# Scatter plot
plt.subplot(2, 3, 5)
plt.scatter(df["Sales"], df["Profit"])
plt.title("Sales vs Profit")

plt.tight_layout()
plt.show()