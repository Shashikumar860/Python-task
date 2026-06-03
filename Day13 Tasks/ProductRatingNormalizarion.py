import numpy as np
ratings = np.array([2, 3, 4, 5, 1])
minimum=ratings.min() #1
maximum=ratings.max() #5
print(minimum,maximum)
#normalize= value-min/min-max(5-1=4)  
# (2-1)/4=1/4=0.25 , (3−1)/4=2/4=0.50   
normalized = (ratings - minimum) / (maximum - minimum)
print(normalized)