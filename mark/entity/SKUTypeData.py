#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/7/7 14:22
#!@Author :SINGLE
#!@File   :Category.py

from entity.BaseEntity import BaseEntity
from libs.jsonModel import jsonModel

@jsonModel({},{})
class SKU:
    def __init__(self):
        self.id=''
        self.type_name=''
        self.state=''

@jsonModel({},{"sku_type":SKU})
class Data:
    def __init__(self):
        self.sku_type=[]

@jsonModel({"data":Data})
class SKUTypeData(BaseEntity):

    def __init__(self):
        BaseEntity.__init__(self)#调用未绑定的超类构造方法【必须显式调用父类的构造方法，否则不会执行父类构造方法，这个跟Java不一样】
        self.data=Data()


