"""
display all failed rules

missing roll number
roll numbers should be from 1 to n
one roll number is missing 
find the missing roll number without sorting

example : 1 2 3 5 6
output : 4

"""
n = int(input("Enter total number of students: "))

roll = list(map(int, input("Enter roll numbers: ")))

for i in range(1, n + 1):
    if i not in roll:
        print("Missing roll number:", i)
