#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/7/7 14:22
#!@Author :SINGLE
#!@File   :Category.py
from libs.jsonModel import jsonModel


@jsonModel()
class Category(object):

    def __init__(self):
        self.color=""
        self.id= ""
        self.sku_name= ""
        self.__category= ""
        self.type_id= ""
        self.url= ""
    #
    # @property
    # def sku_name(self):
    #     return self.__sku_name
    #
    # @sku_name.setter
    # def sku_name(self, value):
    #     self.__sku_name = value

    @property
    def category(self):
        return self.sku_name

    # @category.setter
    # def category(self, value):
    #     self.__category = value