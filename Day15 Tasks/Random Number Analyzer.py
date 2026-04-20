"""2. Random Number Analyzer
Scenario:
A system generates random numbers for testing.
Task:
● Use random to generate 10 numbers
● Store in a list
● Use loop + condition to count even/odd numbers
● Use set to remove duplicates
"""

import random
lst=[random.randint(1,10) for i in range(10)]
print(lst)
even_c=0
odd_c=0
for i in lst:
    if i%2==0:
        even_c+=1
    else:
        odd_c+=1
list_to_set=set(lst)
print(f"count of even {even_c}\ncount of odd {odd_c}\n{list_to_set}")