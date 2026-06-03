import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

products = ["Pen", "Book", "Pencil"]
sales = np.array([50, 80, 40])

dataframe=pd.DataFrame({"products":products,"sales":sales})
print(dataframe)

plt.bar(dataframe["products"],dataframe["sales"])
plt.title("Product sales")
plt.xlabel("products")
plt.ylabel("sales")
plt.show()