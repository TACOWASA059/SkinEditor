import copy
import numpy as np

#2元配列を180度回転
def rotate1(ma:np.array):
    mb=copy.deepcopy(ma)
    for n in range(len(ma)):
        for m in range(len(ma[n])):
            mb[n][m]=ma[len(ma) - 1 - n][len(ma[n]) - 1 - m]
    return mb

def rotate(ma,deg):#deg=1:90度回転,deg=-1:-90度回転
    mb=copy.deepcopy(ma)
    mb=np.rot90(mb,deg)
    return mb
#2元配列の4分割ブロックを右シフト2回
def move(ma):
    n=len(ma)
    m=len(ma[0])
    mb=copy.deepcopy(ma)
    if m%2!=0:
        print("Error\n")
        exit()
    for i in range(n):
        for j in range(int(m/2)):
            mb[i][j+int(m/2)]=ma[i][j]
        for j in range(int(m/2),m):
            mb[i][j-int(m/2)]=ma[i][j]
    return mb
def flip(ma):#二次元配列を左右反転
    n=len(ma)
    m=len(ma[0])
    mb=copy.deepcopy(ma)
    for i in range(n):
        for j in range(m):
            mb[i][j]=ma[i][m-1-j]
    return mb
def upsidedown(ma):#二次元配列を上下反転
    n=len(ma)
    m=len(ma[0])
    mb=copy.deepcopy(ma)
    for i in range(n):
        for j in range(m):
            mb[i][j]=ma[n-1-i][j]
    return mb
#test function
if __name__ == '__main__':
    import cv2
    img1=cv2.imread("1.png",-1)
    img2=rotate(img1,1)
    cv2.imwrite("2.png",img2)
    #img2=rotate(img1,-1)
    #cv2.imwrite("3.png",img2)

    