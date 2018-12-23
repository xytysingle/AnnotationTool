#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/9/30 13:57
#!@Author :SINGLE
#!@File   :Login.py
import time
from tkinter import *
import requests
from configobj import ConfigObj

from Polygon import *
from Const import const
from entity.LoginData import LoginData
import os
from entity.BaseApp import BaseApp
root_login=None

class Login(BaseApp):
    def __init__(self,root):
        self.root_login=root
        label = Label(root, text='用户名:', anchor='c').grid(row=0)
        usr_str=StringVar()
        self.user_Entry = Entry(root,textvariable=usr_str,bd =5)
        self.user_Entry.focus_set()

        self.user_Entry.grid(row=0, column=1)

        label1 = Label(root, text='密码  :', anchor='c').grid(row=1)
        pwd_str = StringVar()
        self.pwd_Entry = Entry(root, show='*',textvariable=pwd_str,bd =5)
        self.pwd_Entry.grid(row=1, column=1)

        self.autologin_booleanVar=BooleanVar()
        self.remember_pwd_booleanVar=BooleanVar()
        self.autologin_ckBtn =Checkbutton(root, text='自动登录', anchor='c', width=6, height=1,variable=self.autologin_booleanVar, command=self.ckBtn_callback)
        self.autologin_ckBtn.grid(row=2, column=0)
        self.remember_pwd_ckBtn=Checkbutton(root, text='记住密码', anchor='c', width=6, height=1, variable=self.remember_pwd_booleanVar,command=self.ckBtn_callback)
        self.remember_pwd_ckBtn.grid(row=2, column=1)
        Button(root, text='重置', anchor='c', width=6, height=1, command=self.ReSet).grid(row=2, column=2)
        Button(root, text='登    录', anchor='c', width=10, height=1, command=self.Show).grid(row=3, column=1)

        self.root_login.bind("<KeyPress-Return>", self.Show)
        self.root_login.bind("<KeyPress-Return>", self.Show)

        #是否记住密码
        self.config=BaseApp.get_conifgObj()
        is_remember_pwd = self.config[const.LOGIN][const.ISREMEMBERPWD]
        is_autologin = self.config[const.LOGIN][const.ISAUTOLOGIN]
        if is_remember_pwd=='1':
            usr_str.set(self.config[const.LOGIN][const.USER])
            pwd_str.set(self.config[const.LOGIN][const.PSWD])
            self.user_Entry.icursor (len(self.user_Entry.get()))
            self.user_Entry.selection_adjust(len(self.user_Entry.get()))
            self.remember_pwd_ckBtn.select()
        # 是否自动登录
        if is_autologin == '1':
            self.autologin_ckBtn.select()
            # time.sleep(1)
            self.Show()

    def ckBtn_callback(self):
        if self.autologin_booleanVar.get():
            if not self.remember_pwd_booleanVar.get():
                self.remember_pwd_ckBtn.select()

        if not self.remember_pwd_booleanVar.get():
            if  self.autologin_booleanVar.get():
                self.autologin_ckBtn.deselect()

    # 判断登录界面是否成功
    def Show(self,*args):

        # root1.title('Entry')
        # if self.user_Entry.get() == 'zhangsan' and self.pwd_Entry.get() == '123456':
        #     Label(root1, text='登陆成功！', fg='blue', width=30, height=8, anchor='c').pack()
        #     # 模拟下网页跳转
        #     Button(root1, text='下一步', width=6, height=1, anchor='c', command=self.NewGui, fg='red').pack()
        # else:
        #     Label(root1, text='用户名或密码错误！', fg='blue', width=30, height=8, anchor='c').pack()
        #     # 销毁root1窗口
        #     Button(root1, text='返回', width=6, height=1, anchor='c', command=root1.destroy, fg='red').pack()
        if not self.user_Entry.get()  or not self.pwd_Entry.get():
            super().msgBox('哼!用户名和密码都不给我还想登录\n咋不上天捏!')
            return
        #-----------------test--------start----------------
        # self.root_login.destroy()
        # goto_main()
        # return
        # -----------------test--------end----------------
        try:
            response=requests.post(const.SERVER_LOGIN, {'username':self.user_Entry.get(), 'password':self.pwd_Entry.get()})
        except Exception:
            super().msgBox('服务器开小差啦！')
            return
        login_data=LoginData()
        login_data.fromJson(response.json())
        code = login_data.code
        if code==200:
            #save user info
            BaseApp.user_info=login_data.data
            # print(BaseApp.user_info.toKeyValue())
            #check ckBtn
            if self.autologin_booleanVar.get():
                self.config[const.LOGIN][const.ISAUTOLOGIN]='1'
            else:
                self.config[const.LOGIN][const.ISAUTOLOGIN]='0'
            if self.remember_pwd_booleanVar.get():
                self.config[const.LOGIN][const.USER]=self.user_Entry.get()
                self.config[const.LOGIN][const.PSWD]=self.pwd_Entry.get()
            else:
                self.config[const.LOGIN][const.USER]='***'
                self.config[const.LOGIN][const.PSWD]='***'
            self.config[const.LOGIN][const.ISREMEMBERPWD]='1' if self.remember_pwd_booleanVar.get() else '0'
            self.config.write()
            self.root_login.destroy()
            goto_main()
        else:
            # root1 = Tk()
            # Label(root1, text='用户名或密码错误！', fg='blue', width=30, height=8, anchor='c').pack()
            # # 销毁root1窗口
            # Button(root1, text='返回', width=6, height=1, anchor='c', command=root1.destroy, fg='red').pack()
            super().msgBox(response.json()['msg'])

    # 重置
    def ReSet(self):
        self.user_Entry.delete(0, END)
        self.pwd_Entry.delete(0, END)
def goto_login():
    root_login = Tk()
    # root_login.overrideredirect(True)#隐藏窗口
    root_login.title('PolygonAnnotationTool -SINGLE')  # 修改框体的名字,也可在创建时使用className参数来命名
    root_login.resizable(0, 0)  # 框体大小可调性，分别表示x,y方向的可变性；
    # root_login.geometry('1210x800')  # 指定主框体大小；
    # root_login.columnconfigure(0, minsize=1000)
    sw = root_login.winfo_screenwidth()
    # 得到屏幕宽度
    sh = root_login.winfo_screenheight()
    # 得到屏幕高度
    ww = 300
    wh = 120
    # 窗口宽高为100
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    # 设置窗口的大小宽x高+偏移量
    root_login.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    #root_login.iconbitmap(const.LOGO)
    mark_tool = Login(root_login)
    root_login.protocol("WM_DELETE_WINDOW", lambda :BaseApp.is_exit(root_login))
    root_login.mainloop()





