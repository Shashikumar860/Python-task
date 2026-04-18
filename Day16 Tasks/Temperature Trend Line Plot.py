import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

temps = np.array([28, 30, 32, 31, 29])
series=pd.Series(temps)
print(series)

plt.plot(series)
plt.title("Daily temperatures")
plt.grid()
plt.show()