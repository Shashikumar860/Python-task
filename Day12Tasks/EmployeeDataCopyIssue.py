import numpy as np
import copy
employee = [[101, "A"], [102, "B"], [103, "C"]]
deepcopy = copy.deepcopy(employee)
employee[0][1] = "S"
print(employee)  
print(deepcopy)  