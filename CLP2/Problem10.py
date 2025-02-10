import matplotlib.pyplot as plt


regions = ["North", "South", "East", "West"]
sales_revenue = [50000, 62000, 48000, 53000]


plt.bar(regions, sales_revenue, color=["red", "blue", "green", "orange"])

plt.xlabel("Regions")
plt.ylabel("Sales Revenue ($)")
plt.title("Sales Revenue Across Different Regions")

plt.show()
