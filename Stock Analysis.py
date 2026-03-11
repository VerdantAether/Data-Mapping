# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 14:43:59 2026

@author: Raleigh Mann
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_curve, auc

df = pd.read_csv("Data/stock_prices_daily.csv")
print(df.describe())

plt.figure(figsize=(10,6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="magma")

#Isolate Truist
tfc_data = df[df["Ticker"] == "TFC"]
print(tfc_data.describe())

# Convert Date column to datetime
tfc_data["Date"] = pd.to_datetime(tfc_data["Date"], utc=True)

tfc_data = tfc_data.sort_values("Date")


#Plotting TFC data
plt.figure()
plt.plot(tfc_data["Date"], tfc_data["High"], label="High")
plt.plot(tfc_data["Date"], tfc_data["Low"], label="Low")

plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.title("TFC High and Low Prices Over Time")
plt.legend()
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()