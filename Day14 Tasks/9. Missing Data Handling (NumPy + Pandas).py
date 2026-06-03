import numpy as np
import pandas as pd
arr = np.array([10, np.nan, 30, np.nan, 50])
Panda_series = pd.Series(arr, index=[10, np.nan, 30, np.nan, 50])
print("panda values:",Panda_series)
mean_value = Panda_series.mean()
print("mean:",mean_value)
#replacing the values with mean value
Updated = Panda_series.fillna(mean_value)
print("updated dat:",Updated)