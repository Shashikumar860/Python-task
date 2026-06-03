import numpy as np
day1=([30,32,31])
day2=([29,33,34])
temperature=np.array([[day1],[day2]])
print("temperature data:")
print(temperature)
total_temperature=np.sum(temperature)
print("total temperature:", total_temperature)