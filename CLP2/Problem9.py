import matplotlib.pyplot as plt

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
temperatures = [22, 24, 21, 23, 25, 26, 27]

plt.plot(days, temperatures, marker="o", linestyle="-", color="b", label="Temperature (°C)")

plt.xlabel("Days of the Week")
plt.ylabel("Temperature (°C)")
plt.title("Temperature Variations Over a Week")



plt.show()
