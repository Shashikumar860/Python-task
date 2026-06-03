"""1. Student Score Processor
Scenario:
A teacher stores student names and marks in a list of tuples.
Task:
● Convert data into a dictionary
● Use a loop + condition to find students scoring above 50
● Use math module to calculate average
● Store results in a text file
"""
import math

list = [("Praween", 85), ("Charan", 45), ("Naveen", 78), ("Reddy", 30), ("Bharath", 90)]

# 2. Convert data into a dictionary
student_dict = dict(list)
print(student_dict)

# 3. Find students scoring above 50
high_scorers = {}
for name, mark in student_dict.items():
    if mark > 50:
        high_scorers[name] = mark


# 4. Use math module to calculate average
total = math.fsum(student_dict.values())
count = len(student_dict)

if count > 0:
    average = total / count
else:
    average = 0
print(total)
# 5. Store results in a text file
with open("student_results.txt", "w") as file:
    file.write(f"High Scorers (>50): {high_scorers}\n")
    file.write(f"Average Mark: {average:.2f}\n")

