def remove_dup_sort(lst):
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] == lst[j]:
                lst.pop(j)
                j -= 1

    return sorted(lst)

lst = list(map(int, input("Enter numbers separated by spaces: ").split()))
print(remove_dup_sort(lst))