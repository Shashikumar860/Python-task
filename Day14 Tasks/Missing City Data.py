import pandas as pd
cities = {"Delhi": 2000000, "Mumbai": 3000000, "Chennai": 1500000}
Series = pd.Series(cities, index=["Delhi", "Chennai", "Bangalore"])
print(Series)
missing_values=Series[Series.isna()]
print(missing_values)