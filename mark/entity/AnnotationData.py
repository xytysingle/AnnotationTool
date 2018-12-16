#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/9/19 10:02
#!@Author :SINGLE
#!@File   :AnnotationData.py
from entity.Bbox import Bbox
from libs.jsonModel import jsonModel


@jsonModel({},{"bboxes":Bbox})
class AnnotationData:
    def __init__(self):
        self.deleted=False
        self.id=""
        self.username=""
        self.sceneType=-1
        self.image=""
        self.rotate=0
        self.created_at=0
        self.updated_at=0
        self.bboxes=[]
