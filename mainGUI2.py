# -*- coding:utf-8 -*-
from Tkinter import *
from PIL import Image, ImageTk
import sys
import os

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        

    def init_window(self):
        self.master.title("应用程序")
        self.pack(fill=BOTH, expand=1)
        self.type=1
        self.loadNum=48
        self.width=4
        self.height=3
        self.pix=80
        self.path='/home/alex/icml2016-master/results/image/'
        #实例化一个Menu对象，这个在主窗体添加一个菜单
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # 创建File菜单，下面有Save和Exit两个子菜单
        file = Menu(menu)
        #file.add_command(label='Save' ,command=self.showImg)
        file.add_command(label='Exit', command=self.client_exit)
        menu.add_cascade(label='File', menu=file)

        # 创建Edit菜单，下面有一个Undo菜单
        edit = Menu(menu)
        edit.add_command(label='Text To Bird', command=self.CreateBird)
        edit.add_command(label='Text To Flower', command=self.CreateFlower)
        edit.add_command(label='Text To Human', command=self.CreateHuman)
        menu.add_cascade(label='Edit', menu=edit)
        
        # 创建Size菜单，下面有一个Undo菜单
        Size = Menu(menu)
        Size.add_command(label='64x64', command=self.Create64)
        Size.add_command(label='128x128', command=self.Create128)
        menu.add_cascade(label='Size', menu=Size)

        # label文本
        self.labeltext = Label(self, text='文本描述', bg="gray",font=('Helvetica', '12', 'bold'))
        self.labeltext.grid(row=0, column=0)

        # 文本输入框
        self.inputBox = Entry(self, width=50, borderwidth=2, font=('Helvetica', '14', 'bold'))
        self.inputBox.grid(row=0, column=1,pady=10,padx=15)

        # 执行按钮
        self.functionButton = Button(self, text='合成图片', bg='gray', command=self.showImg,font=('Helvetica', '12', 'bold'))
        self.functionButton.grid(row=0, column=2)
        #初始图片展示框架
        self.f1 = Frame(self, width=640, height=480, bg='gray', borderwidth=2)
        self.f1.grid(row=1, column=0, columnspan=3)
        # 选优按钮
        self.BetterButton = Button(self, text='择优选择', bg='gray', font=('Helvetica', '12', 'bold'), command=self.pickBetter)
        self.BetterButton.grid(row=2, column=0)
        # 最终结果
        self.f2 = Frame(self,width=640, height=130, bg='gray', borderwidth=2)
        self.f2.grid(row=3, column=0, columnspan=3)

        # #显示label
        # img_open2 = Image.open('2.jpg')
        # img_png2 = ImageTk.PhotoImage(img_open2)
        # self.imgLabel = Label(self,image=img_png2,width=600, height=400, bg="gray")
        # self.imgLabel.grid(row=1, column=0, columnspan=3)

    def client_exit(self):
        exit()
    
    def CreateBird(self):
        self.type=1
        self.functionButton['text']='合成鸟'
    
    def CreateFlower(self):
        self.type=2
        self.functionButton['text']='合成花'
   
    def CreateHuman(self):
        self.type=3
        self.functionButton['text']='合成人'
    
    def Create64(self):
        self.loadNum=48
        
    def Create128(self):
        self.loadNum=12
    
    def load48Img(self):
        self.f1.grid_forget()
        #初始图片展示框架
        self.f1 = Frame(self, width=640, height=480, bg='gray', borderwidth=2)
        self.f1.grid(row=1, column=0, columnspan=3)
        self.imageName = []
        for filename in os.listdir(self.path):
            self.imageName.append(filename)
        if self.loadNum==48:
            self.width=8
            self.height=6
            self.pix=80
        else:
            self.width=4
            self.height=3
            self.pix=160   
        for i in range(0,self.height):
            for j in range(0,self.width):
                filename=self.path+self.imageName[8*i+j]
                load = Image.open(filename) 
                render = ImageTk.PhotoImage(load)
                img = Label(self.f1, image=render, width=self.pix, height=self.pix, bg="gray")
                img.image = render
                img.grid(row=i, column=j)

    def pickBetter(self):
        self.f2.grid_forget()
        self.f2 = Frame(self,width=640, height=140, bg='gray', borderwidth=2)
        self.f2.grid(row=3, column=0, columnspan=3)
        
        if self.pix==160:
            mywidth=160
            myheight=130
        else:
            mywidth=80
            myheight=80
        #print self.imageName
        #print '\n'
        #筛选
        imageNameList=[]
        for j in range(len(self.imageName)) :
            item=[]
            splitName=self.imageName[j].split('-')
            item.append(float(splitName[0].strip('e')))
            item.append(int(splitName[1]))
            imageNameList.append(item)
        #print imageNameList
        
        b=sorted(imageNameList,key=lambda x:(x[1],-x[0]))
      
        for i in range(self.width):
            nameIndex = imageNameList.index(b[i])
            filename =self.imageName[nameIndex]
            #print filename
            filename=self.path+filename
            load = Image.open(filename)  # 我图片放桌面上
            render = ImageTk.PhotoImage(load)
            img = Label(self.f2, image=render, width=mywidth, height=myheight, bg="gray")
            img.image = render
            img.grid(row=0, column=i)

    def showImg(self):
        textstr=self.inputBox.get()
        f1 = open('scripts/describe.txt','w')
        f1.write(textstr)
        f1.close()
        if self.type==1:
           os.system('./scripts/demo_cub.sh')
           #load = Image.open('results/cub/img_1.png')  
        elif self.type==2:
           os.system('./scripts/demo_flowers.sh')
           #load = Image.open('results/flowers/img_1.png')  # 我图片放桌面上
        elif self.type==3:
           os.system('./scripts/demo_coco.sh')
           #load = Image.open('results/coco/img_1.png')  # 我图片放桌面上
        #render = ImageTk.PhotoImage(load)
        #img = Label(self, image=render,width=600, height=400, bg="gray")
        #img.image = render
        #img.grid(row=1, column=0, columnspan=3)
        self.load48Img()

    def showType(self):
        inputstr = str(self.type)
        text = Label(self, text='hello,'+inputstr)
        text.grid(row=1, column=0, columnspan=3)

root = Tk()
root.resizable(False, False)  # 固定窗口大小
windowWidth = 800  # 获得当前窗口宽
windowHeight =700  # 获得当前窗口高
screenWidth, screenHeight = root.maxsize()  # 获得屏幕宽和高
geometryParam = '%dx%d+%d+%d' % (
windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
root.geometry(geometryParam)  # 设置窗口大小及偏移坐标
root.wm_attributes('-topmost', 1)  # 窗口置顶
app = Window(root)
#开启主线程
root.mainloop()
