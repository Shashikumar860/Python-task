import numpy as np
data = np.arange(1, 13)
reshape=data.reshape(3,4)
print("reshape:",reshape)
average=reshape.mean(axis=1)
print("AVerage=",average)