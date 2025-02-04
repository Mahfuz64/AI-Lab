def sum(numbers):
    even_sum = 0
    odd_sum = 0
    
    for num in numbers:
        if num % 2 == 0:
            even_sum += num
        else:
            odd_sum += num
    
    return even_sum, odd_sum


numbers_set = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
even_sum, odd_sum = sum(numbers_set)
print("Sum of even numbers:", even_sum)
print("Sum of odd numbers:", odd_sum)
