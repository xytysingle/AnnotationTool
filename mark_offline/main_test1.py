# import re
#
# s = '1中文中文：123456aa哈哈哈bbcc'
# print(re.match(u"[\u4e00-\u9fa5]+", s) )
#  # None. 只从字符串的开始匹配，没有匹配上返回None,否则返回matchobject
#
# pat = '中文'
# print(re.search(pat, s).group())
#   # matchobject. 对整个字符串进行匹配，，没有匹配上返回None,否则返回matchobject
#
# newpat = '这里是中文内容'
# news = re.sub(pat, newpat, s)  # 正则部分替换，将s中的所有符合pat的全部替换为newpat，newpat也可以是函数
# print(news)
#
#
#
# def newpat_func(matched):
#     return "这里是" + matched.group() + u"内容"
#
#
# print(re.sub(pat, newpat_func, s))


# for i,bbox in enumerate

#
# from tkinter import *
# import threading, time
# trace = 0
# class CanvasEventsDemo:
#   def __init__(self, parent=None):
#     canvas = Canvas(width=300, height=300, bg='beige')
#     canvas.pack()
#     canvas.bind('<ButtonPress-1>', self.onStart)   # click
#     canvas.bind('<B1-Motion>',   self.onGrow)    # and drag
#     canvas.bind('<Double-1>',   self.onClear)   # delete all
#     canvas.bind('<ButtonPress-3>', self.onMove)    # move latest
#     self.canvas = canvas
#     self.drawn = None
#     self.kinds = [canvas.create_oval, canvas.create_rectangle]
#   def onStart(self, event):
#     self.shape = self.kinds[0]
#     self.kinds = self.kinds[1:] + self.kinds[:1]   # start dragout
#     self.start = event
#     self.drawn = None
#   def onGrow(self, event):               # delete and redraw
#     canvas = event.widget
#     if self.drawn: canvas.delete(self.drawn)
#     objectId = self.shape(self.start.x, self.start.y, event.x, event.y)
#     if trace: print(objectId)
#     self.drawn = objectId
#   def onClear(self, event):
#     event.widget.delete('all')            # use tag all
#   def onMove(self, event):
#     if self.drawn:                  # move to click spot
#       if trace: print(self.drawn)
#       canvas = event.widget
#       diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
#       canvas.move(self.drawn, diffX, diffY)
#       self.start = event
# class CanvasEventsDemoTags(CanvasEventsDemo):
#   def __init__(self, parent=None):
#     CanvasEventsDemo.__init__(self, parent)
#     self.canvas.create_text(100, 8, text='Press o and r to move shapes')
#     self.canvas.master.bind('<KeyPress-o>', self.onMoveOvals)
#     self.canvas.master.bind('<KeyPress-r>', self.onMoveRectangles)
#     self.kinds = self.create_oval_tagged, self.create_rectangle_tagged
#   def create_oval_tagged(self, x1, y1, x2, y2):
#     objectId = self.canvas.create_oval(x1, y1, x2, y2)
#     self.canvas.itemconfig(objectId, tag='ovals', fill='blue')
#     return objectId
#   def create_rectangle_tagged(self, x1, y1, x2, y2):
#     objectId = self.canvas.create_rectangle(x1, y1, x2, y2)
#     self.canvas.itemconfig(objectId, tag='rectangles', fill='red')
#     return objectId
#   def onMoveOvals(self, event):
#     print('moving ovals')
#     self.moveInSquares(tag='ovals')      # move all tagged ovals
#   def onMoveRectangles(self, event):
#     print('moving rectangles')
#     self.moveInSquares(tag='rectangles')
#   def moveInSquares(self, tag):         # 5 reps of 4 times per sec
#     for i in range(5):
#       for (diffx, diffy) in [(+20, 0), (0, +20), (-20, 0), (0, -20)]:
#         self.canvas.move(tag, diffx, diffy)
#         self.canvas.update()       # force screen redraw/update
#         time.sleep(0.25)         # pause, but don't block gui
# class CanvasEventsDemoThread(CanvasEventsDemoTags):
#   def moveEm(self, tag):
#     for i in range(5):
#       for (diffx, diffy) in [(+20, 0), (0, +20), (-20, 0), (0, -20)]:
#         self.canvas.move(tag, diffx, diffy)
#         time.sleep(0.25)           # pause this thread only
#   def moveInSquares(self, tag):
#     threading.Thread(self.moveEm, (tag,)).start()
# if __name__ == '__main__':
#   CanvasEventsDemoThread()
#   mainloop()


#python tkinter menu

from tkinter import *

# some vocabulary to keep from getting confused. This terminology
# is something I cooked up for this file, but follows the man pages
# pretty closely
#
#
#
#       This is a MENUBUTTON
#       V
# +-------------+
# |             |
#
# +------------++------------++------------+
# |            ||            ||            |
# |  File      ||  Edit      || Options    |   <-------- the MENUBAR
# |            ||            ||            |
# +------------++------------++------------+
# | New...         |
# | Open...        |
# | Print          |
# |                |  <------ This is a MENU. The lines of text in the menu are
# |                |                          MENU ENTRIES
# |                +---------------+
# | Open Files >   | file1         |
# |                | file2         |
# |                | another file  | <------ this cascading part is also a MENU
# +----------------|               |
#                  |               |
#                  |               |
#                  |               |
#                  +---------------+

__author__ = {'name' : 'Hongten',
              'Email' : 'hongtenzone@foxmail.com',
              'Blog' : 'http://www.cnblogs.com/hongten',
              'QQ' : '648719819',
              'Created' : '2013-09-10'}
# _*_ coding:utf-8 _*_
# from tkinter import *
# tk = Tk()
# canvas = Canvas(width=500,height=500)
# canvas.pack()
#
#
# #canvas.create_polygon(0,0,250,250,fill = 'red')
#
# def echo_event(evt):
#     #打印键盘事件
#     if evt.type == "2":
#         print("键盘：%s" % evt.keysym)
#     #打印鼠标操作
#     if evt.type == "4":
#         print("鼠标： %s" % evt.num)
#     #
#     print(evt.type)
#
# #键盘事件
# # canvas.bind_all("<KeyPress>",echo_event)
# #如果绑定指定的键盘，则"<Key>" 或者"<KeyPress>"都可以，具体到指定键的话后面加入下划线和指定的键就好了，如：绑定小写字母t和Left键
# canvas.bind("<KeyPress-t>",echo_event)
# canvas.bind_all("<KeyPress-Left>",echo_event)
# #鼠标事件
# canvas.bind_all("<Double-Button-1>",echo_event)
# canvas.bind_all("<Button-1>",echo_event)
# canvas.bind_all("<Button-2>",echo_event)
# canvas.bind_all("<Button-3>",echo_event)
# if __name__ == '__main__':
#     mainloop()
# from tkinter import *
#
#
# def call_back(event):
#     print(event.keysym)
#
#
# def main():
#     root = Tk()
#
#     # 创建一个框架，在这个框架中响应事件
#     frame = Frame(root,
#                   width=200, height=200,
#                   background='green')
#
#     # 这样就不用查看 键盘特殊按键的keysym表了。
#     # 试一下就知道了
#     frame.bind("<KeyPress>", call_back)
#     frame.pack()
#
#     # 当前框架被选中，意思是键盘触发，只对这个框架有效
#     frame.focus_set()
#
#     mainloop()
#
#
# if __name__ == '__main__':
#     main()

from tkinter import *

class make_list(Listbox):
    def __init__(self,master, **kw):
        self.canvas=Canvas(master,width=500,height=600,bg='green')
        self.canvas.pack()
        self.canvas.create_rectangle(0,50,100,100,dash=' ')



if __name__ == '__main__':
    tk = Tk()
    make_list(tk)
    tk.mainloop()



