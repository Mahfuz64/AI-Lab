def smallfind(number):
    small=number[0]
    for i in number:
       

        if i<small:
            small=number[i]
    return small



number = [3, 1, 7, 5, 9, 2]
print(smallfind(number))
