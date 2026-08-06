"""
consecutive duplicate detector
accept N integers
display only those numbers that appear consecutively more than once.
input : 1 2 2 3 4 4 5
output : 2 4
 
"""

n = tuple(input())

for i in range(len(n) - 1):
    if n[i] == n[i + 1]:
        if i == 0 or n[i] != n[i - 1]:
            print(n[i])
