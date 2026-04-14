import numpy as np
import pandas as pd
arr = np.array([10, 25, 30, 15, 40])
Panda_series = pd.Series(arr)
print(Panda_series)
value=Panda_series[Panda_series>20]
print(value)