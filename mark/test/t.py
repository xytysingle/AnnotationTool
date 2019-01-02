#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/10/6 16:48
#!@Author :SINGLE
#!@File   :t.py

# !/usr/bin/python
# -*- coding: UTF-8 -*-
import time
# from tkinter import *
#
# def callback():
#     print('hhh')
# top = Tk()
# CheckVar1 = IntVar()
# CheckVar1.set(1)
# CheckVar2 = IntVar()
# C1 = Checkbutton(top, text="RUNOOB", variable=CheckVar1, \
#                  onvalue=1, offvalue=0, height=5, \
#                  width=20)
# C2 = Checkbutton(top, text="GOOGLE", variable=CheckVar2, \
#                  onvalue=1, offvalue=0, height=5, \
#                  width=20)
# C1.pack()
# C2.pack()
# t=StringVar()
# t.set('hhh')
# Entry(top,textvariable=t,relief='flat',bd=5).pack()
# ckbtn=Checkbutton(top,variable=t,relief='flat',bd=5,command=callback,onvalue=1)
# ckbtn.pack()
# Entry(top,textvariable=t,relief='sunken',bd=5).pack()
# Entry(top,textvariable=t,relief='raised',bd=5).pack()
# Entry(top,textvariable=t,relief='groove',bd=5).pack()
# Entry(top,textvariable=t,relief='ridge',bd=5).pack()
#


# from tkinter import *
# root = Tk()
# v = StringVar()
# def test(f,s1,s2):
#     if f == '小甲鱼':
#         print('正确')
#         print(f,s1,s2)
#         return True
#     else:
#         print('错误')
#         print(f,s1,s2)
#         return False
# test_register = root.register(test) #root调用register方法才能用到下边的validatecommand选项中
# e1 = Entry(root,textvariable = v,validate = 'key',\
#            validatecommand = (test_register,'%P','%i','%s')) #这些额外的参数带引号啊 ，要注意
# e2 = Entry(root)
# e1.pack()
# e2.pack()
# mainloop()
#
# from tkinter import *
#
# master = Tk()
#
# frame = Frame(master)
# frame.pack(padx=10, pady=10)
#
#
# def test(
#         content):  # 有些人可能会用输入框的get方法来获取内容，再通过将validate设置为key来判断输入参数合不合法。但是validate参数设置为key后，就不再能用输入框的get方法和textvariable.get方法获取输入内容。因为validate被指定为key时，有任何输入操作都会被拦截，然后调用验证函数，验证完后只有返回True才会将内容放到textvariable关联的变量中。
#     return content.isdigit()  # 字符串的内置方法，是数字返回True；不是返回False
#
#
# v1 = StringVar()
# v2 = StringVar()
# v3 = StringVar()
#
# testCMD = master.register(test)
# e1 = Entry(frame, width=10, textvariable=v1, validate='key', \
#            validatecommand=(testCMD, '%P')).grid(row=0,
#                                                  column=0)  # validate的值是key，那么输入框输入的内容如果是True会保留；是False会清除。设置输入框的宽度是10个字符
#
# Label(frame, text='+').grid(row=0, column=1)
#
# e2 = Entry(frame, width=10, textvariable=v2, validate='key', \
#            validatecommand=(testCMD, '%P')).grid(row=0, column=2)
#
# Label(frame, text='=').grid(row=0, column=3)
#
# e3 = Entry(frame, width=10, textvariable=v3, state='readonly').grid(row=0, column=4)
#
#
# def calc():
#     result = int(v1.get()) + int(v2.get())
#     v3.set(str(result))
#
#
# Button(frame, text='计算结果', command=calc).grid(row=1, column=2, pady=5)
#
# mainloop()

#
# '''用验证函数模拟简单计算器'''
# from tkinter import *
# root = Tk()
# frame = Frame(root) #把整个布局放到框架中，更好调节
# frame.pack(padx = 10,pady = 10)
# v1 = StringVar()
# v2 = StringVar()
# v3 = StringVar()
#
# def test(content):
#     if content.isdigit():#isdigit()方法，这是str的一个函数，只允许输入数字
#        return True
#     else:
#         return False
#
#
# testCmd = root.register(test)#通过register方法转换为validatecommand选项能接收的函数
# Entry(frame,textvariable = v1,width = 10,validate = 'key',\
#       validatecommand = (testCmd,'%P')).grid(row = 0,column = 0) #用%P获取最新输入的字符串,而不用v1.get()小甲鱼说了很多，没看明白，这就不写了，呵呵
# Label(frame,text = '+').grid(row = 0,column = 1)
# Entry(frame,textvariable = v2,width = 10,validate = 'key',\
#       validatecommand = (testCmd,'%P')).grid(row = 0,column = 2)
# Label(frame,text = '=').grid(row = 0,column = 3)
# Entry(frame,textvariable = v3,width = 10,state = 'readonly',validate = 'key',\
#       validatecommand = (testCmd,'%P')).grid(row = 0,column = 4)
#
# def calc():
#     result = int(v1.get()) + int(v2.get())
#     v3.set(result)
#
# Button(frame,text = '计算结果',command = calc).grid(row = 1,column = 2,pady =5)
# mainloop()

# -*- coding: UTF-8 -*-

# include "QDockWidgetdemo.h"
# include <QTextEdit>
# include <QDockWidget>
import tkinter

import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QToolBar, QTextEdit, QAction, QApplication, qApp, QMessageBox
from PyQt5.QtCore import Qt

import threading
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class LineEditEx(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(None, parent)
        self.setGeometry(50, 50, 100, 20)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)  # 开启可拖放事件

    def dragEnterEvent(self, QDragEnterEvent):
        e = QDragEnterEvent  # type:QDragEnterEvent
        print('type:', e.type())  # 事件的类型
        print('pos:', e.pos())  # 拖放位置
        print(e.mimeData().urls())  # 文件所有的路径
        print(e.mimeData().text())  # 文件路径
        print(e.mimeData().formats())  # 支持的所有格式
        print(e.mimeData().data('text/plain'))  # 根据mime类型取路径 值为字节数组
        print(e.mimeData().hasText())  # 是否支持文本文件格式
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text()) #如果之前设置ignore 为False 这里将不会生效

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setUi()

    def setUi(self):
        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle('demo_ui_2')
        self.textEdit = LineEditEx(self)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())