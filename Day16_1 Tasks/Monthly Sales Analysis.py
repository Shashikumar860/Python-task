import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

sales = np.array([100, 150, 200, 180, 220, 300])
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

dataframe=pd.DataFrame({"sales":sales, "months": months})
print(dataframe)
 
plt.figure(figsize=(15,8))
#Line graph
plt.subplot(2,3,1)
plt.plot(dataframe["months"],dataframe["sales"], marker='o' )
plt.title("Line graph → sales trend")
plt.xlabel("sales")
plt.ylabel("months")

#Bar chart 
plt.subplot(2,3,2)
plt.bar(dataframe["months"],dataframe["sales"])
plt.title("month-wise comparison")
plt.xlabel("sales")
plt.ylabel("months")

#Pie chart 
plt.subplot(2,3,3)
plt.pie(dataframe["sales"], labels=dataframe["months"], autopct='%1.1f%%')
plt.title("Sales Contribution")

# histogram
plt.subplot(2, 3, 4)
plt.hist(dataframe["sales"])
plt.title("Sales Distribution")

# Scatter plot
plt.subplot(2, 3, 5)
plt.scatter(dataframe.index, dataframe["sales"])
plt.title("Index vs Sales")


plt.tight_layout()
plt.show()

 