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
QDockWidgetdemo::QDockWidgetdemo(QWidget * parent)
: QMainWindow(parent)
{
    ui.setupUi(this);
setWindowTitle(tr("DockWindows")); // 设置窗口标题
QTextEdit * te = new
QTextEdit(this);
te->setText(tr("Main Window"));
te->setAlignment(Qt::AlignCenter);
setCentralWidget(te); // 将此编辑框设为主窗口的中央窗口
                         // 停靠窗口1
QDockWidget * dock = new
QDockWidget(tr("DockWindow1"), this);
dock->setFeatures(QDockWidget::DockWidgetMovable); // 可移动
dock->setAllowedAreas(Qt::LeftDockWidgetArea | Qt::RightDockWidgetArea);
QTextEdit * te1 = new
QTextEdit();
te1->setText(tr("Window1,the dock widget can be moved between docks by the users"));
dock->setWidget(te1);
addDockWidget(Qt::RightDockWidgetArea, dock); // 初始位置
                                                 // 停靠窗口2
dock = new
QDockWidget(tr("DockWindow2"), this);
dock->setFeatures(QDockWidget::DockWidgetClosable | QDockWidget::DockWidgetFloatable); // 可关闭可浮动
QTextEdit * te2 = new
QTextEdit();
te2->setText(tr("Window2,the dock widget can be detached from the main window"));
dock->setWidget(te2);
addDockWidget(Qt::RightDockWidgetArea, dock); // 初始位置
                                                 // 停靠窗口2
dock = new
QDockWidget(tr("DockWindow3"), this);
dock->setFeatures(QDockWidget::AllDockWidgetFeatures); // 全部特性
QTextEdit * te3 = new
QTextEdit();
te3->setText(tr("Window2,the dock widget can be closed ,moved,and floted"));
dock->setWidget(te3);
addDockWidget(Qt::RightDockWidgetArea, dock); // 初始位置

}
