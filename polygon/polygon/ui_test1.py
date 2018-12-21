#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/9/28 19:42
#!@Author :SINGLE
#!@File   :ui_test1.py

from tkinter import *
root = Tk()
def create():
    top = Toplevel()
    #使用attributes()方法
    top.attributes('-alpha',0.5)
    top.title('我的弹窗')
    msg = Message(top,text = '类似于弹出窗口，具有独立的窗口属性。',width = 150)
    msg.pack()
Button(root,text = '创建一个顶级窗口',command = create).pack(padx = 20,pady = 50)
mainloop()