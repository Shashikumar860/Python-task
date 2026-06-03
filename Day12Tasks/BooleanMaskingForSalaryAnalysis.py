import numpy as np
Employee_salaries = np.array([25000, 40000, 15000, 50000, 30000])
filtered = Employee_salaries[Employee_salaries > 30000]
print("Filtered salaries:", filtered)
count = np.sum(Employee_salaries > 30000)
print("Count:", count)