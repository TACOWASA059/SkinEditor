import cv2
import numpy as np
import os
import matplotlib.image as mimage
from PIL import Image
def modify_image(directory_path):
    png_files = []
    for file in os.listdir(directory_path):
        if file.endswith(".png"):
            png_files.append(file)
    #print(png_files)
    for input_file in png_files:
        input_file=directory_path+"/"+input_file
        # リサイズ後のサイズを指定
        output_size = (64, 64)
        #print(input_file)
        image = cv2.imread(input_file,-1)
        if(len(image)==32):
            resize_image(input_file, input_file, output_size)
            print("modified "+input_file+"\n")

def resize_image(input_path, output_path, size):
    try:
        # 画像を読み込む
        image = cv2.imread(input_path,-1)
        array = np.zeros(shape=(64,64,4))
        for i in range(32):
            for j in range(64):
                array[i][j]=image[i][j]
        for i in range(16,32):
            for j in range(16):
                array[i+32][j+16]=image[i][j]
        for i in range(16,32):
            for j in range(40,56):
                array[i+32][j+16-24]=image[i][j]
        # 出力パスに保存
        cv2.imwrite(output_path, array)
        #print("出力完了")
    except IOError:
        print("ファイルを開けませんでした。")
def resize_img(img):
    array = np.zeros(shape=(64,64,4),dtype=img.dtype)
    for i in range(32):
        for j in range(64):
            array[i][j]=img[i][j]
    for i in range(16,32):
        for j in range(16):
            array[i+32][j+16]=img[i][j]
    for i in range(16,32):
        for j in range(40,56):
            array[i+32][j+16-24]=img[i][j]
    return array
    

if __name__=="__main__":
    modify_image("SkinData")

