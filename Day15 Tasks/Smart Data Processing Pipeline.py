"""9. Smart Data Processing Pipeline
Scenario:
A system processes numeric data from file.
Task:
● Read numbers from a file
● Use NumPy for calculations (mean, std)
● Convert results to Pandas DataFrame
● Use exception handling for bad data
● Use a generator to stream data
● Apply decorator to measure execution time"""

import numpy as np
import pandas as pd
import time
from functools import wraps
def dec(fun):
    def wrapper(file):
        start_time=time.time()
        result=fun(file)
        end_time=time.time()
        print("excution time: ",np.fabs(start_time-end_time))
        return result
    return wrapper
#read
def gen(file):
    for i in open(file):
        try:    
            yield int(i.strip())
        except Exception as e:
            print("bad data",i.strip())
@dec
def calculation(file):
    lst=list(gen(file))
    arr=np.array(lst)
    mean=np.mean(arr)
    std=np.std(arr)
    df=pd.DataFrame({"arr":arr,"std":arr-mean})
    return df
print(calculation("nums.txt"))