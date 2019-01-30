#!/usr/bin/env python
# !-*-coding:utf-8 -*-
# !@time    :2018/6/24 21:07
# !@Author :SINGLEquit
# !@File   :Polygon.py
import win32api
from tkinter import messagebox
from tkinter import *
from tkinter.constants import *

import requests


from Login import *
from PIL import Image, ImageTk
from entity.BaseApp import BaseApp
from entity.Bbox import Bbox
from entity.CategoryData import CategoryData
from entity.AnnotationData import AnnotationData
import os
import random
from Const import const
from io import BytesIO
import json
import copy
import pyperclip
import ctypes

from configobj import ConfigObj
# en_help_str_var = StringVar()
# en_help_str_var.set('Help')


class Main(BaseApp):

    def __init__(self, master):
        self.master=master
        # initialize global variable
        self.config = BaseApp.get_conifgObj()
        self.init_var()
        # make_menu_bar
        self.make_menu_bar()
        # make_ui
        self.make_ui()
        #bind_event
        self.bind_event()
        #get_data
        self.get_data()
        self.wel_hint()


    def wel_hint(self):
        # 欢迎登录问候语提示
        user_dict = {'TanXin': '老谭', 'Teng': '小胖墩儿', 'aoyipeng': '敖大', 'zhanyuqin1': '小占占', 'guoxiaodan': '小丹丹',
                     'zhangyu': '玉儿', 'wuweiling': '大喵', 'ZhangKe': '柯柯', 'fengdanjing': '小姐姐'}
        if self.config[const.LOGIN][const.ISWELCOMEMSG] == '1':
            # self.msgBox('噢耶%s登录成功了哟好棒的呢!	' % user_dict.get(BaseApp.user_info.user_name, ''))
            ctypes.windll.user32.MessageBoxA(0, ("噢耶%s登录成功了哟好棒的呢!" % user_dict.get(BaseApp.user_info.user_name, '小哥哥')).encode('gb2312'),
                                             u' 提示'.encode('gb2312'), 0)

    def init_var(self):
        self.cur_zoom_level = 1
        self.annotation_str_var = StringVar()
        self.category_str_var = StringVar()
        self.categoryObjsOfAll = []
        self.categoryObjsOfSearch = []
        self.categories = []
        self.h_line = None
        self.v_line = None
        self.r = 3  # ???
        self.init_dot = {}
        self.init_dot['zoom_level'] = None
        self.init_dot['x'] = None
        self.init_dot['y'] = None
        self.init_dot['sku_name'] = None
        self.tmp_dot = {}
        self.tmp_dot['x'] = None
        self.tmp_dot['y'] = None
        self.tmp_dot['zoom_level'] = None
        self.temp_rectangle_id = None
        self.bbox_list = []
        self.bbox_list_original = []
        self.copy_bbox_list = []
        self.info_label_id = 0
        self.info_label = None
        self.is_change_annotation_name = False
        self.is_change_coord = False
        self.truncated = ''
        self.annotation_curselection = 0
        self.is_online = False
        self.is_cursor_select = True
        self.images = []
        self.img_root_path = None
        self.annotation_dir_path = None
        self.annotations = []#
        self.annotations_list = []
        self.cur_annotation_index = 0
        self.cur_img_rotate = 0
        self.colors = ['#00ff00', '#ff0000', '#FF00FF', 'purple', '#0000ff','#FF4500', '#BB0000','#DB7093','#FF1493','#C71585','#FF00FF','#00FA9A','#00BFFF','#1E90FF']
        self.bd_width = 1
        self.is_stipple = 'gray12'#error, gray75, gray50, gray25, gray12, hourglass, info, questhead, question, 和 warning
        self.is_cn = 'cn'
        self.is_annotation=False
        self.cur_sku_lib=self.config[const.LOGIN][const.SKU_LIB]
        self.cur_img_index = int(self.config[const.LOGIN][self.cur_sku_lib+'_IMAGE_INDEX'])


    def randomcolor(self):
        colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        color = ""
        for i in range(6):
            color += colorArr[random.randint(0, 14)]
        return "#" + color

    def bind_event(self):
        # category_istbox_event_bind
        self.category_listbox.bind('<<ListboxSelect>>', self.select_correct_category)#<<ListboxSelect>>:选中item变化监听事件
        self.category_listbox.bind('<Double-Button-1>', lambda t:self.open_sku_lib(True))
        self.category_listbox.bind('<Escape>', self.cancel_select_category)
        self.category_listbox.bind('<Control-c>', self.copy_category_)
        # annotation_istbox_event_bind
        self.annotation_listbox.bind('<Button-3>', self.popup_menu)
        self.annotation_listbox.bind('<Delete>', self.delete_annotation)
        self.canvas.bind('<Delete>', self.delete_annotation)
        self.annotation_listbox.bind('<<ListboxSelect>>', self.show_bbox)
        self.annotation_listbox.bind('<Escape>', self.cancel_select)
        # canvas_event_bind
        self.canvas.bind("<Control-MouseWheel>", self.zoom_img)
        self.canvas.bind_all("<Control-r>", self.zoom_img_restore)
        self.canvas.bind("<Alt-MouseWheel>", self.rotate_img)
        self.canvas.bind("<MouseWheel>", self.v_bound_to_mousewheel)
        self.canvas.bind("<Shift-MouseWheel>", self.h__bound_to_mousewheel)
        self.canvas.bind('<Button-1>', self.mouse_click)
        self.canvas.bind('<Control-Button-1>', self.mouse_multi_select)
        self.canvas.bind('<Double-Button-1>', self.mouse_double_click)
        # self.canvas.bind('<KeyPress-Return>', self.mouse_double_click)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_right_release)
        self.canvas.bind('<ButtonRelease-3>', self.mouse_right_release)
        self.canvas.bind('<ButtonPress-3>', self.mouse_right_press)
        self.canvas.bind('<Motion>', self.mouse_move)

        self.canvas.bind("<KeyPress-Left>", self.prevImage)
        self.canvas.bind("<KeyPress-Up>", self.prevImage)
        # self.canvas.bind("<KeyPress-w>", self.prevImage)
        # self.canvas.bind("<KeyPress-a>", self.prevImage)
        self.canvas.bind("<KeyPress-Right>", self.nextImage)
        self.canvas.bind("<KeyPress-Down>", self.nextImage)
        self.canvas.bind("<ButtonPress-2>", self.cancel_select_category)

        self.canvas.bind("<Control-a>", self.show_all_bbox)
        self.canvas.bind("<KeyPress-space>", self.nextImage)
        self.canvas.bind("<Control-Shift-space>", self.prevImage)
        self.canvas.bind("<KeyPress-d>", self.nextImage)

        # self.canvas.bind("<KeyPress-s>", self.nextImage)#todo 和Ctrl+S冲突
        # scrollbar_event_bind
        self.v_scrollbar.bind("<MouseWheel>", self.v_bound_to_mousewheel)
        self.h_scrollbar.bind("<Shift-MouseWheel>", self.h__bound_to_mousewheel)
        self.v_scrollbar.bind("<Enter>", self._unbound_to_mousewheel)
        self.h_scrollbar.bind("<Enter>", self._unbound_to_mousewheel)
        # master_event_bind
        self.master.bind_all("<Control-o>", self.msgBox)
        self.master.bind_all("<Control-s>", self.save)
        self.master.bind_all("<Control-t>", self.toggle_annotation_style)
        self.master.bind_all("<Control-q>", self.master.quit())
        self.master.bind_all("<KeyPress-F1>",self.msgBox)
        self.master.bind_all("<KeyPress-F5>", self.refresh)
        self.master.bind_all('<Escape>', self.cancel_bbox)
        self.master.bind_all("<Control-x>", self.cut_bbox)
        self.master.bind_all("<Control-c>", self.copy_bbox)
        self.master.bind_all("<Control-v>", self.paste_bbox)
        self.master.bind_all("<Control-b>", self.clone_bbox)
        self.master.bind_all("<Control-z>", self.undo_operate)
        self.master.bind_all("<Control-y>", self.redo_operate)
        self.master.bind_all("<KeyPress-F2>", self.change_annotation_name)
        self.master.bind_all("<Control-i>", self.invert_select)
        # master.bind("<Left>", self.prevImage)
        # master.bind("<Right>", self.nextImage)
        # self.canvas.bind("<Up>", self.prevImage)
        # master.bind("<Down>", self.nextImage)
        # self.annotation_listbox.bind('<<ListboxSelect>>', self.msgBox)
        self.img_number_Entry.bind("<KeyPress-Return>",lambda t:self.get_data(self.img_number_Entry.get(),True))
    def open_sku_lib(self,isSearchTxt=False):
        txt=''
        if isSearchTxt:
            txt='-search '+self.category_listbox.get(self.category_listbox.curselection())+' -filter  SKU_LIB'
        win32api.ShellExecute(0, 'open',r'\\old_tan\Software Share\Everything\Everything.exe', txt, '', 1)
    def invert_select(self,*args):
        curselections = self.annotation_listbox.curselection()
        self.annotation_listbox.selection_set(0,END)
        if curselections:
            for i in curselections:
                self.annotation_listbox.selection_clear(i)
            self.show_bbox()
    def undo_operate(self, *args):
        if args and type(args[0].widget)==Entry :
            # print(args[0].widget)
            return
        if self.cur_annotation_index<1:
            return
        self.cur_annotation_index -= 1
        self.bbox_list=copy.deepcopy(self.annotations_list[self.cur_annotation_index])
        self.annotations_data_update()
        self.annotation_listbox.selection_set(0, END)
        self.show_bbox()


    def redo_operate(self, *args):
        if args and type(args[0].widget)==Entry :
            # print(args[0].widget)
            return
        if self.cur_annotation_index > len(self.annotations_list)-2:
            return
        self.cur_annotation_index += 1
        self.bbox_list = copy.deepcopy(self.annotations_list[self.cur_annotation_index])
        self.annotations_data_update()
        self.annotation_listbox.selection_set(0, END)
        self.show_bbox()


    def cut_bbox(self,*args):
        if args and type(args[0].widget) == Entry:
            # print(args[0].widget)
            return
        curselections = self.annotation_listbox.curselection()
        if curselections:
            self.copy_bbox_list.clear()
            for index in curselections:
                self.copy_bbox_list.append(self.bbox_list[index])
            self.delete_annotation()

    def copy_category_(self, *args):
        curselections = self.category_listbox.curselection()
        if curselections:
            text = self.categories[curselections[0]]
            pyperclip.copy(text)
    def copy_fileName(self, *args):
        if args and type(args[0].widget) == Entry:
            # print(args[0].widget)
            return
        curselections = self.annotation_listbox.curselection()
        if curselections:
            text=''
            for i in curselections:
                bbox = self.bbox_list[i]
                truncated = 0 if bbox.truncated == '' else int(bbox.truncated)
                text+= '%s_%s_%s_%s_%s_%s.jpg | ' % (self.images[self.cur_img_index].rstrip('.jpg'), bbox.x1, bbox.y1, bbox.x2, bbox.y2,truncated)
            text=text.rstrip(' | ')
            pyperclip.copy(text)
    def clone_bbox(self,*args):
        if args and type(args[0].widget)==Entry :
            # print(args[0].widget)
            return
        curselections = self.annotation_listbox.curselection()
        if curselections:
            copy_bbox_list = []
            # for index in curselections:
            #     copy_bbox_list.append(copy.deepcopy(self.bbox_list[index]))
            copy_bbox_list.append(copy.deepcopy(self.bbox_list[curselections[-1]]))

            start = len(self.bbox_list)
            for bbox in copy_bbox_list:
                self.bbox_list.append(bbox)
                bbox.username = BaseApp.user_info.user_name
                bbox.x1, bbox.x2 = bbox.x1 + abs(bbox.x2 - bbox.x1), bbox.x2 + abs(bbox.x2 - bbox.x1)
            if copy_bbox_list and len(copy_bbox_list) < 2:
                self.show_info_bbox(bbox)
            end = len(self.bbox_list) - 1
            # annotations update
            self.annotations_data_update()
            self.annotation_listbox.selection_clear(0, END)
            self.annotation_listbox.selection_set(start, end)
            print(start, end)
            self.show_bbox()
            # 数据缓存
            self.data_cache()
    def copy_bbox(self,*args):
        if args and type(args[0].widget)==Entry :
            # print(args[0].widget)
            return
        curselections = self.annotation_listbox.curselection()
        if curselections:
            self.copy_bbox_list.clear()
            for index in curselections:
                self.copy_bbox_list.append(self.bbox_list[index])
    def paste_bbox(self,*args):
        if args and type(args[0].widget)==Entry :
            # print(args[0].widget)
            return
        if  self.copy_bbox_list:
            #先删除选中item在粘贴
            curselections = self.annotation_listbox.curselection()
            if len(curselections) > 0:
                for curselection in reversed(curselections):
                    # print(curselection,self.annotations,self.bbox_list[curselection].sku_name,len(self.bbox_list))
                    self.annotations.pop(curselection)
                    self.canvas.delete(self.bbox_list[curselection].rectangle_id)
                    self.bbox_list.pop(curselection)
            start = len(self.bbox_list)
            for bbox in  self.copy_bbox_list:
                bbox.username=BaseApp.user_info.user_name
                self.bbox_list.append(bbox)
            if self.copy_bbox_list and len(self.copy_bbox_list)<2:
                self.show_info_bbox(bbox)
            end=len(self.bbox_list)-1
            # annotations update
            self.annotations_data_update()
            self.annotation_listbox.selection_clear(0,END)
            self.annotation_listbox.selection_set(start,end)
            print(start,end)
            self.show_bbox()
            #数据缓存
            self.data_cache()
    def cancel_select(self,*args):
        # state reset
        self.is_change_annotation_name = False
        self.is_change_coord = False
        self.cancel_bbox()

    def cancel_select_category(self,*args):
        # state reset
        self.category_listbox.selection_clear(0,END)
        self.cancel_bbox()
        self.is_change_coord=False
        self.is_change_annotation_name = False
        self.show_all_bbox()
    def make_ui(self):
        # layout
        self.category_frame = Frame(self.master, width='250')  # , bg='red')
        self.main_panel_frame = Frame(self.master)  # , bg='blue')
        self.annotation_frame = Frame(self.master, width='350')  # , bg='orange')
        self.status_bar_frame = Frame(self.master, bg='white', height=50)

        self.status_bar_frame.pack(side=BOTTOM, fill=X)
        self.category_frame.pack(side=LEFT, fill=Y)
        self.annotation_frame.pack(side=RIGHT, fill=Y)
        self.main_panel_frame.pack(side=TOP, fill=BOTH, expand=TRUE)
        # category_frame
        entry_change = self.master.register(self.entry_change)  # 需要将函数包装一下，必要的
        self.search_str_var=StringVar()
        self.search_str_var.set('搜索分类...')
        self.search_entry = Entry(self.category_frame,textvariable=self.search_str_var, validate='all', validatecommand=(entry_change, '%P','%V'),
                                  highlightcolor='red', insertbackground='red', insertwidth=3,
                                  relief='sunken',bd =5)  # relief:flat/sunken/raised/groove/ridge
        self.search_entry.pack(fill=X)
        # self.categories = list(map(lambda category:category.category, self.categoryObjsOfSearch))
        # self.category_str_var.set(self.categories)
        self.category_listbox = Listbox(self.category_frame, selectmode=BROWSE, height=80,width=30,bd=5,exportselection=True,
                                        listvariable=self.category_str_var)  # len(self.categorys)#width=0宽度自适应
        self.category_listbox.pack()
        self.category_v_scrollbar = Scrollbar(self.category_frame, orient=VERTICAL, command=self.category_listbox.yview)
        self.category_v_scrollbar.pack(side=RIGHT, fill=Y, before=self.category_listbox)
        self.category_h_scrollbar = Scrollbar(self.category_frame, orient=HORIZONTAL,
                                              command=self.category_listbox.xview)
        self.category_h_scrollbar.pack(side=BOTTOM, fill=X, before=self.category_listbox)
        self.category_listbox.config(yscrollcommand=self.category_v_scrollbar.set,
                                     xscrollcommand=self.category_h_scrollbar.set)
        # main_panel_frame
        self.h_scrollbar = Scrollbar(self.main_panel_frame, orient=HORIZONTAL)
        self.h_scrollbar.pack(side=BOTTOM, fill=X)
        self.v_scrollbar = Scrollbar(self.main_panel_frame, orient=VERTICAL)
        self.v_scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas = Canvas(self.main_panel_frame, width=0, height=0, scrollregion=(0, 0, 0, 0),bd=0,
                             cursor='tcross', yscrollcommand=self.v_scrollbar.set,
                             xscrollcommand=self.h_scrollbar.set)  # pencil tcross
        self.canvas.pack(fill=BOTH, expand=TRUE, side=LEFT)
        self.h_scrollbar.config(command=self.canvas.xview)
        self.v_scrollbar.config(command=self.canvas.yview)
        # annotation_frame
        self.annotation_listbox = Listbox(self.annotation_frame,width=30, height=80, selectmode=EXTENDED,bd=5,exportselection=False,
                                          listvariable=self.annotation_str_var)  # len(self.annotations)
        self.annotation_listbox.pack()
        self.annotation_v_scrollbar = Scrollbar(self.annotation_frame, orient=VERTICAL,
                                                command=self.annotation_listbox.yview)
        self.annotation_v_scrollbar.pack(side=RIGHT, fill=Y, before=self.annotation_listbox)
        self.annotation_h_scrollbar = Scrollbar(self.annotation_frame, orient=HORIZONTAL,
                                                command=self.annotation_listbox.xview)
        self.annotation_h_scrollbar.pack(side=BOTTOM, fill=X, before=self.annotation_listbox)
        self.annotation_listbox.config(yscrollcommand=self.annotation_v_scrollbar.set,
                                       xscrollcommand=self.annotation_h_scrollbar.set)
        # canvas.create_rectangle(50, 25, 150, 75)  # 左上角右下角的坐标
        # ---
        # self.img = Image.open(r"E:\Library\Pictures\1.jpg")
        # self.img_size = self.img.size
        # self.tk_img = ImageTk.PhotoImage(self.img)
        # self.canvas.config(scrollregion=(0, 0, self.img_size[0] * 2, self.img_size[1]))
        # self.cur_img_id = self.canvas.create_image((0, 0), image=self.tk_img, anchor=N + W)
        # ----
        # self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # status_bar_frame
        self.position = Label(self.status_bar_frame,width=10)
        self.position.pack(side='right',padx=10)
        self.angle = Label(self.status_bar_frame)
        self.angle.pack(side='right',padx=10)
        self.imgfile_name_StrVar = StringVar()
        self.percent = Label(self.status_bar_frame,text='100%')
        self.percent.pack(side='right',padx=10)
        self.user_label = Label(self.status_bar_frame,text=BaseApp.user_info.user_name)
        self.user_label.pack(side='right',padx=10)

        self.pre_btn = Button(self.status_bar_frame, bd=5,text='上一张<<', command=self.prevImage)
        self.pre_btn.pack(side='left',padx=10)
        self.next_btn = Button(self.status_bar_frame,bd=5, text='下一张>>', command=self.nextImage)
        self.next_btn.pack(side='left',padx=10)
        get_data=self.master.register(self.get_data)
        self.t=StringVar()
        self.t.set('搜索图片或者BBOX')
        self.img_number_Entry = Entry(self.status_bar_frame,width='24',validate='all',textvariable=self.t, validatecommand=(get_data,'%P',True,'%V') ,highlightcolor='red', insertbackground='red', insertwidth=3,relief='sunken',bd =5)  # relief:flat/sunken/raised/groove/ridge
        self.img_number_Entry.pack(side='left',padx=0)
        self.search_btn = Button(self.status_bar_frame, text='搜  索',bd=5, command=lambda :self.get_data(self.img_number_Entry.get(),True))
        self.search_btn.pack(side='left',padx=0)

        curselection = len(self.annotation_listbox.curselection())
        amount = len(self.bbox_list)
        self.state_label = Label(self.status_bar_frame, text='BBOX: %d/%d'% (curselection,amount))
        self.state_label.pack(side='left', padx=10)

    # todo category可变对象优化,如[{},{}]
    def entry_change(self,content,reason):
        try:
            if not content or (reason=='focusin' and not content):
                response = requests.get(const.DATA_ADDR[self.cur_sku_lib]['SKUS'])
                categories = CategoryData()
                categories.fromJson(response.json())  # json to model
                self.categoryObjsOfAll = categories.data.skus
                # 上色
                i = 0
                # print(self.categoryObjsOfAll[0].color)
                for category in self.categoryObjsOfAll:
                    category.color = self.colors[i]
                    if i < len(self.colors) - 1:
                        i += 1
                    else:
                        i = 0

                self.categories = list(map(lambda category: category.category, self.categoryObjsOfAll))
                self.category_str_var.set(self.categories)
                # for category,color in self.categoryObjsOfSearch.items():
                #     self.category_listbox.itemconfigure(fg=color)
                self.categoryObjsOfSearch = copy.deepcopy(self.categoryObjsOfAll)  # 深拷贝非引用赋值
                for i, category in enumerate(self.categoryObjsOfSearch):
                    self.category_listbox.itemconfigure(i, fg=category.color)
                self.category_listbox.selection_clear(0,END)
                self.category_listbox.selection_set(0)
                self.category_listbox.yview(0)
        except:
            pass

        if reason=='focusin':
            self.search_entry.selection_range(0, END)
            return True
        elif reason=='focusout':
            # if not content.strip(' '):
            #     self.search_str_var.set('搜索分类...')
            return True
        elif content == '搜索分类...':
            return True
        # elif reason=='key':
        def getObjsByKeyWords(category):
            # keywords=filter(lambda str:str==' ',keywords)
            keywords = content.split()
            if len(keywords) < 1:
                return True
            for keyword in keywords:
                if keyword not in category.category:
                    return False
            return True


        if self.categoryObjsOfAll:
            self.categoryObjsOfSearch = list(filter(getObjsByKeyWords, self.categoryObjsOfAll))
            self.categories = list(map(lambda category:category.category, self.categoryObjsOfSearch))
            self.category_str_var.set(self.categories)
            for i, categroy in enumerate(self.categoryObjsOfSearch):
                self.category_listbox.itemconfigure(i, fg=categroy.color)
        return True

    def toggle_annotation_style(self, *args):
        self.truncated = 1 if type(self.truncated) == str else ''

    def change_coord(self, *args):
        curselection = self.annotation_listbox.curselection()
        if len(curselection) == 1:
            self.annotation_curselection = curselection[0]
            self.is_change_coord = TRUE
            self.bbox_clear()

    def show_bbox(self, *args):
        self.bbox_clear()
        curselections = self.annotation_listbox.curselection()
        #更新BBox状态栏
        curselection = len(self.annotation_listbox.curselection())
        amount = len(self.bbox_list)
        self.state_label.configure(text='BBOX: %d/%d'% (curselection,amount))

        self.canvas.delete('info_label')
        for index in curselections:
            cur_bbox = self.bbox_list[index]
            # print(cur_bbox.truncated)
            dash = 1 if type(cur_bbox.truncated) == int else ''
            self.make_rectangle(cur_bbox, dash)
            #TODO 待优化
            #canvas滚动条定位
            # self.canvas.xview_moveto((1 / self.cur_img_size[0]) * cur_bbox.x1)
            # self.canvas.yview_moveto((1 / self.cur_img_size[1]) * (cur_bbox.y1 - 25))
            # self.canvas.update()
            #其他bbox隐藏
            for bbox in list(filter(lambda bbox: bbox.rectangle_id != cur_bbox.rectangle_id, self.bbox_list)):
                bbox.is_show=False
            if len(curselections)<2:
                self.show_info_bbox(cur_bbox)
            else:
                self.canvas.delete('info_label')

    def show_all_bbox(self, *args):
        self.bbox_clear()
        # cur_bbox = self.bbox_list[self.annotation_curselection]
        for bbox in self.bbox_list:
            # if self.is_change_coord and bbox.id==cur_bbox.id:
            #     continue
            dash = 1 if type(bbox.truncated) == int else ''
            self.make_rectangle(bbox, dash)
        self.annotation_listbox.selection_set(0,END)
        # 更新BBox状态栏
        curselection = len(self.annotation_listbox.curselection())
        amount = len(self.bbox_list)
        self.state_label.configure(text='BBOX: %d/%d'% (curselection,amount))

    def make_rectangle(self, bbox, dash):
        bbox.is_show=True
        rectangle_id = self.canvas.create_rectangle(self.getCoordByZoom(bbox.x1), self.getCoordByZoom(bbox.y1), self.getCoordByZoom(bbox.x2),
                                                    self.getCoordByZoom(bbox.y2),
                                                    width=self.bd_width, outline=bbox.color, dash=dash,stipple=self.is_stipple, fill=bbox.color,
                                                    tags=('bbox',))#stipple=self.is_stipple, fill=bbox.color,
        bbox.id=rectangle_id

    def hide_all_bbox(self, *args):
        self.canvas.delete('info_label')
        self.bbox_clear()
        self.annotation_listbox.selection_clear(0,END)
        # 更新BBox状态栏
        curselection = len(self.annotation_listbox.curselection())
        amount = len(self.bbox_list)
        self.state_label.configure(text='BBOX: %d/%d'% (curselection,amount))


    def is_cur_img_change(self):
        if not len(self.bbox_list_original) == len(self.bbox_list):
            return True
        for i,bbox in enumerate(self.bbox_list):
            truncated = 0 if type(bbox.truncated) == str else 1
            truncated_original = 0 if type(self.bbox_list_original[i].truncated) == str else 1
            if truncated!=truncated_original:			
                return True
            elif bbox.className!=self.bbox_list_original[i].className:
                return True
            elif bbox.x1!=self.bbox_list_original[i].x1 or bbox.y1!=self.bbox_list_original[i].y1 or bbox.x2!=self.bbox_list_original[i].x2 or bbox.y2!=self.bbox_list_original[i].y2 :
                return True
        return False
    def img_index_restore(self,isNext):
        if self.cur_img_index < 1:
            return None
        # 图片索引复原
        if isNext:
            self.cur_img_index -= 1
        else:
            self.cur_img_index += 1
    def save(self, isNext=1,*args):

        if not self.is_cur_img_change():
            return
        #标注数据更新
        self.annotationData.bboxes=copy.deepcopy(self.bbox_list)
        for bbox in self.annotationData.bboxes:
            # bbox.truncated = 1 if type(bbox.truncated) == int else 0
            bbox.truncated =0 if bbox.truncated==''else int(bbox.truncated)
        #图片数据更新
        self.annotationData.username=BaseApp.user_info.user_name#
        self.annotationData.rotate=self.cur_img_rotate
        self.annotationData.image=self.images[self.cur_img_index].split('.')[0]
        annotationDataOfjson=self.annotationData.toKeyValue()#dict
        annotationDataOfjson.pop('deleted')
        annotationDataOfjson.pop('id')
        annotationDataOfjson.pop('created_at')
        annotationDataOfjson.pop('updated_at')
        for bbox in annotationDataOfjson['bboxes']:
            bbox.pop('color')
            bbox.pop('rectangle_id')
            bbox.pop('is_show')
            # bbox.pop('_Bbox__annotation')
        annotationDataOfjsonStr=json.dumps(annotationDataOfjson)#dict->jsonStr用于存储和传输数据
        print(annotationDataOfjsonStr)

        #本地保存
        # config = BaseApp.get_conifgObj()
        config=self.config
        config[const.ANNOTATION_DATA]={}
        config[const.ANNOTATION_DATA][annotationDataOfjson['image']]=annotationDataOfjson
        config.write()

        # 网络保存
        response=None
        try:
            response = requests.post(const.DATA_ADDR[self.cur_sku_lib]['ANNOTATION_UPSERT'], json=json.loads(annotationDataOfjsonStr))
        except:
            self.msgBox(annotationDataOfjson['image'] + '保存失败!\n'+'服务器开小差啦！')
            # self.msgBox(annotationDataOfjson['image'] + '保存失败!')
            self.img_index_restore(isNext)
        if response and (response.ok or response.json()['message']=='Bboxes不能为空。'):
            #成功保存
            print('Image No. %s saved' % (self.images[self.cur_img_index]))
            self.bbox_list_original = copy.deepcopy(self.bbox_list)
            #删除本地备份
            # config = BaseApp.get_conifgObj()
            del config[const.ANNOTATION_DATA][annotationDataOfjson['image']]
            config.write()
            if isNext:
                self.nextImage()
            else:
                self.prevImage()
        elif response:
            print(response.json())
            self.msgBox(annotationDataOfjson['image'] + '保存失败!')
            #图片索引复原
            self.img_index_restore(isNext)
        # output_file_path = os.path.join(self.annotation_dir_path,
        #                                 os.path.splitext(self.images[self.cur_img_index])[0] + '.txt')
        # with open(output_file_path, 'w', encoding='UTF-8') as f:
        #     f.write('rotate %d\n' % int(self.cur_img_rotate))
        #     for bbox in self.bbox_list:
        #         is_dashed = '1' if type(bbox.is_dashed) == int else '0'
        #         content = ' '.join([bbox.category, ' '.join(map(str, bbox.coord)), is_dashed])
        #         f.write(content + '\n')



    def select_correct_category(self, event):
        category_listbox_curselection = self.category_listbox.curselection()
        if category_listbox_curselection:
            if self.is_change_annotation_name:
                # state reset
                self.is_change_annotation_name = False
                for curselection in reversed(self.annotation_curselection):
                    selected_category = self.categories[category_listbox_curselection[0]]
                    self.bbox_list[curselection].className = selected_category
                    self.bbox_list[curselection].color = self.getObjByCategory(selected_category).color
                    self.annotations[curselection] = self.bbox_list[curselection].annotation
                    self.bbox_list[curselection].username = self.user_info.user_name
                # refresh listbox variable
                self.annotation_str_var.set(self.annotations)

                for i, bbox in enumerate(self.bbox_list):
                    self.annotation_listbox.itemconfigure(i, fg=bbox.color)
                # 数据缓存
                self.data_cache()
            if self.config[const.LOGIN][const.ISLINKAGE] == '0' :
                return
            #选中分类item并显示对应的bbox
            self.bbox_clear()
            indexs=[]
            for i, bbox in enumerate(self.bbox_list):
                if bbox.className == self.categories[category_listbox_curselection[0]]:
                    indexs.append(i)
                    # dash = 1 if type(bbox.truncated) == int else ''
                    rectangle_id = self.canvas.create_rectangle(self.getCoordByZoom(bbox.x1), self.getCoordByZoom(bbox.y1), self.getCoordByZoom(bbox.x2),
                                                                self.getCoordByZoom(bbox.y2),
                                                                width=self.bd_width,
                                                                outline=self.getObjByCategory(bbox.className).color,
                                                                fill=self.getObjByCategory(bbox.className).color,
                                                                stipple=self.is_stipple,
                                                                dash=bbox.truncated,
                                                                tags='bbox' )
                    bbox.rectangle_id = rectangle_id
            self.annotation_listbox.selection_clear(0, END)
            for i in indexs:
                self.annotation_listbox.selection_set(i)
            # 更新BBox状态栏
            curselection = len(self.annotation_listbox.curselection())
            amount = len(self.bbox_list)
            self.state_label.configure(text='BBOX: %d/%d'% (curselection,amount))
    def bbox_clear(self):
        self.canvas.delete('bbox')#use('bbox','') instead of ('bbox',),will have bug
        # self.annotation_listbox.selection_clear(0, END)
        for bbox in self.bbox_list:
            bbox.is_show=False
    def popup_menu(self, event):
        self.editMenu.post(event.x_root, event.y_root)  # x_root与y_root表示右键点击的位置

    def cancel_bbox(self, *event):
        # self.msgBox()
        # delete preview box
        self.canvas.delete(self.temp_rectangle_id)
        # init_point initialized or reset
        self.init_dot_initialized()


    def cancelBBox(self):
        pass

    def prevImage(self,*args):
        if self.is_cur_img_change() :
            is_save = self.is_save()
            if is_save==6:
                self.save(False)
                return None
            elif is_save is 2:  # 点击了取消 6,7,2
                return None
        if self.cur_img_index < 1:
            return None
        self.cur_img_index -= 1
        imgName = self.images[self.cur_img_index]
        # print(imgName)
        response=None
        try:
            response=requests.get(const.DATA_ADDR[self.cur_sku_lib]['IMAGE'],{'file':imgName})
        except:
            self.msgBox('服务器开小差啦！')
            #图片索引复原
            self.cur_img_index += 1
        if response and  response.ok:
            self.config[const.LOGIN][self.cur_sku_lib + '_IMAGE_INDEX'] = self.cur_img_index
            self.config.write()
            self.open_img(BytesIO(response.content),imgName)
        elif response:
            self.cur_img_index += 1

    def nextImage(self,*args):
        if self.is_cur_img_change() :
            is_save = self.is_save()
            if is_save==6:
                self.save(True)
                return None
            elif is_save is 2:  # 点击了取消 6,7,2
                return None
        if self.cur_img_index > len(self.images) - 2:
            return None
        self.cur_img_index += 1
        imgName = self.images[self.cur_img_index]
        # print(imgName)
        response = None
        try:
            response=requests.get(const.DATA_ADDR[self.cur_sku_lib]['IMAGE'],{'file':imgName})
        except:
            self.msgBox('服务器开小差啦！')
            #图片索引复原
            self.cur_img_index -= 1
        if response and  response.ok:
            self.config[const.LOGIN][self.cur_sku_lib + '_IMAGE_INDEX'] = self.cur_img_index
            self.config.write()
            self.open_img(BytesIO(response.content),imgName)
        elif response:
            self.cur_img_index -= 1


    def mouse_right_press(self, event):
        event.x, event.y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)  # 窗口坐标系转换为画布坐标系
        if event.x < 0 or event.y < 0:
            return
        if event.x > self.cur_img_size[0] or event.y > self.cur_img_size[1]:
            return
        self.toggle_cursor()
        if not self.is_cursor_select:
            if  not self.is_cursor_select:
                self.canvas.delete(self.h_line)
                self.canvas.delete(self.v_line)
                self.canvas.config(cursor='arrow')
                # self.is_cursor_select=False
            else:
                self.canvas.config(cursor='tcross')
        self.tmp_dot['x'] = event.x
        self.tmp_dot['y'] = event.y
        self.tmp_dot['zoom_level']=self.cur_zoom_level
        # print(event)
        # print(event.state)
        # if event.num != 1:# or (event.num==1 and  self.is_cursor_select):#左击
        #     return
        if (self.is_cursor_select and event.num==3) or (not self.is_cursor_select and event.num==1):
            return
        min_item=self.getIndexOfCursor(event)
        try:
            index=self.bbox_list.index(min_item)
            self.show_info_bbox(min_item)

            #print(min_item.className)
        except:
            index=-1
        finally:
            if  index > -1:
                self.annotation_listbox.selection_clear(0, END)
                self.annotation_listbox.selection_set(index)
                self.annotation_listbox.yview(index)
                self.show_bbox()
    def mouse_multi_select(self, event):
        event.x, event.y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)  # 窗口坐标系转换为画布坐标系
        if event.x < 0 or event.y < 0:
            return
        if event.x > self.cur_img_size[0] or event.y > self.cur_img_size[1]:
            return
        self.toggle_cursor()
        if not self.is_cursor_select:
            if  not self.is_cursor_select:
                self.canvas.delete(self.h_line)
                self.canvas.delete(self.v_line)
                self.canvas.config(cursor='arrow')
                # self.is_cursor_select=False
            else:
                self.canvas.config(cursor='tcross')
        self.tmp_dot['x'] = event.x
        self.tmp_dot['y'] = event.y
        self.tmp_dot['zoom_level']=self.cur_zoom_level
        # print(event)
        # print(event.state)
        # if event.num != 1:# or (event.num==1 and  self.is_cursor_select):#左击
        #     return
        if (self.is_cursor_select and event.num==3) or (not self.is_cursor_select and event.num==1):
            return
        min_item=self.getIndexOfCursor(event)
        try:
            index=self.bbox_list.index(min_item)
            self.show_info_bbox(min_item)

            #print(min_item.className)
        except:
            index=-1
        finally:
            if  index > -1:
                curselection = self.annotation_listbox.curselection()
                if index in curselection:
                    self.annotation_listbox.selection_clear(index)
                else:
                    # self.annotation_listbox.selection_clear(0, END)
                    self.annotation_listbox.selection_set(index)
                self.annotation_listbox.yview(index)
                self.show_bbox()

    def mouse_double_click(self, event):

        if self.is_cursor_select:
            # self.mouse_right_press(event)
            self.change_coord()
    def mouse_click(self, event):
        if self.is_cursor_select:
            self.mouse_right_press(event)
        else:
            event.x, event.y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)  # 窗口坐标系转换为画布坐标系

            curselection_category = None
            if self.is_change_coord:
                curselection = self.annotation_listbox.curselection()
                if len(curselection) == 1:
                    curselection_category = self.bbox_list[curselection[0]].className

            else:
                curselections = self.category_listbox.curselection()
                if len(curselections) < 1:
                    self.msgBox('请选择分类!')
                    return None
                curselection_category = self.categories[curselections[0]]
            # print(curselection_category)
            if event.x<0:
                # self.msgBox('亲,坐标点不能越界哦!')
                event.x=0
                # return
            if event.y<0:
                event.y=0
                # return
            # if event.x > self.cur_img_size[0]:
            #     event.x = self.cur_img_size[0]
            # if  event.y > self.cur_img_size[1]:
            #     event.y = self.cur_img_size[1]

            if self.init_dot['zoom_level'] != None:
                # self.canvas.delete(self.init_dot['sku_name'])
                if self.init_dot['zoom_level'] != self.cur_zoom_level:
                    # coord scale
                    self.init_dot['x'] = (self.init_dot['x'] / self.init_dot['zoom_level']) * self.cur_zoom_level
                    self.init_dot['y'] = (self.init_dot['y'] / self.init_dot['zoom_level']) * self.cur_zoom_level
                    self.init_dot['zoom_level'] = self.cur_zoom_level
                if self.init_dot['x'] == event.x and self.init_dot['y'] == event.y:
                    self.msgBox('亲,标注圆点木有意义哦!')
                    return
                if self.init_dot['x'] == event.x or self.init_dot['y'] == event.y:
                    self.msgBox('亲,标注直线或极小的框木有意义哦!')
                    return
                # draw bbox
                if self.is_change_coord:
                    bbox = self.bbox_list[self.annotation_listbox.curselection()[0]]
                    truncated = bbox.truncated
                    truncated = 1 if type(truncated) == int else ''
                    rectangle_id = self.canvas.create_rectangle(self.init_dot['x'], self.init_dot['y'], event.x, event.y,
                                                                width=self.bd_width,
                                                                outline=self.getObjByCategory(bbox.className).color,
                                                                dash=truncated, tags=('bbox',))
                else:
                    rectangle_id = self.canvas.create_rectangle(self.init_dot['x'], self.init_dot['y'], event.x, event.y,
                                                                width=self.bd_width,
                                                                outline=self.getObjByCategory(curselection_category).color,
                                                                dash=self.truncated, tags=('bbox',))
                # new and add bbox object
                # if self.init_dot['zoom_level'] != 1:
                #     # coord scale
                #     self.init_dot['x'] = self.init_dot['x'] / self.init_dot['zoom_level']
                #     self.init_dot['y'] = self.init_dot['y'] / self.init_dot['zoom_level']
                x1=min(self.getCoordByRestore(self.init_dot['x']),self.getCoordByRestore(event.x))
                x2=max(self.getCoordByRestore(self.init_dot['x']),self.getCoordByRestore(event.x))
                y1=min(self.getCoordByRestore(self.init_dot['y']),self.getCoordByRestore(event.y))
                y2=max(self.getCoordByRestore(self.init_dot['y']),self.getCoordByRestore(event.y))

                bbox = Bbox(rectangle_id, curselection_category, self.getObjByCategory(curselection_category).color,const.USERNAME,self.truncated,
                            x1, y1, x2, y2)
                # self.canvas.tag_bind(CURRENT, '', self.show_box(bbox))
                self.show_info_bbox(bbox)
                if self.is_change_coord:
                    curselection_bbox = self.bbox_list[self.annotation_curselection]
                    curselection_bbox.x1,curselection_bbox.y1,curselection_bbox.x2,curselection_bbox.y2 = x1, y1, x2, y2
                    curselection_bbox.username=self.user_info.user_name
                    self.is_change_coord = False
                    self.annotations_data_update()
                else:
                    self.bbox_list.append(bbox)
                    self.annotations_data_update()
                    self.annotation_listbox.select_set(END)
                    self.annotation_listbox.yview(END)
                # annotations update

                # 更新BBox状态栏
                curselection = len(self.annotation_listbox.curselection())
                amount = len(self.bbox_list)
                self.state_label.configure(text='BBOX: %d/%d' % (curselection, amount))

                #self.show_bbox()
                # 数据缓存
                self.data_cache()
                # self.canvas.create_oval(
                #     (event.x - self.r, event.y - self.r, event.x + self.r, event.y + self.r), fill='black')
                self.init_dot_initialized()
            else:
                # self.init_dot['sku_name'] = self.canvas.create_oval(
                #     (event.x - self.r, event.y - self.r, event.x + self.r, event.y + self.r), fill='black')
                self.init_dot['zoom_level'] = self.cur_zoom_level
                self.init_dot['x'] = event.x
                self.init_dot['y'] = event.y

    def getCoordByRestore(self,coord):

        return int(coord//self.cur_zoom_level)

    def mouse_right_release(self, event):
        event.x,event.y=self.canvas.canvasx(event.x),self.canvas.canvasy(event.y)
        # cur_items = self.canvas.find_withtag(CURRENT)
        # print(cur_items)
        # print(list(map(lambda categoryObj: categoryObj.rectangle_id, self.bbox_list)))
        # if cur_items:
        #     for i,bbox in enumerate(self.bbox_list):
        #         if cur_items[-1]==bbox.rectangle_id:
        #             self.editMenu.post(event.x_root, event.y_root)
        #             self.annotation_listbox.selection_clear(0,END)
        #             self.annotation_listbox.selection_set(i)
        self.tmp_dot['x'] = None
        self.tmp_dot['zoom_level'] = None
        self.tmp_dot['y'] = None
        self.canvas.delete('tmp')
        # print(event)
        # print(event.type)
        if event.num==3:
            self.editMenu.post(event.x_root, event.y_root)


    def init_dot_initialized(self):
        self.init_dot['zoom_level'] = None
        self.init_dot['x'] = None
        self.init_dot['y'] = None
        self.init_dot['sku_name'] = None

    def annotations_data_update(self):
        self.annotations.clear()
        for i, bbox in enumerate(self.bbox_list):
            self.annotations.append(bbox.annotation)
        self.annotation_str_var.set(self.annotations)
        # self.annotation_listbox.select_set(END)
        # self.annotation_listbox.yview(END)
        for i, bbox in enumerate(self.bbox_list):
            self.annotation_listbox.itemconfigure(i, fg=bbox.color)
        # self.annotation_listbox.selection_set(0, END)
        # self.show_bbox()

    def mouse_move(self, event):
        event.x, event.y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)  # 窗口坐标系转换为画布坐标系
        # print('x=%d,y=%d' % (event.x, event.y))
        # if self.canvas.find_withtag(CURRENT)[0] !=self.cur_img_id:
        # print(self.canvas.find_withtag(CURRENT))
        # self.canvas.tag_bind(CURRENT, '', self.msgBox())

        tmp_dot_x = self.tmp_dot['x']
        tmp_dot_y = self.tmp_dot['y']
        if tmp_dot_x:
            self.canvas.delete('tmp')
            if self.tmp_dot['zoom_level'] != self.cur_zoom_level:
                # coord scale
                self.tmp_dot['x'] = (self.tmp_dot['x'] / self.tmp_dot['zoom_level']) * self.cur_zoom_level
                self.tmp_dot['y'] = (self.tmp_dot['y'] / self.tmp_dot['zoom_level']) * self.cur_zoom_level
                self.tmp_dot['zoom_level'] = self.cur_zoom_level
            self.canvas.create_rectangle(tmp_dot_x, tmp_dot_y, event.x,
                                         event.y,
                                         width=self.bd_width, fill='#0000FF', stipple=self.is_stipple,
                                         outline='#0000FF', tags=('tmp',))
            indexs=[]
            for i,bbox in enumerate(self.bbox_list):
                r_x,r_y= (event.x + tmp_dot_x) // 2, (event.y + tmp_dot_y) // 2
                bbox_x2 = self.getCoordByZoom(bbox.x2)
                bbox_x1 = self.getCoordByZoom(bbox.x1)
                bbox_y1 = self.getCoordByZoom(bbox.y1)
                bbox_y2 = self.getCoordByZoom(bbox.y2)
                bbox_x,bbox_y= (bbox_x2 +bbox_x1) // 2, (bbox_y2 + bbox_y1) // 2
                if abs(r_x-bbox_x)<(abs(bbox_x2 - bbox_x1) // 2 + abs(event.x - tmp_dot_x) // 2) and abs(r_y - bbox_y)<(abs(
                        bbox_y2 - bbox_y1) // 2 + abs(event.y - tmp_dot_y) // 2):
                    indexs.append(i)

            self.annotation_listbox.selection_clear(0, END)
            if indexs:
                for i in indexs:
                    self.annotation_listbox.selection_set(i)
                self.annotation_listbox.yview(indexs[0])
                self.show_bbox()
            else:
                self.hide_all_bbox()
            return
        curselection = self.category_listbox.curselection()
        if   len(curselection) or self.is_change_coord:
            # is_allow=False
            if event.x > self.cur_img_size[0] or event.y > self.cur_img_size[1]:
                self.is_cursor_select = True
            else:
                self.is_cursor_select = False
            self.toggle_cursor()
        else :
            # is_allow=True
            self.is_cursor_select=True
            self.toggle_cursor()


        if  self.is_cursor_select :
            pass
        else:
            self.position.configure(text='%d : %d' % (event.x, event.y))
            if self.h_line:
                self.canvas.delete(self.h_line)
            self.h_line = self.canvas.create_line(0, event.y, self.cur_img_size[0], event.y, width=1,fill='red')
            if self.v_line:
                self.canvas.delete(self.v_line)
            self.v_line = self.canvas.create_line(event.x, 0, event.x, self.cur_img_size[1], width=1,fill='red')

            self.make_preview_box(event)

        min_item=self.getIndexOfCursor(event)
        try:
            index=self.bbox_list.index(min_item)
            if self.config[const.LOGIN][const.ISPOLL] != '1':
                self.show_info_bbox(min_item)
            self.canvas.focus_set()
            #print(min_item.className)
        except:
            index=-1
        finally:
            if not self.is_annotation and self.config[const.LOGIN][const.ISPOLL] == '1' and index>-1:
                self.annotation_listbox.selection_clear(0, END)
                self.annotation_listbox.selection_set(index)
                self.annotation_listbox.yview(index)
                self.show_bbox()
            elif True:
                pass
        # cur_items = self.canvas.find_withtag(CURRENT)
        # if cur_items:
        #     if cur_items[-1] == self.cur_img_id:
        #         self.canvas.delete('info_label')
        # for bbox in self.bbox_list:
        #     if cur_items[-1] == bbox.rectangle_id:
        #         self.show_info_bbox(bbox)

    def getIndexOfCursor(self,event):
        cur_items = self.canvas.find_withtag(CURRENT)
        if cur_items:
            if cur_items[-1] == self.cur_img_id:
                self.canvas.delete('info_label')
        if self.is_change_coord:
            return
        items = []
        for i, bbox in enumerate(self.bbox_list):
            xMin = self.getCoordByZoom(min(bbox.x1, bbox.x2))
            xMax = self.getCoordByZoom(max(bbox.x1, bbox.x2))
            yMin = self.getCoordByZoom(min(bbox.y1, bbox.y2))
            yMax = self.getCoordByZoom(max(bbox.y1, bbox.y2))
            if event.x > xMin and event.x < xMax and event.y > yMin and event.y < yMax:
                # if event.x in range(xMin,xMax) and event.y in range(yMin ,yMax):
                items.append(bbox)
                # self.show_info_bbox(bbox)

                # if not self.canvas.find_withtag(bbox.sku_name):
                # self.bbox_clear()
                # dash = 1 if type(bbox.truncated) == int else ''
                # self.make_recttangle(bbox,dash)
        belong_items = []
        for i, bbox in enumerate(items):
            if i < len(items) - 1:
                bbox_next = items[i + 1]
                x1 = int(self.getCoordByZoom(bbox.x1))
                y1 = int(self.getCoordByZoom(bbox.y1))
                y2 = int(self.getCoordByZoom(bbox.y2))
                x2 = int(self.getCoordByZoom(bbox.x2))
                x1_next = int(self.getCoordByZoom(bbox_next.x1))
                x2_next = int(self.getCoordByZoom(bbox_next.x2))
                y1_next = int(self.getCoordByZoom(bbox_next.y1))
                y2_next = int(self.getCoordByZoom(bbox_next.y2))
                if x1 in range(x1_next - 2, x2_next + 2) and x2 in range(x1_next - 2, x2_next + 2) and y1 in range(
                        y1_next - 2, y2_next + 2) and y2 in range(y1_next - 2, y2_next + 2):
                    try:
                        belong_items.index(bbox)
                    except:
                        belong_items.append(bbox)
                    try:
                        belong_items.index(bbox_next)
                    except:
                        belong_items.append(bbox_next)
                else:
                    if x1_next in range(x1 - 2, x2 + 2) and x2_next in range(x1 - 2, x2 + 2) and y1_next in range(
                            y1 - 2, y2 + 2) and y2_next in range(y1 - 2, y2 + 2):
                        try:
                            belong_items.index(bbox)
                        except:
                            belong_items.append(bbox)
                        try:
                            belong_items.index(bbox_next)
                        except:
                            belong_items.append(bbox_next)

                # print(bbox_next.className)
        if belong_items:
            # print(len(items))
            # print(len(belong_items))
            min_item = belong_items[0]
            for i, bbox in enumerate(belong_items):
                if i < len(belong_items) - 1:
                    bbox_next = belong_items[i + 1]
                    x2_min = self.getCoordByZoom(min_item.x2)
                    x1_min = self.getCoordByZoom(min_item.x1)
                    y2_min = self.getCoordByZoom(min_item.y2)
                    y1_min = self.getCoordByZoom(min_item.y1)
                    y2_next = self.getCoordByZoom(bbox_next.y2)
                    y1_next = self.getCoordByZoom(bbox_next.y1)
                    if (x2_min - x1_min) < (bbox_next.x2 - bbox_next.x1) and (y2_min - y1_min) < (y2_next - y1_next):
                        pass
                        # print(min_item.className)
                        # print(bbox_next.className)
                    else:
                        min_item = bbox_next
            return min_item
        else:
            if items:
                return  items[-1]
            else:
                return None
    def zoom_img(self, event):
        if event.delta > 0:
            if self.cur_zoom_level > 2.0:
                return None
            else:
                self.cur_zoom_level += 0.1
        else:
            if self.cur_zoom_level < 0.2:
                return None
            else:
                self.cur_zoom_level -= 0.1

        img_rotate = self.img.rotate(self.cur_img_rotate, expand=True)


        w, h = self.img_size
        zoom_width = w * self.cur_zoom_level
        zoom_height = h * self.cur_zoom_level
        img_resize = self.resize(zoom_width, zoom_height, zoom_width, zoom_height, img_rotate)
        self.cur_img_size=img_resize.size
        # img_resize = self.img.resize((int(zoom_width), int(zoom_height)))
        # img_rotate = self.img.cur_img_rotate(45)
        # self.img.resize((w  * 2, h * 2), Image.ANTIALIAS)
        self.tk_img = ImageTk.PhotoImage(img_resize)
        self.canvas.itemconfigure(self.cur_img_id, image=self.tk_img, anchor=N + W)
        # self.canvas.config(scrollregion=(0, 0, self.img_size[0] * 2, self.img_size[1]))
        # self.canvas.config(scrollregion=(0,0,self.zoom_width*2, self.zoom_height*2))
        # self.canvas.config(width=zoom_width,height=zoom_height)

        # show
        self.percent.configure(text='%d%%' % (self.cur_zoom_level*100))
        print(str(self.cur_zoom_level * 10) + "%", self.main_panel_frame.winfo_height() - zoom_height, self.img.size)
        # preview_box zoom
        self.make_preview_box(event)
        # bbox zoom
        # for bbox in self.bbox_list:
        #     # coord zoom
        #     x = self.getCoordByZoom(bbox.x1)
        #     y = self.getCoordByZoom(bbox.y1)
        #     x1 = self.getCoordByZoom(bbox.x2 )
        #     y1 = self.getCoordByZoom(bbox.y2)
        #     self.canvas.coords(bbox.sku_name, (x, y, x1, y1))

        curselections = self.annotation_listbox.curselection()
        if len(curselections)<2:
            self.show_bbox()
        else:
            self.show_all_bbox(self.annotation_curselection)#todo 框缩放的bug临时解决方案
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
    def zoom_img_restore(self, event):
        self.cur_zoom_level = 1.0
        img_rotate = self.img.rotate(self.cur_img_rotate, expand=True)


        w, h = self.img_size
        zoom_width = w * self.cur_zoom_level
        zoom_height = h * self.cur_zoom_level
        img_resize = self.resize(zoom_width, zoom_height, zoom_width, zoom_height, img_rotate)
        self.cur_img_size=img_resize.size
        # img_resize = self.img.resize((int(zoom_width), int(zoom_height)))
        # img_rotate = self.img.cur_img_rotate(45)
        # self.img.resize((w  * 2, h * 2), Image.ANTIALIAS)
        self.tk_img = ImageTk.PhotoImage(img_resize)
        self.canvas.itemconfigure(self.cur_img_id, image=self.tk_img, anchor=N + W)
        # self.canvas.config(scrollregion=(0, 0, self.img_size[0] * 2, self.img_size[1]))
        # self.canvas.config(scrollregion=(0,0,self.zoom_width*2, self.zoom_height*2))
        # self.canvas.config(width=zoom_width,height=zoom_height)

        # show
        self.percent.configure(text='%d%%' % (self.cur_zoom_level*100))
        print(str(self.cur_zoom_level * 10) + "%", self.main_panel_frame.winfo_height() - zoom_height, self.img.size)
        # preview_box zoom
        self.make_preview_box(event)
        # bbox zoom
        # for bbox in self.bbox_list:
        #     # coord zoom
        #     x = self.getCoordByZoom(bbox.x1)
        #     y = self.getCoordByZoom(bbox.y1)
        #     x1 = self.getCoordByZoom(bbox.x2 )
        #     y1 = self.getCoordByZoom(bbox.y2)
        #     self.canvas.coords(bbox.sku_name, (x, y, x1, y1))

        curselections = self.annotation_listbox.curselection()
        if len(curselections)<2:
            self.show_bbox()
        else:
            self.show_all_bbox(self.annotation_curselection)#todo 框缩放的bug临时解决方案
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

    def make_preview_box(self, event):
        curselections = self.category_listbox.curselection()

        if curselections:
            curselection_category = self.categories[curselections[0]]
        if self.init_dot['zoom_level'] != None :
            self.canvas.delete(self.temp_rectangle_id)
            # print(self.init_dot['x'], self.init_dot['y'])
            if self.init_dot['zoom_level'] != self.cur_zoom_level:
                # coord scale
                self.init_dot['x'] = (self.init_dot['x'] / self.init_dot['zoom_level']) * self.cur_zoom_level
                self.init_dot['y'] = (self.init_dot['y'] / self.init_dot['zoom_level']) * self.cur_zoom_level
                self.init_dot['zoom_level'] = self.cur_zoom_level
                # print(self.init_dot['x'],self.init_dot['y'])
            if self.is_change_coord:
                curselection = self.annotation_listbox.curselection()
                if len(curselection) < 1:
                    self.is_change_coord = False
                    return None
                cur_bbox = self.bbox_list[curselection[0]]
                curselection_category = cur_bbox.className
                truncated = cur_bbox.truncated
                truncated = 1 if type(truncated) == int else ''
                self.temp_rectangle_id = self.canvas.create_rectangle(self.init_dot['x'], self.init_dot['y'], event.x,
                                                                      event.y,
                                                                      width=self.bd_width,
                                                                      dash=self.truncated,
                                                                      outline=self.getObjByCategory(
                                                                          cur_bbox.className).color,
                                                                      tags=('bbox',))
            else:
                self.temp_rectangle_id = self.canvas.create_rectangle(self.init_dot['x'], self.init_dot['y'], event.x,
                                                                      event.y,
                                                                      width=self.bd_width,
                                                                      dash=self.truncated,
                                                                      outline=self.getObjByCategory(
                                                                          curselection_category).color, tags=('bbox',))
                # Bbox(0,curselection_category,(self.init_dot['x'], self.init_dot['y'], event.x,
                #                               event.y),'','red',0)
            # if curselections:
                # self, rectangle_id = "", className = "", color = "", username = None, truncated = 0, x1 = 0, y1 = 0, x2 = 0, y2 = 0, side_truncated = 0, type_id = "1", sceneType = "-1", id = "", check = "False", score = 0, type = "0")
            self.show_info_bbox(Bbox(0,curselection_category,'','',0,self.getCoordByRestore(self.init_dot['x']), self.getCoordByRestore(self.init_dot['y']), self.getCoordByRestore(event.x),self.getCoordByRestore(event.y)))

    def _unbound_to_mousewheel(self, event):
        self.v_scrollbar.unbind_all("<MouseWheel>")
        self.h_scrollbar.unbind("<MouseWheel>")

    def h__bound_to_mousewheel(self, event):
        self.canvas.xview_scroll(-1 * (event.delta // 120), "units")

    def v_bound_to_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def show_info_bbox(self, bbox):
        # info_label = self.canvas.find_withtag('info_label')
        username=' '+bbox.username if bbox.username else ''
        x1=min(self.getCoordByZoom(bbox.x1),self.getCoordByZoom(bbox.x2))
        x2=max(self.getCoordByZoom(bbox.x1),self.getCoordByZoom(bbox.x2))
        y1=min(self.getCoordByZoom(bbox.y1),self.getCoordByZoom(bbox.y2))
        y2=max(self.getCoordByZoom(bbox.y1),self.getCoordByZoom(bbox.y2))
        value = bbox.className+username
        length = len(value)
        utf8_length = len(value.encode('utf-8'))
        cn_nums=(utf8_length - length) // 2
        letters=length-cn_nums
        # length = cn_nums + length
        cn_width = 12
        letter_width = 8
        offset=10
        deviation=2
        info_width= cn_nums * cn_width + letters * letter_width
        # print(info_width)
        #中心点
        center_x,center_y=(x1 + (x2 - x1) / 2),y1-cn_width/2-offset
        img_scroll_x=self.cur_img_size[0]*self.h_scrollbar.get()[0]
        img_scroll_y=self.cur_img_size[1]*self.v_scrollbar.get()[0]
        info_bbox_x1=center_x-info_width/2-img_scroll_x
        info_bbox_y1=center_y-(cn_width)/2-img_scroll_y
        info_bbox_x2=center_x+info_width/2-img_scroll_x
        info_bbox_y2=center_y+(cn_width+offset)/2-img_scroll_y
        if info_bbox_x1<0 and info_bbox_y1<0:#WN
            center_x=info_width/2+img_scroll_x
            center_y= y2 + (letter_width+offset)
            # print(center_x, center_y,W+N)
        elif info_bbox_x2>self.canvas.winfo_width() and info_bbox_y1 < 0:#EN
            center_x = self.canvas.winfo_width() - info_width / 2+img_scroll_x-deviation
            center_y = y2 + (letter_width+offset)
            # print(center_x, center_y,E+N)
        elif info_bbox_x2>self.cur_img_size[0]-img_scroll_x and info_bbox_y1 < 0:#EN
            center_x = self.cur_img_size[0]-img_scroll_x-info_width / 2-deviation
            center_y = y2 + (letter_width+offset)
            # print(center_x, center_y,E+N)
        elif info_bbox_y1 < 0:#N
            center_y = y2 + (letter_width+offset)
            # print(center_x, center_y,info_bbox_y1,(cn_width+offset),N)
        elif  info_bbox_x1<0:#W
            center_x = img_scroll_x+info_width/2
            # print(center_x, center_y,W)
        elif info_bbox_x2>self.canvas.winfo_width():#E
            center_x = self.canvas.winfo_width()-info_width / 2+img_scroll_x-deviation
            # print(center_x, center_y, E)
        elif info_bbox_x2>self.cur_img_size[0]-img_scroll_x:#E
            center_x = self.cur_img_size[0]-img_scroll_x-info_width / 2-deviation
            # print(cen/ter_x, center_y, E)

        self.canvas.delete('info_label')
        x1_ =center_x - info_width / 2
        y1_ =center_y - 10
        x2_ = center_x + info_width / 2
        y2_ =center_y + 10
        self.canvas.create_rectangle(x1_, y1_, x2_, y2_, fill='white', tags='info_label', outline='#fff')
        # print(self.canvas.canvasx(x1_,), y1_, x2_, y2_)
        self.canvas.create_text(center_x, center_y, text=bbox.className+username, tags="info_label")
        # self.info_label_id = self.canvas.create_window(center_x, center_y, window=self.info_label,tags='info_label')

    def getCoordByZoom(self,coord):
        return coord*self.cur_zoom_level

    def resize(self, w, h, w_box, h_box, pil_image):
        '''
        resize a pil_image object so it will fit into
        a box of size w_box times h_box, but retain aspect ratio
        '''
        f1 = 1.0 * w_box / w  # 1.0 forces float division in Python2
        f2 = 1.0 * h_box / h
        factor = min([f1, f2])
        # print(f1, f2, factor) # test
        # use best down-sizing filter
        width = int(w * factor)
        height = int(h * factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    def make_menu_bar(self,*args):
        self.is_cn=self.config[const.LOGIN][const.LANGUAGE]

        if self.is_cn=='cn':
            self.MENU_BAR=const.CN_MENU_ITEMS
            self.MENU_FILE_ITEMS=const.CN_FILE_MENU_ITEMS
            self.MENU_EDIT_ITEMS=const.CN_EDIT_MENU_ITEMS
            self.MENU_VIEW_ITEMS=const.CN_VIEW_MENU_ITEMS
            self.MENU_TOOLS_ITEMS=const.CN_TOOLS_MENU_ITEMS
            self.MENU_LANGUAGE_ITEMS=const.CN_LANGUAGE_MENU_ITEMS
            self.MENU_HELP_ITEMS=const.CN_HELP_MENU_ITEMS

        elif self.is_cn=='en':
            self.MENU_BAR=const.EN_MENU_ITEMS
            self.MENU_FILE_ITEMS = const.EN_FILE_MENU_ITEMS
            self.MENU_EDIT_ITEMS = const.EN_EDIT_MENU_ITEMS
            self.MENU_VIEW_ITEMS = const.EN_VIEW_MENU_ITEMS
            self.MENU_TOOLS_ITEMS = const.EN_TOOLS_MENU_ITEMS
            self.MENU_LANGUAGE_ITEMS = const.EN_LANGUAGE_MENU_ITEMS
            self.MENU_HELP_ITEMS = const.EN_HELP_MENU_ITEMS

        self.cur_sku_lib = self.config[const.LOGIN][const.SKU_LIB]
        self.menu = Menu(self.master)
        #file_menu
        self.fileMenu = Menu(self.menu, tearoff=False)
        self.fileMenu.add_command(label=self.MENU_FILE_ITEMS['open'], command=self.msgBox, accelerator='Ctr+O')
        self.fileMenu.add_command(label=self.MENU_FILE_ITEMS['save'], command=self.save, accelerator="Ctrl+S")
        self.fileMenu.add_command(label=self.MENU_FILE_ITEMS['openWindow'], command=self.msgBox, accelerator="")
        self.fileMenu.add_command(label=self.MENU_FILE_ITEMS['importData'], command=self.msgBox, accelerator="")
        self.fileMenu.add_command(label=self.MENU_FILE_ITEMS['exportData'], command=self.msgBox, accelerator="")
        self.fileMenu.add_command(label=self.MENU_FILE_ITEMS['autoBackup'], command=self.msgBox, accelerator="")
        self.fileMenu.add_command(label=self.MENU_FILE_ITEMS['openSKULib'], command=self.open_sku_lib, accelerator="")
        self.fileMenu.add_separator()#分割线
        self.fileMenu.add_command(label=self.MENU_FILE_ITEMS['exit'], command=self.master.quit, accelerator="Ctrl+Q")
        self.menu.add_cascade(label=self.MENU_BAR['file'], menu=self.fileMenu)
        #eidt_menu
        self.editMenu = Menu(self.menu, tearoff=0)
        #self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['refresh'], command=self.msgBox, accelerator="")
        #self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['toggleCursor'], command=self.toggle_cursor, accelerator="")
        #self.editMenu.add_separator()#分割线
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['editCategory'], command=self.change_annotation_name, accelerator="F2")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['editCoord'], command=self.change_coord, accelerator="左键双击")
        # editProperty
        self.editProperty = Menu(self.editMenu, tearoff=0)
        self.property0_StringVar = BooleanVar()
        self.property0_StringVar.set(False)
        self.property1_StringVar = BooleanVar()
        self.property1_StringVar.set(False)
        self.property2_StringVar = BooleanVar()
        self.property2_StringVar.set(False)
        self.editProperty.add_checkbutton(label='无',
                                          command=lambda: self.property_rdBtn_callback('无'), variable=self.property0_StringVar,
                                          onvalue=True)  # value=0为默认选中
        self.editProperty.add_checkbutton(label='属性0',
                                          command=lambda: self.property_rdBtn_callback('属性0'), variable=self.property1_StringVar,
                                          onvalue=True)
        self.editProperty.add_checkbutton(label='属性1',
                                          command=lambda: self.property_rdBtn_callback('属性1'), variable=self.property2_StringVar,
                                          onvalue=True)
        # self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['editProperty'], command=self.change_coord, accelerator="")
        self.editMenu.add_cascade(label=self.MENU_EDIT_ITEMS['editProperty'], menu=self.editProperty)
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['deleteCategory'], command=self.delete_annotation, accelerator="Delete")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['copyCategory'], command=self.copy_category, accelerator="")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['copyFileName'], command=self.copy_fileName, accelerator="")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['copyBBOX'], command=self.copy_bbox, accelerator="Ctrl+C")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['pasteBBOX'], command=self.paste_bbox, accelerator="Ctrl+V")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['cutBBOX'], command=self.cut_bbox, accelerator="Ctrl+X")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['toggleStyle'], command=self.toggle_style, accelerator="")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['undo'], command=self.undo_operate, accelerator="Ctrl+Z")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['restore'], command=self.redo_operate, accelerator="Ctrl+Y")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['showALl'], command=self.show_all_bbox, accelerator="Ctrl+A")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['invertSelect'], command=self.invert_select, accelerator="Ctrl+I")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['hideALl'], command=self.hide_all_bbox, accelerator="Esc")

        self.menu.add_cascade(label=self.MENU_BAR['edit'], menu=self.editMenu)
        #view_menu
        self.viewMenu = Menu(self.menu, tearoff=0)
        self.pollmode_StrVar = StringVar()
        self.pollmode_StrVar.set('pollmode' if self.config[const.LOGIN][const.ISPOLL] == '1' else None)
        self.linkage_StrVar = StringVar()
        self.linkage_StrVar.set('linkage' if self.config[const.LOGIN][const.ISLINKAGE] == '1' else None)
        self.viewMenu.add_checkbutton(label=self.MENU_VIEW_ITEMS['linkage'], command=self.ckBtn_callback,
                                         variable=self.linkage_StrVar, onvalue='linkage')
        self.viewMenu.add_checkbutton(label=self.MENU_VIEW_ITEMS['pollmode'], command=self.ckBtn_callback,
                                      variable=self.pollmode_StrVar, onvalue='pollmode')
        self.viewMenu.add_command(label=self.MENU_VIEW_ITEMS['autoLocation'], command=self.msgBox, accelerator="")
        self.viewMenu.add_command(label=self.MENU_VIEW_ITEMS['refresh'], command=self.refresh, accelerator="F5")

        self.toggleSKUMenu = Menu(self.viewMenu, tearoff=0)
        self.rdBtn_IntVar_SKU = IntVar()
        
        # for key in const.DATA_ADDR.keys():
        #     self.toggleSKUMenu.add_radiobutton(label=self.MENU_VIEW_ITEMS[key],
        #                                        command=lambda : self.rdBtn_callback(key), variable=self.rdBtn_IntVar_SKU,
        #                                        value=0 if self.cur_sku_lib == key else 1)  # value=0为默认选中

        self.toggleSKUMenu.add_radiobutton(label=self.MENU_VIEW_ITEMS['SKU'],
                                               command=lambda: self.rdBtn_callback('SKU'), variable=self.rdBtn_IntVar_SKU,
                                               value=0 if self.cur_sku_lib == 'SKU' else 1)  # value=0为默认选中
        self.toggleSKUMenu.add_radiobutton(label=self.MENU_VIEW_ITEMS['SKU_MARS'],
                                               command=lambda: self.rdBtn_callback('SKU_MARS'), variable=self.rdBtn_IntVar_SKU,
                                               value=0 if self.cur_sku_lib == 'SKU_MARS' else 1)  # value=0为默认选中
        self.toggleSKUMenu.add_radiobutton(label=self.MENU_VIEW_ITEMS['SKU_MOUTH'],
                                           command=lambda: self.rdBtn_callback('SKU_MOUTH'),
                                           variable=self.rdBtn_IntVar_SKU,
                                           value=0 if self.cur_sku_lib == 'SKU_MOUTH' else 1)  # value=0为默认选中
        self.toggleSKUMenu.add_radiobutton(label=self.MENU_VIEW_ITEMS['SKU_SEASONING'],
                                           command=lambda: self.rdBtn_callback('SKU_SEASONING'),
                                           variable=self.rdBtn_IntVar_SKU,
                                           value=0 if self.cur_sku_lib == 'SKU_SEASONING' else 1)  # value=0为默认选中
        self.toggleSKUMenu.add_radiobutton(label=self.MENU_VIEW_ITEMS['SKU_CLEANING'],
                                           command=lambda: self.rdBtn_callback('SKU_CLEANING'),
                                           variable=self.rdBtn_IntVar_SKU,
                                           value=0 if self.cur_sku_lib == 'SKU_CLEANING' else 1)  # value=0为默认选中
        self.toggleSKUMenu.add_radiobutton(label=self.MENU_VIEW_ITEMS['SKU_MB_PRODUCTS'],
                                           command=lambda: self.rdBtn_callback('SKU_MB_PRODUCTS'),
                                           variable=self.rdBtn_IntVar_SKU,
                                           value=0 if self.cur_sku_lib == 'SKU_MB_PRODUCTS' else 1)  # value=0为默认选中
        self.viewMenu.add_cascade(label=self.MENU_VIEW_ITEMS['toggleSKU'], menu=self.toggleSKUMenu)

        self.menu.add_cascade(label=self.MENU_BAR['view'], menu=self.viewMenu)
        #tools_menu
        self.ToolsMenu = Menu(self.menu, tearoff=0)
        self.ToolsMenu.add_command(label=self.MENU_TOOLS_ITEMS['semiAuto'], command=self.msgBox, accelerator="")

        self.OptionsMenu = Menu(self.ToolsMenu, tearoff=0)
        self.autologin_StrVar = StringVar()
        self.welcome_StrVar = StringVar()
        self.poweron_StrVar = StringVar()
        #读取并设置为配置文件中的状态值
        self.autologin_StrVar.set('autologin' if self.config[const.LOGIN][const.ISAUTOLOGIN]=='1' else None)
        self.welcome_StrVar.set('welcome' if self.config[const.LOGIN][const.ISWELCOMEMSG]=='1' else None)
        self.poweron_StrVar.set('poweron' if self.config[const.LOGIN][const.ISPOWERON]=='1' else None)

        self.OptionsMenu.add_checkbutton(label=self.MENU_TOOLS_ITEMS['autologin'], command=self.ckBtn_callback, variable=self.autologin_StrVar,onvalue='autologin')
        self.OptionsMenu.add_checkbutton(label=self.MENU_TOOLS_ITEMS['welcome'], command=self.ckBtn_callback,  variable=self.welcome_StrVar,onvalue='welcome')
        self.OptionsMenu.add_checkbutton(label=self.MENU_TOOLS_ITEMS['poweron'], command=self.ckBtn_callback,  variable=self.poweron_StrVar,onvalue='poweron')

        # language_menu
        self.LanguageMenu = Menu(self.OptionsMenu, tearoff=0)
        self.rdBtn_IntVar = IntVar()
        self.LanguageMenu.add_radiobutton(label=self.MENU_LANGUAGE_ITEMS['cn'], command=lambda :self.rdBtn_callback('cn'), variable=self.rdBtn_IntVar, value=0 if self.is_cn=='cn' else 1)#value=0为默认选中
        self.LanguageMenu.add_radiobutton(label=self.MENU_LANGUAGE_ITEMS['en'], command=lambda :self.rdBtn_callback('en'), variable=self.rdBtn_IntVar, value=0 if self.is_cn=='en' else 1)
        self.LanguageMenu.add_command(label=self.MENU_LANGUAGE_ITEMS['korean'], command=lambda :self.rdBtn_callback('korean'))
        self.LanguageMenu.add_command(label=self.MENU_LANGUAGE_ITEMS['japanese'], command=lambda :self.rdBtn_callback('japanese'))

        self.CloseMenu = Menu(self.OptionsMenu, tearoff=0)
        self.close_IntVar = IntVar()
        self.CloseMenu.add_radiobutton(label=self.MENU_TOOLS_ITEMS['minimize'],command=self.msgBox,variable=self.close_IntVar,value=0)
        self.CloseMenu.add_radiobutton(label=self.MENU_TOOLS_ITEMS['exit'],command=self.msgBox,variable=self.close_IntVar,value=1)
        self.OptionsMenu.add_cascade(label=self.MENU_TOOLS_ITEMS['close'], menu=self.CloseMenu)

        # self.config[const.LOGIN][const.LANGUAGE] = 0 if self.is_cn else 1
        # self.
        self.OptionsMenu.add_cascade(label=self.MENU_BAR['language'], menu=self.LanguageMenu)
        self.ToolsMenu.add_cascade(label=self.MENU_TOOLS_ITEMS['options'], menu=self.OptionsMenu)
        self.menu.add_cascade(label=self.MENU_BAR['tools'], menu=self.ToolsMenu)

        #help_menu
        self.helpMenu = Menu(self.menu, tearoff=0)
        self.helpMenu.add_command(label=self.MENU_HELP_ITEMS['help'], command=self.msgBox, accelerator="F1")
        self.helpMenu.add_command(label=self.MENU_HELP_ITEMS['about'], command=self.msgBox, accelerator="")

        # self.helpMenu.entryconfig(0, state=DISABLED)
        self.menu.add_cascade(label=self.MENU_BAR['help'], menu=self.helpMenu)
        #refresh root_main window config
        self.master.config(menu=self.menu)
    def ckBtn_callback(self):
        self.config[const.LOGIN][const.ISAUTOLOGIN]='1' if self.autologin_StrVar.get()=='autologin' else '0'
        self.config[const.LOGIN][const.ISWELCOMEMSG]= '1' if self.welcome_StrVar.get()=='welcome' else  '0'
        self.config[const.LOGIN][const.ISPOWERON]='1' if self.poweron_StrVar.get()=='poweron' else '0'
        self.config[const.LOGIN][const.ISPOLL]='1' if self.pollmode_StrVar.get() == 'pollmode' else '0'
        self.config[const.LOGIN][const.ISLINKAGE]='1' if self.linkage_StrVar.get() == 'linkage' else '0'
        self.config.write()
    def property_rdBtn_callback(self,selected_attribute):
        # category_curselection = self.category_listbox.curselection()
        curselection = self.annotation_listbox.curselection()
        if len(curselection) < 1:
            return
        if selected_attribute=='无':
            self.property0_StringVar.set( self.property0_StringVar.get())
        elif selected_attribute=='属性0':
            self.property1_StringVar.set(self.property1_StringVar.get())
        elif selected_attribute=='属性1':
            self.property2_StringVar.set( self.property2_StringVar.get())

        for i in curselection:
            self.bbox_list[i].attribute = selected_attribute
            self.annotations[i] = self.bbox_list[i].annotation
        # refresh listbox variable
        self.annotation_str_var.set(self.annotations)

        # 数据缓存
        self.data_cache()
        # 更新BBox状态栏
        curselection = len(self.annotation_listbox.curselection())
        amount = len(self.bbox_list)
        self.state_label.configure(text='BBOX: %d/%d' % (curselection, amount))
    def rdBtn_callback(self,language):
        # print(language)
        if language==self.is_cn or language==self.cur_sku_lib:
            return
        if language=='japanese' :
            self.msgBox('啊呸可把你牛逼坏了还会'+const.CN_LANGUAGE_MENU_ITEMS['japanese']+'就不给你介个鬼子翻译!')
            return
        if language=='korean' :
            self.msgBox('啊呸可把你牛逼坏了还会'+const.CN_LANGUAGE_MENU_ITEMS['korean']+'就不给你介个棒子翻译!')
            return

        if language in list(const.DATA_ADDR.keys()):
            self.config[const.LOGIN][const.SKU_LIB]=language
            self.cur_sku_lib=language
            self.cur_img_index = int(self.config[const.LOGIN][language + '_IMAGE_INDEX'])
            self.get_data()
        if language == 'cn' or language=='en':
            self.config[const.LOGIN][const.LANGUAGE]=  language
        self.config.write()
        self.make_menu_bar(self.master)
    def toggle_cursor(self):
        if  self.is_cursor_select:
            self.canvas.delete(self.h_line)
            self.canvas.delete(self.v_line)
            self.canvas.config(cursor='arrow')
            # self.is_cursor_select=False
        else:
            self.canvas.config(cursor='tcross')
            # self.is_cursor_select=True
    def  get_data(self, imgNoWithLocation=None,is_search=False,reason=None):

        try:
            if reason=='focusin':
                self.img_number_Entry.selection_range(0, END)
                return True
            elif reason in ('focusout',):
                return True
            if imgNoWithLocation=='搜索图片或者BBOX':
                return True
            if imgNoWithLocation and len(imgNoWithLocation)<6:
                return True
            if self.is_cur_img_change() :
                is_save = self.is_save()
                if is_save==6:
                    self.save(False)
                    return None
                elif is_save is 2:  # 点击了取消 6,7,2
                    return None
            self.categoryObjsOfAll.clear()
            self.images.clear()
            response=requests.get(const.DATA_ADDR[self.cur_sku_lib]['IMAGES'])#,timeout=20,5
            self.images=response.json()
            # print(self.images)
            response = requests.get(const.DATA_ADDR[self.cur_sku_lib]['SKUS'])
            categories = CategoryData()
            categories.fromJson(response.json())  # json to model
            self.categoryObjsOfAll=categories.data.skus
            # 上色
            i = 0
            # print(self.categoryObjsOfAll[0].color)
            for category in self.categoryObjsOfAll:
                category.color=self.colors[i]
                if i < len(self.colors)-1:
                    i += 1
                else:
                    i = 0

            self.categories = list(map(lambda category:category.category, self.categoryObjsOfAll))
            self.category_str_var.set(self.categories)
            # for category,color in self.categoryObjsOfSearch.items():
            #     self.category_listbox.itemconfigure(fg=color)
            self.categoryObjsOfSearch = copy.deepcopy(self.categoryObjsOfAll)  # 深拷贝非引用赋值
            for i, category in enumerate(self.categoryObjsOfSearch):
                self.category_listbox.itemconfigure(i, fg=category.color)
            # img file
            imgNo=''
            if is_search:
                imgNo=imgNoWithLocation.replace(' ','')
                imgFileName_split_tuple = ''
                if imgNo.find('_') < 0:
                    imgNo = imgNo.split('-')[0]
                else:
                    imgNo = imgNo.split('_')[0]

            imgNo=imgNo+'.jpg' if  imgNo else self.images[self.cur_img_index]
            
            if imgNo in self.images:
                self.cur_img_index=self.images.index(imgNo)
            else:
                imgNo=imgNo.replace('.jpg', '.png')
                if imgNo in self.images:
                    self.cur_img_index = self.images.index(imgNo)
                else:
                    self.msgBox('查无此图!')
                return True
            response=requests.get(const.DATA_ADDR[self.cur_sku_lib]['IMAGE'],{'file': imgNo})
            if response and response.ok:
                self.config[const.LOGIN][self.cur_sku_lib + '_IMAGE_INDEX'] = self.cur_img_index
                self.config.write()
            #todo trycatch
            self.open_img(BytesIO(response.content),imgNo,imgNoWithLocation,is_search)
        finally:
            return True


    def get_annotation_data(self,imgBaseName,imgNoWithLocation,is_search):
        self.annotations.clear()
        self.bbox_list.clear()
        self.init_dot_initialized()
        self.is_change_coord = False
        self.is_change_annotation_name = False

        response = requests.get(const.DATA_ADDR[self.cur_sku_lib]['ANNOTATION'],{'image':imgBaseName})
        # print(response.json())
        self.annotationData = AnnotationData()
        self.annotationData.fromJson(response.json())  # json to model
        self.bbox_list = self.annotationData.bboxes

        self.cur_img_rotate = self.annotationData.rotate

        #图片文件名刷新
        self.master.title('AnnotationTool —%s'%self.images[self.cur_img_index])  # 修改框体的名字,也可在创建时使用className参数来命名
        self.rotate_img()
        # print(annotationData.bboxes[0].annotation)
        for bbox in self.bbox_list:

            bbox.truncated = 1 if int(bbox.truncated) == 1 else ''
            if  self.getObjByCategory(bbox.className):
                bbox.color = self.getObjByCategory(bbox.className).color
            bbox.rectangle_id = self.canvas.create_rectangle(self.getCoordByZoom(bbox.x1),self.getCoordByZoom(bbox.y1),self.getCoordByZoom(bbox.x2),self.getCoordByZoom(bbox.y2),
                                                             width=self.bd_width, outline=bbox.color,#stipple=self.is_stipple, fill=bbox.color,
                                                             dash=bbox.truncated, tags=('bbox',))#fill=bbox.color,, stipple=self.is_stipple
            # print(bbox.annotation)
            self.annotations.append(bbox.annotation)
        #副本
        self.bbox_list_original = copy.deepcopy(self.bbox_list)
        self.annotations_list.clear()
        self.annotations_list.append(self.bbox_list_original)

        self.annotation_str_var.set(self.annotations)

        for i, bbox in enumerate(self.bbox_list):
            self.annotation_listbox.itemconfigure(i, fg=bbox.color)
        if is_search:
            imgFileName_split_tuple=imgNoWithLocation.split('_')

            for i, bbox in enumerate(self.bbox_list):
                coords=(str(bbox.x1), str(bbox.y1), str(bbox.x2), str(bbox.y2))
                if  not  [False for j in coords if j not in imgFileName_split_tuple]:
                    self.annotation_listbox.selection_clear(0, END)
                    self.annotation_listbox.selection_set(i)
                    self.annotation_listbox.yview(i)
                    self.canvas.xview_moveto((1/self.cur_img_size[0])*self.getCoordByZoom(bbox.x1))
                    self.canvas.yview_moveto((1/self.cur_img_size[1])*(self.getCoordByZoom(bbox.y1)-25))
                    # print((1/self.cur_img_size[0])*bbox.x1)
                    # print((1/self.cur_img_size[1])*bbox.y1)
                    self.show_bbox()
                    break
        else:
            self.annotation_listbox.selection_clear(0, END)
            self.annotation_listbox.selection_set(0,END)
            self.annotation_listbox.yview(0)
            self.canvas.xview_moveto(0)
            self.canvas.yview_moveto(0)

        # 更新BBox状态栏
        curselection = len(self.annotation_listbox.curselection())
        amount = len(self.bbox_list)
        self.state_label.configure(text='BBOX: %d/%d'% (curselection,amount))

    def getObjByCategory(self, category):
        if self.categoryObjsOfAll:
            categoryObjsOfAll = list(filter(lambda categoryObj: categoryObj.category == category, self.categoryObjsOfAll))
            if categoryObjsOfAll:
                return categoryObjsOfAll[0]
        return None

    def open_img(self, img_path,imgName,imgNoWithLocation='',is_search=False):
        try:
            self.img = Image.open(img_path)
        except Exception as e:
            print(e)
            self.cur_img_index+=1
            self.get_data()
            return
        finally:
            pass
        self.img_size =self.cur_img_size= self.img.size#原图大小
        w, h = self.img_size
        zoom_width = w * self.cur_zoom_level
        zoom_height = h * self.cur_zoom_level
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.canvas.config(scrollregion=(0, 0, zoom_width, zoom_height))
        # self.canvas.config(scrollregion=(0, 0, self.img_size[0] * 2, self.img_size[1]))
        self.canvas.delete('all')
        self.cur_img_id = self.canvas.create_image((0, 0), image=self.tk_img, anchor=N + W)

        # annotation file
        basename = os.path.splitext(imgName)[0]
        try:
            self.get_annotation_data(basename,imgNoWithLocation,is_search)
        except:
            pass

    def rotate_img(self,event=None):
        if event:
            if event.delta > 0:
                self.cur_img_rotate+=const.ROTATE_ANGLE
            else:
                self.cur_img_rotate-=const.ROTATE_ANGLE
        cur_img_rotate = abs(self.cur_img_rotate)
        cur_img_rotate %= 360
        self.cur_img_rotate = cur_img_rotate if self.cur_img_rotate > 0 else -cur_img_rotate#方向
        # print(self.cur_img_rotate)
        img_rotate = self.img.rotate(self.cur_img_rotate, expand=True)
        w, h = self.img_size
        zoom_width = w * self.cur_zoom_level
        zoom_height = h * self.cur_zoom_level
        img_resize = self.resize(zoom_width, zoom_height, zoom_width, zoom_height, img_rotate)
        self.tk_img = ImageTk.PhotoImage(img_resize)
        self.cur_img_size=img_resize.size
        self.canvas.itemconfig(self.cur_img_id, image=self.tk_img)
        #show
        self.angle.configure(text='%d°' % self.cur_img_rotate)
    def refresh(self,*args):
        self.get_data()
    def copy_category(self):
        curselection = self.annotation_listbox.curselection()
        if len(curselection) >0:
            text=self.bbox_list[curselection[0]].className
            self.search_str_var.set(text)
            pyperclip.copy(text)
            if len(self.categoryObjsOfSearch)==1:
                self.category_listbox.selection_clear(0,END)
                self.category_listbox.selection_set(0)
                self.category_listbox.yview(0)
    def change_annotation_name(self,*args):
        # category_curselection = self.category_listbox.curselection()
        curselection = self.annotation_listbox.curselection()
        if len(curselection) > 0:
            self.annotation_curselection = curselection
            self.is_change_annotation_name = TRUE

    def delete_annotation(self, *args):
        curselections = self.annotation_listbox.curselection()
        if len(curselections) < 1:
            return None
        # refresh canvas
        for curselection in reversed(curselections):
            # print(curselection,self.annotations,self.bbox_list[curselection].sku_name,len(self.bbox_list))
            self.annotations.pop(curselection)
            self.canvas.delete(self.bbox_list[curselection].rectangle_id)
            self.bbox_list.pop(curselection)
            # print(curselection,self.annotations,len(self.bbox_list))
            # print(curselection,self.annotations,self.bbox_list[curselection].sku_name)
        # listbox variable refresh
        self.annotation_str_var.set(self.annotations)

        self.annotation_listbox.selection_clear(0,END)
        print(curselections[0])
        self.annotation_listbox.selection_set(curselections[0])
        self.show_bbox()
        # 数据缓存
        self.data_cache()


    def data_cache(self):
        if self.cur_annotation_index<len(self.annotations_list)-1:
            for i in reversed(range(self.cur_annotation_index + 1, len(self.annotations_list))):
                self.annotations_list.pop(i)
        self.annotations_list.append(copy.deepcopy(self.bbox_list))
        self.cur_annotation_index = len(self.annotations_list) - 1

    def toggle_style(self, *event):
        curselections = self.annotation_listbox.curselection()
        if curselections:
            self.bbox_clear()
            for index in curselections:
                cur_bbox = self.bbox_list[index]
                cur_bbox.truncated = 1 if type(cur_bbox.truncated) == str else ''
                self.make_rectangle(cur_bbox, cur_bbox.truncated)
            #数据缓存
            self.data_cache()
    def cn_switch(self):
        #todo:???
        # sys.stdout.flush()
        # self.helpMenu.update_idletasks()
        # self.helpMenu.update()
        self.is_cn = 'cn'
        self.make_menu_bar(self.master)


    def en_switch(self):
        self.is_cn = 'en'
        self.make_menu_bar(self.master)


def goto_main():
    root_main = Tk()
    root_main.title('AnnotationTool')  # 修改框体的名字,也可在创建时使用className参数来命名
    # master.resizable(0,0)#框体大小可调性，分别表示x,y方向的可变性；
    # root_login.geometry('1210x800')  # 指定主框体大小；
    # root_login.columnconfigure(0, minsize=1000)
    sw = root_main.winfo_screenwidth()
    # 得到屏幕宽度
    sh = root_main.winfo_screenheight()
    # 得到屏幕高度
    ww = 1400
    wh = 800
    # 窗口宽高为100
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    # 设置窗口的大小宽x高+偏移量
    root_main.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    #root_main.iconbitmap(const.LOGO)
    # root_login.overrideredirect(True)
    mark_tool = Main(root_main)
    root_main.protocol("WM_DELETE_WINDOW", lambda :BaseApp.is_exit(root_main,mark_tool.config,mark_tool.cur_sku_lib,mark_tool.cur_img_index,mark_tool.is_cur_img_change(),))
    root_main.mainloop()
if __name__ == '__main__':
    goto_login()

def unit_test():
    root = Tk()
    root.title('AnnotationTool')  # 修改框体的名字,也可在创建时使用className参数来命名
    # master.resizable(0,0)#框体大小可调性，分别表示x,y方向的可变性；
    # root_login.geometry('1210x800')  # 指定主框体大小；
    # root_login.columnconfigure(0, minsize=1000)
    # root_login.protocol("WM_DELETE_WINDOW", mark_tool.is_exit)
    sw = root.winfo_screenwidth()
    # 得到屏幕宽度
    sh = root.winfo_screenheight()
    # 得到屏幕高度
    ww = 1210
    wh = 800
    # 窗口宽高为100
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    # 设置窗口的大小宽x高+偏移量
    root.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    root.iconbitmap(r"imgs/main.ico")
    # root_login.overrideredirect(True)
    mark_tool = Main(root)
    root.mainloop()
