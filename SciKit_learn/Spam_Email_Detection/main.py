# ===========================================================
#                           Spam Email Detection
#============================================================
# Algorithms used:
# 1. Logistic Regression
# 2. Support Vector Machine(SVM) 
# 3. Naive Bayes 

# =========================================
# Import Libraries
# =========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# =========================================
# Load Dataset
# =========================================

df = pd.read_csv("spam.csv", encoding='latin-1')

# Keep only required columns
df = df[['Category', 'Message']]

print(df.head())

# =========================================
# Dataset Information
# =========================================

print(df.info())

print(df.isnull().sum())

print(df['Category'].value_counts())

# =========================================
# Remove Duplicate Rows
# =========================================

df.drop_duplicates(inplace=True)

# =========================================
# Graph 1 : Spam vs Ham Distribution
# =========================================

plt.figure(figsize=(6,5))

ax = sns.countplot(data=df, x='Category')

for container in ax.containers:
    ax.bar_label(container)

plt.title("Spam vs Ham Distribution")

plt.show()

# =========================================
# Label Encoding
# =========================================

encoder = LabelEncoder()

df['label'] = encoder.fit_transform(df['Category'])

# ham = 0
# spam = 1

# =========================================
# Features and Labels
# =========================================

X = df['Message']

y = df['label']

# =========================================
# TF-IDF Vectorization
# =========================================

vectorizer = TfidfVectorizer(
    stop_words='english'
)

X_vectorized = vectorizer.fit_transform(X)

# =========================================
# Train Test Split
# =========================================

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

# ===================================================
# 1. Logistic Regression
# ===================================================

lr = LogisticRegression()

lr.fit(X_train, y_train)

lr_pred = lr.predict(X_test)

print("\n===== Logistic Regression =====")

print("Accuracy :", accuracy_score(y_test, lr_pred))

print(classification_report(y_test, lr_pred))

# ===================================================
# 2. Support Vector Machine(SVM) 
# ===================================================

svm = SVC(kernel='linear')

svm.fit(X_train, y_train)

svm_pred = svm.predict(X_test)

print("\n===== SVM =====")

print("Accuracy :", accuracy_score(y_test, svm_pred))

print(classification_report(y_test, svm_pred))

# ===================================================
# 3. Naive Bayes
# ===================================================

nb = MultinomialNB()

nb.fit(X_train, y_train)

nb_pred = nb.predict(X_test)

print("\n===== Naive Bayes =====")

print("Accuracy :", accuracy_score(y_test, nb_pred))

print(classification_report(y_test, nb_pred))

# =========================================
# Graph 2 : Confusion Matrix
# =========================================

cm = confusion_matrix(y_test, svm_pred)

sns.heatmap(
    cm,
    annot=True,
    cmap='Blues',
    fmt='1.0f'
)

plt.title("SVM Confusion Matrix")

plt.xlabel("Predicted")

plt.ylabel("Actual")

plt.show()

# =========================================
# Graph 3 : Accuracy Comparison
# =========================================

models = [
    'Logistic Regression',
    'SVM',
    'Naive Bayes'
]

accuracy = [

    accuracy_score(y_test, lr_pred),
    accuracy_score(y_test, svm_pred),
    accuracy_score(y_test, nb_pred)
]

plt.figure(figsize=(8,5))

plt.bar(models, accuracy)

plt.ylabel("Accuracy")

plt.title("Accuracy Comparison")

plt.show()