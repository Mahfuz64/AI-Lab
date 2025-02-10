import numpy as np


matrix = np.random.randint(1, 101, (5, 5))
print("Matrix:\n", matrix)

row_sums = []
for row in matrix:
    row_sum = 0
    for num in row:
        row_sum += num
    row_sums.append(int(row_sum))
print("Row-wise sums:", row_sums)