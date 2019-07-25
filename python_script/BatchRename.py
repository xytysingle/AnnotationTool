#!/usr/bin/env python3
#!-*-coding:utf-8 -*-

#J
import os
def main():
    path = '/data/tanx/test'
    filelist = os.listdir(path)
    # print(type(filelist))
    total_num = len(filelist)
    i = 6059698
    for item in filelist:
        if item.endswith('.jpg'):
            src = os.path.join(path, item)
            dst = os.path.join(path,f"{str(i):0>7s}" + '.jpg')
            try:
                os.rename(src, dst)
                i = i + 1
            except:
                continue


if __name__ == '__main__':
    main()

