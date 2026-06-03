import numpy as np
import pandas as pd
names = np.array(["A", "B", "C"])
marks = np.array([80, 90, 70])
dataFrame = pd.DataFrame({"Name": names,"Marks": marks})
print(dataFrame)
filtered_dataFrame = dataFrame[dataFrame["Marks"] > 75]
print(filtered_dataFrame)