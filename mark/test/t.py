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

from tkinter import *

import ttk

import threading

import random

import time


class UIThread:

    def __init__(self, root, count=10):

        self.count = count

        self.value = 0

        self.b_exit = False

        self.root = root

        self.event = threading.Event()

        self.pbar = ttk.Progressbar(root, length=200, maximum=count)

        self.pbar.pack()

        root.after(0, self.update)

    def set_max(self, max):

        self.pbar.config(maximum=max)

    def set_val(self, val):

        self.value = val

    def start(self):

        self.event.set()

    def stop(self):

        self.b_exit = True

    def update(self):

        print
        'waiting...'

        self.event.wait()

        print
        'start progress...'

        while 1:

            self.pbar.config(value=self.value)

            self.pbar.update()

            if self.b_exit:
                break

        self.root.quit()

        print
        'root quit()'

    def increase(slef):

        self.value += 1


def work_func(count, ui):
    ui.set_max(count)

    ui.start()

    print
    '->working<-'

    for i in range(1, count + 1):
        rnd_t = random.uniform(.2, .5)

        print
        i, threading.currentThread().getName(), ':', time.ctime()

        ui.set_val(i)

        time.sleep(rnd_t)

    ui.stop()


if __name__ == '__main__':
    root = Tk()

    ui = UIThread(root)

    work_thread = threading.Thread(target=work_func, args=(5, ui))

    work_thread.start()

    root.mainloop()

    work_thread.join()

    raw_input('Press return...')