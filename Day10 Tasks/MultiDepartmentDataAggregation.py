import numpy as np
branchA=np.array([[10,20],[30,40]])
branchB=np.array([[5,15],[25,35]])
employees=branchA+branchB
totalemployee=np.sum(employees)
print(totalemployee)