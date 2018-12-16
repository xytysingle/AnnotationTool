#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/9/16 20:59
#!@Author :SINGLE
#!@File   :BaseEntity.py

from libs.jsonModel import jsonModel


@jsonModel()
class BaseEntity:

    def __init__(self):
        self.data={}
        self.code=""
        self.msg=""


