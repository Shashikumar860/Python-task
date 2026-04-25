# ============================================================
# Project Title: Gaming Review Data Analysis
# Analyze ign.csv dataset using NumPy, Pandas, Matplotlib
# ============================================================

# ============================================================
# 1. imoprt Required Libraries
# ============================================================

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

## ============================================================
#�� Scenario 1: Data Loading & Preprocessing
## ============================================================

"""You are given the ign.csv dataset containing game reviews.
�� Tasks:
1. Load the dataset using Pandas.
2. Display:
○ First 5 rows (head())
○ Last 5 rows (tail())
○ Shape of dataset
3. Remove the unnecessary column:
○ "Unnamed: 0" (index column)
4. Check for missing values in:
○ score, genre, platform
5. Handle missing values:
○ Fill numeric column score with mean
○ Fill categorical column genre with mode
6. Ensure correct data types:
○ score → float
○ release_year, release_month, release_day → integer """

#1.1 Load the dataset using Pandas
df = pd.read_csv("ign.csv")

#1.2 Display:
# First 5 rows (head())
print("First 5 rows:")
print(df.head())
# Last 5 rows (tail())
print("\nLast 5 rows:")
print(df.tail())
# Shape of dataset
print("\nShape of dataset:")
print(df.shape) # Rows and column

# 1.3Remove the unnecessary column:
# "Unnamed: 0" (index column)
df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore') 

#1.4 Check for missing values in:
# score, genre, platform
df[["score", "genre", "platform"]].isnull().sum()

#1.5 5. Handle missing values:
# Fill numeric column score with mean
df["score"].fillna(df["score"].mean(), inplace=True)
# Fill categorical column genre with mode
df["genre"].fillna(df["genre"].mode()[0], inplace=True)

#1.6 6. Ensure correct data types:
# score → float
# release_year, release_month, release_day → integer
df["score"] = df["score"].astype(float)
df["release_year"] = df["release_year"].astype(int)
df["release_month"] = df["release_month"].astype(int)
df["release_day"] = df["release_day"].astype(int)

# ============================================================
#�� Scenario 2: Line Graph (Score Trend) + Save
# ============================================================

"""You want to analyze how game scores change over time.
�� Tasks:
1. Group data by release_year.
2. Calculate average score per year using Pandas.
3. Convert results into NumPy arrays.
4. Plot a line graph:
○ X-axis → release_year
○ Y-axis → average score
5. Add:
○ Title: "Average Game Score Over Years"
○ Axis labels
6. Save the graph: plt.savefig("avg_score_trend.png)"""

#2.1 Group data by release_year.
df_grouped = df.groupby("release_year") #groupby("release_year") → Groups all rows that have the same year together

#2.2 Calculate average score per year using Pandas.
avg_score = df_grouped["score"].mean()  #mean() → calculates average score for each year
print("\n Average Score:", avg_score)

#2.3 Convert results into NumPy arrays.
years = np.array(avg_score.index)  #avg_score.index - it contains years
scores = np.array(avg_score.values)  #avg_score.values - it contains average scores

#2.4 plot Line Graph
plt.figure(figsize=(12,8))
plt.plot(years, avg_score , marker='o')
plt.xlabel("Release Year")
plt.ylabel("Average Score")
plt.title("Average Game Score Over Years")
plt.xticks(rotation=70)
plt.savefig("Avg Score Trend")
plt.grid()
plt.show()

# ============================================================
#�� Scenario 3: Filtering + Bar Chart + Save
# ============================================================

"""You want to compare top platforms.
Tasks:
1. Filter dataset where:
○ score > 7
2. Count number of high-rated games per platform.
3. Select top 10 platforms using Pandas.
4. Convert data into NumPy arrays.
5. Plot a bar chart:
○ X-axis → platform
○ Y-axis → count of games
6. Rotate x-axis labels for readability.
Save the graph: plt.savefig("top_platforms_bar.png")"""

#3.1 Filter dataset where:
# score > 7
df_high = df[df["score"] > 7]   #df["score"] > 7- it creates a condition
#print("\n data set >7 :", df_high)

#3.2 Count number of high-rated games per platform.
platform_counts = df_high["platform"].value_counts()   

#3.3 Select top 10 platforms using Pandas.
top_platforms = platform_counts.head(10)  #head(10)- it select only first 10 entries (already sorted in descending order)

#3.4 Convert data into NumPy arrays.
platform_names = np.array(top_platforms.index) #index → platform names (X-axis)
game_counts = np.array(top_platforms.values)  #values → counts (Y-axis)

#3.3 Plot a Bar Chart
plt.figure(figsize=(12,8))
plt.bar(platform_names, game_counts)
plt.xticks(rotation=70) #Vlues Redaibility
plt.xlabel("Platform")
plt.ylabel("Count of Games")
plt.title("Top Platforms")
plt.savefig("Top Platforms Bar")
plt.legend()
plt.show()

# ============================================================
#�� Scenario 4: Aggregation + Pie Chart + Save
# ============================================================

"""You want to analyze genre distribution.
�� Tasks:
1. Count the number of games per genre.
2. Select top 5 genres using Pandas.
3. Prepare labels and values.
4. Plot a pie chart:
○ Labels → genre
○ Values → count
5. Add percentage labels (autopct).
Save the graph: plt.savefig("genre_distribution.png")"""

#4.1 Count the number of games per genre.
no_genre_counts = df["genre"].value_counts()  #value_counts()- counts occurrences of each genre

#4.2 Select top 5 genres using Pandas.
top_games_genre = no_genre_counts.sort_values(ascending=False).head(5)

#4.3 Prepare labels and values.
top_genre=top_games_genre.index
count=top_games_genre.values

#4.4 Plot Pie Chart
plt.figure(figsize=(6,6))
plt.pie(count,labels=top_genre,autopct="%1.1f%%")
plt.title("Game Genres Distribution")
plt.savefig("Genre_Distribution")
plt.show()

# ============================================================
#�� Scenario 5: Advanced Analysis + Multiple Graphs
# ============================================================

# ============================================================
#�� Part 1: Feature Engineering
# ============================================================
"""
1. Create a new column:
○ score_category:
■ score >= 9 → "Excellent"
■ 7 <= score < 9 → "Good"
■ < 7 → "Average"
2. Convert editors_choice:
○ Y → 1, N → 0"""

# ============================================================
#�� Part 2: NumPy Analysis
# ============================================================
"""3. Use NumPy to:
○ Calculate yearly score growth using np.diff() on average yearly  """
# ============================================================
##�� Part 3: Visualizations
# ============================================================
"""�� Line Graph
4. Plot trend of:
○ Average score per release_year
�� Stacked Bar Chart
5. Show count of:
○ score_category per release_year
�� Histogram
6. Plot distribution of:
○ score """

#5.1.1 create new column
#○ score_category
def categorize(score):
    if score >= 9:
        return "Excellent"
    elif score >= 7:
        return "Good"
    else:
        return "Average"

df["score_category"] = df["score"].apply(categorize)  # apply() runs function on each score | *score_category - Creates a new column 

#5.1.2 Convert editors_choice:
# Y → 1, N → 0
df["editors_choice"] = df["editors_choice"].map({"Y": 1, "N": 0}) # Converts to numeric

#5.2.3 Use NumPy to:
# Calculate yearly score growth using np.diff() on average yearly
yearly_score_growth=np.insert(np.diff(avg_score),0,0)


# 5.3 Visualization
#line Graph
plt.figure(figsize=(12,8))
plt.plot(years, yearly_score_growth, marker='o')
plt.xticks(rotation=70)
plt.xlabel("Release Year")
plt.ylabel("Average Score")
plt.title("Average Score Trend Over Years")
plt.savefig("Score Trend")
plt.legend()
plt.show()  

# Stacked Bar Chart
score_catageroy=df.groupby(["release_year","score_category"]).size()
tab=score_catageroy.unstack(fill_value=0)
excellent=np.array(tab["Excellent"])
average=np.array(tab["Average"])
good=np.array(tab["Good"])
years = tab.index.to_numpy()
x = np.arange(len(years)) 

plt.figure(figsize=(12,8))
plt.bar(x,good,width=0.5,label="Good")
plt.bar(x,average,width=0.5,label="Average",bottom=good)
plt.bar(x,excellent,width=0.5,label="Excellent",bottom=average+good)
plt.xticks(x,years,rotation=60)
plt.ylabel("Count of score category")
plt.xlabel("Release Year")
plt.title("Score Categories Per Year")
plt.legend()
plt.tight_layout()
plt.savefig("Score Category Stacked")
plt.show()

# Histogram
plt.hist(df["score"], bins=20, edgecolor='white')
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.title("Score Distribution")
plt.savefig("Score Distribution")
plt.tight_layout()
plt.show()

# ============================================================
#�� Part 5: Insights
# ============================================================
#Identify:
# Which years had highest scores
print(avg_score.sort_values(ascending=False).head())
# Ans: The highest average scores were observed around 2008–2012

# Whether high scores increased over time
print("\n high Scores", yearly_score_growth)
# Ans: Excellent scores remain relatively rare compared to "Good"

# If editors_choice correlates with high scores
# Ans: Excellent" has the highest probability of being editor’s choice
print(df.groupby("score_category")["editors_choice"].mean())
