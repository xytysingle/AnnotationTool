#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/6/22 9:43
#!@Author :SINGLE
#!@File   :testt.py
#导入cv模块
import cv2 as cv
# 读取图像，支持 bmp、jpg、png、tiff 等常用格式
img = cv.imread(r"E:\Library\Pictures\test.png")
#创建窗口并显示图像
cv.namedWindow("Image")
cv.imshow("Image",img)
cv.waitKey(0)
#释放窗口
cv.destroyAllWindows()

print (cv.__version__)

# import cv2 as cv
#
# fname = r"E:\Library\Pictures\test.png"
# img = cv.imread(fname)
# # 画矩形框
# cv.rectangle(img, (212,317), (290,436), (0,255,0), 4)
# # 标注文本
# font=cv.FONT_HERSHEY_SIMPLEX
#
# text = 'hhhhhhhhhhhhh'
# cv.putText(img, text, (212, 310), font, 2, (0,0,255), 1)
# cv.imwrite('001_new.jpg', img)