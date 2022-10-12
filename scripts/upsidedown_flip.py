import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import copy
import transform as tf
#slimとclassicの判定が一応あり

#四肢の上下反転
def upsidedown_limb(img1,x,y):#左上が(4x,4y)、右下が(4(x+4),4(y+4))のピクセルに対応
    q=4
    img2=copy.deepcopy(img1)
    img1[x*q:(x+1)*q,(y+1)*q:(y+2)*q]=img2[x*q:(x+1)*q,(y+2)*q:(y+3)*q]
    img1[x*q:(x+1)*q,(y+2)*q:(y+3)*q]=img2[x*q:(x+1)*q,(y+1)*q:(y+2)*q]
    img1[(x+1)*q:(x+4)*q,y*q:(y+4)*q]=tf.upsidedown(img1[(x+1)*q:(x+4)*q,y*q:(y+4)*q])
    return img1
def upsidedown_arm(img1,x,y):#slim用,classicはlimbを使う
    q=4
    #4x3のrotate(2ヶ所)
    img2=copy.deepcopy(img1)
    img1[x*q:(x+1)*q,(y+1)*q:(y+2)*q-1]=img2[x*q:(x+1)*q,(y+2)*q-1:(y+3)*q-2]
    img1[x*q:(x+1)*q,(y+2)*q-1:(y+3)*q-2]=img2[x*q:(x+1)*q,(y+1)*q:(y+2)*q-1]
    #右端を消し飛ばす(4x3の右側)4x2を消す
    img1[x*q:(x+1)*q,(y+3)*q-2:(y+3)*q]=np.full(img1[x*q:(x+1)*q,(y+3)*q-2:(y+3)*q].shape, 0)
    #上下反転
    img1[(x+1)*q:(x+4)*q,y*q:(y+4)*q-2]=tf.upsidedown( img1[(x+1)*q:(x+4)*q,y*q:(y+4)*q-2])
    #右端を消し飛ばす(12x14の右側)12x2を消す
    img1[(x+1)*q:(x+4)*q,(y+4)*q-2:(y+4)*q]=np.full(img1[(x+1)*q:(x+4)*q,(y+4)*q-2:(y+4)*q].shape,0)
    return img1
#2段目と3段目
def upsidedown_body(img1,number,flag):#numberは行(縦)の指定,上が4*number、下が4*(number+4)
    q=4
    n1=number
    n2=number+1
    n3=number+4
    #一番左
    upsidedown_limb(img1,n1,0)
    #一番右
    #slim用
    if flag==True:
        upsidedown_arm(img1,n1,10)
    else :
        upsidedown_limb(img1,n1,10)
    #真ん中
    img2=copy.deepcopy(img1)
    img1[n1*q:n2*q,5*q:7*q]=img2[n1*q:n2*q,7*q:9*q]
    img1[n1*q:n2*q,7*q:9*q]=img2[n1*q:n2*q,5*q:7*q]
    img1[n2*q:n3*q,4*q:10*q]=tf.upsidedown(img1[n2*q:n3*q,4*q:10*q])
    return img1
def upsidedown_head(img1):#顔の反転操作
    p=8
    #顔の部分
    #顔の上面と下面
    img2=copy.deepcopy(img1)
    img1[:p,p:2*p]=img2[:p,2*p:3*p]
    img1[:p,2*p:3*p]=img2[:p,p:2*p]
    img1[:p,5*p:6*p]=img2[:p,6*p:7*p]
    img1[:p,6*p:7*p]=img2[:p,5*p:6*p]
    #4面の右シフト
    img1[p:2*p,:4*p]=tf.upsidedown(img1[p:2*p,:4*p])
    img1[p:2*p,4*p:8*p]=tf.upsidedown(img1[p:2*p,4*p:8*p])
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
def cut_list(img1,axis):
    #リストを半分にする
    img2=[]
    if axis==0:
        #行を半分にする
        for i in range(int(len(img1)/2)):
            img2.append((img1[2*i]/2+img1[2*i+1]/2))
    elif axis==1:
        #列を半分にする
        img3=img1.transpose(1,0,2)
        for i in range(int(len(img3)/2)):
            img2.append((img3[2*i]/2+img3[2*i+1]/2))
        img2=np.array(img2).transpose(1,0,2)
    return img2

def upperside_leg(img1,x,y):
    q=4
    img2=copy.deepcopy(img1)
    img1[x+2:x+q,y+q:y+2*q]=np.array([img2[x+4,y+q:y+2*q]]).repeat(2,axis=0)
    img1[x:x+2,y+q:y+2*q]=tf.flip(np.array([img2[x+4,y+3*q:y+4*q]]).repeat(2,axis=0))

def exchange_upsidedown(img1):#上下の交換
    #img2=np.zeros(img1.shape,dtype=np.float16)
    img2=np.zeros(img1.shape)
    p=8
    q=4
    #手だけコピー
    img2[48:64,32:48]=img1[48:64,32:48]
    img2[16:32,40:56]=img1[16:32,40:56]
    img2[48:64,48:64]=img1[48:64,48:64]
    img2[32:48,40:56]=img1[32:48,40:56]

    #顔の下位レイヤー
    #上面
    img2[0:p,p:p+q]=img1[4*q:5*q,q:2*q].repeat(2,axis=0)#行方向に伸ばす
    img2[4*q:5*q,2*q:3*q]=cut_list(img1[0:p,2*p:2*p+q],axis=0)

    img2[0:p,p+q:2*p]=img1[12*q:13*q,5*q:6*q].repeat(2,axis=0)
    img2[12*q:13*q,6*q:7*q]=cut_list(img1[0:p,2*p+q:3*p],axis=0)

    #側面
    img2[p:2*p,0:p]=img1[5*q:7*q,0:q].repeat(2,axis=1)
    img2[5*q+4:7*q+4,0:q]=cut_list(img1[p:2*p,0:p],axis=1)

    img2[p:2*p,p:p+q]=img1[5*q:7*q,q:2*q]
    img2[5*q+4:7*q+4,q:2*q]=img1[p:2*p,p:p+q]

    img2[p:2*p,p+q:2*p]=img1[13*q:15*q,5*q:6*q]
    img2[13*q+4:15*q+4,5*q:6*q]=img1[p:2*p,p+q:2*p]

    img2[p:2*p,2*p:3*p]=img1[13*q:15*q,6*q:7*q].repeat(2,axis=1)
    img2[13*q+4:15*q+4,6*q:7*q]=cut_list(img1[p:2*p,2*p:3*p],axis=1)

    img2[p:2*p,3*p:3*p+q]=img1[13*q:15*q,7*q:8*q]
    img2[13*q+4:15*q+4,7*q:8*q]=img1[p:2*p,3*p:3*p+q]

    img2[p:2*p,3*p+q:4*p]=img1[5*q:7*q,3*q:4*q]
    img2[5*q+4:7*q+4,3*q:4*q]=img1[p:2*p,3*p+q:4*p]
    #顔の上位レイヤー
    #上面
    img2[0:p,5*p:5*p+q]=img1[8*q:9*q,q:2*q].repeat(2,axis=0)#行方向に伸ばす
    img2[8*q:9*q,2*q:3*q]=cut_list(img1[0:p,6*p:6*p+q],axis=0)

    img2[0:p,5*p+q:6*p]=img1[12*q:13*q,q:2*q].repeat(2,axis=0)
    img2[12*q:13*q,2*q:3*q]=cut_list(img1[0:p,6*p+q:7*p],axis=0)
    
    img2[p:2*p,4*p:5*p]=img1[9*q:11*q,0:q].repeat(2,axis=1)
    img2[9*q+4:11*q+4,0:q]=cut_list(img1[p:2*p,4*p:5*p],axis=1)

    img2[p:2*p,5*p:5*p+q]=img1[9*q:11*q,q:2*q]
    img2[9*q+4:11*q+4,q:2*q]=img1[p:2*p,5*p:5*p+q]

    img2[p:2*p,5*p+q:6*p]=img1[13*q:15*q,q:2*q]
    img2[13*q+4:15*q+4,q:2*q]=img1[p:2*p,5*p+q:6*p]

    img2[p:2*p,6*p:7*p]=img1[13*q:15*q,2*q:3*q].repeat(2,axis=1)
    img2[13*q+4:15*q+4,2*q:3*q]=cut_list(img1[p:2*p,6*p:7*p],axis=1)

    img2[p:2*p,7*p:7*p+q]=img1[13*q:15*q,3*q:4*q]
    img2[13*q+4:15*q+4,3*q:4*q]=img1[p:2*p,7*p:7*p+q]

    img2[p:2*p,7*p+q:8*p]=img1[9*q:11*q,3*q:4*q]
    img2[9*q+4:11*q+4,3*q:4*q]=img1[p:2*p,7*p+q:8*p]

    #胴体と右足(下位レイヤー)
    img2[5*q:6*q,4*q:6*q]=img1[7*q:8*q,0:2*q]
    img2[5*q:6*q,0:2*q]=img1[7*q:8*q,4*q:6*q]

    img2[5*q:6*q,9*q:10*q]=img1[7*q:8*q,3*q:4*q]
    img2[5*q:6*q,3*q:4*q]=img1[7*q:8*q,9*q:10*q]
    #胴体と左足(下位レイヤー)
    img2[5*q:6*q,6*q:9*q]=img1[15*q:16*q,5*q:8*q]
    img2[13*q:14*q,5*q:8*q]=img1[7*q:8*q,6*q:9*q]

    #胴体4つ下げ(下位レイヤー)
    img2[6*q:8*q,4*q:10*q]=img1[5*q:7*q,4*q:10*q]
    #胴体4つ下げ(上位レイヤー)
    img2[10*q:12*q,4*q:10*q]=img1[9*q:11*q,4*q:10*q]

    #胴体と右足(上位レイヤー)
    img2[9*q:10*q,4*q:6*q]=img1[11*q:12*q,0:2*q]
    img2[9*q:10*q,0:2*q]=img1[11*q:12*q,4*q:6*q]

    img2[9*q:10*q,9*q:10*q]=img1[11*q:12*q,3*q:4*q]
    img2[9*q:10*q,3*q:4*q]=img1[11*q:12*q,9*q:10*q]
    #胴体と左足(上位レイヤー)
    img2[9*q:10*q,6*q:9*q]=img1[15*q:16*q,q:4*q]
    img2[13*q:14*q,q:4*q]=img1[11*q:12*q,6*q:9*q]

    #顔の底面側の指定
    #下位レイヤー
    img2[p-4:p,2*p:3*p]=np.array([img2[2*p-1,p:2*p]]).repeat(4,axis=0)
    img2[:p-4,2*p:3*p]=tf.flip(np.array([img2[2*p-1,3*p:4*p]]).repeat(4,axis=0))
    img2[:p,2*p:2*p+2]=np.array([img2[2*p-1,:p]]).transpose(1,0,2).repeat(2,axis=1)
    img2[:p,3*p-2:3*p]=tf.upsidedown(np.array([img2[2*p-1,2*p:3*p]]).transpose(1,0,2).repeat(2,axis=1))
    #上位レイヤー
    img2[p-4:p,6*p:7*p]=np.array([img2[2*p-1,5*p:6*p]]).repeat(4,axis=0)
    img2[:p-4,6*p:7*p]=tf.flip(np.array([img2[2*p-1,7*p:8*p]]).repeat(4,axis=0))
    img2[:p,6*p:6*p+2]=np.array([img2[2*p-1,4*p:5*p]]).transpose(1,0,2).repeat(2,axis=1)
    img2[:p,7*p-2:7*p]=tf.upsidedown(np.array([img2[2*p-1,6*p:7*p]]).transpose(1,0,2).repeat(2,axis=1))
    #胴体の上面の指定
    #下位レイヤー
    img2[5*q-2:5*q,5*q:7*q]=np.array([img2[5*q,5*q:7*q]]).repeat(2,axis=0)
    img2[4*q:5*q-2,5*q:7*q]=tf.flip(np.array([img2[5*q,8*q:10*q]]).repeat(2,axis=0))
    img2[4*q:5*q,5*q:5*q+2]=np.array([img2[5*q,4*q:5*q]]).transpose(1,0,2).repeat(2,axis=1)
    img2[4*q:5*q,7*q-2:7*q]=tf.upsidedown(np.array([img2[5*q,7*q:8*q]]).transpose(1,0,2).repeat(2,axis=1))
    #上位レイヤー
    img2[9*q-2:9*q,5*q:7*q]=np.array([img2[9*q,5*q:7*q]]).repeat(2,axis=0)
    img2[8*q:9*q-2,5*q:7*q]=tf.flip(np.array([img2[9*q,8*q:10*q]]).repeat(2,axis=0))
    img2[8*q:9*q,5*q:5*q+2]=np.array([img2[9*q,4*q:5*q]]).transpose(1,0,2).repeat(2,axis=1)
    img2[8*q:9*q,7*q-2:7*q]=tf.upsidedown(np.array([img2[9*q,7*q:8*q]]).transpose(1,0,2).repeat(2,axis=1))

    #胴体の底面の指定
    #下位レイヤー
    img2[5*q-2:5*q,7*q:9*q]=np.array([img2[8*q-1,5*q:7*q]]).repeat(2,axis=0)
    img2[4*q:5*q-2,7*q:9*q]=tf.flip(np.array([img2[8*q-1,8*q:10*q]]).repeat(2,axis=0))
    img2[4*q:5*q,7*q:7*q+2]=np.array([img2[8*q-1,4*q:5*q]]).transpose(1,0,2).repeat(2,axis=1)
    img2[4*q:5*q,9*q-2:9*q]=tf.upsidedown(np.array([img2[8*q-1,7*q:8*q]]).transpose(1,0,2).repeat(2,axis=1))
    #上位レイヤー
    img2[9*q-2:9*q,7*q:9*q]=np.array([img2[12*q-1,5*q:7*q]]).repeat(2,axis=0)
    img2[8*q:8*q+2,7*q:9*q]=tf.flip(np.array([img2[12*q-1,8*q:10*q]]).repeat(2,axis=0))
    img2[8*q:9*q,7*q:7*q+2]=(np.array([img2[12*q-1,4*q:5*q]]).transpose(1,0,2).repeat(2,axis=1))
    img2[8*q:9*q,9*q-2:9*q]=tf.upsidedown(np.array([img2[12*q-1,7*q:8*q]]).transpose(1,0,2).repeat(2,axis=1))

    #足の上面の指定
    upperside_leg(img2,16,0)
    upperside_leg(img2,32,0)
    upperside_leg(img2,48,0)
    upperside_leg(img2,48,16)

    #足の側面
    img2[5*q:8*q,2*q:3*q]=img2[13*q:16*q,5*q:6*q]
    img2[9*q:12*q,2*q:3*q]=img2[13*q:16*q,1*q:2*q]
    img2[13*q:16*q,4*q:5*q]=img2[5*q:8*q,1*q:2*q]
    img2[13*q:16*q,0*q:1*q]=img2[9*q:12*q,1*q:2*q]

    return img2

#メインの関数
def flip_upsidedown(file_name):
    img1=cv2.imread(file_name,-1)
    if len(img1)!=64 or len(img1[0])!=64 :
        print("Pixel Size Error:input image size must be 64x64.")
        exit()
    flag=judge_slim_classic(img1)
    #顔の部分
    upsidedown_head(img1)
    #2段目
    upsidedown_body(img1,4,flag)
    #3段目
    upsidedown_body(img1,8,flag)
    #4段目
    upsidedown_limb(img1,12,0)
    upsidedown_limb(img1,12,4)
    if flag==True:
        upsidedown_arm(img1,12,8)
        upsidedown_arm(img1,12,12)
    else :
        upsidedown_limb(img1,12,8)
        upsidedown_limb(img1,12,12)

    img2=copy.deepcopy(img1)
    img1=exchange_upsidedown(img1)#上下入れ替え
    #test func
    #cv2.imwrite("2.png",img1)
    return img1,flag
def upsidedown(img1):
    flag=judge_slim_classic(img1)
    #顔の部分
    upsidedown_head(img1)
    #2段目
    upsidedown_body(img1,4,flag)
    #3段目
    upsidedown_body(img1,8,flag)
    #4段目
    upsidedown_limb(img1,12,0)
    upsidedown_limb(img1,12,4)
    if flag==True:
        upsidedown_arm(img1,12,8)
        upsidedown_arm(img1,12,12)
    else :
        upsidedown_limb(img1,12,8)
        upsidedown_limb(img1,12,12)

    img2=copy.deepcopy(img1)
    img1=exchange_upsidedown(img1)#上下入れ替え
    #test func
    #cv2.imwrite("2.png",img1)
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
        img1,flag=flip_upsidedown(i)
        if flag==True:
            output_file=i.replace(".png","-upsidedown-slim.png")
        else :
            output_file=i.replace(".png","-upsidedown-classic.png")
        print("output file:",output_file)
        cv2.imwrite(output_file,img1)
