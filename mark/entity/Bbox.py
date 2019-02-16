#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/7/1 9:25
#!@Author :SINGLE
#!@File   :Bbox.py
from libs.jsonModel import jsonModel


@jsonModel()
class Bbox(object):
    def __init__(self, rectangle_id="",className="",color="",username=None,truncated=0,x1=0,y1=0,x2=0,y2=0,id="",time='',side_truncated=0,type_id="1",sceneType="-1",check="False",score=0,type="0",attribute=''):
        # self.__id=sku_name
        # self.__category= category
        # self.__coord= coord
        self.__annotation=''

        # self.id = ""
        # self.__category = ""
        # self.__coord = ""  #tuples
        # self.is_dashed = ""
        self.color = color
        self.rectangle_id = rectangle_id
        self.is_show=True
        # self.rotate = rotate
        # self.annotation ='%s%s' % ("", "")

        # self.annotation = '%s(%s)' % (category, coord)

        #json实体类
        self.username=username
        self.side_truncated=side_truncated
        self.type_id=type_id
        self.sceneType=sceneType
        self.id=id
        self.truncated=truncated
        self.check=check
        self.className=className
        self.type=type
        self.score=score
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
        self.attribute=attribute
        self.time=time
    # def __str__(self):
    #     print()

    # @property
    # def id(self):
    #     return self.__id

    # @id.setter
    # def id(self, value):
        # if not isinstance(value, int):
        #     raise ValueError('score must be an integer!')
        # if value < 0 or value > 100:
        #     raise ValueError('score must between 0 ~ 100!')
        # self.__id = value

    # @property
    # def coord(self):
    #     return self.__coord
    #
    # @coord.setter
    # def coord(self, value):
    #     self.__coord=value
    #     self.annotation = '%s%s' % (self.category, value)
    @property
    def annotation(self):
        return  '%s %s %s%s'%(self.username,self.attribute,self.className,( self.x1,self.y1,self.x2,self.y2))

    # @annotation.setter
    # def annotation(self, value):
    #     self.__category=value
    #     self.annotation = '%s%s' % (value, self.coord)

    #定制类
    # def __init__(self):
    #     self.a, self.b = 0, 1  # 初始化两个计数器a，b
    #
    # def __iter__(self):
    #     return self  # 实例本身就是迭代对象，故返回自己
    #
    # def __next__(self):
    #     self.a, self.b = self.b, self.a + self.b  # 计算下一个值
    #     if self.a > 100000:  # 退出循环的条件
    #         raise StopIteration()
    #     return self.a  # 返回下一个值
