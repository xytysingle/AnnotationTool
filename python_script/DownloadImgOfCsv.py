#!/usr/bin/env python3
#!-*-coding:utf-8 -*-

import requests
import os
import json
import pandas as pds
def main():
    data = pds.read_csv(open('./res/冰露堆头24.csv'),header=None)
    pds.set_option('display.max_columns', 1000)
    pds.set_option('display.width', 1000)
    pds.set_option('display.max_colwidth', 1000)
    #
    # # print(data.head(0))
    # # print(data.info())
    print(data.iloc[0,0])
    print(data.shape[0])
    # print(json.load(data.iloc[0][0])[0])

    id=0
    for i in range(data.shape[0]):
        #读取指定行列
        img_urls = json.loads(data.iloc[i,0])
        # print(type(img_urls))
        # 遍历获取图片链接并下载到本地
        for img_url in img_urls:
            response = requests.get(img_url)
            img = response.content
            with open('./imgs/{0}.jpg'.format(id), 'wb') as file:
                file.write(img)
            id += 1
    #
    print('conout %d' % id)
if __name__ == '__main__':
    main()

