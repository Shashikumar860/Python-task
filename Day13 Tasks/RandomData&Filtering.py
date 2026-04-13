import numpy as np
nums = np.random.randint(1, 100, 10)
filter= nums[nums % 5 == 0]
print(filter)
sort_result = np.sort(filter)
print(sort_result)