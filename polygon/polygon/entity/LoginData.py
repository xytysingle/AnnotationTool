#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/7/7 14:22
#!@Author :SINGLE
#!@File   :Category.py
from pylint.test.functional.arguments_differ import ParentClass

from entity.Category import Category
from entity.BaseEntity import BaseEntity
from libs.jsonModel import jsonModel


@jsonModel()
class User:
    def __init__(self):
        self.user_id=''
        self.user_name=''
        self.user_type=''

@jsonModel({"data":User},{})
class LoginData(BaseEntity):

    def __init__(self):
        BaseEntity.__init__(self)#调用未绑定的超类构造方法【必须显式调用父类的构造方法，否则不会执行父类构造方法，这个跟Java不一样】
        self.data=User()


