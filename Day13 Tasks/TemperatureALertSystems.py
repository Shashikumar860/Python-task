import numpy as np
temperature = np.array([28, 32, 35, 31, 29, 40, 38])
indices1 = np.where(temperature > 30)[0]

#print true false
boolean_values=[temperature > temperature.mean()]
print(indices1)
print(boolean_values)