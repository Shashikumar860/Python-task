import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

names = ["A", "B", "C", "D"]
marks = np.array([70, 85, 60, 90])

dataframe=pd.DataFrame({"names":names,"marks":marks})
print(dataframe)

plt.bar(dataframe["names"],dataframe["marks"])
plt.xlabel("students names")
plt.ylabel("marks")
plt.title("student marks")
plt.show()
