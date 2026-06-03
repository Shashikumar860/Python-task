import pandas as pd

# Load CSV file
df = pd.read_csv("railway_gauge 1 data.csv")
# First 5 rows
print(df.head())

# Column names
print(df.columns)