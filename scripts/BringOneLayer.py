import numpy as np
def bring_one_layer(img,id):
    array1=np.array(img.copy())
    array1=np.transpose(array1,axes=(1, 0, 2))
    # id=1のとき2層目にまとめる
    for i in range(32):
        for j in range(16):
            if array1[i+32][j][3]!=0:
                array1[i][j]=array1[i+32][j].copy()
    array1[32:,:16,:]=0
    
    for i in range(56):
        for j in range(16,32):
            if array1[i][j+16][3]!=0:
                array1[i][j]=array1[i][j+16].copy()
    array1[:56,32:48,:]=0
    for i in range(16):
        for j in range(48,64):
            if array1[i][j][3]!=0:
                array1[i+16][j]=array1[i][j].copy()
    array1[:16,48:,:]=0
    for i in range(32,48):
        for j in range(48,64):
            if array1[i+16][j][3]!=0:
                array1[i][j]=array1[i+16][j].copy()
    array1[48:,48:,:]=0
    
    if id==1:
        array1[32:64,:16]=array1[:32,:16]
        array1[:32,:16,:]=0
        array1[:,32:48]=array1[:,16:32]
        array1[:,16:32,:]=0
        array1[:16,48:]=array1[16:32,48:]
        array1[16:32,48:,:]=0
        array1[48:,48:]=array1[32:48,48:]
        array1[32:48,48:,:]=0
    array1=np.transpose(array1,axes=(1, 0, 2))
    return array1
                