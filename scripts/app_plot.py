import tkinter as tk
from tkinter import filedialog,messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import matplotlib.image as image
import matplotlib.pyplot as plt
import skin_view as sv
import os
from tkinter import font
import backward_flip_reform as bf
import lj_flip as lf
import upsidedown_flip as uf
import face_rotate as fr
import lift
import Convert32to64
import SlimWideConverter
from PIL import Image, ImageTk, ImageDraw

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.img_list=[[],[],[],[]]
        self.master = master
        self.master.geometry("1000x900") 
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
        button.place(x=x+190,y=y+32)
        button.config(command=lambda id=0: self.plot_graph(index=id))
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
        label = tk.Label(self.master, text='スキンを反転',font=self.boldfont)
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
        label = tk.Label(self.master, text='headを回転',font=self.boldfont)
        
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
        button = tk.Button(self.master, text='持ち上げスキンに変更',font=self.font,command=self.compress)
        button.place(x=10,y=100) 
        button = tk.Button(self.master, text='頭を別スキンで置き換え',font=self.font,command=self.replace)
        button.place(x=10,y=70) 
        button = tk.Button(self.master, text='slimスキンに統一',font=self.font,command=self.toslim)
        button.place(x=10,y=130) 
        button = tk.Button(self.master, text='wideスキンに統一',font=self.font,command=self.towide)
        button.place(x=170,y=130) 
        button = tk.Button(self.master, text='スキンの余白を削除',font=self.font,command=self.erase_margin)
        button.place(x=10,y=160) 
        
        x=30
        y=270
        label=tk.Label(root,text="Skin Merge",font=self.boldfont)
        label.place(x=x-20,y=y-60)
        label=tk.Label(root,text="優先1",font=self.boldfont)
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
        y=470
        label=tk.Label(root,text="優先2",font=self.boldfont)
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
        
        # 描画のslimかwideかを決める用
        self.iswide=True
        
        self.wide_slimbutton=tk.Button(self.master,text="wide",font=self.font,command=self.change_slim_wide)
        self.wide_slimbutton.place(x=505,y=10)
        
        button=tk.Button(self.master,text="Merge",font=self.boldfont,command=self.merge)
        button.place(x=100,y=652)
        
        label=tk.Label(self.master,text="パーツ境界を表示",font=self.boldfont)
        label.place(x=770,y=410)
        
        self.display_border_button=tk.Button(self.master,text="表示",font=self.font,command=self.change_display_border)
        self.display_border_button.place(x=896,y=408)
        
        self.display_index=0

        self.init_graph()
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
        else:
            self.display_border_button.config(text="表示")
            self.add_skin_border(self.canvas)
    def change_state(self,button,index):
        if button["relief"]=="solid":
            button.config(relief=tk.FLAT)
            button.config(bg="white")
        else :
            button.config(relief=tk.SOLID)
            button.config(bg="orange")
        self.plot_graph(index)
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
        if hasattr(self,"ax"):
            self.ax.clear()
        if not hasattr(self,"fig"):
            self.fig = plt.figure(figsize=(5,20))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.axis("off")
        self.ax.set_box_aspect((1,1,2))
        self.fig_canvas = FigureCanvasTkAgg(self.fig, frame)
        # matplotlibのツールバーを作成
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, frame)
        # matplotlibのグラフをフレームに配置
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        #描画用フレームをウィンドウに配置(右下)
        frame.place(x=556,y=10,width=384,height=400)
        #frame.pack(fill='y',side=tk.RIGHT,anchor=tk.S)
        
        self.canvas_size=6
        self.canvas = tk.Canvas(root, bg="#c0c0c0", width=64*self.canvas_size, height=64*self.canvas_size)
        self.canvas.place(x=556,y=430)
        self.add_skin_border(self.canvas)
        
    def add_skin_border(self,canvas):
        if not self.display_border_button["text"]=="表示":
            return
        size=self.canvas_size
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
            plt.close()
            self.master.destroy()
            exit()
    def open_file(self,index):
        ''' ファイルを開く'''
        # ファイルを開くダイアログ
        filenames = filedialog.askopenfilenames(initialdir = os.getcwd())
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
                    print("invalid file:ファイルは64x64のpngを選択してください\n")
                    self.output_status_bar("invalid file:ファイルは32x64または64x64のpngを選択してください\n")
                    continue
                self.img_list[index].append(img)
                self.add_List(index,basename)
                self.output_status_bar("ファイル"+basename+"がリストに追加されました")
                continue
            else:
                print("入力ファイルが読み込めませんでした\n")
                self.output_status_bar("入力ファイルが読み込めませんでした")
    def open_dir(self,index):
        ''' ディレクトリを選択し、その中のPNGファイルを読み込む '''
        directory = filedialog.askdirectory(initialdir=os.getcwd())
        if not directory:
            return  # キャンセルされた場合

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
                image.imsave(directory+"/"+self.listbox[index].get(i),img=self.erase_parts(index,self.img_list[index][i]))
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
    #前後
    def backwards(self,index):
        if len(self.img_list[index])==0:
            self.output_status_bar("ファイルが読み込まれていません")
            return 
        indices = self.listbox[index].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        for i in indices: 
            img=self.img_list[index][i]
            self.img_list[index][i]=bf.backwards(img)
        self.plot_graph(index)
    #左右
    def flip(self,index):
        if len(self.img_list[index])==0:
            self.output_status_bar("ファイルが読み込まれていません")
            return 
        indices = self.listbox[index].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        for i in indices: 
            img=self.img_list[index][i]
            self.img_list[index][i]=lf.flip(img)
        self.plot_graph(index)
    def upsidedown(self,index):
        if len(self.img_list[index])==0:
            self.output_status_bar("ファイルが読み込まれていません")
            return 
        indices = self.listbox[index].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        for i in indices: 
            img=self.img_list[index][i]
            self.img_list[index][i]=uf.upsidedown(img)
        self.plot_graph(index)
    def up(self):
        if len(self.img_list[0])==0:
            self.output_status_bar("ファイルが読み込まれていません")
            return 
        indices = self.listbox[0].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        for i in indices: 
            img=self.img_list[0][i]
            self.img_list[0][i]=fr.head_rotate_horizontal(img)
        self.plot_graph(0)
    def down(self):
        if len(self.img_list[0])==0:
            self.output_status_bar("ファイルが読み込まれていません")
            return 
        indices = self.listbox[0].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        for i in indices: 
            img=self.img_list[0][i]
            img=fr.head_rotate_horizontal(img)
            img=fr.head_rotate_horizontal(img)
            self.img_list[0][i]=fr.head_rotate_horizontal(img)
        self.plot_graph(0)
    def right(self):
        if len(self.img_list[0])==0:
            self.output_status_bar("ファイルが読み込まれていません")
            return 
        indices = self.listbox[0].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        for i in indices: 
            img=self.img_list[0][i]
            self.img_list[0][i]=fr.head_rotate_vertical(img)
        self.plot_graph(0)
    def left(self):
        if len(self.img_list[0])==0:
            self.output_status_bar("ファイルが読み込まれていません")
            return 
        indices = self.listbox[0].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        for i in indices: 
            img=self.img_list[0][i]
            img=fr.head_rotate_vertical(img)
            img=fr.head_rotate_vertical(img)
            self.img_list[0][i]=fr.head_rotate_vertical(img)
        self.plot_graph(0)
    def rotate_clock(self):
        if len(self.img_list[0])==0:
            self.output_status_bar("ファイルが選択されていません")
            return 
        indices = self.listbox[0].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        for i in indices: 
            img=self.img_list[0][i]
            self.img_list[0][i]=fr.head_rotate(img)
        self.plot_graph(0)
    def rotate_counter_clock(self):
        if len(self.img_list[0])==0:
            self.output_status_bar("ファイルが選択されていません")
            return 
        indices = self.listbox[0].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        for i in indices: 
            img=self.img_list[0][i]
            img=fr.head_rotate(img)
            img=fr.head_rotate(img)
            self.img_list[0][i]=fr.head_rotate(img)
        self.plot_graph(0)
    def compress(self):#圧縮
        if len(self.img_list[0])==0:
            self.output_status_bar("ファイルが選択されていません")
            return 
        indices = self.listbox[0].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        for i in indices: 
            img=self.img_list[0][i]
            self.img_list[0][i]=lift.compress_list(img)
        self.plot_graph(0)
    def toslim(self):
        if len(self.img_list[0])==0:
            self.output_status_bar("ファイルが選択されていません")
            return 
        indices = self.listbox[0].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        for i in indices: 
            img=self.img_list[0][i]
            if not lf.judge_slim_classic(img):
                self.img_list[0][i]=SlimWideConverter.wide2slim(img)
        self.plot_graph(0)
    def towide(self):
        if len(self.img_list[0])==0:
            self.output_status_bar("ファイルが選択されていません")
            return 
        indices = self.listbox[0].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        for i in indices: 
            img=self.img_list[0][i]
            if lf.judge_slim_classic(img):
                self.img_list[0][i]=SlimWideConverter.slim2wide(img)
        self.plot_graph(0)
    def replace(self):#headの置き換え
        if len(self.img_list[0])==0:
            self.output_status_bar("ファイルが選択されていません")
            return 
        indices = self.listbox[0].curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        ###
        filename = tk.filedialog.askopenfilename(initialdir = os.getcwd())
        basename = os.path.basename(filename)
        print("入力ファイル:"+filename)
        try:
            img2 = image.imread(filename)
            if img2.shape==(32,64,4):
                    img2=Convert32to64.resize_img(img2)
            if img2.shape!=(64,64,4):
                print("invalid file:ファイルは32x64または64x64のpngを選択してください\n")
                self.output_status_bar("invalid file:ファイルは32x64または64x64のpngを選択してください\n")
                return
            for i in indices: 
                img=self.img_list[0][i]
                self.img_list[0][i]=lift.replace_head(img,img2)
            self.plot_graph(0)
        except TypeError:
            print("入力ファイルが読み込めませんでした\n")
            self.output_status_bar("入力ファイルが読み込めませんでした")
        ###
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
        return array1
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
        
    def plot_graph(self,index):
        if len(self.img_list[index])==0 :
            img=np.zeros((64,64,4),dtype=np.uint8)
            self.output_status_bar("ファイルが選択されていません")
        elif len(self.img_list[index])==1:
            img=self.img_list[index][0]
        else :
            indices = self.listbox[index].curselection()
            if len(indices)==0:
                self.output_status_bar("ファイルが選択されていません")
                return
            img=self.img_list[index][indices[0]]
        plt.clf()
        img=self.erase_parts(index,img)
        self.init_graph()
        # グラフの描画
        sv.main(self.ax,img,self.iswide)
        
        # 表示
        self.fig_canvas.draw()
        img=Image.fromarray((img * 255).astype('uint8')).resize((64*self.canvas_size, 64*self.canvas_size),Image.NEAREST)
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.add_skin_border(self.canvas)
        self.display_index=index

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()