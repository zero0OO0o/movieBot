#-*- coding: UTF-8 -*-

from tkinter import *
from PIL import Image, ImageTk
import _gui.do

def callback():

    _gui.do.start_wechat_bot()


root = Tk() # 初始化Tk()
root.title("frame-test")    # 设置窗口标题
root.geometry("900x700")    # 设置窗口大小 注意：是x 不是*
root.resizable(width=False, height=False) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True

config_frame = Frame(master=root)

Label(master=root,text='WeChat\nMovieBot',background='black',foreground='white',width=16,height=30).pack(side=LEFT)

Button(master=config_frame,text='Start',background='black',foreground='white',width=15,height=3,command=callback).pack(side=BOTTOM)

Label(master=config_frame,text='Want your own wechat bot? \nclick "start" to start\n↓').pack(side=BOTTOM)


render = ImageTk.PhotoImage(Image.open('_gui/logo_gui.png'))

photo_show = Label(master=root,image=render)

photo_show.place(x=340,y=100)

config_frame.pack(side=BOTTOM)

root.mainloop()