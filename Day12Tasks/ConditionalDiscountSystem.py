import numpy as np
prices = [100, 200, 300, 400]
updated_list = [p * 0.9 if p > 200 else p for p in prices]
print(updated_list)