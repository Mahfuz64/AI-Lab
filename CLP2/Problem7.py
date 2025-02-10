import pandas as pd

df = pd.read_csv("Product.csv")

df["Revenue"] = df["Quantity"] * df["Price"]
total_revenue = df.groupby("Product")["Revenue"].sum()

print(total_revenue)