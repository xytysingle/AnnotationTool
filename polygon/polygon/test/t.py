#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/10/6 16:48
#!@Author :SINGLE
#!@File   :t.py

# !/usr/bin/python
# -*- coding: UTF-8 -*-


def isInsidePolygon(pt, poly):
    c = False
    i = -1
    l = len(poly)
    j = l - 1
    while i < l - 1:
        i += 1
        print
        i, poly[i], j, poly[j]
        if ((poly[i]["lat"] <= pt["lat"] and pt["lat"] < poly[j]["lat"]) or (
                poly[j]["lat"] <= pt["lat"] and pt["lat"] < poly[i]["lat"])):
            if (pt["lng"] < (poly[j]["lng"] - poly[i]["lng"]) * (pt["lat"] - poly[i]["lat"]) / (
                    poly[j]["lat"] - poly[i]["lat"]) + poly[i]["lng"]):
                c = not c
        j = i
    return c


if __name__ == '__main__':
    abc = [{'lat': 1, 'lng': 1}, {'lat': 1, 'lng': 4}, {'lat': 3, 'lng': 7}, {'lat': 4, 'lng': 4}, {'lat': 4, 'lng': 1}]
    print(isInsidePolygon({'lat': 3, 'lng': 5}, abc))
#