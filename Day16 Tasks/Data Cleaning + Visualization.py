import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

data = np.array([100, np.nan, 200, 150, np.nan, 300])

series=pd.Series(data)
print(series)
average=series.mean()
series=series.fillna(average)
print(series)

plt.figure(figsize=(10,2))

plt.subplot(1,2,1)
plt.plot(series,marker="o")
plt.title("bar graph of clened data")
plt.xlabel("values")
plt.ylabel("data")

bar_avg=series[series>average]
plt.subplot(1,2,2)
plt.bar(bar_avg.index,bar_avg.values)
plt.title("Bar chart of values > average")
plt.xlabel("values")
plt.ylabel("data")
plt.show()