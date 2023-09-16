import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import copy
import transform as tf
import upsidedown_flip as uf

def compress_leg(img1,x,y,flag=True):#x,yは左上
    q=4
    list1=np.zeros((12,16,4))
    if flag:
        list1=tf.upsidedown(img1[(x+1)*q:(x+4)*q,(y)*q:(y+4)*q])
    else :
        list1=img1[(x+1)*q:(x+4)*q,(y)*q:(y+4)*q]
    for i in range(8):
        n=int(12.0*float(i)/8.0)
        a=12.0*i/8.0-float(n)
        for j in range(len(list1[i])):
            if(list1[n][j][3]!=0 and list1[n+1][j][3]!=0):
                list1[i][j]=float(1-a)*list1[n][j]+float(a)*list1[n+1][j]
            else:
                list1[i,j,:]=0
    for i in range(4):
        list1[i+8]=np.zeros((16,4))
    for i in range(12):
        for j in range(16):
            if list1[i][j][3]>0 and list1[i][j][3]<=0.5:
                list1[i,j,:]=0
    if flag:
        img1[(x+1)*q:(x+4)*q,(y)*q:(y+4)*q]=tf.upsidedown(list1)
        return img1
    else :
        return list1
    #print(type(img1))
    
def compress_body(img1,x,y,flag=True):#圧縮されたlistを返す(逆順)
    q=4
    list1=np.zeros((12,24,4))
    if flag:
        list1=tf.upsidedown(img1[(x+1)*q:(x+4)*q,(y)*q:(y+6)*q])
    else :
        list1=img1[(x+1)*q:(x+4)*q,(y)*q:(y+6)*q]
    for i in range(8):
        n=int(12.0*float(i)/8.0)
        a=12.0*i/8.0-float(n)
        for j in range(len(list1[i])):
            if(list1[n][j][3]!=0 and list1[n+1][j][3]!=0):
                list1[i][j]=float(1-a)*list1[n][j]+float(a)*list1[n+1][j]
            else:
                list1[i,j,:]=0
    for i in range(4):
        list1[i+8]=np.zeros((24,4))
    for i in range(12):
        for j in range(24):
            if list1[i][j][3]>0 and list1[i][j][3]<=0.5:
                list1[i,j,:]=0
    return list1

#上側に圧縮 踏みつけスキン
def compress_list_upper(img1):
    list1=compress_body(img1,4,4,False)
    
    list2=compress_body(img1,8,4,False)
    img1[20:28,16:40]=list1[:8,:]
    img1[36:44,16:40]=list2[:8,:]
    
    list3=compress_leg(img1,4,0,False)
    list4=compress_leg(img1,8,0,False)
    list5=compress_leg(img1,12,0,False)
    list6=compress_leg(img1,12,4,False)
    
    img1[28:32,16:24]=list3[:4,:8]
    img1[28:32,24:36]=list6[:4,4:]
    img1[28:32,36:40]=list3[:4,12:16]
    
    img1[44:48,16:24]=list4[:4,:8]
    img1[44:48,24:36]=list5[:4,4:]
    img1[44:48,36:40]=list4[:4,12:16]
    # ここまでで胴体の側面は確定
    # 胴体の底面(16:20,28:36)(32:36,28:36)
    #胴体の底面の指定
    #下位レイヤー
    q=4
    img1[5*q-2:5*q,7*q:9*q]=np.array([img1[8*q-1,5*q:7*q]]).repeat(2,axis=0)
    img1[4*q:5*q-2,7*q:9*q]=tf.flip(np.array([img1[8*q-1,8*q:10*q]]).repeat(2,axis=0))
    img1[4*q:5*q,7*q:7*q+2]=np.array([img1[8*q-1,4*q:5*q]]).transpose(1,0,2).repeat(2,axis=1)
    img1[4*q:5*q,9*q-2:9*q]=tf.upsidedown(np.array([img1[8*q-1,7*q:8*q]]).transpose(1,0,2).repeat(2,axis=1))
    #上位レイヤー
    img1[9*q-2:9*q,7*q:9*q]=np.array([img1[12*q-1,5*q:7*q]]).repeat(2,axis=0)
    img1[8*q:8*q+2,7*q:9*q]=tf.flip(np.array([img1[12*q-1,8*q:10*q]]).repeat(2,axis=0))
    img1[8*q:9*q,7*q:7*q+2]=(np.array([img1[12*q-1,4*q:5*q]]).transpose(1,0,2).repeat(2,axis=1))
    img1[8*q:9*q,9*q-2:9*q]=tf.upsidedown(np.array([img1[12*q-1,7*q:8*q]]).transpose(1,0,2).repeat(2,axis=1))
    
    # 足を上に移動
    img1[20:24,:16]=img1[24:28,:16]
    img1[24:32,:16,:]=0
    img1[36:40,:16]=img1[40:44,:16]
    img1[40:48,:16,:]=0
    img1[52:56,:16]=img1[56:60,:16]
    img1[56:,:16,:]=0
    img1[52:56,16:32]=img1[56:60,16:32]
    img1[56:,16:32,:]=0
    
    #足の上面の指定
    uf.upperside_leg(img1,16,0)
    uf.upperside_leg(img1,32,0)
    uf.upperside_leg(img1,48,0)
    uf.upperside_leg(img1,48,16)
    
    p=8
    
    img1[4*q:5*q,2*q:3*q]=uf.cut_list(img1[0:p,2*p:2*p+q],axis=0)
    img1[12*q:13*q,6*q:7*q]=uf.cut_list(img1[0:p,2*p+q:3*p],axis=0)
    
    img1[5*q+4:7*q+4,0:q]=uf.cut_list(img1[p:2*p,0:p],axis=1)
    img1[5*q+4:7*q+4,q:2*q]=img1[p:2*p,p:p+q]
    img1[13*q+4:15*q+4,5*q:6*q]=img1[p:2*p,p+q:2*p]
    img1[13*q+4:15*q+4,6*q:7*q]=uf.cut_list(img1[p:2*p,2*p:3*p],axis=1)
    img1[13*q+4:15*q+4,7*q:8*q]=img1[p:2*p,3*p:3*p+q]
    img1[5*q+4:7*q+4,3*q:4*q]=img1[p:2*p,3*p+q:4*p]
    
    img1[8*q:9*q,2*q:3*q]=uf.cut_list(img1[0:p,6*p:6*p+q],axis=0)
    img1[12*q:13*q,2*q:3*q]=uf.cut_list(img1[0:p,6*p+q:7*p],axis=0)
    img1[9*q+4:11*q+4,0:q]=uf.cut_list(img1[p:2*p,4*p:5*p],axis=1)
    img1[9*q+4:11*q+4,q:2*q]=img1[p:2*p,5*p:5*p+q]
    img1[13*q+4:15*q+4,q:2*q]=img1[p:2*p,5*p+q:6*p]
    img1[13*q+4:15*q+4,2*q:3*q]=uf.cut_list(img1[p:2*p,6*p:7*p],axis=1)
    img1[13*q+4:15*q+4,3*q:4*q]=img1[p:2*p,7*p:7*p+q]
    img1[9*q+4:11*q+4,3*q:4*q]=img1[p:2*p,7*p+q:8*p]
    
    img1[5*q:8*q,2*q:3*q]=img1[13*q:16*q,5*q:6*q]
    img1[9*q:12*q,2*q:3*q]=img1[13*q:16*q,1*q:2*q]
    img1[13*q:16*q,4*q:5*q]=img1[5*q:8*q,1*q:2*q]
    img1[13*q:16*q,0*q:1*q]=img1[9*q:12*q,1*q:2*q]
    return img1
    
# 下側に圧縮　持ち上げスキン
def compress_list(img1):
    flag1=uf.judge_slim_classic(img1)
    
    #手を反転させる
    if flag1==True:
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
    img1[12*q-4:12*q,4*q:10*q]=tf.upsidedown(list2[4:8])#

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
    #足の側面(不要)
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
def replace_leg(img1,img2):#img1のlegをimg2のheadで置き換え
    p=8
    q=4
    img1[16:20,8:12,:]=0
    img1[24:32,:16,:]=0
    img1[32:36,8:12,:]=0
    img1[40:48,:16,:]=0
    img1[48:52,8:12,:]=0
    img1[56:64,:16,:]=0
    img1[48:52,24:28,:]=0
    img1[56:64,16:32,:]=0
    
    img1[4*q:5*q,2*q:3*q]=uf.cut_list(img2[0:p,2*p:2*p+q],axis=0)
    img1[12*q:13*q,6*q:7*q]=uf.cut_list(img2[0:p,2*p+q:3*p],axis=0)
    img1[5*q+4:7*q+4,0:q]=uf.cut_list(img2[p:2*p,0:p],axis=1)
    img1[5*q+4:7*q+4,q:2*q]=img2[p:2*p,p:p+q]
    img1[13*q+4:15*q+4,5*q:6*q]=img2[p:2*p,p+q:2*p]
    img1[13*q+4:15*q+4,6*q:7*q]=uf.cut_list(img2[p:2*p,2*p:3*p],axis=1)
    img1[13*q+4:15*q+4,7*q:8*q]=img2[p:2*p,3*p:3*p+q]
    img1[5*q+4:7*q+4,3*q:4*q]=img2[p:2*p,3*p+q:4*p]
    
    img1[8*q:9*q,2*q:3*q]=uf.cut_list(img2[0:p,6*p:6*p+q],axis=0)
    img1[12*q:13*q,2*q:3*q]=uf.cut_list(img2[0:p,6*p+q:7*p],axis=0)
    img1[9*q+4:11*q+4,0:q]=uf.cut_list(img2[p:2*p,4*p:5*p],axis=1)
    img1[9*q+4:11*q+4,q:2*q]=img2[p:2*p,5*p:5*p+q]
    img1[13*q+4:15*q+4,q:2*q]=img2[p:2*p,5*p+q:6*p]
    img1[13*q+4:15*q+4,2*q:3*q]=uf.cut_list(img2[p:2*p,6*p:7*p],axis=1)
    img1[13*q+4:15*q+4,3*q:4*q]=img2[p:2*p,7*p:7*p+q]
    img1[9*q+4:11*q+4,3*q:4*q]=img2[p:2*p,7*p+q:8*p]
    
    
    img1[5*q:8*q,2*q:3*q]=img1[13*q:16*q,5*q:6*q]
    img1[9*q:12*q,2*q:3*q]=img1[13*q:16*q,1*q:2*q]
    img1[13*q:16*q,4*q:5*q]=img1[5*q:8*q,1*q:2*q]
    img1[13*q:16*q,0*q:1*q]=img1[9*q:12*q,1*q:2*q]
    return img1
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