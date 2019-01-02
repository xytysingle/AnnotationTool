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

songs = ['爱情买卖', '朋友', '回家过年', '好日子']
films = ['阿凡达', '猩球崛起']


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(677, 442)
        self.setWindowTitle("我的程序")

        self.createUI()
        self.createAction()
        self.createStatusbar()
        self.createMenu()
        self.createToolbar()

    def createUI(self):
        self.textedit = QTextEdit()
        self.setCentralWidget(self.textedit)

    # 动作
    def createAction(self):
        self.exit_action = QAction(QIcon("ico_new.jpg"), "退出", self, triggered=qApp.quit)
        self.exit_action.setStatusTip("退出程序")
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(qApp.quit)

    # 状态栏
    def createStatusbar(self):
        self.statusBar()

    # 菜单栏
    def createMenu(self):
        # menubar = QMenuBar(self)
        menubar = self.menuBar()
        menu = menubar.addMenu("文件(F)")
        menu.addAction(QAction(QIcon("ico_new_16_16.jpg"), "新建", self, triggered=qApp.quit))  # 带图标，文字
        menu.addAction(QAction(QIcon("ico_open_16_16.jpg"), "打开", self, triggered=qApp.quit))
        menu.addAction(QAction(QIcon("ico_save_16_16.jpg"), "保存", self, triggered=qApp.quit))
        menu.addSeparator()
        menu.addAction(
            QAction(QIcon("ico_close_16_16.jpg"), "关闭", self, triggered=lambda: QMessageBox.about(self, '关闭', '关闭。。。')))

        menu = menubar.addMenu("编辑(E)")
        menu.addAction(QAction("撤销", self, triggered=qApp.quit))  # 不带图标
        menu.addAction(QAction("剪切", self, triggered=qApp.quit))
        menu.addAction(QAction("复制", self, triggered=qApp.quit))
        menu.addAction(QAction("粘贴", self, triggered=qApp.quit))

        menu = menubar.addMenu("娱乐(S)")
        menu.addAction(QAction("音乐", self, triggered=lambda: self.thread_it(self.music, songs)))  # 线程
        menu.addAction(QAction("电影", self, triggered=lambda: self.thread_it(self.movie, films)))

        menu = menubar.addMenu("帮助(H)")
        menu.addAction('&New', lambda: QMessageBox.about(self, 'New', '新建。。。'), Qt.CTRL + Qt.Key_N)  # 注意快捷键
        menu.addAction('关于', lambda: QMessageBox.about(self, '关于', '关于。。。'), Qt.CTRL + Qt.Key_Q)

    # 工具栏
    def createToolbar(self):
        toolbar = self.addToolBar('文件')
        toolbar.addAction(QAction(QIcon("ico_new_16_16.jpg"), "新建", self, triggered=qApp.quit))  # 带图标，文字
        toolbar.addAction(QAction(QIcon("ico_open_16_16.jpg"), "打开", self, triggered=qApp.quit))
        toolbar.addSeparator()
        toolbar.addAction(QAction(QIcon("ico_save_16_16.jpg"), "打开", self, triggered=qApp.quit))

        toolbar = self.addToolBar("编辑")
        toolbar.addAction(QAction("撤销", self, triggered=qApp.quit))  # 不带图标
        toolbar.addAction(QAction("剪切", self, triggered=qApp.quit))

    # 逻辑：听音乐
    def music(self, songs):
        for x in songs:
            self.textedit.append("听音乐：%s \t-- %s" % (x, time.ctime()))
            time.sleep(3)

    # 逻辑：看电影
    def movie(self, films):
        for x in films:
            self.textedit.append("看电影：%s \t-- %s" % (x, time.ctime()))
            time.sleep(5)

    # 打包进线程（耗时的操作）
    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)  # 守护--就算主界面关闭，线程也会留守后台运行（不对!）
        t.start()  # 启动
        # t.join()          # 阻塞--会卡死界面！


app = QApplication(sys.argv)
win = MyWindow()
win.show()
sys.exit(app.exec_())

