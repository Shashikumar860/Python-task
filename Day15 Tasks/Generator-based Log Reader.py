"""7. Generator-based Log Reader
Scenario:
A large log file needs to be processed.
Task:
● Create a generator to read file line by line
● Use loop to process logs
● Use condition to filter errors
● Count occurrences using a dictionary
"""

def gen_read():
    with open("generate.txt","r") as file:
        data=file.readline()
        yield data
for i in gen_read():
    print(i)