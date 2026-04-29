# ==========================================================================================================
# 📊 Project Title: House Sales Data Analysis (kc_house_data.csv)
# Analyze house sales dataset using Pandas, NumPy, and Matplotlib
# ==========================================================================================================

# ==========================================================================================================
# 📦 Import Required Libraries
# ==========================================================================================================
import pandas as pd              # For data handling
import numpy as np               # For numerical operations
import matplotlib.pyplot as plt  # For visualization
  
# ==========================================================================================================
# 🟢 SCENARIO 1: Data Loading & Basic Cleaning
# ==========================================================================================================
# Tasks:
# 1. Load dataset using Pandas
# 2. Display first 5 rows and column names
# 3. Check missing values in bedrooms, bathrooms, sqft_living, price
# 4. Fill missing values:
#    - bedrooms → mode
#    - bathrooms → mean
#    - sqft_living → mean
#    - price → mean
# 5. Convert columns to numeric if required
# ==========================================================================================================
 
# 1.1 Load dataset
df = pd.read_csv("kc_house_data.csv")
 
# 1.2 Display first 5 rows
print("First 5 rows:")
print(df.head())
print("------------------------------------------------------------")
 
# Display column names
print("Column names:")
print(df.columns)
print("------------------------------------------------------------")
 
# 1.3 Check missing values
print("Missing values BEFORE cleaning:")
print(df[["bedrooms", "bathrooms", "sqft_living", "price"]].isnull().sum())
print("------------------------------------------------------------")
 
# 1.4  Fill missing values
df["bedrooms"].fillna(df["bedrooms"].mode()[0], inplace=True)   # mode
df["bathrooms"].fillna(df["bathrooms"].mean(), inplace=True)    # mean
df["sqft_living"].fillna(df["sqft_living"].mean(), inplace=True) # mean
df["price"].fillna(df["price"].mean(), inplace=True)            # mean
 
# Check missing values after cleaning
print("Missing values AFTER cleaning:")
print(df[["bedrooms", "bathrooms", "sqft_living", "price"]].isnull().sum())
print("------------------------------------------------------------")

# 1.5 Convert columns to numeric (invalid values become NaN)
df["bedrooms"] = pd.to_numeric(df["bedrooms"], errors="coerce")
df["bathrooms"] = pd.to_numeric(df["bathrooms"], errors="coerce")
df["sqft_living"] = pd.to_numeric(df["sqft_living"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# ==========================================================================================================
# 🔵 SCENARIO 2: Line Graph + Save
# ==========================================================================================================
# Tasks:
# 1. Select id and price columns
# 2. Take first 10 rows
# 3. Convert price to NumPy array
# 4. Plot line graph (X = index, Y = price)
# 5. Add title, labels
# 6. Save graph as "house_prices_line.png"
# ==========================================================================================================

# 2.1 Select id and price columns
subset = df[["id", "price"]]
 
# 2.2 Take first 10 rows
subset_10 = subset.head(10)
 
# 2.3 Convert price to NumPy array
price_array = subset_10["price"].to_numpy()
 
# Create X-axis (0 to 9)
x_index = np.arange(len(price_array))
 
# 2.4 Plot line graph
plt.figure(figsize=(12,8))
plt.plot(x_index, price_array, marker="o")
# Add title and labels
plt.title("House Prices (First 10 Entries)")
plt.xlabel("Index (0-9)")
plt.ylabel("Price")
plt.xticks(rotation=70)
plt.tight_layout()
plt.savefig("house_prices_line.png")
plt.show()
 
# ==========================================================================================================
# 🟡 SCENARIO 3: Filtering + Bar Chart + Save
# ==========================================================================================================
# Tasks:
# 1. Filter houses where price > 1,000,000
# 2. Count number of houses per bedrooms
# 3. Select top bedroom categories
# 4. Convert to NumPy arrays
# 5. Plot bar chart
# 6. Rotate labels
# 7. Save graph as "expensive_houses_bar.png"
# ==========================================================================================================
 
# 3.1 Filter houses where price > 1,000,000
expensive_houses = df[df["price"] > 1000000]
 
# 3.2 Count number of houses per bedroom
bedroom_counts = expensive_houses["bedrooms"].value_counts()
 
# Select top bedroom categories (top 5)
top_bedrooms = bedroom_counts.head(5)
 
# 3.4 Convert to NumPy arrays
bedrooms = top_bedrooms.index.to_numpy()
counts = top_bedrooms.values
 
# 3.5 Plot bar chart
plt.figure(figsize=(12,8))
plt.bar(bedrooms, counts)
plt.title("Expensive Houses by Bedroom Count")
plt.xlabel("Number of Bedrooms")
plt.ylabel("Number of Houses")
plt.xticks(rotation=70)
plt.tight_layout()
plt.savefig("expensive_houses_bar.png")
plt.show()
 
# ==========================================================================================================
# 📊 SCENARIO 4: Pie Chart (Bedroom Distribution) + Save
# ==========================================================================================================
# Tasks:
# 1. Count number of houses by bedrooms
# 2. Select top 5 bedroom categories
# 3. Prepare labels and values
# 4. Plot a pie chart
# 5. Add percentage labels
# 6. Save graph as "bedroom_distribution.png"
# ==========================================================================================================
 
# 4.1 Count number of houses by bedrooms
bedroom_counts = df["bedrooms"].value_counts()
 
# 4.2 Select top 5 bedroom categories
top_5_bedrooms = bedroom_counts.head(5)
 
# 4.3 Prepare labels (bedroom numbers)
labels = top_5_bedrooms.index.to_numpy()
# Prepare values (counts)
values = top_5_bedrooms.values
 
# 4.4 Create pie chart
plt.figure()
plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
plt.title("Bedroom Distribution (Top 5 Categories)")
plt.tight_layout()
plt.legend()
plt.savefig("bedroom_distribution.png")
plt.show()
 
# ==========================================================================================================
# 🔴 SCENARIO 5: Advanced Analysis + Multiple Graphs
# ==========================================================================================================
# Part 1: Feature Creation
# Create a new column "price_category":
# - price >= 1000000 → Luxury
# - 500000 – 999999 → Mid Range
# - < 500000 → Affordable

df["price_category"] = np.where(
    df["price"] >= 1000000, "Luxury",
    np.where(df["price"] >= 500000, "Mid Range", "Affordable")
)
 
# ==========================================================================================================
# Part 2: NumPy Usage
# 1. Convert price column to NumPy array
# 2. Calculate price differences using np.diff()

price_array = df["price"].to_numpy()
price_diff = np.diff(price_array)
 
print("Sample price differences:")
print(price_diff[:10])
print("------------------------------------------------------------")
 
# ==========================================================================================================
# Part 3: Visualizations
# Line Graph 
# 4. Plot height trend for all hills. 
# Stacked Bar Chart 
# 5. Show count of Height Category per Region. 
# Histogram 
# 6. Plot distribution of Height.

# 📈 Line Graph
x_index = np.arange(len(price_array))
plt.figure(figsize=(12,8))
plt.plot(x_index, price_array)
plt.title("Price Trend of Houses")
plt.xlabel("Index")
plt.ylabel("Price")
plt.xticks(rotation=70)
plt.tight_layout()
plt.savefig("price_trend.png")
plt.show()
 
# 📊 Stacked Bar Chart
category_counts = df.pivot_table(index="bedrooms", columns="price_category",aggfunc="size",fill_value=0)
category_counts.plot(kind="bar", stacked=True, figsize=(18,8))
plt.title("Price Category Distribution by Bedrooms")
plt.xlabel("Bedrooms")
plt.ylabel("Number of Houses")
plt.xticks(rotation=70)
plt.tight_layout()
plt.savefig("price_category_stacked.png")
plt.show()
 
# 📊 Histogram
plt.figure(figsize=(12,8))
plt.hist(df["price"], bins=20 ,edgecolor='black')
plt.title("Price Distribution of Houses")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("price_histogram.png")
plt.show()
 
# ==========================================================================================================
# Part 5: Insights
# Answer these: 
# 1. Which bedroom category has the most expensive houses? 
# 2. Which price category is most common? 
# 3. What is the distribution pattern of house prices? 
# ○ Right-skewed? 
# ○ Normal? 
# ○ Concentrated in a lower price range?
# ==========================================================================================================

# 1. Which bedroom category has the most expensive houses? 
expensive_houses = df[df["price"] > 1000000]
bedroom_expensive = expensive_houses["bedrooms"].value_counts().idxmax()
print("Bedroom category with most expensive houses:")
print(bedroom_expensive)
print("------------------------------------------------------------")

# 2. Which price category is most common? 
common_category = df["price_category"].value_counts().idxmax()
print("Most common price category:")
print(common_category)
print("------------------------------------------------------------")

# 3. What is the distribution pattern of house prices? 
# ○ Right-skewed? 
# ○ Normal? 
# ○ Concentrated in a lower price range?
print("Price distribution insight:")
mean_price = df["price"].mean()
median_price = df["price"].median()
if mean_price > median_price:
    print("Right-skewed distribution (more high-value outliers)")
elif mean_price < median_price:
    print("Left-skewed distribution")
else:
    print("Approximately normal distribution")

 