def find_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

numbers_set = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print("Sum of Numbers:", find_sum(numbers_set))
