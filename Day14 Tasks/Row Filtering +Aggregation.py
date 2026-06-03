import numpy as np
import pandas as pd
arr = np.array([
    [100, 200],
    [150, 250],
    [80, 120],
    [300, 400]
])
dataframe = pd.DataFrame(arr, columns=["Sales", "Profit"])
print(dataframe)
filtered_dataframe = dataframe[dataframe["Sales"] > 100]
print("filtered data:",filtered_dataframe)
average_profit = filtered_dataframe["Profit"].mean()
print("average profit:",average_profit)