import numpy as np
customers=np.array(["Ravi", "Anil", "Sita", "John"])
alphabet=np.sort(customers)
print(alphabet)

import numpy as np
arr = np.array([1, 2, 3, 4, 5])
x = arr.copy()
arr[0] = 42
print(arr)
print(x)