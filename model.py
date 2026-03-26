import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

# Simple dataset
data = {
    "budget": [3000, 5000, 7000, 10000, 15000, 20000, 8000, 12000],
    "days": [1, 2, 3, 4, 5, 6, 2, 4],
    "season": [0, 0, 1, 1, 2, 2, 0, 1],  # 0=Summer, 1=Winter, 2=Monsoon
    "category": ["Food", "Adventure", "Adventure", "Historical",
                 "Spiritual", "Adventure", "Food", "Historical"]
}

df = pd.DataFrame(data)

X = df[["budget", "days", "season"]]
y = df["category"]

model = LogisticRegression(max_iter=200)
model.fit(X, y)

pickle.dump(model, open("travel_model.pkl", "wb"))

print("Model trained and saved successfully!")