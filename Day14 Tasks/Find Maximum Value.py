import pandas as pd
import numpy as np
arr = np.array([12, 45, 22, 67, 34])
Panda_series = pd.Series(arr, index=[12, 45, 22, 67, 34])
Maximum=arr.max()
print(Panda_series)
print(Maximum)