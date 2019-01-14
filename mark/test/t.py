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

import os
import cv2
from tkinter.messagebox import askyesno
from tkinter.filedialog import askdirectory
# from tkFileDialog import askdirectory
# from tkMessageBox import askyesno

WINDOW_NAME = 'Simple Bounding Box Labeling Tool'
FPS = 24
SUPPOTED_FORMATS = ['jpg', 'jpeg', 'png']
DEFAULT_COLOR = {'Object': (255, 0, 0)}
COLOR_GRAY = (192, 192, 192)
BAR_HEIGHT = 16

KEY_UP = 65362
KEY_DOWN = 65364
KEY_LEFT = 65361
KEY_RIGHT = 65363
KEY_ESC = 27
KEY_DELETE = 65535
KEY_EMPTY = 0

get_bbox_name = '{}.bbox'.format


class SimpleBBoxLabeling:

    def __init__(self, data_dir, fps=FPS, window_name=None):
        self._data_dir = data_dir
        self.fps = fps
        self.window_name = window_name if window_name else WINDOW_NAME

        self._pt0 = None
        self._pt1 = None
        self._drawing = False
        self._cur_label = None
        self._bboxes = []

        label_path = '{}.labels'.format(self._data_dir)
        self.label_colors = DEFAULT_COLOR if not os.path.exists(label_path) else self.load_labels(label_path)

        imagefiles = [x for x in os.listdir(self._data_dir) if x[x.rfind('.') + 1:].lower() in SUPPOTED_FORMATS]
        labeled = [x for x in imagefiles if os.path.exists(get_bbox_name(x))]
        to_be_labeled = [x for x in imagefiles if x not in labeled]

        self._filelist = labeled + to_be_labeled
        self._index = len(labeled)
        if self._index > len(self._filelist) - 1:
            self._index = len(self._filelist) - 1

    def _mouse_ops(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self._drawing = True
            self._pt0 = (x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            self._drawing = False
            self._pt1 = (x, y)
            self._bboxes.append((self._cur_label, (self._pt0, self._pt1)))

        elif event == cv2.EVENT_MOUSEMOVE:
            self._pt1 = (x, y)

        elif event == cv2.EVENT_RBUTTONUP:
            if self._bboxes:
                self._bboxes.pop()

    def _clean_bbox(self):
        self._pt0 = None
        self._pt1 = None
        self._drawing = False
        self._bboxes = []

    def _draw_bbox(self, img):

        h, w = img.shape[:2]
        canvas = cv2.copyMakeBorder(img, 0, BAR_HEIGHT, 0, 0, cv2.BORDER_CONSTANT, value=COLOR_GRAY)

        label_msg = '{}: {}, {}'.format(self._cur_label, self._pt0, self._pt1) \
            if self._drawing \
            else 'Current label: {}'.format(self._cur_label)
        msg = '{}/{}: {} | {}'.format(self._index + 1, len(self._filelist), self._filelist[self._index], label_msg)

        cv2.putText(canvas, msg, (1, h+12),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 0), 1)
        for label, (bpt0, bpt1) in self._bboxes:
            label_color = self.label_colors[label] if label in self.label_colors else COLOR_GRAY
            cv2.rectangle(canvas, bpt0, bpt1, label_color, thickness=2)
            cv2.putText(canvas, label, (bpt0[0]+3, bpt0[1]+15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, label_color, 2)
        if self._drawing:
            label_color = self.label_colors[self._cur_label] if self._cur_label in self.label_colors else COLOR_GRAY
            if self._pt1[0] >= self._pt0[0] and self._pt1[1] >= self._pt0[1]:
                cv2.rectangle(canvas, self._pt0, self._pt1, label_color, thickness=2)
            cv2.putText(canvas, self._cur_label, (self._pt0[0] + 3, self._pt0[1] + 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, label_color, 2)
        return canvas

    @staticmethod
    def export_bbox(filepath, bboxes):
        if bboxes:
            with open(filepath, 'w') as f:
                for bbox in bboxes:
                    line = repr(bbox) + '\n'
                    f.write(line)
        elif os.path.exists(filepath):
            os.remove(filepath)

    @staticmethod
    def load_bbox(filepath):
        bboxes = []
        with open(filepath, 'r') as f:
            line = f.readline().rstrip()
            while line:
                bboxes.append(eval(line))
                line = f.readline().rstrip()
        return bboxes

    @staticmethod
    def load_labels(filepath):
        label_colors = {}
        with open(filepath, 'r') as f:
            line = f.readline().rstrip()
            while line:
                label, color = eval(line)
                label_colors[label] = color
                line = f.readline().rstrip()
        return label_colors

    @staticmethod
    def load_sample(filepath):
        img = cv2.imread(filepath)
        bbox_filepath = get_bbox_name(filepath)
        bboxes = []
        if os.path.exists(bbox_filepath):
            bboxes = SimpleBBoxLabeling.load_bbox(bbox_filepath)
        return img, bboxes

    def _export_n_clean_bbox(self):
        bbox_filepath = os.sep.join([self._data_dir, get_bbox_name(self._filelist[self._index])])
        self.export_bbox(bbox_filepath, self._bboxes)
        self._clean_bbox()

    def _delete_current_sample(self):
        filename = self._filelist[self._index]
        filepath = os.sep.join([self._data_dir, filename])
        if os.path.exists(filepath):
            os.remove(filepath)
        filepath = get_bbox_name(filepath)
        if os.path.exists(filepath):
            os.remove(filepath)
        self._filelist.pop(self._index)
        print('{} is deleted!'.format(filename))

    def start(self):

        last_filename = ''
        label_index = 0
        labels = list(self.label_colors.keys())
        n_labels = len(labels)

        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self._mouse_ops)
        key = KEY_EMPTY
        delay = int(1000 / FPS)

        while key != KEY_ESC:

            if key == KEY_UP:
                if label_index == 0:
                    pass
                else:
                    label_index -= 1

            elif key == KEY_DOWN:
                if label_index == n_labels - 1:
                    pass
                else:
                    label_index += 1

            elif key == KEY_LEFT:
                if self._index > 0:
                    self._export_n_clean_bbox()

                self._index -= 1
                if self._index < 0:
                    self._index = 0

            elif key == KEY_RIGHT:
                if self._index < len(self._filelist) - 1:
                    self._export_n_clean_bbox()

                self._index += 1
                if self._index > len(self._filelist) - 1:
                    self._index = len(self._filelist) - 1

            elif key == KEY_DELETE:
                if askyesno('Delete Sample', 'Are you sure?'):
                    self._delete_current_sample()
                    key = KEY_EMPTY
                    continue

            filename = self._filelist[self._index]
            if filename != last_filename:
                filepath = os.sep.join([self._data_dir, filename])
                img, self._bboxes = self.load_sample(filepath)
            self._cur_label = labels[label_index]

            canvas = self._draw_bbox(img)
            cv2.imshow(self.window_name, canvas)
            key = cv2.waitKey(delay)

            last_filename = filename

        print('Finished!')

        cv2.destroyAllWindows()
        self.export_bbox(os.sep.join([self._data_dir, get_bbox_name(filename)]), self._bboxes)

        print('Labels updated!')

if __name__ == '__main__':
    dir_with_images = askdirectory(title='Where are the images?')
    labeling_task = SimpleBBoxLabeling(dir_with_images)
    labeling_task.start()
