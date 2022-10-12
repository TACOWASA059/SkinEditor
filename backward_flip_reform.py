import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import copy
import transform as tf
#slimとclassicの判定が一応あり

#四肢の反転
def backwards_limb(img1,x,y):#左上が(4x,4y)、右下が(4(x+4),4(y+4))のピクセルに対応
    q=4
    img1[x*q:(x+1)*q,(y+1)*q:(y+2)*q]=tf.rotate1(img1[x*q:(x+1)*q,(y+1)*q:(y+2)*q])
    img1[x*q:(x+1)*q,(y+2)*q:(y+3)*q]=tf.rotate1( img1[x*q:(x+1)*q,(y+2)*q:(y+3)*q])
    img1[(x+1)*q:(x+4)*q,y*q:(y+4)*q]=tf.move( img1[(x+1)*q:(x+4)*q,y*q:(y+4)*q])
    return img1
def backwards_arm(img1,x,y):#slim用,classicはlimbを使う
    q=4
    #4x3のrotate1(2ヶ所)
    img1[x*q:(x+1)*q,(y+1)*q:(y+2)*q-1]=tf.rotate1(img1[x*q:(x+1)*q,(y+1)*q:(y+2)*q-1])
    img1[x*q:(x+1)*q,(y+2)*q-1:(y+3)*q-2]=tf.rotate1( img1[x*q:(x+1)*q,(y+2)*q-1:(y+3)*q-2])
    #右端を消し飛ばす(4x3の右側)4x2を消す
    img1[x*q:(x+1)*q,(y+3)*q-2:(y+3)*q]=np.full(img1[x*q:(x+1)*q,(y+3)*q-2:(y+3)*q].shape, 0)
    #右シフト
    img1[(x+1)*q:(x+4)*q,y*q:(y+4)*q-2]=tf.move( img1[(x+1)*q:(x+4)*q,y*q:(y+4)*q-2])
    #右端を消し飛ばす(12x14の右側)12x2を消す
    img1[(x+1)*q:(x+4)*q,(y+4)*q-2:(y+4)*q]=np.full(img1[(x+1)*q:(x+4)*q,(y+4)*q-2:(y+4)*q].shape,0)
    return img1
#2段目と3段目
def backwards_body(img1,number,flag):#numberは行(縦)の指定,上が4*number、下が4*(number+4)
    q=4
    n1=number
    n2=number+1
    n3=number+4
    #一番左
    backwards_limb(img1,n1,0)
    #一番右
    #slim用
    if flag==True:
        backwards_arm(img1,n1,10)
    else :
        backwards_limb(img1,n1,10)
    #真ん中
    img1[n1*q:n2*q,5*q:7*q]=tf.rotate1(img1[n1*q:n2*q,5*q:7*q])
    img1[n1*q:n2*q,7*q:9*q]=tf.rotate1(img1[n1*q:n2*q,7*q:9*q])
    img1[n2*q:n3*q,4*q:10*q]=tf.move(img1[n2*q:n3*q,4*q:10*q])
    return img1
def backwards_head(img1):#顔の反転操作
    p=8
    #顔の部分
    #顔の上面と下面
    img1[:p,p:2*p]=tf.rotate1(img1[:p,p:2*p])
    img1[:p,2*p:3*p]=tf.rotate1(img1[:p,2*p:3*p])
    img1[:p,5*p:6*p]=tf.rotate1(img1[:p,5*p:6*p])
    img1[:p,6*p:7*p]=tf.rotate1(img1[:p,6*p:7*p])
    #4面の右シフト
    img1[p:2*p,:4*p]=tf.move(img1[p:2*p,:4*p])
    img1[p:2*p,4*p:8*p]=tf.move(img1[p:2*p,4*p:8*p])
    return img1
def exchange_limb(img1):#右手と左手の交換,右足と左足の交換
    img2=copy.deepcopy(img1)
    #左足と右足の入れ替え(上位レイヤー)
    img1[32:48,0:16]=img2[48:64,0:16]
    img1[48:64,0:16]=img2[32:48,0:16]
    #左足と右足の入れ替え
    img1[16:32,0:16]=img2[48:64,16:32]
    img1[48:64,16:32]=img2[16:32,0:16]
    #左腕と右腕の入れ替え
    img1[48:64,32:48]=img2[16:32,40:56]
    img1[16:32,40:56]=img2[48:64,32:48]
    #左腕と右腕の入れ替え(上位レイヤー)
    img1[48:64,48:64]=img2[32:48,40:56]
    img1[32:48,40:56]=img2[48:64,48:64]
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

#メインの関数
def flip_backwards(file_name):
    img1=cv2.imread(file_name,-1)
    if len(img1)!=64 or len(img1[0])!=64 :
        print("Pixel Size Error:input image size must be 64x64.")
        exit()
    flag=judge_slim_classic(img1)
    #顔の部分
    backwards_head(img1)
    #2段目
    backwards_body(img1,4,flag)
    #3段目
    backwards_body(img1,8,flag)
    #4段目
    backwards_limb(img1,12,0)
    backwards_limb(img1,12,4)
    if flag==True:
        backwards_arm(img1,12,8)
        backwards_arm(img1,12,12)
    else :
        backwards_limb(img1,12,8)
        backwards_limb(img1,12,12)

    img2=copy.deepcopy(img1)
    exchange_limb(img1)#左右変更
    #test func
    #cv2.imwrite("2.png",img1)
    return img1,flag

def backwards(img1):#配列入力あり
    flag=judge_slim_classic(img1)
    #顔の部分
    backwards_head(img1)
    #2段目
    backwards_body(img1,4,flag)
    #3段目
    backwards_body(img1,8,flag)
    #4段目
    backwards_limb(img1,12,0)
    backwards_limb(img1,12,4)
    if flag==True:
        backwards_arm(img1,12,8)
        backwards_arm(img1,12,12)
    else :
        backwards_limb(img1,12,8)
        backwards_limb(img1,12,12)

    img2=copy.deepcopy(img1)
    exchange_limb(img1)#左右変更
    return img1
    
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
        print("input file:",i)
        img1,flag=flip_backwards(i)
        if flag==True:
            output_file=i.replace(".png","-slim.png")
        else :
            output_file=i.replace(".png","-classic.png")
        print("output file:",output_file)
        cv2.imwrite(output_file,img1)
