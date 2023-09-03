import numpy as np
def slim2wide(img):
    img=slim2wideparts(img,40,16)
    img=slim2wideparts(img,40,32)
    img=slim2wideparts(img,32,48)
    img=slim2wideparts(img,48,48)
    return img
def wide2slim(img):
    img=wide2slimparts(img,40,16)
    img=wide2slimparts(img,40,32)
    img=wide2slimparts(img,32,48)
    img=wide2slimparts(img,48,48)
    return img
def slim2wideparts(img,x,y):
    array1=np.array(img)
    array1=np.transpose(array1,axes=(1, 0, 2))
    up=array1[x+4:x+7,y:y+4]
    up=three2four(up)
    down=array1[x+7:x+10,y:y+4]
    down=three2four(down)
    
    side2=array1[x+4:x+7,y+4:y+16]
    side2=three2four(side2)
    side3=array1[x+7:x+11,y+4:y+16]
    side4=array1[x+11:x+14,y+4:y+16].copy()
    side4=three2four(side4)
    array1[x+8:x+12,y:y+4]=down
    array1[x+4:x+8,y:y+4]=up
    
    array1[x+12:x+16,y+4:y+16]=side4
    array1[x+8:x+12,y+4:y+16]=side3
    array1[x+4:x+8,y+4:y+16]=side2
    array1=np.transpose(array1,axes=(1, 0, 2))
    return array1
def wide2slimparts(img,x,y):
    array1=np.array(img)
    array1=np.transpose(array1,axes=(1, 0, 2))
    up=array1[x+4:x+8,y:y+4]
    up=four2three(up)
    down=array1[x+8:x+12,y:y+4]
    down=four2three(down)
    
    side2=array1[x+4:x+8,y+4:y+16]
    side2=four2three(side2)
    side3=array1[x+8:x+12,y+4:y+16].copy()
    side4=array1[x+12:x+16,y+4:y+16]
    side4=four2three(side4)
    array1[x+10:x+12,y:y+4,:]=0
    array1[x+14:x+16,y+4:y+16,:]=0
    array1[x+7:x+10,y:y+4]=down
    array1[x+4:x+7,y:y+4]=up
    
    array1[x+11:x+14,y+4:y+16]=side4
    array1[x+7:x+11,y+4:y+16]=side3
    array1[x+4:x+7,y+4:y+16]=side2
    array1=np.transpose(array1,axes=(1, 0, 2))
    return array1

def three2four(array):
    # 新しい4x4の配列を作成
    x,y,z=array.shape
    new_array = np.zeros((4,y,z), dtype=array.dtype)
    # 両端の行をコピーして新しい配列に挿入
    new_array[0, :] = array[0, :]
    new_array[3, :] = array[2, :]
    # 元の真ん中の行をコピーして新しい配列に挿入
    new_array[1:3, :] = array[1:2, :]
    return new_array

def four2three(array):
    # 新しい4x4の配列を作成
    x,y,z=array.shape
    new_array = np.zeros((3,y,z), dtype=array.dtype)
    # 両端の行をコピーして新しい配列に挿入
    new_array[0, :] = array[0, :]
    new_array[2, :] = array[3, :]
    # 元の真ん中の行をコピーして新しい配列に挿入
    new_array[1, :] = array[1, :]
    return new_array