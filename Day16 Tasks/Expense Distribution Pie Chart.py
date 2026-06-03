import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

expenses = np.array([500, 300, 200])
labels = ["Food", "Rent", "Travel"]

plt.pie(expenses, labels=labels, autopct='%1.1f%%')
plt.title("Monthly expenses")
plt.show()
