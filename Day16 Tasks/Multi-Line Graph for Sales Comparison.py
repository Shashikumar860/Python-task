import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

data = {
"Month": ["Jan", "Feb", "Mar"],
"Store_A": [100, 150, 200],
"Store_B": [90, 140, 210]
}

dataframe=pd.DataFrame(data)
print(data)

plt.plot(dataframe["Month"], dataframe["Store_A"], label="Store_A")
plt.plot(dataframe["Month"], dataframe["Store_B"], label="Store_B")

plt.xlabel("Month")
plt.ylabel("Sales")
plt.title("Store Sales Comparison")
plt.legend()
plt.show()