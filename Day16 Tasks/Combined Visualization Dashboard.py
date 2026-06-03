import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

sales = np.array([100, 200, 150, 300])
products = ["A", "B", "C", "D"]

df = pd.DataFrame({
    "Product": products,
    "Sales": sales
})

plt.figure(figsize=(12, 4))

# Line graph
plt.subplot(1, 3, 1) # 1 row, 3 columns, position 1
plt.plot(df["Product"], df["Sales"], marker='o')
plt.title("Sales Trend")
plt.xlabel("products")
plt.ylabel("sales")

# Bar chart
plt.subplot(1, 3, 2) # 1 row, 3 columns, position 2
plt.bar(df["Product"], df["Sales"])
plt.title("Sales Comparison")
plt.xlabel("products")
plt.ylabel("sales")

# Pie chart
plt.subplot(1, 3, 3) # 1 row, 3 columns, position 3
plt.pie(df["Sales"], labels=df["Product"], autopct='%1.1f%%')
plt.title("Sales Distribution")

plt.tight_layout() #adjust spacing btween subplots to avoid overlapping
plt.show()