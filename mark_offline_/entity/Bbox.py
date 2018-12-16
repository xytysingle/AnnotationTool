#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/7/1 9:25
#!@Author :SINGLE
#!@File   :Bbox.py

class Bbox(object):
    def __init__(self,id, category,coord,is_dashed,color,rotate):
        # self.__id=id
        # self.__category= category
        # self.__coord= coord
        # self.__annotation= '%s(%s)'%(category,coord)
        self.id = id
        self.__category = category
        self.__coord = coord  #tuples
        self.is_dashed = is_dashed
        self.color = color
        self.rotate = rotate
        self.annotation ='%s%s' % (category, coord)
        # self.annotation = '%s(%s)' % (category, coord)


    def __str__(self):
        print()

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        # if not isinstance(value, int):
        #     raise ValueError('score must be an integer!')
        # if value < 0 or value > 100:
        #     raise ValueError('score must between 0 ~ 100!')
        self.__id = value

    @property
    def coord(self):
        return self.__coord

    @coord.setter
    def coord(self, value):
        self.__coord=value
        self.annotation = '%s%s' % (self.category, value)
    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value):
        self.__category=value
        self.annotation = '%s%s' % (value, self.coord)

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
