import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import copy
import transform as tf
def head_rotate_layer(img1,y):
    img2=copy.deepcopy(img1)
    p=8
    img2[p:2*p,p+y:2*p+y]=tf.rotate(img1[p:2*p,p+y:2*p+y],-1)
    img2[p:2*p,y:p+y]=tf.rotate(img1[:p,y+2*p:y+3*p],1)#
    img2[p:2*p,y:p+y]=tf.upsidedown(img2[p:2*p,y:p+y])
    img2[p:2*p,y+2*p:y+3*p]=tf.rotate(img1[:p,y+p:y+2*p],-1)#
    img2[p:2*p,y+3*p:y+4*p]=tf.rotate(img1[p:2*p,y+3*p:y+4*p],1)
    img2[:p,y+p:y+2*p]=tf.rotate(img1[p:2*p,y:y+p],-1)#
    img2[:p,y+2*p:y+3*p]=tf.rotate(img1[p:2*p,y+2*p:y+3*p],1)#
    img2[:p,y+2*p:y+3*p]=tf.flip(img2[:p,y+2*p:y+3*p])
    return img2
def head_rotate(img1):#正面手前方向に軸
    img1=head_rotate_layer(img1,0)
    img1=head_rotate_layer(img1,32)
    return img1

def head_rotate_layer_vertical(img1,y):
    img2=copy.deepcopy(img1)
    p=8
    img2[:p,y+p:y+2*p]=tf.rotate(img1[:p,y+p:y+2*p],1)
    img2[:p,y+2*p:y+3*p]=tf.rotate(img1[:p,y+2*p:y+3*p],1)
    img2[p:2*p,y+p:y+4*p]=img1[p:2*p,y:y+3*p]
    img2[p:2*p,y:y+p]=img1[p:2*p,y+3*p:y+4*p]
    return img2
#vertical(垂直)軸周りの回転
def head_rotate_vertical(img1):
    img1=head_rotate_layer_vertical(img1,0)
    img1=head_rotate_layer_vertical(img1,32)
    return img1
#垂直周りの回転
def head_rotate_horizontal(img1):
    img1=head_rotate_vertical(img1)
    img1=head_rotate(img1)
    img1=head_rotate(img1)
    img1=head_rotate(img1)
    img1=head_rotate_vertical(img1)
    img1=head_rotate_vertical(img1)
    img1=head_rotate_vertical(img1)
    return img1
def count_zero(img1,x,y):#透過pixelカウント
    count1=0
    q=4
    list=(img1[x*q:(x+1)*q,(y+3)*q-2:(y+3)*q,3])
    list2=(img1[(x+1)*q:(x+4)*q,(y+4)*q-2:(y+4)*q,3])
    for ix in list:
        count1+=ix.tolist().count(0)
    for ix in list2:
        count1+=ix.tolist().count(0)
    return count1
def judge_slim_classic(img1):#slimかclassicかの判定
    #改善する必要あり
    #tot_count=32*4
    count=0
    count+=count_zero(img1,4,10)
    count+=count_zero(img1,8,10)
    count+=count_zero(img1,12,8)
    count+=count_zero(img1,12,12)
    #print(count)
    if count>100:
        return True #slim判定
    else :
        return False #classic判定
if __name__=="__main__":
    #ウインドウ作成
    baseGround = tk.Tk()
    #非表示
    baseGround.withdraw()

    #ファイルタイプの指定
    typ = [('pngファイル','*.png')]     
    #ディレクトリの指定
    dir = '.'
    #ファイル選択画面の表示
    fle = filedialog.askopenfilenames(filetypes = typ, initialdir = dir) 
    for i in fle:
        img1=cv2.imread(i,-1)
        if len(img1)!=64 or len(img1[0])!=64 :
            print("Pixel Size Error:input image size must be 64x64.")
            exit()
        print("input file:",i)
        img1=head_rotate_horizontal(img1)
        flag=judge_slim_classic(img1)
        if flag==True:
            output_file=i.replace(".png","-head90-slim.png")
        else :
            output_file=i.replace(".png","-head90-classic.png")
        print("output file:",output_file)
        cv2.imwrite(output_file,img1)