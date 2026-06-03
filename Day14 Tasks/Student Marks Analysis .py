import numpy as np
import pandas as pd
arr = np.array([
    [80, 90],
    [70, 60],
    [85, 95]
])
Data_frame=pd.DataFrame(arr,columns=["Math", "Science"])
print(Data_frame)
Data_frame["Total"] = Data_frame["Math"] + Data_frame["Science"]
print(Data_frame)
Highest = Data_frame["Total"].idxmax()
print(Highest)