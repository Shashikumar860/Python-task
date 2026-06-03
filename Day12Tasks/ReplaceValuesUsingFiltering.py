import numpy as np
dataset = np.array([5, 12, 18, 7, 25, 30])
dataset[dataset > 15] = 0
print(dataset)