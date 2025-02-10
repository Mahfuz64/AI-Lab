import pandas as pd

try:
    df = pd.read_csv("data.csv")
except FileNotFoundError:
    print("Error: 'data.csv' not found.")
    exit()

df.fillna(df.mean(numeric_only=True), inplace=True)

print(df.head())
