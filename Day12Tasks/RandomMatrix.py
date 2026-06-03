import numpy as np
matrix = np.random.randint(0, 51, (3, 3))
print("Matrix:", matrix)
filtered = matrix[matrix > 25]
print("Values", filtered)
