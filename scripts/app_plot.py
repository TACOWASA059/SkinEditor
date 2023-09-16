import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog,messagebox,font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import matplotlib.image as image
import matplotlib.pyplot as plt
import skin_view as sv
import os
import re
import copy
import backward_flip_reform as bf
import lj_flip as lf
import upsidedown_flip as uf
import face_rotate as fr
import lift
import Convert32to64
import SlimWideConverter
import SkinRetreive as sr
import BringOneLayer as bl
import gray
from PIL import Image, ImageTk, ImageDraw

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.img_list=[[],[],[],[]]
        self.master = master
        self.master.geometry("1500x900") 
        self.master.title('スキン編集')
        
        
        
        self.font=font.Font ( size=10)
        self.boldfont=font.Font(size=10,weight="bold")

        # ウィンドウの x ボタンが押された時に呼ばれるメソッドを設定
        self.master.protocol("WM_DELETE_WINDOW", self.delete_window)

        # ステータスバーの作成
        self.create_status_bar()
        
        #img_list
        # listboxの多元化
        ########################################################
        x=310
        y=8
        listbox1 = tk.Listbox(width=20, height=12,selectmode="extended")
        listbox1.drop_target_register(DND_FILES)
        listbox1.dnd_bind('<<Drop>>', lambda e:self.input_file(e,index=0))
        listbox1.place(x=x,y=y+22,width=190,height=100)
        #スクロールバーの作成
        scroll=tk.Scrollbar(listbox1)
        #スクロールバーの配置を決める
        scroll.pack(side=tk.RIGHT,fill="y")
        scroll["command"]=listbox1.yview
        label = tk.Label(self.master, text='(0)読み込みリスト',font=self.font)
        label.place(x=x,y=y+2) 
        #ファイル選択ボタン
        button1 = tk.Button(self.master, text='+',font=self.font)
        button1.config(command=lambda id=0: self.open_file(index=id))
        button1.place(x=x+127,y=y) 
        #ディレクトリ選択ボタン
        button_dir = tk.Button(self.master, text='□',font=self.font)
        button_dir.place(x=x+145,y=y) 
        button_dir.config(command=lambda id=0: self.open_dir(index=id))
        #削除ボタン
        button2 = tk.Button(self.master, text='-',font=self.font)
        button2.place(x=x+170,y=y) 
        button2.config(command=lambda id=0: self.deleteSelectedList(index=id))
        
        #描画ボタン作成
        button = tk.Button(self.master, text = "描画⇒",font=self.font, command = self.plot_graph)
        button.config(command=lambda id=0: self.plot_graph(index=id))
        button.place(x=x+190,y=y+32)
        button = tk.Button(self.master, text='複製',font=self.font,command=self.duplicate)
        button.place(x=x+60,y=y+122) 
        
        button = tk.Button(self.master,text="全選択",font=self.font)
        button.place(x=x+100,y=y+122)
        button.config(command=lambda id=0: self.select_all(index=id))
        button3 =tk.Button(self.master, text = "保存",font=self.font)
        button3.place(x=x+150,y=y+122)
        button3.config(command=lambda id=0: self.save_fig(index=id))
        
        button=tk.Button(self.master,text="(1)",font=self.font)
        button.config(command=lambda : self.move_list_contents(id1=0,id2=1))
        button.place(x=x+1,y=y+122)
        button=tk.Button(self.master,text="(2)",font=self.font)
        button.config(command=lambda : self.move_list_contents(id1=0,id2=2))
        button.place(x=x+26,y=y+122)

        ###########################################################
        y=180
        listbox2 = tk.Listbox(width=20, height=12,selectmode="extended")
        listbox2.drop_target_register(DND_FILES)
        listbox2.dnd_bind('<<Drop>>', lambda e:self.input_file(e,index=1))
        listbox2.place(x=x,y=y+22,width=190,height=100)
        #スクロールバーの作成
        scroll=tk.Scrollbar(listbox2)
        #スクロールバーの配置を決める
        scroll.pack(side=tk.RIGHT,fill="y")
        scroll["command"]=listbox2.yview
        label = tk.Label(self.master, text='(1)優先1リスト',font=self.font)
        label.place(x=x,y=y+2) 
        #ファイル選択ボタン
        button1 = tk.Button(self.master, text='+',font=self.font)
        button1.config(command=lambda id=1: self.open_file(index=id))
        button1.place(x=x+127,y=y) 
        #ディレクトリ選択ボタン
        button_dir = tk.Button(self.master, text='□',font=self.font)
        button_dir.place(x=x+145,y=y) 
        button_dir.config(command=lambda id=1: self.open_dir(index=id))
        #削除ボタン
        button2 = tk.Button(self.master, text='-',font=self.font)
        button2.place(x=x+170,y=y) 
        button2.config(command=lambda id=1: self.deleteSelectedList(index=id))
        #描画ボタン作成
        button = tk.Button(self.master, text = "描画⇒",font=self.font, command = self.plot_graph)
        button.place(x=x+190,y=y+32)
        button.config(command=lambda id=1: self.plot_graph(index=id))
        button = tk.Button(self.master,text="全選択",font=self.font)
        button.place(x=x+100,y=y+122)
        button.config(command=lambda id=1: self.select_all(index=id))
        button3 =tk.Button(self.master, text = "保存",font=self.font)
        button3.place(x=x+150,y=y+122)
        button3.config(command=lambda id=1: self.save_fig(index=id))
        
        button=tk.Button(self.master,text="(0)",font=self.font)
        button.config(command=lambda : self.move_list_contents(id1=1,id2=0))
        button.place(x=x+1,y=y+122)
        button=tk.Button(self.master,text="(2)",font=self.font)
        button.config(command=lambda : self.move_list_contents(id1=1,id2=2))
        button.place(x=x+26,y=y+122)
        ###########################################################
        y=380
        listbox3 = tk.Listbox(width=20, height=12,selectmode="extended")
        listbox3.drop_target_register(DND_FILES)
        listbox3.dnd_bind('<<Drop>>', lambda e:self.input_file(e,index=2))
        listbox3.place(x=x,y=y+22,width=190,height=100)
        #スクロールバーの作成
        scroll=tk.Scrollbar(listbox3)
        #スクロールバーの配置を決める
        scroll.pack(side=tk.RIGHT,fill="y")
        scroll["command"]=listbox3.yview
        label = tk.Label(self.master, text='(2)優先２リスト',font=self.font)
        label.place(x=x,y=y+2) 
        #ファイル選択ボタン
        button1 = tk.Button(self.master, text='+',font=self.font)
        button1.config(command=lambda id=2: self.open_file(index=id))
        button1.place(x=x+127,y=y) 
        #ディレクトリ選択ボタン
        button_dir = tk.Button(self.master, text='□',font=self.font)
        button_dir.place(x=x+145,y=y) 
        button_dir.config(command=lambda id=2: self.open_dir(index=id))
        #削除ボタン
        button2 = tk.Button(self.master, text='-',font=self.font)
        button2.place(x=x+170,y=y) 
        button2.config(command=lambda id=2: self.deleteSelectedList(index=id))
        #描画ボタン作成
        button = tk.Button(self.master, text = "描画⇒",font=self.font, command = self.plot_graph)
        button.place(x=x+190,y=y+32)
        button.config(command=lambda id=2: self.plot_graph(index=id))
        button = tk.Button(self.master,text="全選択",font=self.font)
        button.place(x=x+100,y=y+122)
        button.config(command=lambda id=2: self.select_all(index=id))
        button3 =tk.Button(self.master, text = "保存",font=self.font)
        button3.place(x=x+150,y=y+122)
        button3.config(command=lambda id=2: self.save_fig(index=id))
        
        button=tk.Button(self.master,text="(0)",font=self.font)
        button.config(command=lambda : self.move_list_contents(id1=2,id2=0))
        button.place(x=x+1,y=y+122)
        button=tk.Button(self.master,text="(1)",font=self.font)
        button.config(command=lambda : self.move_list_contents(id1=2,id2=1))
        button.place(x=x+26,y=y+122)
        ###########################################################
        y=580
        listbox4 = tk.Listbox(width=20, height=12,selectmode="extended")
        listbox4.place(x=x,y=y+22,width=190,height=100)
        #スクロールバーの作成
        scroll=tk.Scrollbar(listbox4)
        #スクロールバーの配置を決める
        scroll.pack(side=tk.RIGHT,fill="y")
        scroll["command"]=listbox4.yview
        label = tk.Label(self.master, text='(3)Mergeされたスキンリスト',font=self.font)
        label.place(x=x,y=y+2) 
        #削除ボタン
        button2 = tk.Button(self.master, text='-',font=self.font)
        button2.place(x=x+170,y=y) 
        button2.config(command=lambda id=3: self.deleteSelectedList(index=id))
        #描画ボタン作成
        button = tk.Button(self.master, text = "描画⇒",font=self.font, command = self.plot_graph)
        button.place(x=x+190,y=y+32)
        button.config(command=lambda id=3: self.plot_graph(index=id))
        button = tk.Button(self.master,text="全選択",font=self.font)
        button.place(x=x+100,y=y+122)
        button.config(command=lambda id=3: self.select_all(index=id))
        button3 =tk.Button(self.master, text = "保存",font=self.font)
        button3.place(x=x+150,y=y+122)
        button3.config(command=lambda id=3: self.save_fig(index=id))
        
        button=tk.Button(self.master,text="(0)",font=self.font)
        button.config(command=lambda : self.move_list_contents(id1=3,id2=0))
        button.place(x=x+1,y=y+122)
        button=tk.Button(self.master,text="(1)",font=self.font)
        button.config(command=lambda : self.move_list_contents(id1=3,id2=1))
        button.place(x=x+26,y=y+122)
        button=tk.Button(self.master,text="(2)",font=self.font)
        button.config(command=lambda : self.move_list_contents(id1=3,id2=2))
        button.place(x=x+51,y=y+122)
        ###########################################################
        self.listbox=[listbox1,listbox2,listbox3,listbox4]
        ###########################################################
        #反転ボタン
        label = tk.Label(self.master, text='[1]スキンを反転',font=self.boldfont)
        label.place(x=10,y=10) 
        button = tk.Button(self.master, text = "前後",font=self.font)
        button.config(command=lambda id=0: self.backwards(index=id))
        button.place(x=10,y=40)
        button = tk.Button(self.master, text = "左右",font=self.font)
        button.config(command=lambda id=0: self.flip(index=id))
        button.place(x=50,y=40)       
        button = tk.Button(self.master, text = "上下",font=self.font)
        button.place(x=90,y=40)   
        button.config(command=lambda id=0: self.upsidedown(index=id))
        #head回転
        label = tk.Label(self.master, text='[2]headを回転',font=self.boldfont)
        
        # ラベルに画像を配置
        label.place(x=170,y=10) 
        button = tk.Button(self.master, text = "↑",font=self.font, command = self.up)
        button.place(x=190,y=40)
        button = tk.Button(self.master, text = "⤵︎",font=self.font, command = self.rotate_clock)
        button.place(x=220,y=40)
        button = tk.Button(self.master, text = "↓",font=self.font, command = self.down)
        button.place(x=190,y=100)   
        button = tk.Button(self.master, text = "⤴︎",font=self.font, command = self.rotate_counter_clock)
        button.place(x=220,y=100)
        button = tk.Button(self.master, text = "←",font=self.font, command = self.left)
        button.place(x=160,y=70) 
        button = tk.Button(self.master, text = "→",font=self.font, command = self.right)
        button.place(x=250,y=70) 
        label = tk.Label(self.master, text='回転方向',font=self.font)
        label.place(x=190,y=70) 
        label = tk.Label(self.master, text='[3]持ち上げ',font=self.boldfont)
        label.place(x=10,y=70) 
        button = tk.Button(self.master, text='持ち上げスキンに変更',font=self.font,command=self.compress)
        button.place(x=10,y=100) 
        button = tk.Button(self.master, text='頭を別スキンで置き換え',font=self.font,command=self.replace)
        button.place(x=10,y=130) 
        
        
        label = tk.Label(self.master, text='[4]slim/wide',font=self.boldfont)
        label.place(x=170,y=130) 
        button = tk.Button(self.master, text='wide',font=self.font,command=self.towide)
        button.place(x=170,y=160) 
        button = tk.Button(self.master, text='slim',font=self.font,command=self.toslim)
        button.place(x=210,y=160) 
        
        label = tk.Label(self.master, text='[5]踏みつけ',font=self.boldfont)
        label.place(x=10,y=160) 
        button = tk.Button(self.master, text='踏みつけスキンに変更',font=self.font,command=self.toStamp)
        button.place(x=10,y=190) 
        button = tk.Button(self.master, text='足を別の頭に置き換え',font=self.font,command=self.replace_leg)
        button.place(x=10,y=220) 
        
        label = tk.Label(self.master, text='[6]レイヤー',font=self.boldfont)
        label.place(x=170,y=190) 
        button = tk.Button(self.master, text='内側レイヤーに集約',font=self.font,command=self.toInnerLayer)
        button.place(x=170,y=220) 
        button = tk.Button(self.master, text='外側レイヤーに集約',font=self.font,command=self.toOuterLayer)
        button.place(x=170,y=250) 
        
        label=tk.Label(self.master,font=self.boldfont,text="[7]MCID入力")
        label.place(x=10,y=250)
        button=tk.Button(self.master,font=self.font,text="スキン取得",command=self.retreive_skin)
        button.place(x=90,y=250)
        self.input_text=tk.Text(self.master,height=4, width=18,font=self.font)
        self.input_text.place(x=10,y=280)
        
        label = tk.Label(self.master, text='[8]その他',font=self.boldfont)
        label.place(x=170,y=280) 
        button = tk.Button(self.master, text='画像の余白を削除',font=self.font,command=self.erase_margin)
        button.place(x=170,y=310) 
        
        button = tk.Button(self.master, text='グレースケール化',font=self.font,command=self.toGray)
        button.place(x=170,y=340) 
        
        x=30
        y=400
        label=tk.Label(root,text="[9]Skin Merge",font=self.boldfont)
        label.place(x=x-20,y=y-60)
        label=tk.Label(root,text="(1)優先1",font=self.boldfont)
        label.place(x=x,y=y-40)
        label=tk.Label(root,text="body",font=self.boldfont)
        label.place(x=x+30,y=y-20)
        self.head_button=tk.Button(root,text="head",width=4,height=2,relief=tk.SOLID,bg="orange")
        self.head_button.config(command=lambda btn=self.head_button: self.change_state(button=btn,index=1))
        self.head_button.place(x=x+30,y=y)
        self.body_button=tk.Button(root,text="body",width=4,height=3,relief=tk.SOLID,bg="orange")
        self.body_button.config(command=lambda btn=self.body_button: self.change_state(button=btn,index=1))
        self.body_button.place(x=x+30,y=y+45)
        self.Rarm_button=tk.Button(root,text="R\narm",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Rarm_button.config(command=lambda btn=self.Rarm_button: self.change_state(button=btn,index=1))
        self.Rarm_button.place(x=x+5,y=y+45)
        self.Larm_button=tk.Button(root,text="L\narm",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Larm_button.config(command=lambda btn=self.Larm_button: self.change_state(button=btn,index=1))
        self.Larm_button.place(x=x+70,y=y+45)
        self.Rleg_button=tk.Button(root,text="R\nleg",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Rleg_button.config(command=lambda btn=self.Rleg_button: self.change_state(button=btn,index=1))
        self.Rleg_button.place(x=x+25,y=y+105)
        self.Lleg_button=tk.Button(root,text="L\nleg",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Lleg_button.config(command=lambda btn=self.Lleg_button: self.change_state(button=btn,index=1))
        self.Lleg_button.place(x=x+50,y=y+105)
        x+=90
        label=tk.Label(root,text="overlay",font=self.boldfont)
        label.place(x=x+25,y=y-20)
        self.head_button2=tk.Button(root,text="head",width=4,height=2,relief=tk.SOLID,bg="orange")
        self.head_button2.config(command=lambda btn=self.head_button2: self.change_state(button=btn,index=1))
        self.head_button2.place(x=x+30,y=y)
        self.body_button2=tk.Button(root,text="body",width=4,height=3,relief=tk.SOLID,bg="orange")
        self.body_button2.config(command=lambda btn=self.body_button2: self.change_state(button=btn,index=1))
        self.body_button2.place(x=x+30,y=y+45)
        self.Rarm_button2=tk.Button(root,text="R\narm",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Rarm_button2.config(command=lambda btn=self.Rarm_button2: self.change_state(button=btn,index=1))
        self.Rarm_button2.place(x=x+5,y=y+45)
        self.Larm_button2=tk.Button(root,text="L\narm",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Larm_button2.config(command=lambda btn=self.Larm_button2: self.change_state(button=btn,index=1))
        self.Larm_button2.place(x=x+70,y=y+45)
        self.Rleg_button2=tk.Button(root,text="R\nleg",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Rleg_button2.config(command=lambda btn=self.Rleg_button2: self.change_state(button=btn,index=1))
        self.Rleg_button2.place(x=x+25,y=y+105)
        self.Lleg_button2=tk.Button(root,text="L\nleg",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Lleg_button2.config(command=lambda btn=self.Lleg_button2: self.change_state(button=btn,index=1))
        self.Lleg_button2.place(x=x+50,y=y+105)
        
        
        x=30
        y=600
        label=tk.Label(root,text="(2)優先2",font=self.boldfont)
        label.place(x=x,y=y-40)
        label=tk.Label(root,text="body",font=self.boldfont)
        label.place(x=x+30,y=y-20)
        self.head_button3=tk.Button(root,text="head",width=4,height=2,relief=tk.SOLID,bg="orange")
        self.head_button3.config(command=lambda btn=self.head_button3: self.change_state(button=btn,index=2))
        self.head_button3.place(x=x+30,y=y)
        self.body_button3=tk.Button(root,text="body",width=4,height=3,relief=tk.SOLID,bg="orange")
        self.body_button3.config(command=lambda btn=self.body_button3: self.change_state(button=btn,index=2))
        self.body_button3.place(x=x+30,y=y+45)
        self.Rarm_button3=tk.Button(root,text="R\narm",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Rarm_button3.config(command=lambda btn=self.Rarm_button3: self.change_state(button=btn,index=2))
        self.Rarm_button3.place(x=x+5,y=y+45)
        self.Larm_button3=tk.Button(root,text="L\narm",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Larm_button3.config(command=lambda btn=self.Larm_button3: self.change_state(button=btn,index=2))
        self.Larm_button3.place(x=x+70,y=y+45)
        self.Rleg_button3=tk.Button(root,text="R\nleg",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Rleg_button3.config(command=lambda btn=self.Rleg_button3: self.change_state(button=btn,index=2))
        self.Rleg_button3.place(x=x+25,y=y+105)
        self.Lleg_button3=tk.Button(root,text="L\nleg",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Lleg_button3.config(command=lambda btn=self.Lleg_button3: self.change_state(button=btn,index=2))
        self.Lleg_button3.place(x=x+50,y=y+105)
        x+=90
        label=tk.Label(root,text="overlay",font=self.boldfont)
        label.place(x=x+25,y=y-20)
        self.head_button4=tk.Button(root,text="head",width=4,height=2,relief=tk.SOLID,bg="orange")
        self.head_button4.config(command=lambda btn=self.head_button4: self.change_state(button=btn,index=2))
        self.head_button4.place(x=x+30,y=y)
        self.body_button4=tk.Button(root,text="body",width=4,height=3,relief=tk.SOLID,bg="orange")
        self.body_button4.config(command=lambda btn=self.body_button4: self.change_state(button=btn,index=2))
        self.body_button4.place(x=x+30,y=y+45)
        self.Rarm_button4=tk.Button(root,text="R\narm",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Rarm_button4.config(command=lambda btn=self.Rarm_button4: self.change_state(button=btn,index=2))
        self.Rarm_button4.place(x=x+5,y=y+45)
        self.Larm_button4=tk.Button(root,text="L\narm",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Larm_button4.config(command=lambda btn=self.Larm_button4: self.change_state(button=btn,index=2))
        self.Larm_button4.place(x=x+70,y=y+45)
        self.Rleg_button4=tk.Button(root,text="R\nleg",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Rleg_button4.config(command=lambda btn=self.Rleg_button4: self.change_state(button=btn,index=2))
        self.Rleg_button4.place(x=x+25,y=y+105)
        self.Lleg_button4=tk.Button(root,text="L\nleg",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Lleg_button4.config(command=lambda btn=self.Lleg_button4: self.change_state(button=btn,index=2))
        self.Lleg_button4.place(x=x+50,y=y+105)
        
        x=900
        y=50
        self.head_button5=tk.Button(root,text="head",width=4,height=2,relief=tk.SOLID,bg="orange")
        self.head_button5.config(command=lambda btn=self.head_button5: self.change_3state(button=btn))
        self.head_button5.place(x=x+30,y=y)
        self.body_button5=tk.Button(root,text="body",width=4,height=3,relief=tk.SOLID,bg="orange")
        self.body_button5.config(command=lambda btn=self.body_button5: self.change_3state(button=btn))
        self.body_button5.place(x=x+30,y=y+45)
        self.Rarm_button5=tk.Button(root,text="R\narm",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Rarm_button5.config(command=lambda btn=self.Rarm_button5: self.change_3state(button=btn))
        self.Rarm_button5.place(x=x+5,y=y+45)
        self.Larm_button5=tk.Button(root,text="L\narm",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Larm_button5.config(command=lambda btn=self.Larm_button5: self.change_3state(button=btn))
        self.Larm_button5.place(x=x+70,y=y+45)
        self.Rleg_button5=tk.Button(root,text="R\nleg",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Rleg_button5.config(command=lambda btn=self.Rleg_button5: self.change_3state(button=btn))
        self.Rleg_button5.place(x=x+25,y=y+105)
        self.Lleg_button5=tk.Button(root,text="L\nleg",width=2,height=3,relief=tk.SOLID,bg="orange")
        self.Lleg_button5.config(command=lambda btn=self.Lleg_button5: self.change_3state(button=btn))
        self.Lleg_button5.place(x=x+50,y=y+105)
        
        # 描画のslimかwideかを決める用
        self.iswide=True
        
        self.wide_slimbutton=tk.Button(self.master,text="wide",font=self.font,command=self.change_slim_wide)
        self.wide_slimbutton.place(x=505,y=10)
        
        button=tk.Button(self.master,text="Merge",font=self.boldfont,command=self.merge)
        button.place(x=100,y=762)
        
        label=tk.Label(self.master,text="パーツ境界を表示",font=self.boldfont)
        label.place(x=870,y=330)
        
        self.display_border_button=tk.Button(self.master,text="表示",font=self.font,command=self.change_display_border)
        self.display_border_button.place(x=996,y=328)
        
        self.display_index=0
        
        self.canvas_size=7
        self.canvas = tk.Canvas(root, bg="#c0c0c0", width=64*self.canvas_size, height=64*self.canvas_size)
        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind('<<Drop>>', lambda e:self.input_file(e,index=0))
        self.canvas.place(x=556,y=360)
        self.add_skin_border(self.canvas)
        ###################################################
        self.image=Image.fromarray(np.zeros(shape=(64,64,4),dtype=np.uint8))
        self.canvas.bind("<Button-2>", self.select_pixel)
        self.canvas.bind("<ButtonPress-1>", self.start_selection_add)
        self.canvas.bind("<Button1-Motion>", self.update_selection_add)
        self.canvas.bind("<ButtonRelease-1>", self.finish_selection_add)

        self.canvas.bind("<ButtonPress-2>", self.start_selection_remove)
        self.canvas.bind("<Button2-Motion>", self.update_selection_remove)
        self.canvas.bind("<ButtonRelease-2>", self.finish_selection_remove)
        label=tk.Label(root,text="画像修正用",font=self.boldfont)
        label.place(x=1050,y=10)
        # 選択をリセットするボタン
        self.reset_button=tk.Button(root,text='選択解除',font=self.font,command=self.reset_selection)
        self.reset_button.place(x=1100,y=50)
        # 閾値の設定
        self.Threshold = tk.DoubleVar()
        self.Threshold.set(50)  # 初期値を設定
        # スクロールバーと変数の結び付け
        label=tk.Label(root,text="類似色の閾値",font=self.font)
        label.place(x=1100,y=235)
        self.scale = tk.Scale(root, command=self.set_threshold, orient="horizontal",font=self.font, from_=0, to=250,showvalue=True)
        self.scale.place(x=1100,y=250)
        self.scale.set(50)
        #選択部分を残すモードと選択部分を削除するモード
        self.mode = tk.BooleanVar()
        self.mode.set(True)
        self.label_frame = tk.LabelFrame(root, text='削除モード',font=self.font)
        self.radio_a = tk.Radiobutton(self.label_frame, text='選択部分を残す',font=self.font, command=self.update_mode, value=True, variable=self.mode)
        self.radio_b = tk.Radiobutton(self.label_frame, text='選択部分を消す',font=self.font, command=self.update_mode, value=False, variable=self.mode)
        self.label_frame.place(x=1100,y=100)
        self.radio_a.pack(side="left")
        self.radio_b.pack(side="right")
        #色選択のモード
        self.color_mode = tk.BooleanVar()
        self.color_mode.set(True)
        self.label_frame2 = tk.LabelFrame(root, text='色選択モード',font=self.font)
        self.radio_a2 = tk.Radiobutton(self.label_frame2, text='選択部分のみ',font=self.font, command=self.update_mode, value=True, variable=self.color_mode)
        self.radio_b2 = tk.Radiobutton(self.label_frame2, text='類似色も自動選択',font=self.font, command=self.update_mode, value=False, variable=self.color_mode)
        self.label_frame2.place(x=1100,y=150)
        self.radio_a2.pack(side="left")
        self.radio_b2.pack(side="right")
        # 画像を表示するキャンバス
        self.preview_canvas = tk.Canvas(root, bg="#c0c0c0", width=64*self.canvas_size, height=64*self.canvas_size)
        self.preview_canvas.drop_target_register(DND_FILES)
        self.preview_canvas.dnd_bind('<<Drop>>', lambda e:self.input_file(e,index=0))
        self.preview_canvas.place(x=1026,y=360)
        self.add_skin_border(self.preview_canvas)
        # slim to wide
        self.slim2wide_button=tk.Button(root,text="slim→wide",font=self.font,command=self.slim2wide)
        self.slim2wide_button.place(x=1100,y=200)
        # wide to slim
        self.wide2slim_button=tk.Button(root,text="wide→slim",font=self.font,command=self.wide2slim)
        self.wide2slim_button.place(x=1200,y=200)
        #読み込みリストに追加
        reflect_button=tk.Button(root,text="入力画像を読み込みリストに追加",font=self.font,command=lambda :self.reflect(i=0))
        reflect_button.place(x=1230,y=270)
        reflect_button=tk.Button(root,text="プレビューを読み込みリストに追加",font=self.font,command=lambda :self.reflect(i=1))
        reflect_button.place(x=1230,y=300)
        label=tk.Label(root,text="入力画像",font=self.boldfont)
        label.place(x=730,y=340)
        label=tk.Label(root,text="プレビュー",font=self.boldfont)
        label.place(x=1230,y=340)

        # 矩形選択関連の変数
        self.selection_start = None
        self.selection_rectangle = None
        self.is_selecting = False
        # 選択したピクセルを保持するリスト
        self.selected_pixels = set()
        ####################################################
        self.init_graph()
    def retreive_skin(self):
        text=self.input_text.get(0., tk.END)
        if text.startswith("<ol>"):
            html_code=text.split("\n")
            text=[]
            for html_line in html_code:
                match = re.search(r'<a.*?>(.*?)</a>', html_line)
                if match:
                    text.append(match.group(1))
        else :
            text=text.split("\n")
            text=[a for a in text if a != '']
        text2=""
        for mcid in text:
            value=sr.get_skin_data(mcid)
            if value==None:
                text2+=mcid+"\n"
                self.output_status_bar("MCID:"+mcid+"のスキンは入手できませんでした")
                continue
            img=np.array(value,dtype=float)/255.0
            if img.shape==(32,64,4):
                img=Convert32to64.resize_img(img)
            self.img_list[0].append(img)
            self.add_List(0,mcid+".png")
            self.output_status_bar(mcid+"のスキンを追加しました。")
        self.input_text.delete(0.,tk.END)
        self.input_text.insert(tk.END,text2)
        print(text)
    ###############################################################
    # 画像をリストに反映
    def reflect(self,i):
        if hasattr(self,"fname"):
            if i==0:
                img=np.array(self.image.copy(),dtype=float)/255.0
            elif i==1:
                img=np.array(self.processed_image.copy(),dtype=float)/255.0
            self.img_list[0].append(img)
            self.add_List(0,self.fname)
            self.reset_selection()
            self.highlight_selected_pixels()
            self.output_status_bar("画像をリスト(0)に追加しました。")
    #色の閾値
    def set_threshold(self,value):
        self.Threshold.set(self.scale.get())
        self.highlight_selected_pixels()
        self.add_skin_border(self.canvas)
        self.add_skin_border(self.preview_canvas)
    # モード切替１
    def update_mode(self):
        self.highlight_selected_pixels()
    # 範囲選択の削除
    def reset_selection(self):
        self.selected_pixels = set()
        self.highlight_selected_pixels()
    #範囲に追加
    def add_pixel(self,i,j):
        try:
            _, _, _, alpha = self.image.getpixel((i,j))
        except IndexError:
            return
        if alpha==0:
            return
        if (i, j) not in self.selected_pixels:
            self.selected_pixels.add((i, j))
    #範囲から削除
    def remove_pixel(self,i,j):
        try:
            r, g, b, alpha = self.image.getpixel((i,j))
        except IndexError:
            return
        if alpha==0:
            return
        if (i, j) in self.selected_pixels:
            self.selected_pixels.remove((i, j))
    def update_pixel(self,i,j):
        _, _, _, alpha = self.image.split()
        if alpha.getpixel((i,j))==0:
            return
        if (i, j) in self.selected_pixels:
            self.selected_pixels.remove((i, j))
        else:
            self.selected_pixels.add((i, j))
    def start_selection_add(self, event):
        if not self.is_selecting:
            self.selection_start = (event.x, event.y)
            self.is_selecting = True
    def update_selection_add(self, event):
        if self.is_selecting:
            if self.selection_rectangle:
                self.canvas.delete(self.selection_rectangle)
            x, y = self.selection_start
            self.selection_rectangle = self.canvas.create_rectangle(x, y, event.x, event.y, outline="red")

    def finish_selection_add(self, event):
        if self.is_selecting:
            if self.selection_rectangle:
                self.canvas.delete(self.selection_rectangle)
                x1, y1 = self.selection_start
                x2, y2 = event.x, event.y
                i1,i2=int(x1/self.canvas_size),int(x2/self.canvas_size)
                j1,j2=int(y1/self.canvas_size),int(y2/self.canvas_size)
                for i in range(min(i1, i2), max(i1, i2)+1):
                    for j in range(min(j1,j2), max(j1, j2)+1):
                        self.add_pixel(i,j)
                self.highlight_selected_pixels()
                self.is_selecting = False
    def start_selection_remove(self, event):
        if not self.is_selecting:
            self.selection_start = (event.x, event.y)
            self.is_selecting = True
    def update_selection_remove(self, event):
        if self.is_selecting:
            if self.selection_rectangle:
                self.canvas.delete(self.selection_rectangle)
            x, y = self.selection_start
            self.selection_rectangle = self.canvas.create_rectangle(x, y, event.x, event.y, outline="blue")

    def finish_selection_remove(self, event):
        if self.is_selecting:
            if self.selection_rectangle:
                self.canvas.delete(self.selection_rectangle)
                x1, y1 = self.selection_start
                x2, y2 = event.x, event.y
                i1,i2=int(x1/self.canvas_size),int(x2/self.canvas_size)
                j1,j2=int(y1/self.canvas_size),int(y2/self.canvas_size)
                for i in range(min(i1, i2), max(i1, i2)+1 ):
                    for j in range(min(j1,j2), max(j1, j2)+1):
                        self.remove_pixel(i,j)
                self.highlight_selected_pixels()
                self.is_selecting = False

    def select_pixel(self, event):
        if not self.is_selecting:
            x, y = event.x, event.y
            i, j = int(x/self.canvas_size), int(y/self.canvas_size)
            self.update_pixel(i,j)
            self.highlight_selected_pixels()
    # 入力画像の更新
    def highlight_selected_pixels(self):
        if not hasattr(self,"image"):
            return
        highlighted_image = Image.fromarray(self.erase_parts(self.display_index,np.array(self.image.copy()))).resize((64*self.canvas_size, 64*self.canvas_size),Image.NEAREST)
        draw = ImageDraw.Draw(highlighted_image)
        
        for x, y in self.selected_pixels:
            draw.rectangle((x*self.canvas_size, y*self.canvas_size, (x+1)*self.canvas_size, (y+1)*self.canvas_size), outline="red")
        self.photo = ImageTk.PhotoImage(highlighted_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.update_preview()
        self.add_skin_border(self.canvas)
        self.add_skin_border(self.preview_canvas)
    # プレビューの更新
    def update_preview(self):
        image=self.process()
        resized_image = image.resize((64*self.canvas_size, 64*self.canvas_size),Image.NEAREST)
        self.preview_photo = ImageTk.PhotoImage(resized_image)
        self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.preview_photo)
    # slimからwideに
    def slim2wide(self):
        if not hasattr(self,"image"):
            return
        img=np.array(self.image.copy(),dtype=float)/255.0
        img=SlimWideConverter.slim2wide(img)
        self.image=Image.fromarray(np.array(img*255,dtype=np.uint8))
        self.reset_selection()
        self.highlight_selected_pixels()
        self.add_skin_border(self.canvas)
        self.add_skin_border(self.preview_canvas)
    # wideからslimに
    def wide2slim(self):
        if not hasattr(self,"image"):
            return
        img=np.array(self.image.copy(),dtype=float)/255.0
        img=SlimWideConverter.wide2slim(img)
        self.image=Image.fromarray(np.array(img*255,dtype=np.uint8))
        self.reset_selection()
        self.highlight_selected_pixels()
        self.add_skin_border(self.canvas)
        self.add_skin_border(self.preview_canvas)
    # previewの更新用
    def process(self):
        processed_image = self.image.copy()
        processed_image = Image.fromarray(self.erase_parts(self.display_index,np.array(processed_image)))
        if self.color_mode.get()==True:
            pixels_to_remove = set(self.selected_pixels)
            for x in range(processed_image.width):
                for y in range(processed_image.height):
                    if self.mode.get()==True:
                        if (x, y) not in pixels_to_remove:
                            processed_image.putpixel((x, y), (0,0,0,0))  # 削除するピクセルを白色で塗りつぶす
                    else :
                        if (x, y) in pixels_to_remove:
                            processed_image.putpixel((x, y), (0,0,0,0))  # 削除するピクセルを白色で塗りつぶす
                        
        else :
            remove_list=set([self.image.getpixel((x[0],x[1])) for x in self.selected_pixels])
            for x in range(processed_image.width):
                for y in range(processed_image.height):
                    distance=255.0
                    r2,g2,b2,a2=processed_image.getpixel((x,y))
                    for pixel in remove_list:
                        r,g,b,a=pixel
                        if a==0:
                            continue
                        distance=min(distance,np.sqrt((r-r2)*(r-r2)+(g-g2)*(g-g2)+(b-b2)*(b-b2)))
                    if self.mode.get()==True:
                        if distance>self.Threshold.get():
                            processed_image.putpixel((x, y), (0, 0, 0,0))  
                    else:
                        if distance<=self.Threshold.get():
                            processed_image.putpixel((x, y), (0, 0, 0,0))  
        self.processed_image=processed_image
        return processed_image
    ###############################################
    # listbox内のコンテンツの移動
    def move_list_contents(self,id1,id2):
        if len(self.img_list[id1])==0:
            self.output_status_bar("ファイルが選択されていません")
            return 
        indices = self.listbox[id1].curselection()
        if(len(indices)==0):
            self.output_status_bar("ファイルが選択されていません")
            return
        #逆順にすることで番号がずれるのを防ぐ
        first=len(self.img_list[id2])
        for i in reversed(indices):
            img=self.img_list[id1][i].copy()
            name=self.listbox[id1].get(i)
            self.img_list[id1].pop(i)
            self.listbox[id1].delete(i)
            self.img_list[id2].append(img)
            self.add_List(id2,name)
        if first>0:
            self.listbox[id2].selection_clear(0, first-1)
        self.listbox[id2].select_set(first, tk.END)
                
    def change_display_border(self):
        if self.display_border_button["text"]=="表示":
            self.display_border_button.config(text="非表示")
            self.canvas.delete("rectangle")
            self.preview_canvas.delete("rectangle")
        else:
            self.display_border_button.config(text="表示")
            self.add_skin_border(self.canvas)
            self.add_skin_border(self.preview_canvas)
    def change_state(self,button,index):
        if button["relief"]=="solid":
            button.config(relief=tk.FLAT)
            button.config(bg="white")
        else :
            button.config(relief=tk.SOLID)
            button.config(bg="orange")
        self.plot_graph(index)
    def change_3state(self,button):
        if button["relief"]=="solid":
            button.config(relief=tk.RIDGE)
            button.config(bg="#f0e68c")
        elif button["relief"]=="ridge":
            button.config(relief=tk.FLAT)
            button.config(bg="white")
        else :
            button.config(relief=tk.SOLID)
            button.config(bg="orange")
        self.plot_graph(self.display_index,flag=True)
    def select_all(self,index):
        self.listbox[index].select_set(0, tk.END)  # 0から最後までの要素を選択
    def change_slim_wide(self):
        if self.wide_slimbutton["text"]=="wide":
            self.wide_slimbutton.config(text="slim")
            self.iswide=False
        else:
            self.wide_slimbutton.config(text="wide")
            self.iswide=True
        self.plot_graph(self.display_index)
    def init_graph(self):
        # matplotlib配置用フレーム
        frame = tk.Frame(self.master,relief=tk.SOLID)
        frame.drop_target_register(DND_FILES)
        frame.dnd_bind('<<Drop>>', lambda e:self.input_file(e,index=0))
        #描画用フレームをウィンドウに配置(右)
        frame.place(x=556,y=10,width=284,height=320)
        if hasattr(self,"ax"):
            self.azim = self.ax.azim  # 現在の方位角を取得
            self.elev = self.ax.elev  # 現在の仰角を取得
            self.ax.clear()
        if not hasattr(self,"fig"):
            self.fig = plt.figure(figsize=(10,10))
            self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_position([0, 0, 1, 1])
        self.ax.set_box_aspect((1,1,2))
        if hasattr(self,"azim") and hasattr(self,"elev"):
            self.ax.view_init(azim=self.azim, elev=self.elev)
        self.ax.axis("off")
        
        self.fig_canvas = FigureCanvasTkAgg(self.fig, frame)
        # matplotlibのツールバーを作成
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, frame)
        # matplotlibのグラフをフレームに配置
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True,padx=0,pady=0)
        
        #frame.pack(fill='y',side=tk.RIGHT,anchor=tk.S)
        
    def add_skin_border(self,canvas):
        if not self.display_border_button["text"]=="表示":
            return
        canvas.delete("rectangle")
        self.add_skin_parts_border(canvas,0,0,8,8,8,'#7fff00')
        self.add_skin_parts_border(canvas,32,0,8,8,8,'#006400')
        
        self.add_skin_parts_border(canvas,0,16,4,4,12,'#ff0000')
        self.add_skin_parts_border(canvas,16,16,4,8,12,'#0000ff')
        self.add_skin_parts_border(canvas,40,16,4,3,12,'#ffdead')
        self.add_skin_parts_border(canvas,40,16,4,4,12,'#000000')
        
        self.add_skin_parts_border(canvas,0,32,4,4,12,'#228b22')
        self.add_skin_parts_border(canvas,16,32,4,8,12,'#191970')
        self.add_skin_parts_border(canvas,40,32,4,3,12,'#ffdead')
        self.add_skin_parts_border(canvas,40,32,4,4,12,'#8a2be2')
        
        self.add_skin_parts_border(canvas,0,48,4,4,12,'#228b22')
        self.add_skin_parts_border(canvas,16,48,4,4,12,'#ff0000')
        self.add_skin_parts_border(canvas,32,48,4,3,12,'#ffdead')
        self.add_skin_parts_border(canvas,32,48,4,4,12,'#000000')
        self.add_skin_parts_border(canvas,48,48,4,3,12,'#ffdead')
        self.add_skin_parts_border(canvas,48,48,4,4,12,'#8a2be2')
    def add_skin_parts_border(self,canvas,x,y,xsize,ysize,zsize,color):
        size=self.canvas_size
        canvas.create_rectangle((x+xsize)*size, y*size+1, (x+xsize+ysize)*size, (y+xsize)*size, outline= color,tags="rectangle")
        canvas.create_rectangle((x+xsize+ysize)*size, y*size+1, (x+xsize+2*ysize)*size, (y+xsize)*size, outline=  color,tags="rectangle")
        canvas.create_rectangle(x*size+1, (y+xsize)*size, (x+xsize)*size, (y+xsize+zsize)*size, outline=  color,tags="rectangle")  
        canvas.create_rectangle((x+xsize)*size, (y+xsize)*size, (x+xsize+ysize)*size, (y+xsize+zsize)*size, outline=  color,tags="rectangle")  
        canvas.create_rectangle((x+xsize+ysize)*size, (y+xsize)*size, (x+2*xsize+ysize)*size, (y+xsize+zsize)*size, outline=  color,tags="rectangle")  
        canvas.create_rectangle((x+2*xsize+ysize)*size, (y+xsize)*size, (x+2*xsize+2*ysize)*size, (y+xsize+zsize)*size, outline=  color,tags="rectangle")  
        
    def delete_window(self):#ウインドウを閉じる処理
        ret = tk.messagebox.askyesno(
            title = "終了確認",
            message = "プログラムを終了しますか？")

        if ret == True:
            # 「はい」がクリックされたとき
            plt.clf()
            plt.close()
            
            self.master.destroy()
            exit()
    def dndstrtoary(self, drop_str):
        i = 0
        files = []
        while i < len(drop_str):
            if drop_str[i] == '{':
                fd = drop_str.find('}', i)
                filname = drop_str[i+1:fd]
                i = fd + 1

                files.append(filname)
                if len(drop_str) <= i:
                    break

                if drop_str[i] == ' ':
                    i += 1
            else:
                fd = drop_str.find(' ', i)
                if fd < 0:
                    filname = drop_str[i:]
                    i = len(drop_str)
                else:
                    filname = drop_str[i:fd]
                    i = fd + 1
                files.append(filname)
        return files
    def input_file(self,e,index):
        self.input_file_path(index,self.dndstrtoary(e.data))
            
    def open_file(self,index):
        ''' ファイルを開く'''
        # ファイルを開くダイアログ
        filenames = filedialog.askopenfilenames(initialdir = os.getcwd())
        self.input_file_path(index,filenames=filenames)
    def input_file_path(self,index,filenames):
        id=len(self.img_list[index])
        for filename in filenames:
            if not filename.endswith('.png'):
                continue
            basename = os.path.basename(filename)
            print("入力ファイル:"+filename)
            if os.path.exists(filename):
                img = image.imread(filename)#matplotlib
                if img.shape==(32,64,4):
                    img=Convert32to64.resize_img(img)
                if img.shape!=(64,64,4):
                    print("invalid file:ファイルは64x64のpngを選択してください")
                    self.output_status_bar("invalid file:ファイルは32x64または64x64のpngを選択してください")
                    continue
                self.img_list[index].append(img)
                self.add_List(index,basename)
                self.output_status_bar("ファイル"+basename+"がリストに追加されました")
                continue
            else:
                print("入力ファイルが読み込めませんでした\n")
                self.output_status_bar("入力ファイルが読み込めませんでした")
        if len(self.img_list[index])!=0:
            if id>1:
                self.listbox[index].selection_clear(0,id)
            self.listbox[index].select_set(id,tk.END)
    def open_dir(self,index):
        ''' ディレクトリを選択し、その中のPNGファイルを読み込む '''
        directory = filedialog.askdirectory(initialdir=os.getcwd())
        if not directory:
            return  # キャンセルされた場合
        id=len(self.img_list[index])
        # ディレクトリ内のPNGファイルを読み込む
        n=0
        for filename in os.listdir(directory):
            if filename.endswith('.png'):
                file_path = directory+"/"+filename
                if os.path.exists(file_path):
                    img = image.imread(file_path)
                    if img.shape==(32,64,4):
                        img=Convert32to64.resize_img(img)
                    if img.shape == (64, 64, 4):
                        self.img_list[index].append(img)
                        self.add_List(index,filename)
                        n+=1
        if len(self.img_list[index])!=0:
            if id>1:
                self.listbox[index].selection_clear(0,id)
            self.listbox[index].select_set(id,tk.END)
        self.output_status_bar(f"{n}個のファイルがリストに追加されました")
    #リストボックスに追加
    def add_List(self,index,text):
        # テキストが既に存在するか確認
        if len(self.img_list[index])>0:
            existing_texts = self.listbox[index].get(0, tk.END)
            if text in existing_texts:
                suffix = 2
                text=text.replace(".png","")
                while f"{text}{suffix}.png" in existing_texts:
                    suffix += 1
                text = f"{text}{suffix}.png"
        self.listbox[index].insert(tk.END, text)
        if self.listbox[index].size()==1:
            self.plot_graph(index)
    # ボタンが押されたらリストボックスの選択されている部分を削除
    def deleteSelectedList(self,index):    
        if len(self.img_list[index])==0:
            return 
        else :
            indices = self.listbox[index].curselection()
            if(len(indices)==0):
                return
            #逆順にすることで番号がずれるのを防ぐ
            for i in reversed(indices):
                self.img_list[index].pop(i)
                self.listbox[index].delete(i)
    #ファイルの保存
    def save_fig(self,index):
        #選択項目を取得
        indices = self.listbox[index].curselection()
        if len(indices)==0:
            print("ファイルが選択されていません")
            self.output_status_bar("ファイルが選択されていません")
            return
        elif len(indices)==1:
            img2=self.img_list[index][indices[0]]
            filename = tk.filedialog.asksaveasfilename( initialfile=self.listbox[index].get(indices[0]),defaultextension=".png",filetypes = [("PNG", ".png")])
            if ".png" not in filename:
                filename+=".png"
            if(filename == ".png"):
                return 
            print("保存ファイル名:"+filename)
            img2=self.erase_parts(index,img2)
            image.imsave(filename,img2)
            self.output_status_bar(filename +"として保存されました。")
        elif len(indices)>1:
            directory = filedialog.askdirectory()
            if not directory:
                return
            confirm = messagebox.askyesno("確認", "選択したフォルダ内に同名のファイルがあると上書きされます。")
            if not confirm:
                self.output_status_bar("保存はキャンセルされました。")
                return # 上書きしない場合はスキップ
            for i in indices:
                image.imsave(directory+"/"+self.listbox[index].get(i),self.erase_parts(index,self.img_list[index][i]))
    #ステータスバーを作成
    def create_status_bar(self):
        '''ステータスバー'''
        self.frame_status_bar = tk.Frame(self.master, borderwidth = 2, relief = tk.SUNKEN)
        self.label1 = tk.Label(self.frame_status_bar, text = "ファイルを選択してください")
        self.label1.pack(side = tk.LEFT)
        self.frame_status_bar.pack(side = tk.BOTTOM, fill = tk.X)
    def output_status_bar(self,text):
        self.label1.pack_forget()
        self.label1 = tk.Label(self.frame_status_bar, text = text)
        self.label1.pack(side = tk.LEFT)
        self.frame_status_bar.pack(side = tk.BOTTOM, fill = tk.X)
    def extract_selection(self,index):
        if len(self.img_list[index])==0:
            self.output_status_bar("ファイルが読み込まれていません")
            return []
        indices = self.listbox[index].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return []
        return indices
    def operation(self,index,func):
        indices = self.extract_selection(index)
        for i in indices: 
            img=self.img_list[index][i]
            self.img_list[index][i]=func(img)
        self.plot_graph(index)
    #前後
    def backwards(self,index):
        self.operation(index,bf.backwards)
    #左右
    def flip(self,index):
        self.operation(index,lf.flip)
    #上下
    def upsidedown(self,index):
        self.operation(index,uf.upsidedown)
    #回転
    def up(self):
        self.operation(0,fr.head_rotate_horizontal)
    def down(self):
        indices = self.extract_selection(0)
        for i in indices: 
            img=self.img_list[0][i]
            img=fr.head_rotate_horizontal(img)
            img=fr.head_rotate_horizontal(img)
            self.img_list[0][i]=fr.head_rotate_horizontal(img)
        self.plot_graph(0)
    def right(self):
        self.operation(0,fr.head_rotate_vertical)
    def left(self):
        indices = self.extract_selection(0)
        for i in indices: 
            img=self.img_list[0][i]
            img=fr.head_rotate_vertical(img)
            img=fr.head_rotate_vertical(img)
            self.img_list[0][i]=fr.head_rotate_vertical(img)
        self.plot_graph(0)
    def rotate_clock(self):
        self.operation(0,fr.head_rotate)
    def rotate_counter_clock(self):
        indices = self.extract_selection(0)
        for i in indices: 
            img=self.img_list[0][i]
            img=fr.head_rotate(img)
            img=fr.head_rotate(img)
            self.img_list[0][i]=fr.head_rotate(img)
        self.plot_graph(0)
    def compress(self):#圧縮
        self.operation(0,lift.compress_list)
    def toslim(self):
        indices = self.extract_selection(0)
        for i in indices: 
            img=self.img_list[0][i]
            if not lf.judge_slim_classic(img):
                self.img_list[0][i]=SlimWideConverter.wide2slim(img)
        self.plot_graph(0)
    def towide(self):
        indices = self.extract_selection(0)
        for i in indices: 
            img=self.img_list[0][i]
            if lf.judge_slim_classic(img):
                self.img_list[0][i]=SlimWideConverter.slim2wide(img)
        self.plot_graph(0)
    def toInnerLayer(self):
        indices = self.extract_selection(0)
        for i in indices: 
            img=self.img_list[0][i]
            self.img_list[0][i]=bl.bring_one_layer(img,0)
        self.plot_graph(0)
    def toOuterLayer(self):
        indices = self.extract_selection(0)
        for i in indices: 
            img=self.img_list[0][i]
            self.img_list[0][i]=bl.bring_one_layer(img,1)
        self.plot_graph(0)
    def toStamp(self):
        self.operation(0,lift.compress_list_upper)
    def toGray(self):
        self.operation(0,gray.toGray)
    def duplicate(self):
        indices = self.extract_selection(0)
        for i in indices: 
            img=copy.deepcopy(self.img_list[0][i])
            filename=self.listbox[0].get(i)
            self.img_list[0].append(img)
            self.add_List(0,filename)
    def replace_parts(self,func):
        if len(self.img_list[0])==0:
            self.output_status_bar("ファイルが選択されていません")
            return 
        indices = self.listbox[0].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        ###
        filenames = tk.filedialog.askopenfilenames(initialdir = os.getcwd())
        for filename in filenames:
            basename=os.path.basename(filename)
            print("入力ファイル:"+filename)
            if os.path.exists(filename):
                img2 = image.imread(filename)
                if img2.shape==(32,64,4):
                        img2=Convert32to64.resize_img(img2)
                if img2.shape!=(64,64,4):
                    print("invalid file:ファイルは32x64または64x64のpngを選択してください")
                    self.output_status_bar("invalid file:ファイルは32x64または64x64のpngを選択してください")
                    return
                for i in indices: 
                    img=self.img_list[0][i]
                    img3=func(copy.deepcopy(img),img2)
                    self.img_list[0].append(img3)
                    name1=self.listbox[0].get(i).replace(".png","")+"-"+basename+".png"
                    self.add_List(0,name1)
                self.plot_graph(0)
            else:
                print("入力ファイルが読み込めませんでした\n")
                self.output_status_bar("入力ファイルが読み込めませんでした")
    def replace(self):#headの置き換え
        self.replace_parts(lift.replace_head)
    def replace_leg(self):#headの置き換え
        self.replace_parts(lift.replace_leg)
    def merge(self):
        if len(self.img_list[1])==0:
            self.output_status_bar("優先1リストにファイルがありません")
            return 
        if len(self.img_list[2])==0:
            self.output_status_bar("優先2リストにファイルがありません")
            return 
        first=len(self.img_list[3])
        for i in range(len(self.img_list[1])):
            for j in range(len(self.img_list[2])):
                fname1=self.listbox[1].get(i).replace(".png","")
                fname2=self.listbox[2].get(j).replace(".png","")
                new_fname=fname1+"-"+fname2+".png"
                img1=self.img_list[1][i]
                img2=self.img_list[2][j]
                img1=self.erase_parts(1,img1)
                new_img=self.erase_parts(2,img2).copy()
                for x in range(64):
                    for y in range(64):
                        if img1[x][y][3]!=0:
                            new_img[x][y]=img1[x][y]
                self.img_list[3].append(new_img)
                self.add_List(3,new_fname)
        if first>0:
            self.listbox[3].selection_clear(0, first-1)
        self.listbox[3].select_set(first, tk.END)
                
    def erase_parts(self,index,img):
        array1=img.copy()
        if index==1:
            array1=np.transpose(array1,axes=(1, 0, 2))
            if self.head_button["relief"]=="flat":
                array1[0:32,0:16,:]=0
            if self.head_button2["relief"]=="flat":
                array1[32:64,0:16,:]=0
            if self.body_button["relief"]=="flat":
                array1[16:40,16:32,:]=0
            if self.body_button2["relief"]=="flat":
                array1[16:40,32:48,:]=0
            if self.Rarm_button["relief"]=="flat":
                array1[40:56,16:32,:]=0
            if self.Rarm_button2["relief"]=="flat":
                array1[40:56,32:48,:]=0
                
            if self.Rleg_button2["relief"]=="flat":
                array1[0:16,32:48,:]=0
            if self.Rleg_button["relief"]=="flat":
                array1[0:16,16:32,:]=0
            if self.Lleg_button2["relief"]=="flat":
                array1[0:16,48:64,:]=0
            if self.Lleg_button["relief"]=="flat":
                array1[16:32,48:64,:]=0
            if self.Larm_button2["relief"]=="flat":
                array1[48:64,48:64,:]=0
            if self.Larm_button["relief"]=="flat":
                array1[32:48,48:64,:]=0
            array1=np.transpose(array1,axes=(1, 0, 2))
        elif index==2:
            array1=np.transpose(array1,axes=(1, 0, 2))
            if self.head_button3["relief"]=="flat":
                array1[0:32,0:16,:]=0
            if self.head_button4["relief"]=="flat":
                array1[32:64,0:16,:]=0
            if self.body_button3["relief"]=="flat":
                array1[16:40,16:32,:]=0
            if self.body_button4["relief"]=="flat":
                array1[16:40,32:48,:]=0
            if self.Rarm_button3["relief"]=="flat":
                array1[40:56,16:32,:]=0
            if self.Rarm_button4["relief"]=="flat":
                array1[40:56,32:48,:]=0
                
            if self.Rleg_button4["relief"]=="flat":
                array1[0:16,32:48,:]=0
            if self.Rleg_button3["relief"]=="flat":
                array1[0:16,16:32,:]=0
            if self.Lleg_button4["relief"]=="flat":
                array1[0:16,48:64,:]=0
            if self.Lleg_button3["relief"]=="flat":
                array1[16:32,48:64,:]=0
            if self.Larm_button4["relief"]=="flat":
                array1[48:64,48:64,:]=0
            if self.Larm_button3["relief"]=="flat":
                array1[32:48,48:64,:]=0
            array1=np.transpose(array1,axes=(1, 0, 2))
            
        array1=np.transpose(array1,axes=(1, 0, 2))
        if self.head_button5["relief"]=="ridge":
            array1[32:64,0:16,:]=0
        elif self.head_button5["relief"]=="flat":
            array1[:64,0:16,:]=0
        if self.body_button5["relief"]=="ridge":
            array1[16:40,32:48,:]=0
        elif self.body_button5["relief"]=="flat":
            array1[16:40,16:48,:]=0
        if self.Rarm_button5["relief"]=="ridge":
            array1[40:56,32:48,:]=0
        elif self.Rarm_button5["relief"]=="flat":
            array1[40:56,16:48,:]=0
        if self.Rleg_button5["relief"]=="ridge":
            array1[0:16,32:48,:]=0
        elif self.Rleg_button5["relief"]=="flat":
            array1[0:16,16:48,:]=0
        if self.Lleg_button5["relief"]=="ridge":
            array1[0:16,48:64,:]=0
        elif self.Lleg_button5["relief"]=="flat":
            array1[0:32,48:64,:]=0
        if self.Larm_button5["relief"]=="ridge":
            array1[48:64,48:64,:]=0
        elif self.Larm_button5["relief"]=="flat":
            array1[32:64,48:64,:]=0
        
        array1=np.transpose(array1,axes=(1, 0, 2))
        return array1
    
    #余白の削除
    def erase_margin(self):
        if len(self.img_list[0])==0:
            self.output_status_bar("ファイルが選択されていません")
            return 
        indices = self.listbox[0].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        for i in indices: 
            img=self.img_list[0][i]
            self.img_list[0][i]=self.erase_mergin_img(img)
        self.plot_graph(0)
    def erase_mergin_img(self,img):
        array1=img.copy()
        array1[:8,:8,:]=0
        array1[:8,24:40,:]=0
        array1[:8,56:,:]=0
        array1[16:20,:4,:]=0
        array1[16:20,12:20,:]=0
        array1[16:20,36:44,:]=0
        array1[16:20,52:56,:]=0
        array1[32:36,:4,:]=0
        array1[32:36,12:20,:]=0
        array1[32:36,36:44,:]=0
        array1[32:36,52:56,:]=0
        array1[16:48,56:,:]=0
        array1[48:52,:4,:]=0
        array1[48:52,12:20,:]=0
        array1[48:52,28:36,:]=0
        array1[48:52,44:52,:]=0
        array1[48:52,60:,:]=0
        return array1
        
    def plot_graph(self,index,flag=False):
        if not flag:
            if len(self.img_list[index])==0 :
                img=np.zeros((64,64,4),dtype=np.uint8)
                self.output_status_bar("ファイルが選択されていません")
                return 
            elif len(self.img_list[index])==1:
                img=self.img_list[index][0]
                self.fname=self.listbox[index].get(0)
            else :
                indices = self.listbox[index].curselection()
                if len(indices)==0:
                    self.output_status_bar("ファイルが選択されていません")
                    return
                img=self.img_list[index][indices[0]]
                self.fname=self.listbox[index].get(indices[0])
            plt.clf()
            self.image=Image.fromarray((img * 255).astype('uint8'))
            
            img=self.erase_parts(index,img)
            self.display_index=index
        else :
            img=self.erase_parts(index,np.array(self.image,dtype=float)/255.0)
        self.init_graph()
        # グラフの描画
        sv.main(self.ax,img,self.iswide)
        
        # 表示
        self.fig_canvas.draw()
        img=Image.fromarray((img * 255).astype('uint8')).resize((64*self.canvas_size, 64*self.canvas_size),Image.NEAREST)
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.preview_canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.highlight_selected_pixels()
        self.add_skin_border(self.canvas)
        self.add_skin_border(self.preview_canvas)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = Application(master=root)
    app.mainloop()