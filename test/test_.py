#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/6/18 21:09
#!@Author :SINGLE
#!@File   :test.py





#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    :  2018年6月9日下午7:15:28
# @Author  : single
# @Version :
# @desc :
# import os
'a test doc'
__author__ = 'SINGLE'
from collections import Iterable
from functools import reduce
import functools
import os
import json
from multiprocessing import Process
from tkinter import *
import tkinter.messagebox as messagebox

'''
a = ['af']
b = 'fsfd'
a = b
b = 1
print(a)
'''

a = ['1', 'abc', 3]
c = ('1', 'abc', [1, '2'])  # tuple
cc = ('1', 'abc', 2)  # tuple
d = 1, 2  # tuple可以省略括号
b = {'1': 'f', 'a1': 'f', 0: 3}
bb = {'1': 'f', cc: 'f', 0: 3}


# print(a[0])
# print(b['1'])
# print(b[0])
# a[0]
# b['1']
# b[0]

# aa = a.reverse()
# for x in a:
#     print(x)
# print(input('please:'))

# help(a)


def my_abs(x):
    if x >= 0:
        return x
    else:
        return -x


# print(my_abs(-1))
# print(d)

def power(x=2, n=2):
    a = x ** n
    return a


# print(power(0))
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum


a = [1, 2]


# print(calc(*a))


def findMinAndMax(Li):
    if isinstance(Li, Iterable) and len(Li) > 0:
        min = max = Li[-2]
        for val in Li:
            # print(i,Li[i])
            if min > val:
                min = val
            elif max < val:
                max = val
    return min, max


# print(findMinAndMax(list(range(10))))

# print(list(map(int, ['1', '2'])))


def f(x, y):
    x = int(x)
    y = int(y)
    return x * 10 + y


def fn(l):
    l = list(map(int, l))
    s = l[0] * 10 + l[1]
    for i, v in enumerate(l):
        if i < 2:
            continue
        s = s * 10 + l[i]
    return s


# print(reduce(f, ['1', '2', '3']))
# print(fn(['1', '2', '3']))
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]


def by_name(t):
    def getName(t):
        return t[-1]

    return sorted(L, key=getName, reverse=True)


# print(by_name(L))

def createCounter():
    i = 0

    def counter():
        nonlocal i
        i += 1
        return i

    return counter


counterA = createCounter()
# print(counterA(), counterA(), counterA(), counterA(), counterA())  # 1 2 3 4 5


L = list(filter(lambda n: n % 2 == 1, range(1, 20)))


# print(L)


def is_odd(n):
    if lambda n: n % 2:
        return True
    else:
        return False


L = list(filter(is_odd, range(1, 20)))


# print(L)


class Test(object):
    def __init__(self, name):
        self.name = name

    def print_name(self):
        print(self.name)


t = Test('single')


# t.print_name()


def log(param):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s()' % (param[0], func.__name__))
            return func(*args, **kw)

        return wrapper

    return decorator


@log('fool')
def now():
    print('hello')


# now()
# print(now.__name__)

class Screen(object):
    # w = 1

    @property
    def resolution(self):
        return self._width * self._height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value


# 测试:
s = Screen()
s.width = 1024
s.height = 768
# print('resolution =', s.resolution)


testDir = r'E:\Library\Desktop\coca_box2\test'
testFile = 'test.txt'
testFilePath = os.path.join(testDir, testFile)

with open(testFilePath, 'w', encoding='utf-8', errors='ignore') as f:
    # print(f.write('test3'))
    pass
with open(testFilePath, 'r', encoding='utf-8', errors='ignore') as f:
    pass
    # print(f.read())

# print(os.environ['PATH'])
# print(os.path.join(r'E:\Library\Desktop\coca_box2','test'))
# print(os.mkdir(r'E:\Library\Desktop\coca_box2\test\test.txt'))
# print(os.rmdir(r'E:\Library\Desktop\coca_box2\test\1'))

# print(os.path.splitext(testFilePath))
# print(os.rename(testFilePath,r'E:\Library\Desktop\coca_box2\test\e.txt'))
# os.mkdir(os.path.join(testDir,'t.txt'))
# print(os.listdir(testDir))

# print([x for x in os.listdir(testDir) if os.path.isfile(os.path.join(testDir,x)) and os.path.splitext(x)[1]=='.txt'])

obj = dict(name='小明', age=20)
s = json.dumps(obj, ensure_ascii=False)
obj = json.loads(s)
# print(s)


from multiprocessing import Pool
import os, time, random


def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))


if __name__ != '__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        # self.nameInput = Entry(self)
        # self.nameInput.pack()

        self.userLabel = Label(self, text='用户名: ')
        self.userLabel.grid(row=1, column=0, sticky=W)
        self.userLabel.pack()


        # 定义StringVar()类对象
        self.userInput = StringVar()
        En = Entry(self, textvariable=self.userInput)
        En.grid_bbox(row=0)
        En.pack()
        # 对象值设定
        self.userInput.set('TanXin')

        self.psdLabel = Label(self, text='密码: ')

        self.psdLabel.pack()
        # 定义StringVar()类对象
        self.pwdInput = StringVar()
        En = Entry(self, textvariable=self.pwdInput, show='*').pack()
        # 对象值设定
        self.pwdInput.set('111111')

        self.alertButton = Button(self, text='登录', command=self.hello)
        self.alertButton.pack()

    def hello(self):
        name = self.userInput.get() or 'world'
        messagebox.showinfo('Message', 'Hello, %s' % name)


app = Application()
# 设置窗口标题:
app.master.title('Hello World')
# 主消息循环:
# app.mainloop()


from tkinter import *

root = Tk()

Label(root,text='帐号 :').grid(row=0,column=0) # 对Label内容进行 表格式 布局
Label(root,text='密码 :').grid(row=1,column=0)

v1=StringVar()    # 设置变量 .
v2=StringVar()

e1 = Entry(root,textvariable=v1)            # 用于储存 输入的内容
e2 = Entry(root,textvariable=v2,show='*')
e1.grid(row=0,column=1,padx=10,pady=5)      # 进行表格式布局 .
e2.grid(row=1,column=1,padx=10,pady=5)
def show():
    print("帐号 :%s" % e1.get())          # get 变量内容
    print("密码 :%s" % e2.get())

Button(root,text='芝麻开门',width=10,command=show).grid(row=3,column=0,sticky=W,padx=10,pady=5)  # 设置 button 指定 宽度 , 并且 关联 函数 , 使用表格式布局 .
Button(root,text='退出',width=10,command=root.quit).grid(row=3,column=1,sticky=E,padx=10,pady=5)

# mainloop()

import time, threading

# 假定这是你的银行存款:
balance = 0


def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n


def run_thread(n):
    for i in range(10000):
        change_it(n)


t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# print(balance)


from datetime import datetime

now=datetime.now()
print(now)
print(now.timestamp())
print(now.date)
print(datetime.fromtimestamp(now.timestamp()))
print(datetime(2012,1,1,1,1,1))

from collections import namedtuple

Point=namedtuple('点',['x','y'])
p=Point(1,2)
print(p.x)

import hashlib

md5=hashlib.md5()

from urllib import request

# with request.urlopen('https://api.douban.com/v2/book/2129650') as f:
#     data = f.read()
#     print('Status:', f.status, f.reason)
#     for k, v in f.getheaders():
#         print('%s: %s' % (k, v))
#     print('Data:', data.decode('utf-8'))


from PIL import Image

img=Image.open('test.jpg')
w,h=img.size
print('Original image size: %sx%s' % (w, h))
img.thumbnail(w//2,h//2)
print('Resize image to: %sx%s' % (w//2, h//2))
# 把缩放后的图像用jpeg格式保存:
img.save('thumbnail.jpg', 'jpeg')

