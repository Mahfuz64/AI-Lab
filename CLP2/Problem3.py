students = [
    ("Mahfuz", 20, 3.5),
    ("Shakil", 22, 3.8),
    ("Rahman", 19, 3.00),
    ("Awranga", 21, 3.4),
    ("Noman", 20, 3.88)
]
n=len(students)
for i in range(n):
    for j in range(0, n - i - 1):
        if students[j][2] > students[j + 1][2]:  
            students[j], students[j + 1] = students[j + 1], students[j]

student=tuple(students)
for i in student:
    print(i)
   
