import pandas as pd
S1 = pd.Series([10, 20, 30], index=["a", "b", "c"])
S2 = pd.Series([5, 15, 25], index=["b", "c", "d"])
print(S1,S2)
add=S1+S2
print(add)
Repalcing = add.fillna(0)
print(Repalcing)