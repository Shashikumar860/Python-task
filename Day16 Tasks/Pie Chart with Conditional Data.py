import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

scores = np.array([40, 60, 80, 30, 90])  
 
result = np.where(scores > 50, "Pass", "Fail")
print(result)

"""#using Numpy
pass_count = np.sum(scores > 50)
fail_count = np.sum(scores <= 50)

print("Pass:", pass_count)
print("Fail:", fail_count)

"""
#using pandas
series = pd.Series(result)
counts = series.value_counts()
print(counts) 

plt.pie(counts, labels=counts.index, autopct='%1.1f%%')

plt.title("Pass vs Fail Distribution")

plt.show()