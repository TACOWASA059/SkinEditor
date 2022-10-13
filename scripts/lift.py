import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import copy
import transform as tf
import upsidedown_flip as uf

def compress_leg(img1,x,y):#x,yは左上
    q=4
    list1=np.zeros((12,16,4))
    list1=tf.upsidedown(img1[(x+1)*q:(x+4)*q,(y)*q:(y+4)*q])
    for i in range(8):
        n=int(12.0*float(i)/8.0)
        a=12.0*i/8.0-float(n)
        list1[i]=np.float32(1-a)*list1[n]+np.float32(a)*list1[n+1]
    for i in range(4):
        list1[i+8]=np.zeros((16,4))
    img1[(x+1)*q:(x+4)*q,(y)*q:(y+4)*q]=tf.upsidedown(list1)
    #print(type(img1))
    return img1
def compress_body(img1,x,y):#圧縮されたlistを返す(逆順)
    q=4
    list1=np.zeros((12,24,4))
    list1=tf.upsidedown(img1[(x+1)*q:(x+4)*q,(y)*q:(y+6)*q])
    for i in range(8):
        n=int(12.0*float(i)/8.0)
        a=12.0*i/8.0-float(n)
        list1[i]=np.float32(1-a)*list1[n]+np.float32(a)*list1[n+1]
    for i in range(4):
        list1[i+8]=np.zeros((24,4))
    return list1
def compress_list(img1):
    flag=uf.judge_slim_classic(img1)
    
    #手を反転させる
    if flag==True:
        uf.upsidedown_arm(img1,12,8)
        uf.upsidedown_arm(img1,12,12)
        uf.upsidedown_arm(img1,4,10)
        uf.upsidedown_arm(img1,8,10)
    else :
        uf.upsidedown_limb(img1,12,8)
        uf.upsidedown_limb(img1,12,12)
        uf.upsidedown_limb(img1,4,10)
        uf.upsidedown_limb(img1,8,10)

    #足の圧縮(12マスを8マスに圧縮)
    compress_leg(img1,4,0)
    compress_leg(img1,8,0)
    compress_leg(img1,12,0)
    compress_leg(img1,12,4)

    #胴体の圧縮(返り値は逆順)
    list1=compress_body(img1,4,4)
    list2=compress_body(img1,8,4)
    q=4
    img1[5*q:5*q+4,0:2*q]=tf.upsidedown(list1[:4,:8])
    img1[5*q:5*q+4,3*q:4*q]=tf.upsidedown(list1[:4,20:24])
    img1[13*q:13*q+4,5*q:8*q]=tf.upsidedown(list1[:4,8:20])
    img1[9*q:9*q+4,0:2*q]=tf.upsidedown(list2[:4,:8])
    img1[9*q:9*q+4,3*q:4*q]=tf.upsidedown(list2[:4,20:24])
    img1[13*q:13*q+4,1*q:4*q]=tf.upsidedown(list2[:4,8:20])

    #bodyを下に移動
    img1[8*q-4:8*q,4*q:10*q]=tf.upsidedown(list1[4:8])
    img1[12*q-4:12*q,4*q:10*q]=tf.upsidedown(list2[4:8])

    #頭を胴体に移動
    p=8
    img1[5*q:7*q,4*q:5*q]=uf.cut_list(img1[p:2*p,0:p],axis=1)
    img1[5*q:7*q,5*q:7*q]=copy.deepcopy(img1[p:2*p,p:2*p])
    img1[5*q:7*q,7*q:8*q]=uf.cut_list(img1[p:2*p,2*p:3*p],axis=1)
    img1[5*q:7*q,8*q:10*q]=copy.deepcopy(img1[p:2*p,3*p:4*p])
        #上側
    img1[4*q:5*q,5*q:7*q]=uf.cut_list(img1[0:p,p:2*p],axis=0)

    img1[9*q:11*q,4*q:5*q]=uf.cut_list(img1[p:2*p,4*p:5*p],axis=1)
    img1[9*q:11*q,5*q:7*q]=copy.deepcopy(img1[p:2*p,5*p:6*p])
    img1[9*q:11*q,7*q:8*q]=uf.cut_list(img1[p:2*p,6*p:7*p],axis=1)
    img1[9*q:11*q,8*q:10*q]=copy.deepcopy(img1[p:2*p,7*p:8*p])
        #上側
    img1[8*q:9*q,5*q:7*q]=uf.cut_list(img1[0:p,5*p:6*p],axis=0)

    #胴体の底面の指定
    #下位レイヤー
    img1[5*q-2:5*q,7*q:9*q]=np.array([img1[8*q-1,5*q:7*q]]).repeat(2,axis=0)
    img1[4*q:5*q-2,7*q:9*q]=tf.flip(np.array([img1[8*q-1,8*q:10*q]]).repeat(2,axis=0))
    img1[4*q:5*q,7*q:7*q+2]=np.array([img1[8*q-1,4*q:5*q]]).transpose(1,0,2).repeat(2,axis=1)
    img1[4*q:5*q,9*q-2:9*q]=tf.upsidedown(np.array([img1[8*q-1,7*q:8*q]]).transpose(1,0,2).repeat(2,axis=1))
    #上位レイヤー
    img1[9*q-2:9*q,7*q:9*q]=np.array([img1[12*q-1,5*q:7*q]]).repeat(2,axis=0)
    img1[8*q:8*q+2,7*q:9*q]=tf.flip(np.array([img1[12*q-1,8*q:10*q]]).repeat(2,axis=0))
    img1[8*q:9*q,7*q:7*q+2]=(np.array([img1[12*q-1,4*q:5*q]]).transpose(1,0,2).repeat(2,axis=1))
    img1[8*q:9*q,9*q-2:9*q]=tf.upsidedown(np.array([img1[12*q-1,7*q:8*q]]).transpose(1,0,2).repeat(2,axis=1))

    #足の上面の指定
    uf.upperside_leg(img1,16,0)
    uf.upperside_leg(img1,32,0)
    uf.upperside_leg(img1,48,0)
    uf.upperside_leg(img1,48,16)
    #print(type(img1))
    #足の側面
    img1[5*q:6*q,2*q:3*q]=img1[13*q:14*q,5*q:6*q]
    img1[9*q:10*q,2*q:3*q]=img1[13*q:14*q,1*q:2*q]
    img1[13*q:14*q,4*q:5*q]=img1[5*q:6*q,1*q:2*q]
    img1[13*q:14*q,0*q:1*q]=img1[9*q:10*q,1*q:2*q]
    return img1
def compress(file_name:str):
    img1=cv2.imread(file_name,-1)
    if len(img1)!=64 or len(img1[0])!=64 :
        print("Pixel Size Error:input image size must be 64x64.")
        exit()
    return compress_list(img1)

def replace_head(img1,img2):#img1のhead部分をimg2のheadに置き換え
    p=8
    img1[0:2*p]=copy.deepcopy(img2[0:2*p])
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
        img1,flag=compress(i)
        if flag==True:
            output_file=i.replace(".png","-lift-slim.png")
        else :
            output_file=i.replace(".png","-lift-classic.png")
        print("output file:",output_file)
        cv2.imwrite(output_file,img1)