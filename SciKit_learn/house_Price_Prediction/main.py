# Importing required libraries
import numpy as np                  # For numerical operations
import pandas as pd                 # For handling datasets

# Loading dataset
dataset = pd.read_csv("kc_house_data.csv")   # Read CSV file
print(dataset.head())               # Display first 5 rows

# Selecting features (X) and target (y)
X = dataset[['bedrooms','bathrooms','sqft_living','sqft_lot','floors',
             'condition','grade','sqft_basement','yr_built','yr_renovated']].values

y = dataset['price'].values

# Display shape of data
print('-'*80)
print(f'Shape of X is {X.shape}\nShape of y is {y.shape}')

# Splitting dataset into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

print('-'*80)
print(f"Length of X_train: {len(X_train)}\nLength of X_test: {len(X_test)}")
print(f"Length of y_train: {len(y_train)}\nLength of y_test: {len(y_test)}")


# -----------------------------
# Feature Scaling
# -----------------------------
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

# Fit on training data and transform
X_train = sc.fit_transform(X_train)

# Transform test data (important: do NOT fit again)
X_test = sc.transform(X_test)

#========================================================================
# Evaluation Function (Regression)
#========================================================================
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def evaluate_reg(y_test, y_pred):
    print("MAE:", mean_absolute_error(y_test, y_pred))
    print("MSE:", mean_squared_error(y_test, y_pred))
    print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
    print("R2 Score:", r2_score(y_test, y_pred))
    print("-"*50)

#========================================================================
# 1. Linear Regression
#========================================================================
from sklearn.linear_model import LinearRegression
print("\n------ Linear Regression ------")
model = LinearRegression()
model.fit(X_train, y_train)
evaluate_reg(y_test, model.predict(X_test))

#========================================================================
# 2. Decision Tree
#========================================================================
from sklearn.tree import DecisionTreeRegressor
print("\n------ Decision Tree ------")
model = DecisionTreeRegressor(random_state=42)
model.fit(X_train, y_train)
evaluate_reg(y_test, model.predict(X_test))

#========================================================================
# 3. Random Forest
#========================================================================
from sklearn.ensemble import RandomForestRegressor
print("\n------ Random Forest ------")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
evaluate_reg(y_test, model.predict(X_test))

#========================================================================
# 4. KNN Regressor
#========================================================================
from sklearn.neighbors import KNeighborsRegressor
print("\n------ KNN ------")
model = KNeighborsRegressor(n_neighbors=5)
model.fit(X_train, y_train)
evaluate_reg(y_test, model.predict(X_test))

#========================================================================
# 5. Support Vector Regression (SVR)
#========================================================================
from sklearn.svm import SVR
print("\n------ SVR ------")
model = SVR()
model.fit(X_train, y_train)
evaluate_reg(y_test, model.predict(X_test))

#========================================================================
# 6. Gradient Boosting
#========================================================================
from sklearn.ensemble import GradientBoostingRegressor
print("\n------ Gradient Boosting ------")
model = GradientBoostingRegressor()
model.fit(X_train, y_train)
evaluate_reg(y_test, model.predict(X_test))

#========================================================================
# 7. Naive Bayes (GaussianNB) - Classification
#========================================================================
print("\n------ Naive Bayes (GaussianNB) ------")

# Convert price → categories
y_class = pd.qcut(dataset['price'], q=3, labels=["Low","Medium","High"])

# Split again for classification
X_train_nb, X_test_nb, y_train_nb, y_test_nb = train_test_split(
    X, y_class, test_size=0.2, random_state=42
)

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

model = GaussianNB()
model.fit(X_train_nb, y_train_nb)

y_pred_nb = model.predict(X_test_nb)
print("Accuracy:", accuracy_score(y_test_nb, y_pred_nb))
print("-"*50)
