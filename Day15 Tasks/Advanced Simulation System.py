import numpy as np
import pandas as pd
import math
class Student:
    def __init__(self,name,marks):
        self.name=name
        self.marks=marks
    def assign_grades(self):
        grades=""
        if self.marks>90 :
            grades="A" 
        elif self.marks>80 :
            grades="B" 
        elif self.marks>70 :
            grades="C"
        elif self.marks>60 :
            grades="D"
        else:
            grades="E"
        return grades
try:
    n=5#int(input("enter size:"))
    arr=np.random.randint(1,100,size=(n))
    print(arr)
    lst=["praween","charan","anirudh","vinod","reddy"]#[input() for i in range(n)]
    arr = np.array(arr)
    mean = sum(arr) / n
    std = math.sqrt(sum((x - mean) ** 2 for x in arr) / n)
    students = []
    for i in range(n):
        s = Student(lst[i], arr[i])
        students.append(s)
    df = pd.DataFrame({
        "Name": [s.name for s in students],
        "Marks": [s.marks for s in students],
        "Grade": [s.assign_grades() for s in students]
    })
    print(df)
    print("\nMean:", mean)
    print("Std:", std)
    df.to_csv("report.txt", index=False)
    print("\nReport saved successfully!")
except Exception as e:
    print("Error:", e)