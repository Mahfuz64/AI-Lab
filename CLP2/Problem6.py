import numpy as np

arr = np.random.rand(100)

# Find min and max using a loop
min_val = arr[0]
max_val = arr[0]

for num in arr:
    if num < min_val:
        min_val = num
    if num > max_val:
        max_val = num

normalized_arr = []
for num in arr:
    normalized_arr.append((num - min_val) / (max_val - min_val))

print("Normalized Array:", normalized_arr)