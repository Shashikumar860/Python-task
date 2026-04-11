import numpy as np
import copy
classe = [["Math", [30, 35]], ["Science", [25, 28]]]
copy = copy.deepcopy(classe)
classe[0][1][0] = 99 
print("Original class:", classe)
print("Copied class:", copy)