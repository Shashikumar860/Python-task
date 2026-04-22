# ============================================================
# Project Title: Railway Gauge Data Analysis
# Analyze railway gauge dataset using NumPy, Pandas, Matplotlib
# ============================================================

# ============================================================
# 📦 1. Import Required Libraries
# ============================================================
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
#===============================================================================
#Scenario 1: Basic Data Loading & Cleaning
#===============================================================================
"""Tasks:
1. Load the dataset into a Pandas DataFrame.
2. Display the first 5 rows and column names.
3. Check for missing values and replace them with 0.
4. Convert all gauge columns (Broad, Metre, Narrow, Total) to numeric types."""

#load the csv file
df = pd.read_csv("railway_gauges.csv")
#read first 5 rows
print(df.head())
#read only columns names
print("\n Column names: \n",df.columns)

#check missing values nan and replace with 0
print(df.isnull().sum())
print(df.fillna(0))

#coverting guage columns to numeric types
guage_columns = ['Broad Gauge', 'Metre Gauge', 'Narrow Gauge', 'Total']
df[guage_columns] = df[guage_columns].apply(pd.to_numeric, errors='coerce').fillna(0) #errors='coerce' → converts invalid values to NaN

#===============================================================================
#Scenario 2: Simple Visualization
#===============================================================================
"""Tasks:
1. Extract Year and Total columns.
2. Plot a line graph showing Total tracks over years.
3. Add:
○ Title
○ X and Y labels
4. Identify whether the trend is increasing or decreasing."""

#extracting year and total columns
year=df["Year"]
total=df["Total"]

#poltting line graph
plt.figure(figsize=(12,8))
plt.plot(df["Year"],df["Total"], marker='o')
plt.xticks(rotation=70) #rotate years all will be visible
plt.title("Total tracks over years")
plt.xlabel("Year")
plt.ylabel("Total Tracks")
plt.show()

# check trend is increasing or decreasing
if total.iloc[-1] > total.iloc[0]:
    print("Trend is Increasing")
elif total.iloc[-1] < total.iloc[0]:
    print("Trend is Decreasing")
else:
    print("Trend is Stable")

#===============================================================================
#Scenario 3: Filtering + Bar Chart
#===============================================================================
"""Tasks:
1. Filter the dataset for years after 2000.
2. Select Broad Gauge, Metre Gauge, and Narrow Gauge.
3. Plot a grouped bar chart comparing all three gauges.
4. Add legend and proper labels.
5. Identify which gauge dominates in recent years."""

#Filterig data set year>2000
df['Year_num'] = df['Year'].str[:4].astype(int)  #(2006-07) [:4] takes first 4 characyers 
df_filter=df[df["Year_num"]>2000]
print(df_filter)

#Grouped bar chart
x = np.arange(len(df_filter)) 
w = 0.25
plt.figure(figsize=(12,8))
plt.bar(x, df_filter["Broad Gauge"], w, label="Broad") #x positions on the x-axis , w width of each bar
plt.bar(x + w, df_filter["Metre Gauge"], w, label="Metre")  #x + w shifts bars slightly to the right
plt.bar(x + 2*w, df_filter["Narrow Gauge"], w, label="Narrow")  #x + 2*w shifts even more to the right
plt.xticks(x, df_filter["Year"], rotation=70)
plt.xlabel("Year")
plt.ylabel("Tracks")
plt.title("Gauge Comparison After 2000")
plt.legend()
plt.show()

#identifying gauges domination
gauges_dominant = df_filter[['Broad Gauge', 'Metre Gauge', 'Narrow Gauge']].mean()
dominant = gauges_dominant.idxmax()  #idmax selcts index with column highest value
print("gauge Dominant:",dominant)

#===============================================================================
#Scenario 4: Feature Engineering + Pie Chart
#===============================================================================

"""Tasks:
1. Calculate total sum of each gauge across all years.
2. Create a new structure (Series/DataFrame) for totals.
3. Plot a pie chart showing percentage contribution.
4. Add percentage labels (autopct).
5. Interpret which gauge contributes the most."""

# Calculate total sum of gauges across all years
total_sum=df[["Broad Gauge", "Metre Gauge", "Narrow Gauge"]].sum()
print(total_sum)

#new structure (Series/DataFrame) for totals.
dataframe = total_sum.to_frame(name="Total")
print(dataframe)

#Plot Pie Chart
plt.pie(total_sum, labels=total_sum.index, autopct='%1.1f%%',explode=(0.1,0,0),startangle=180)
plt.savefig("Percentage Contribution")
plt.title("Percentage Contribution")
plt.show()

#interpret gauges
print("Highest contribution:", total_sum.idxmax())

#===============================================================================
#Scenario 5: Advanced Analysis + Multiple Graphs
#===============================================================================
"""�Tasks:
1. Create new columns:
○ % Broad Gauge
○ % Metre Gauge
○ % Narrow Gauge
2. Use NumPy (np.diff) to calculate yearly growth of Total tracks.
3. Plot:
○ Line graph for all gauges
○ Stacked bar chart showing composition
4. Highlight:
○ Years with highest growth
○ Decline in any gauge
5. Provide a final conclusion:
“Is the railway system shifting towards a single dominant gauge?” """

# Total tracks per year
df["Year_num"] = df["Year"].astype(str).str[:4].astype(int)
df["Total"] = df["Broad Gauge"] + df["Metre Gauge"] + df["Narrow Gauge"]

# Percentage columns
df["% Broad Gauge"] = (df["Broad Gauge"] / df["Total"]) * 100
df["% Metre Gauge"] = (df["Metre Gauge"] / df["Total"]) * 100
df["% Narrow Gauge"] = (df["Narrow Gauge"] / df["Total"]) * 100

#calculate yearly growth of Total tracks.
yearly_growth = np.diff(df["Total"]) #np.diff() calculates the difference between consecutive values
print("Yearly Growth:", yearly_growth) #Difference = Current Year - Previous Year

#Plot line graph
plt.figure(figsize=(12,8))
plt.plot(df["Year"], df["Broad Gauge"], label="Broad Gauge" ,marker='o')
plt.plot(df["Year"], df["Metre Gauge"], label="Metre Gauge" ,marker='o')
plt.plot(df["Year"], df["Narrow Gauge"], label="Narrow Gauge" ,marker='o')
plt.xticks(rotation=70)
plt.legend()
plt.title("Line Graph for all Gauges")
plt.savefig("Line Graph for all Gauges")
plt.xlabel("Year")
plt.ylabel("Tracks")
plt.show()

#Stacked bar chart 
x = np.arange(len(df_filter)) 
w = 0.25
plt.figure(figsize=(12,8))
plt.bar(df["Year"], df["Broad Gauge"], label="Broad Gauge")
plt.bar(df["Year"], df["Metre Gauge"], label="Metre Gauge")
plt.bar(df["Year"], df["Narrow Gauge"], label="Narrow Gauge")
plt.xticks(rotation=70)
plt.legend()
plt.savefig("Gauge Composition")
plt.title("Gauge Composition")
plt.xlabel("Year")
plt.ylabel("Tracks")
plt.show()

# Highlights
# Highest growth year
max_growth_year = df["Year"].iloc[np.argmax(yearly_growth) + 1]
print("Highest Growth Year:", max_growth_year)
# Check decline
if any(yearly_growth < 0):
    print("Decline observed in some years")
else:
    print("No decline observed")

#Final Conclusion
print("Yes, the railway system is clearly shifting toward a single dominant gauge that is Broad Gauge.")
