import numpy as np
marks = np.array([  
[70, 80, 90],  #70+80+90n= 240
[60, 75, 85],  #60+75+85 = 220
[50, 65, 70],  #50+65+70 = 185
[90, 95, 85],  #90+95+85 = 270
[40, 55, 60]   #40+55+60 = 155
])
#axis add the columns
total=marks.sum(axis=1)
#average=sum of marks /5
class_average = total.mean()
#check the average > sum of each row
above_average = np.where(total > class_average)[0]

print(total)
print(class_average)
print(above_average)