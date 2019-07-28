#!/usr/bin/env python3
#!-*-coding:utf-8 -*-

#J
import os
def main():
    path = '/data/tanx/test'
    filename_list = os.listdir(path)
    # print(type(filename_list))
    total_num = len(filename_list)
    i = 6059698
    for filename in filename_list:
        if filename.endswith('.jpg'):
            src = os.path.join(path, filename)
            dst = os.path.join(path,f"{str(i):0>7s}" + '.jpg')
            os.rename(src, dst)
            i = i + 1


if __name__ == '__main__':
    main()

