import pandas as pd
df = pd.DataFrame({
    "A": [10, 20, 30],
    "B": [5, 15, 25]
}, index=["x", "y", "z"])
print(df)
rowindex_y = df.loc["y"]
print(rowindex_y)
delete_x = df.drop("x")
print(delete_x)