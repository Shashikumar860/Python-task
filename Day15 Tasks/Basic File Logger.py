"""4. Basic File Logger
Scenario:
A system logs user actions.
Task:
● Take user input
● Store logs in a file
● Use loop to allow multiple entries
● Handle file errors using exception handling
"""

try:
    with open("log.txt","a") as file:
        while True:
            inp=input("enter login or logout: ")
            if inp=="logout":
                break
            file.write(inp+"\n")
except FileNotFoundError as f:
    print("file not found",f)
except Exception as e:
    print("exception occured",e)