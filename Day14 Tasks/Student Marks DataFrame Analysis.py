import numpy as np
import pandas as pd
data = pd.DataFrame({
"Name": ["A", "B", "C"],
"Math": [80, 70, 60],
"Science": [90, 60, 70]
})
Data_frame=pd.DataFrame(data,columns=["Math", "Science"])
print(Data_frame)
Data_frame["Total"] = Data_frame["Math"] + Data_frame["Science"]
print(Data_frame)
Highest = Data_frame["Total"].idxmax()
print(Highest)