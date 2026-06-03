import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

marks = np.array([45, 80, 60, 30, 90])
names = ["A", "B", "C", "D", "E"]

dataframe=pd.DataFrame({"marks":marks,"names":names})
print(dataframe)

filter_students=dataframe[dataframe["marks"]>50]
print(filter_students)

plt.bar(filter_students["names"],filter_students["marks"])
plt.xlabel("marks>50")
plt.ylabel("names")
plt.show()