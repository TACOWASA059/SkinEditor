import tkinter as tk
#from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import matplotlib.image as image
import matplotlib.pyplot as plt
import skin_view as sv
import os

import backward_flip_reform as bf
import lj_flip as lf
import upsidedown_flip as uf
import face_rotate as fr
class Application(tk.Frame):
    img_list=[]
    def __init__(self, master=None):
        super().__init__(master)
        self.img_list=[]
        self.master = master
        self.master.geometry("1000x700") 
        self.master.title('スキン編集')

        # ステータスバーの作成
        self.create_status_bar()
        self.listbox = tk.Listbox(width=20, height=12)
        self.listbox.place(x=310,y=40,width=200,height=200)
        label = tk.Label(self.master, text='読み込みファイルリスト')
        label.place(x=330,y=10) 
        #ファイル選択ボタン
        button1 = tk.Button(self.master, text='ファイルを読み込み',command=self.open_click)
        button1.place(x=10,y=10) 
        #削除ボタン
        button2 = tk.Button(self.master, text='選択項目を削除',command=self.deleteSelectedList)
        button2.place(x=150,y=10) 
        self.init_graph()
        #描画ボタン作成
        
        button = tk.Button(self.master, text = "選択項目を描画", command = self.plot_graph)
        button.place(x=150,y=60)

        button3 =tk.Button(self.master, text = "選択項目を保存", command = self.save_fig)
        button3.place(x=150,y=110)

        #反転ボタン
        label = tk.Label(self.master, text='選択項目のスキンを反転')
        label.place(x=10,y=230) 
        button = tk.Button(self.master, text = "前後", command = self.backwards)
        button.place(x=10,y=270)
        button = tk.Button(self.master, text = "左右", command = self.flip)
        button.place(x=80,y=270)       
        button = tk.Button(self.master, text = "上下", command = self.upsidedown)
        button.place(x=150,y=270)   
        #head回転
        label = tk.Label(self.master, text='選択項目のheadを回転')
        label.place(x=10,y=300) 
        button = tk.Button(self.master, text = "↑", command = self.up)
        button.place(x=80,y=330)
        button = tk.Button(self.master, text = "⤵︎", command = self.rotate_clock)
        button.place(x=150,y=330)
        button = tk.Button(self.master, text = "↓", command = self.down)
        button.place(x=80,y=410)   
        button = tk.Button(self.master, text = "⤴︎", command = self.rotate_counter_clock)
        button.place(x=150,y=410)
        button = tk.Button(self.master, text = "←", command = self.left)
        button.place(x=10,y=370) 
        button = tk.Button(self.master, text = "→", command = self.right)
        button.place(x=150,y=370) 
        label = tk.Label(self.master, text='回転方向')
        label.place(x=70,y=370) 
    def init_graph(self):
        # matplotlib配置用フレーム
        frame = tk.Frame(self.master,relief=tk.RIDGE)
        fig = plt.figure(figsize=(3,5))
        self.ax = fig.add_subplot(111, projection='3d')
        self.ax.axis("off")
        self.ax.set_box_aspect((1,1,2))
        self.fig_canvas = FigureCanvasTkAgg(fig, frame)
        # matplotlibのツールバーを作成
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, frame)
        # matplotlibのグラフをフレームに配置
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        #描画用フレームをウィンドウに配置(右下)
        frame.place(x=550,y=10,width=400,height=600)
        #frame.pack(fill='y',side=tk.RIGHT,anchor=tk.S)
    def open_click(self):
        ''' ファイルを開く'''
        # ファイルを開くダイアログ
        filename = tk.filedialog.askopenfilename(initialdir = os.getcwd())
        basename = os.path.basename(filename)
        print("入力ファイル:"+filename)
        try:
            img = image.imread(filename)
            if len(img)!=64 or len(img[0])!=64 or len(img[0][0])!=4:
                print("invalid file:ファイルは64x64のpngもしくはjpegを選択してください\n")
                self.output_status_bar("invalid file:ファイルは64x64のpngもしくはjpegを選択してください\n")
                return
            self.img_list.append(img)
            self.add_List(basename)
            self.output_status_bar("ファイル"+basename+"がリストに追加されました")
            return
        except TypeError:
            print("入力ファイルが読み込めませんでした\n")
            self.output_status_bar("入力ファイルが読み込めませんでした")
    #リストボックスに追加
    def add_List(self,text):
        self.listbox.insert(tk.END, text)
        self.listbox.place(x=310,y=40,width=200,height=200)
        print("done\n")
        if self.listbox.size()==1:
            self.plot_graph()
    # ボタンが押されたらリストボックスの選択されている部分を削除
    def deleteSelectedList(self):
        # 選択されているリストの番号
        selectedIndex = tk.ACTIVE
        print(selectedIndex)
        
        if len(self.img_list)==0:
            return 
        else :
            indices = self.listbox.curselection()
            self.img_list.pop(indices[0])
        self.listbox.delete(selectedIndex)
    #ファイルの保存
    def save_fig(self):
        #選択項目を取得
        indices = self.listbox.curselection()
        if len(indices)==0:
            print("ファイルが選択されていません")
            self.output_status_bar("ファイルが選択されていません")
            return
        img2=self.img_list[indices[0]]
        #print(img2)
        filename = tk.filedialog.asksaveasfilename( filetypes = [("PNG", ".png")])
        if ".png" not in filename:
            filename+=".png"
        print("保存ファイル名:"+filename)
        image.imsave(filename,img2)
        self.output_status_bar(filename +"として保存されました。")
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
    def backwards(self):
        if len(self.img_list)==0:
            self.output_status_bar("ファイルが読み込まれていません")
            return 
        indices = self.listbox.curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        img=self.img_list[indices[0]]
        self.img_list[indices[0]]=bf.backwards(img)
        self.plot_graph()
    #左右
    def flip(self):
        if len(self.img_list)==0:
            self.output_status_bar("ファイルが読み込まれていません")
            return 
        indices = self.listbox.curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        img=self.img_list[indices[0]]
        self.img_list[indices[0]]=lf.flip(img)
        self.plot_graph()
    def upsidedown(self):
        if len(self.img_list)==0:
            self.output_status_bar("ファイルが読み込まれていません")
            return 
        indices = self.listbox.curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        img=self.img_list[indices[0]]
        #print(self.img_list[indices[0]])
        self.img_list[indices[0]]=uf.upsidedown(img)
        #print(self.img_list[indices[0]])
        self.plot_graph()
    def up(self):
        if len(self.img_list)==0:
            self.output_status_bar("ファイルが読み込まれていません")
            return 
        indices = self.listbox.curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        img=self.img_list[indices[0]]
        #print(self.img_list[indices[0]])
        self.img_list[indices[0]]=fr.head_rotate_horizontal(img)
        #print(self.img_list[indices[0]])
        self.plot_graph()
    def down(self):
        if len(self.img_list)==0:
            self.output_status_bar("ファイルが読み込まれていません")
            return 
        indices = self.listbox.curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        img=self.img_list[indices[0]]
        #print(self.img_list[indices[0]])
        img=fr.head_rotate_horizontal(img)
        img=fr.head_rotate_horizontal(img)
        self.img_list[indices[0]]=fr.head_rotate_horizontal(img)
        #print(self.img_list[indices[0]])
        self.plot_graph()
    def right(self):
        if len(self.img_list)==0:
            self.output_status_bar("ファイルが読み込まれていません")
            return 
        indices = self.listbox.curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        img=self.img_list[indices[0]]
        self.img_list[indices[0]]=fr.head_rotate_vertical(img)
        self.plot_graph()
    def left(self):
        if len(self.img_list)==0:
            self.output_status_bar("ファイルが読み込まれていません")
            return 
        indices = self.listbox.curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        img=self.img_list[indices[0]]
        img=fr.head_rotate_vertical(img)
        img=fr.head_rotate_vertical(img)
        self.img_list[indices[0]]=fr.head_rotate_vertical(img)
        self.plot_graph()
    def rotate_clock(self):
        if len(self.img_list)==0:
            self.output_status_bar("ファイルが選択されていません")
            return 
        indices = self.listbox.curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        img=self.img_list[indices[0]]
        self.img_list[indices[0]]=fr.head_rotate(img)
        self.plot_graph()
    def rotate_counter_clock(self):
        if len(self.img_list)==0:
            self.output_status_bar("ファイルが選択されていません")
            return 
        indices = self.listbox.curselection()
        if len(indices)==0:
            self.output_status_bar("ファイルが選択されていません。リストからファイルを選択してください")
            return 
        img=self.img_list[indices[0]]
        img=fr.head_rotate(img)
        img=fr.head_rotate(img)
        self.img_list[indices[0]]=fr.head_rotate(img)
        self.plot_graph()
    def plot_graph(self):
        if len(self.img_list)==0:
            img=np.zeros((64,64,4),dtype=np.uint8)
            self.output_status_bar("ファイルが選択されていません")
        elif len(self.img_list)==1:
            img=self.img_list[0]
        else :
            indices = self.listbox.curselection()
            img=self.img_list[indices[0]]
        plt.clf()
        self.init_graph()

        # グラフの描画
        sv.main(self.ax,img)
        # 表示
        self.fig_canvas.draw()
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()