import numpy as np
data = [[1, 2, 3], [4, 5], [6]]
flatten = [num for sublist in data for num in sublist]
print(flatten)