import numpy as np
array = [-5, 10, 15, -2, 20, 25, 30]
array = np.array(array)
filtered = array[(array> 0) & (array % 2 == 0)]
print(filtered)