import pandas as pd
df = pd.DataFrame({"Price": [100, 200, 300]})
print(df)
df["Discount"] = df["Price"] * 0.10
print(df)
df["Final Price"] = df["Price"] - df["Discount"]
print(df)