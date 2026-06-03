import numpy as np
dataset=np.array([10, 20, 30, 40])
copy=dataset.copy()
dataset[1]=50
print("orginal:",dataset)
print("modified:",copy)

view=dataset.view()
dataset[1]=60
print(dataset)
print(view)

