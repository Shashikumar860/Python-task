import numpy as np
sales = np.array([12000, 18000, 9000, 22000, 15000, 30000])
#avaerage=total sum of sales /6
filter_sales = [sales > sales.mean()]
print(filter_sales)