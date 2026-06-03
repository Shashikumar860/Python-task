import numpy as np
data = np.array([1, 2, 2, 3, 1, 4, 2, 3])
unique_value = np.unique(data)
print("unique:",unique_value)
counts=np.unique(data,return_counts=True)
print(counts)