#!/usr/bin/env python
# !-*-coding:utf-8 -*-
# !@time    :2018/6/24 21:07
# !@Author :SINGLE
# !@File   :main.py
from tkinter import messagebox
from tkinter import *
from tkinter.constants import *
from PIL import Image, ImageTk
from entity.Bbox import *
from entity.Category import *
import random
import os
from tkinter import filedialog
from Const import const

# en_help_str_var = StringVar()
# en_help_str_var.set('Help')


class App:

    def __init__(self, master):
        self.master=master
        # initialize global variable
        self.init_var()

        # make_menu_bar
        self.make_menu_bar()
        # make_ui
        self.make_ui()
        #import_file
        self.import_file()
        #bind_event
        self.bind_event()

    def init_var(self):
        self.cur_zoom_level = 1
        self.annotation_str_var = StringVar()
        self.category_str_var = StringVar()
        self.categoryObjsOfAll = []
        self.categoryObjsOfSearch = []
        self.categories = []
        self.h_line = NONE
        self.v_line = NONE
        self.r = 3  # ???
        self.init_dot = {}
        self.init_dot['zoom_level'] = NONE
        self.init_dot['x'] = NONE
        self.init_dot['y'] = NONE
        self.init_dot['id'] = NONE
        self.temp_rectangle_id = NONE
        self.bbox_list = []
        self.info_label_id = 0
        self.info_label = NONE
        self.is_change_annotation_name = False
        self.is_change_coord = False
        self.is_dashed = ''
        self.annotation_curselection = 0
        self.is_online = False
        self.is_cursor_select = False
        self.images = []
        self.img_root_path = NONE
        self.annotation_dir_path = NONE
        self.cur_img_index = 0
        self.annotations = []
        self.cur_img_rotate = 0
        self.colors = ['#00ff00', '#ff0000', '#FF00FF', 'purple', '#0000ff']
        self.bd_width = 1
        self.is_stipple = 'gray50'
        self.is_cn = FALSE

    def bind_event(self):
        # category_istbox_event_bind
        self.category_listbox.bind('<<ListboxSelect>>', self.select_correct_category)#<<ListboxSelect>>:选中item变化监听事件
        # annotation_istbox_event_bind
        self.annotation_listbox.bind('<Button-3>', self.popup_menu)
        self.annotation_listbox.bind('<Delete>', self.delete_annotation)
        self.annotation_listbox.bind('<<ListboxSelect>>', self.show_bbox)
        self.annotation_listbox.bind('<Escape>', self.cancel_select)
        # canvas_event_bind
        self.canvas.bind("<Control-MouseWheel>", self.img_zoom)
        self.canvas.bind("<MouseWheel>", self.v_bound_to_mousewheel)
        self.canvas.bind("<Shift-MouseWheel>", self.h__bound_to_mousewheel)
        self.canvas.bind('<Button-1>', self.mouse_click)
        self.canvas.bind('<Button-3>', self.mouse_right_click)
        self.canvas.bind('<Motion>', self.mouse_move)
        self.canvas.bind('<Escape>', self.cancel_bbox)
        self.canvas.bind("<KeyPress-Left>", self.prevImage)
        self.canvas.bind("<KeyPress-Up>", self.prevImage)
        self.canvas.bind("<KeyPress-w>", self.prevImage)
        self.canvas.bind("<KeyPress-a>", self.prevImage)
        self.canvas.bind("<KeyPress-Right>", self.nextImage)
        self.canvas.bind("<KeyPress-Down>", self.nextImage)
        self.canvas.bind("<KeyPress-d>", self.nextImage)
        # self.canvas.bind("<KeyPress-s>", self.nextImage)#todo 和Ctrl+S冲突
        # scrollbar_event_bind
        self.v_scrollbar.bind("<MouseWheel>", self.v_bound_to_mousewheel)
        self.h_scrollbar.bind("<Shift-MouseWheel>", self.h__bound_to_mousewheel)
        self.v_scrollbar.bind("<Enter>", self._unbound_to_mousewheel)
        self.h_scrollbar.bind("<Enter>", self._unbound_to_mousewheel)
        # master_event_bind
        self.master.bind_all("<Control-o>", self.import_file)
        self.master.bind_all("<Control-s>", self.save)
        self.master.bind_all("<Control-t>", self.toggle_annotation_style)
        self.master.bind_all("<Control-q>", quit)
        self.master.bind_all("<KeyPress-F1>", self.msgBox)

        # master.bind("<Left>", self.prevImage)
        # master.bind("<Right>", self.nextImage)
        # self.canvas.bind("<Up>", self.prevImage)
        # master.bind("<Down>", self.nextImage)
        # self.annotation_listbox.bind('<<ListboxSelect>>', self.msgBox)

    def cancel_select(self,*args):
        # state reset
        self.is_change_annotation_name = False
        self.is_change_coord = False

    def make_ui(self):
        # layout
        self.category_frame = Frame(self.master, width='250')  # , bg='red')
        self.main_panel_frame = Frame(self.master)  # , bg='blue')
        self.annotation_frame = Frame(self.master, width='250')  # , bg='orange')
        self.status_bar_frame = Frame(self.master, bg='gray', height=50)

        self.status_bar_frame.pack(side=BOTTOM, fill=X)
        self.category_frame.pack(side=LEFT, fill=Y)
        self.annotation_frame.pack(side=RIGHT, fill=Y)
        self.main_panel_frame.pack(side=TOP, fill=BOTH, expand=TRUE)
        # category_frame
        self.search_entry = Entry(self.category_frame, validate='key', validatecommand=self.entry_change,
                                  highlightcolor='red', insertbackground='red', insertwidth=3,
                                  relief='sunken')  # relief:flat/sunken/raised/groove/ridge
        self.search_entry.pack(fill=X)
        # self.categories = list(map(lambda category:category.category, self.categoryObjsOfSearch))
        # self.category_str_var.set(self.categories)
        self.category_listbox = Listbox(self.category_frame, selectmode=BROWSE, height=80,
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
        self.canvas = Canvas(self.main_panel_frame, width=0, height=0, scrollregion=(0, 0, 0, 0), bg='green',
                             cursor='pencil', yscrollcommand=self.v_scrollbar.set,
                             xscrollcommand=self.h_scrollbar.set)  # pencil tcross
        self.canvas.pack(fill=BOTH, expand=TRUE, side=LEFT)
        self.h_scrollbar.config(command=self.canvas.xview)
        self.v_scrollbar.config(command=self.canvas.yview)
        # annotation_frame
        self.annotation_listbox = Listbox(self.annotation_frame, height=80, selectmode=EXTENDED,
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
        self.position = Label(self.status_bar_frame)
        self.position.pack()
        self.test_btn = Button(self.status_bar_frame, text='test', command=self.msgBox)
        self.test_btn.pack()
    # todo category可变对象优化,如[{},{}]
    def entry_change(self):

        def getObjsByKeyWords(category):
            keywords = self.search_entry.get()
            # keywords=filter(lambda str:str==' ',keywords)
            keywords = keywords.split()
            if len(keywords) < 1:
                return True
            for keyword in keywords:
                if keyword not in category.category:
                    return False
            return True

        self.categoryObjsOfSearch = list(filter(getObjsByKeyWords, self.categoryObjsOfAll))
        self.categories = list(map(lambda category:category.category, self.categoryObjsOfSearch))
        self.category_str_var.set(self.categories)
        for i, categroy in enumerate(self.categoryObjsOfSearch):
            self.category_listbox.itemconfigure(i, fg=categroy.color)

        return True

    def toggle_annotation_style(self, *args):
        self.is_dashed = 1 if type(self.is_dashed) == str else ''

    def change_coord(self, *args):
        curselection = self.annotation_listbox.curselection()
        if len(curselection) == 1:
            self.annotation_curselection = curselection[0]
            self.is_change_coord = TRUE
            self.bbox_clear()

    def show_bbox(self, *args):
        self.bbox_clear()
        curselections = self.annotation_listbox.curselection()
        for index in curselections:
            cur_bbox = self.bbox_list[index]
            dash = 1 if type(cur_bbox.is_dashed) == int else ''
            self.make_rectangle(cur_bbox, dash)
            if len(curselections)<2:
                self.show_info_bbox(cur_bbox)
            else:
                self.canvas.delete('info_label')

    def show_all_bbox(self, *args):
        self.bbox_clear()
        cur_bbox = self.bbox_list[self.annotation_curselection]
        for bbox in self.bbox_list:
            if self.is_change_coord and bbox.id==cur_bbox.id:
                continue
            dash = 1 if type(bbox.is_dashed) == int else ''
            self.make_rectangle(bbox, dash)
 
    def make_rectangle(self, bbox, dash):
        rectangle_id = self.canvas.create_rectangle(self.getCoordByZoom(bbox.coord[0]), self.getCoordByZoom(bbox.coord[1]), self.getCoordByZoom(bbox.coord[2]),
                                                    self.getCoordByZoom(bbox.coord[3]),
                                                    width=self.bd_width, outline=bbox.color, dash=dash,
                                                    stipple=self.is_stipple, fill=bbox.color,
                                                    tags=('bbox',))
        bbox.id=rectangle_id

    def hide_all_bbox(self, *args):
        self.bbox_clear()

    def save(self, *args):
        if len(self.images) > 0:
            output_file_path = os.path.join(self.annotation_dir_path,
                                            os.path.splitext(self.images[self.cur_img_index])[0] + '.txt')
            with open(output_file_path, 'w', encoding='UTF-8') as f:
                f.write('rotate %d\n' % int(self.cur_img_rotate))
                for bbox in self.bbox_list:
                    is_dashed = '1' if type(bbox.is_dashed) == int else '0'
                    content = ' '.join([bbox.category, ' '.join(map(str, bbox.coord)), is_dashed])
                    f.write(content + '\n')
            print('Image No. %s saved' % (output_file_path))

    def select_correct_category(self, event):
        category_listbox_curselection = self.category_listbox.curselection()
        if category_listbox_curselection:
            if self.is_change_annotation_name:
                self.is_change_annotation_name = False#state reset
                for curselection in reversed(self.annotation_curselection):
                    selected_category = self.categories[category_listbox_curselection[0]]
                    self.bbox_list[curselection].category = selected_category
                    self.bbox_list[curselection].color = self.getObjByCategory(selected_category).color
                    self.annotations[curselection] = self.bbox_list[curselection].annotation
                # refresh listbox variable
                self.annotation_str_var.set(self.annotations)

                for i, bbox in enumerate(self.bbox_list):
                    self.annotation_listbox.itemconfigure(i, fg=bbox.color)
            #选中分类item并显示对应的bbox
            self.bbox_clear()
            for bbox in self.bbox_list:
                if bbox.category == self.categories[category_listbox_curselection[0]]:
                    # dash = 1 if type(bbox.is_dashed) == int else ''
                    rectangle_id = self.canvas.create_rectangle(self.getCoordByZoom(bbox.coord[0]), self.getCoordByZoom(bbox.coord[1]), self.getCoordByZoom(bbox.coord[2]),
                                                                self.getCoordByZoom(bbox.coord[3]),
                                                                width=self.bd_width,
                                                                outline=self.getObjByCategory(bbox.category).color,
                                                                fill=self.getObjByCategory(bbox.category).color,
                                                                dash=bbox.is_dashed,
                                                                tags='bbox',
                                                                stipple=self.is_stipple)
                    bbox.id = rectangle_id

    def bbox_clear(self):
        self.canvas.delete('bbox')#use('bbox','') instead of ('bbox',),will have bug

    def popup_menu(self, event):
        popup_menu=Menu(self.annotation_listbox,tearoff=False)
        popup_menu.add_command(label=self.MENU_EDIT_ITEMS['editCategory'], command=self.change_annotation_name,
                                  accelerator="")
        popup_menu.add_command(label=self.MENU_EDIT_ITEMS['deleteCategory'], command=self.delete_annotation,
                                  accelerator="")
        popup_menu.add_command(label=self.MENU_EDIT_ITEMS['editCoord'], command=self.change_coord, accelerator="")
        popup_menu.add_command(label=self.MENU_EDIT_ITEMS['toggleStyle'], command=self.toggle_style, accelerator="")
        popup_menu.add_command(label=self.MENU_EDIT_ITEMS['showALl'], command=self.show_all_bbox, accelerator="")
        popup_menu.add_command(label=self.MENU_EDIT_ITEMS['hideALl'], command=self.hide_all_bbox, accelerator="")
        popup_menu.post(event.x_root, event.y_root)  # x_root与y_root表示右键点击的位置


    def cancel_bbox(self, event):
        # self.msgBox()
        # delete preview box
        self.canvas.delete(self.temp_rectangle_id)
        # init_point initialized or reset
        self.init_dot_initialized()


    def cancelBBox(self):
        pass

    def prevImage(self, event):
        if self.cur_img_index < 1:
            return NONE
        self.cur_img_index -= 1
        cur_img_path = os.path.join(self.img_root_path, self.images[self.cur_img_index])
        self.open_img(cur_img_path)

        annotation_file_path = os.path.join(self.annotation_dir_path,
                                            os.path.splitext(self.images[self.cur_img_index])[0] + '.txt')
        self.open_annotation_file(annotation_file_path)

    def nextImage(self, event):
        if self.cur_img_index > len(self.images) - 2:
            return NONE
        self.cur_img_index += 1
        cur_img_path = os.path.join(self.img_root_path, self.images[self.cur_img_index])
        self.open_img(cur_img_path)

        annotation_file_path = os.path.join(self.annotation_dir_path,
                                            os.path.splitext(self.images[self.cur_img_index])[0] + '.txt')
        self.open_annotation_file(annotation_file_path)

    def mouse_click(self, event):
        self.canvas.focus_set()
        if self.is_cursor_select:
            pass
        else:
            curselection_category = None
            if self.is_change_coord:
                curselection = self.annotation_listbox.curselection()
                if len(curselection) == 1:
                    curselection_category = self.bbox_list[curselection[0]].category

            else:
                curselections = self.category_listbox.curselection()
                if len(curselections) < 1:
                    self.msgBox('请选择分类!')
                    return NONE
                curselection_category = self.categories[curselections[0]]
            # print(curselection_category)

            if self.init_dot['zoom_level'] != NONE:
                # self.canvas.delete(self.init_dot['id'])
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
                    is_dashed = bbox.is_dashed
                    is_dashed = 1 if type(is_dashed) == int else ''
                    rectangle_id = self.canvas.create_rectangle(self.init_dot['x'], self.init_dot['y'], event.x, event.y,
                                                                width=self.bd_width,
                                                                outline=self.getObjByCategory(bbox.category).color,
                                                                dash=is_dashed, tags=('bbox',))
                else:
                    rectangle_id = self.canvas.create_rectangle(self.init_dot['x'], self.init_dot['y'], event.x, event.y,
                                                                width=self.bd_width,
                                                                outline=self.getObjByCategory(curselection_category).color,
                                                                dash=self.is_dashed, tags=('bbox',))
                # new and add bbox object
                # if self.init_dot['zoom_level'] != 1:
                #     # coord scale
                #     self.init_dot['x'] = self.init_dot['x'] / self.init_dot['zoom_level']
                #     self.init_dot['y'] = self.init_dot['y'] / self.init_dot['zoom_level']

                bbox = Bbox(rectangle_id, curselection_category, (
                self.getCoordByRestore(self.init_dot['x']), self.getCoordByRestore(self.init_dot['y']), self.getCoordByRestore(event.x), self.getCoordByRestore(event.y)),
                            self.is_dashed, self.getObjByCategory(curselection_category).color, self.cur_img_rotate)
                # self.canvas.tag_bind(CURRENT, '', self.show_box(bbox))
                self.show_info_bbox(bbox)
                if self.is_change_coord:
                    self.bbox_list[self.annotation_curselection].coord = (self.getCoordByRestore(self.init_dot['x']), self.getCoordByRestore(self.init_dot['y']), self.getCoordByRestore(event.x), self.getCoordByRestore(event.y))
                    self.is_change_coord = False
                else:
                    self.bbox_list.append(bbox)
                # annotations update
                self.annotations_data_update()

                # self.canvas.create_oval(
                #     (event.x - self.r, event.y - self.r, event.x + self.r, event.y + self.r), fill='black')
                self.init_dot_initialized()
            else:
                # self.init_dot['id'] = self.canvas.create_oval(
                #     (event.x - self.r, event.y - self.r, event.x + self.r, event.y + self.r), fill='black')
                self.init_dot['zoom_level'] = self.cur_zoom_level
                self.init_dot['x'] = event.x
                self.init_dot['y'] = event.y

    def getCoordByRestore(self,coord):
        return int(coord//self.cur_zoom_level)

    def mouse_right_click(self,event):
        cur_items = self.canvas.find_withtag(CURRENT)
        if cur_items:
            for i,bbox in enumerate(self.bbox_list):
                if cur_items[-1]==bbox.id:
                    self.editMenu.post(event.x_root, event.y_root)
                    self.annotation_listbox.selection_clear(0,END)
                    self.annotation_listbox.selection_set(i)



    def init_dot_initialized(self):
        self.init_dot['zoom_level'] = NONE
        self.init_dot['x'] = NONE
        self.init_dot['y'] = NONE
        self.init_dot['id'] = NONE

    def annotations_data_update(self):
        self.annotations.clear()
        for i, bbox in enumerate(self.bbox_list):
            self.annotations.append(bbox.annotation)
        self.annotation_str_var.set(self.annotations)
        # self.annotation_listbox.select_set(END)
        self.annotation_listbox.yview(END)
        for i, bbox in enumerate(self.bbox_list):
            self.annotation_listbox.itemconfigure(i, fg=bbox.color)

    def mouse_move(self, event):
        # print('x=%d,y=%d' % (event.x, event.y))
        # if self.canvas.find_withtag(CURRENT)[0] !=self.cur_img_id:
        # print(self.canvas.find_withtag(CURRENT))
        # self.canvas.tag_bind(CURRENT, '', self.msgBox())
        if self.is_cursor_select:
            pass
        else:
            self.position.configure(text='%d : %d' % (event.x, event.y))
            if self.h_line:
                self.canvas.delete(self.h_line)
            self.h_line = self.canvas.create_line(0, event.y, self.canvas.winfo_width(), event.y, width=1)
            if self.v_line:
                self.canvas.delete(self.v_line)
            self.v_line = self.canvas.create_line(event.x, 0, event.x, self.canvas.winfo_height(), width=1)

            self.make_preview_box(event)

            for bbox in self.bbox_list:
                xMin=min(bbox.coord[0],bbox.coord[2])
                xMax=max(bbox.coord[0],bbox.coord[2])
                yMin=min(bbox.coord[1],bbox.coord[3])
                yMax=max(bbox.coord[1],bbox.coord[3])
                if event.x>xMin and event.x<xMax and event.y>yMin and event.y<yMax:
                    self.show_info_bbox(bbox)
                    # if not self.canvas.find_withtag(bbox.id):
                    # self.bbox_clear()
                    # dash = 1 if type(bbox.is_dashed) == int else ''
                    # self.make_recttangle(bbox,dash)
                cur_items = self.canvas.find_withtag(CURRENT)
                if cur_items:
                    if cur_items[-1] == self.cur_img_id:
                            self.canvas.delete('info_label')

                # cur_items = self.canvas.find_withtag(CURRENT)
                # if cur_items:
                #     for bbox in self.bbox_list:
                #         if cur_items[-1] == bbox.id:
                #             self.show_info_bbox(bbox)
                #         if cur_items[-1] == self.cur_img_id:
                #             self.canvas.delete('info_label')


    def img_zoom(self, event):
        if event.delta > 0:
            if self.cur_zoom_level > 1.9:
                return NONE
            else:
                self.cur_zoom_level += 0.1
        else:
            if self.cur_zoom_level < 0.6:
                return NONE
            else:
                self.cur_zoom_level -= 0.1

        w, h = self.img_size
        zoom_width = w * self.cur_zoom_level
        zoom_height = h * self.cur_zoom_level
        img_resize = self.resize(zoom_width, zoom_height, zoom_width, zoom_height, self.img)
        # img_resize = self.img.resize((int(zoom_width), int(zoom_height)))
        # img_rotate = self.img.cur_img_rotate(45)
        # self.img.resize((w  * 2, h * 2), Image.ANTIALIAS)
        self.tk_img = ImageTk.PhotoImage(img_resize)
        self.canvas.itemconfigure(self.cur_img_id, image=self.tk_img, anchor=N + W)
        # self.canvas.config(scrollregion=(0, 0, self.img_size[0] * 2, self.img_size[1]))
        # self.canvas.config(scrollregion=(0,0,self.zoom_width*2, self.zoom_height*2))
        # self.canvas.config(width=zoom_width,height=zoom_height)

        print(str(self.cur_zoom_level * 10) + "%", self.main_panel_frame.winfo_height() - zoom_height, self.img.size)
        # preview_box zoom
        self.make_preview_box(event)
        # bbox zoom
        # for bbox in self.bbox_list:
        #     # coord zoom
        #     x = self.getCoordByZoom(bbox.coord[0])
        #     y = self.getCoordByZoom(bbox.coord[1])
        #     x1 = self.getCoordByZoom(bbox.coord[2] )
        #     y1 = self.getCoordByZoom(bbox.coord[3])
        #     self.canvas.coords(bbox.id, (x, y, x1, y1))
        self.show_all_bbox(self.annotation_curselection)#todo 框缩放的bug临时解决方案
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

    def make_preview_box(self, event):
        curselections = self.category_listbox.curselection()
        if curselections:
            curselection_category = self.categories[curselections[0]]
        if self.init_dot['zoom_level'] != NONE and self.temp_rectangle_id:
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
                is_dashed = cur_bbox.is_dashed
                is_dashed = 1 if type(is_dashed) == int else ''
                self.temp_rectangle_id = self.canvas.create_rectangle(self.init_dot['x'], self.init_dot['y'], event.x,
                                                                      event.y,
                                                                      width=self.bd_width,
                                                                      outline=self.getObjByCategory(
                                                                          cur_bbox.category).color,
                                                                      tags=('bbox',))
            else:
                self.temp_rectangle_id = self.canvas.create_rectangle(self.init_dot['x'], self.init_dot['y'], event.x,
                                                                      event.y,
                                                                      width=self.bd_width,
                                                                      outline=self.getObjByCategory(
                                                                          curselection_category).color, tags=('bbox',))
                # Bbox(0,curselection_category,(self.init_dot['x'], self.init_dot['y'], event.x,
                #                               event.y),'','red',0)
            if curselections:
                self.show_info_bbox(Bbox(0,curselection_category,(self.init_dot['x'], self.init_dot['y'], event.x,
                                                              event.y),'','red',0))

    def _unbound_to_mousewheel(self, event):
        self.v_scrollbar.unbind_all("<MouseWheel>")
        self.h_scrollbar.unbind("<MouseWheel>")

    def h__bound_to_mousewheel(self, event):
        self.canvas.xview_scroll(-1 * (event.delta // 120), "units")

    def v_bound_to_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def show_info_bbox(self, bbox):
        info_label = self.canvas.find_withtag('info_label')
        if info_label:
            self.canvas.coords(self.info_label_id,
                               (bbox.coord[0] + (bbox.coord[-2] - bbox.coord[0]) / 2, bbox.coord[1] - 20))
            # self.canvas.itemconfigure(self.info_label_id)
            self.info_label.config(text=bbox.category)#+ str(random.randint(0, 100)))
        else:
            self.info_label = Label(self.canvas, text=bbox.category, bg='white')
            self.info_label_id = self.canvas.create_window(
                (bbox.coord[0] + (bbox.coord[-2] - bbox.coord[0]) / 2, bbox.coord[1] - 20), window=self.info_label,tags='info_label')

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
        if self.is_cn:
            self.MENU_BAR=const.CN_MENU_ITEMS
            self.MENU_FILE_ITEMS=const.CN_FILE_MENU_ITEMS
            self.MENU_EDIT_ITEMS=const.CN_EDIT_MENU_ITEMS
            self.MENU_VIEW_ITEMS=const.CN_VIEW_MENU_ITEMS
            self.MENU_TOOLS_ITEMS=const.CN_TOOLS_MENU_ITEMS
            self.MENU_LANGUAGE_ITEMS=const.CN_LANGUAGE_MENU_ITEMS
            self.MENU_HELP_ITEMS=const.CN_HELP_MENU_ITEMS

        else:
            self.MENU_BAR=const.EN_MENU_ITEMS
            self.MENU_FILE_ITEMS = const.EN_FILE_MENU_ITEMS
            self.MENU_EDIT_ITEMS = const.EN_EDIT_MENU_ITEMS
            self.MENU_VIEW_ITEMS = const.EN_VIEW_MENU_ITEMS
            self.MENU_TOOLS_ITEMS = const.EN_TOOLS_MENU_ITEMS
            self.MENU_LANGUAGE_ITEMS = const.EN_LANGUAGE_MENU_ITEMS
            self.MENU_HELP_ITEMS = const.EN_HELP_MENU_ITEMS

        self.menu = Menu(self.master)
        #file_menu
        self.fileMenu = Menu(self.menu, tearoff=False)
        self.fileMenu.add_command(label=self.MENU_FILE_ITEMS['open'], command=self.import_file, accelerator="Ctr+O")
        self.fileMenu.add_command(label=self.MENU_FILE_ITEMS['save'], command=self.save, accelerator="Ctrl+S")
        self.fileMenu.add_separator()#分割线
        self.fileMenu.add_command(label=self.MENU_FILE_ITEMS['exit'], command=self.master.quit, accelerator="Ctrl+Q")
        self.menu.add_cascade(label=self.MENU_BAR['file'], menu=self.fileMenu)
        #eidt_menu
        self.editMenu = Menu(self.menu, tearoff=0)
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['refresh'], command=self.msgBox, accelerator="")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['toggleCursor'], command=self.toggle_cursor, accelerator="")
        self.editMenu.add_separator()#分割线
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['editCategory'], command=self.change_annotation_name, accelerator="")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['deleteCategory'], command=self.delete_annotation, accelerator="")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['editCoord'], command=self.change_coord, accelerator="")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['toggleStyle'], command=self.toggle_style, accelerator="")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['showALl'], command=self.show_all_bbox, accelerator="")
        self.editMenu.add_command(label=self.MENU_EDIT_ITEMS['hideALl'], command=self.hide_all_bbox, accelerator="")
        self.menu.add_cascade(label=self.MENU_BAR['edit'], menu=self.editMenu)
        #view_menu
        self.viewMenu = Menu(self.menu, tearoff=0)
        self.viewMenu.add_command(label=self.MENU_VIEW_ITEMS['refresh'], command=self.msgBox, accelerator="")
        self.menu.add_cascade(label=self.MENU_BAR['view'], menu=self.viewMenu)
        #tools_menu
        self.ToolsMenu = Menu(self.menu, tearoff=0)
        self.ToolsMenu.add_command(label=self.MENU_TOOLS_ITEMS['options'], command=self.msgBox, accelerator="")
        self.menu.add_cascade(label=self.MENU_BAR['tools'], menu=self.ToolsMenu)
        #language_menu
        self.LanguageMenu = Menu(self.menu, tearoff=0)
        self.LanguageMenu.add_command(label=self.MENU_LANGUAGE_ITEMS['cn'], command=self.cn_switch, accelerator="")
        self.LanguageMenu.add_command(label=self.MENU_LANGUAGE_ITEMS['en'], command=self.en_switch, accelerator="")
        self.menu.add_cascade(label=self.MENU_BAR['language'], menu=self.LanguageMenu)
        #help_menu
        self.helpMenu = Menu(self.menu, tearoff=0)
        self.helpMenu.add_command(label=self.MENU_HELP_ITEMS['about'], command=self.msgBox, accelerator="F1")
        self.helpMenu.entryconfig(1, state=DISABLED)
        self.menu.add_cascade(label=self.MENU_BAR['help'], menu=self.helpMenu)
        #refresh root window config
        self.master.config(menu=self.menu)

    def toggle_cursor(self):
        if self.is_cursor_select:
            self.canvas.config(cursor='pencil')
            self.is_cursor_select=False
        else:
            self.canvas.delete(self.h_line)
            self.canvas.delete(self.v_line)
            self.canvas.config(cursor='arrow')
            self.is_cursor_select=True
    def import_file(self, *agrs):
        # import category,img and annotation
        dir_path = filedialog.askdirectory()  # filetypes=[('TXT','.txt'),('All Files','*')])
        # category file
        category_file_path = os.path.join(dir_path, 'classes.txt')
        self.categoryObjsOfAll.clear()
        if os.path.exists(category_file_path):
            with open(category_file_path, 'r', encoding='utf-8') as f:
                i = 0
                for line in f.readlines():
                    line = line.strip()
                    category = Category(line, self.colors[i])
                    self.categoryObjsOfAll.append(category)
                    if i < len(self.colors) - 1:
                        i += 1
                    else:
                        i = 0
        self.categories = list(map(lambda category:category.category, self.categoryObjsOfAll))
        self.category_str_var.set(self.categories)
        # for category,color in self.categoryObjsOfSearch.items():
        #     self.category_listbox.itemconfigure(fg=color)
        self.categoryObjsOfSearch = self.categoryObjsOfAll.copy()  # 深拷贝非引用赋值
        for i, category in enumerate(self.categoryObjsOfSearch):
            self.category_listbox.itemconfigure(i, fg=category.color)
        # img file
        img_dir_path = os.path.join(dir_path, 'images')
        self.images.clear()
        self.cur_img_index = 0
        self.cur_zoom_level=1
        if os.path.exists(img_dir_path):
            self.img_root_path = img_dir_path
            for root, dirs, files in os.walk(img_dir_path):
                for file in files:
                    # if dirs:
                    #     continue
                    if os.path.splitext(file)[1] == '.jpg':
                        self.images.append(file)
            img_path = os.path.join(self.img_root_path, self.images[self.cur_img_index])
            # print(img_path+'00')
            self.open_img(img_path)
        # annotation file

        annotation_dir_path = os.path.join(dir_path, 'annotations')

        if os.path.exists(annotation_dir_path):
            self.annotation_dir_path = annotation_dir_path
            # for root,dirs,files in os.walk(annotation_dir_path):
            #     for file in files:
            #         # if dirs:
            #         #     continue
            #         if os.path.splitext(file)[1]=='.txt':
            #             self.annotation_names.append(file)
            annotation_file_path = os.path.join(self.annotation_dir_path,
                                                os.path.splitext(self.images[0])[0] + '.txt')
            # annotation_file_path = os.path.join(self.annotation_dir_path, self.annotation_names[self.cur_img_index])
            self.open_annotation_file(annotation_file_path)

    def open_annotation_file(self, annotation_path):
        self.annotations.clear()
        self.bbox_list.clear()
        if os.path.exists(annotation_path):
            with open(annotation_path, 'r', encoding='UTF-8') as f:
                for i, line in enumerate(f):
                    line = line.strip()
                    if i == 0:
                        pass  # todo self.img_rotate
                        self.cur_img_rotate = line.split()[-1]
                        continue
                    strs = line.split()
                    category = strs[0]

                    coord = tuple(map(int, strs[1:-1]))
                    is_dashed = strs[-1]
                    is_dashed = 1 if int(is_dashed) == 1 else ''
                    color = self.getObjByCategory(category).color
                    rectangle_id = self.canvas.create_rectangle(coord[0], coord[1], coord[2],
                                                                coord[3],
                                                                width=self.bd_width, outline=color, fill=color,
                                                                dash=is_dashed, tags=('bbox',), stipple=self.is_stipple)
                    bbox = Bbox(rectangle_id, category, coord, is_dashed, color, self.cur_img_rotate)
                    # print(bbox.annotation)
                    self.bbox_list.append(bbox)
                    self.annotations.append(bbox.annotation)
        self.annotation_str_var.set(self.annotations)
        for i, bbox in enumerate(self.bbox_list):
            self.annotation_listbox.itemconfigure(i, fg=bbox.color)

    def getObjByCategory(self, category):
        if self.categoryObjsOfSearch:
            categoryObjsOfSearch = list(filter(lambda categoryObj: categoryObj.category == category, self.categoryObjsOfSearch))
            if categoryObjsOfSearch:
                return categoryObjsOfSearch[0]
        return None

    def open_img(self, img_path):
        self.img = Image.open(img_path)
        self.img_size = self.img.size
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.canvas.config(scrollregion=(0, 0, self.img_size[0], self.img_size[1]))
        # self.canvas.config(scrollregion=(0, 0, self.img_size[0] * 2, self.img_size[1]))
        self.canvas.delete('all')
        self.cur_img_id = self.canvas.create_image((0, 0), image=self.tk_img, anchor=N + W)

    def change_annotation_name(self):
        # category_curselection = self.category_listbox.curselection()
        curselection = self.annotation_listbox.curselection()
        if len(curselection) > 0:
            self.annotation_curselection = curselection
            self.is_change_annotation_name = TRUE

    def delete_annotation(self, *args):
        curselections = self.annotation_listbox.curselection()
        if len(curselections) < 1:
            return NONE
        # refresh canvas
        for curselection in reversed(curselections):
            # print(curselection,self.annotations,self.bbox_list[curselection].id,len(self.bbox_list))
            self.annotations.pop(curselection)
            self.canvas.delete(self.bbox_list[curselection].id)
            self.bbox_list.pop(curselection)
            # print(curselection,self.annotations,len(self.bbox_list))
            # print(curselection,self.annotations,self.bbox_list[curselection].id)
        # listbox variable refresh
        self.annotation_str_var.set(self.annotations)

    def toggle_style(self, *event):
        curselections = self.annotation_listbox.curselection()
        if curselections:
            self.bbox_clear()
            for index in curselections:
                cur_bbox = self.bbox_list[index]
                cur_bbox.is_dashed = 1 if type(cur_bbox.is_dashed) == str else ''
                self.make_rectangle(cur_bbox, cur_bbox.is_dashed)

    def msgBox(self, info=NONE):
        messagebox.showinfo(title='HELLO', message=info)

    def cn_switch(self):
        #todo:???
        # sys.stdout.flush()
        # self.helpMenu.update_idletasks()
        # self.helpMenu.update()
        self.is_cn = True
        self.make_menu_bar(self.master)


    def en_switch(self):
        self.is_cn = FALSE
        self.make_menu_bar(self.master)
    def is_exit(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            root.destroy()


if __name__ == '__main__':
    root = Tk()
    root.title('Mark Tool -SINGLE')  # 修改框体的名字,也可在创建时使用className参数来命名
    # master.resizable(0,0)#框体大小可调性，分别表示x,y方向的可变性；
    # root.geometry('1210x800')  # 指定主框体大小；
    # root.columnconfigure(0, minsize=1000)
    # root.protocol("WM_DELETE_WINDOW", mark_tool.is_exit)
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
    root.iconbitmap(r"E:\Library\Pictures\main.ico")
    # root.overrideredirect(True)
    mark_tool = App(root)
    root.mainloop()
