import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

sales = np.array([100, 150, 200, 250, 300])
months = ["Jan", "Feb", "Mar", "Apr", "May"]

dataframe=pd.DataFrame({"months":months,"sales": sales})
print(dataframe)

plt.plot(dataframe["months"], dataframe["sales"])
plt.xlabel('months')
plt.ylabel('sales')
plt.show()