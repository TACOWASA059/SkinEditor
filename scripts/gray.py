import numpy as np
def toGray(img):
    array1=np.array(img)
    for i in range(len(array1)):
        for j in range(len(array1[i])):
            sum=np.average(array1[i][j][:3])
            array1[i][j][:3]=sum
    return array1