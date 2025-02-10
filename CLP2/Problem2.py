def setcommon(lst1,lst2):
   return list(set(lst1) & set(lst2))
lst1 = list(map(int, input("Enter numbers separated by spaces: ").split()))
lst2 = list(map(int, input("Enter numbers separated by spaces: ").split()))
print(setcommon(lst1,lst2))