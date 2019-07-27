#!/usr/bin/env python3
#!-*-coding:utf-8 -*-

import requests
import time
import json
import os
import pandas as pds
def main():
    data_src='/data/tanx/res/data_src/冰露堆头24.csv'
    data = pds.read_csv(open(data_src),header=None)
    pds.set_option('display.max_columns', 1000)
    pds.set_option('display.width', 1000)
    pds.set_option('display.max_colwidth', 1000)

    # print(data.head(0))
    # print(data.info())
    print(data.iloc[0,0])
    print(data.shape[0])
    # print(json.load(data.iloc[0][0])[0])

    id=0
    dir_name=os.path.join('/data/tanx/res/output/',os.path.split(data_src)[1].split('.')[0]+'_'+time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
    #print(dir_name)
    os.mkdir(dir_name)
    if os.path.exists(dir_name):
        for i in range(data.shape[0]):
            #读取指定行列
            print(id,id == 15)
            # if id > 5:
            #     break
            img_urls = json.loads(data.iloc[i,0])
            # 遍历获取图片链接并下载到本地
            for img_url in img_urls:
                response = requests.get(img_url)
                img = response.content
                img_name=time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
                with open(os.path.join(dir_name,f'{img_name}.jpg'), 'wb') as file:
                    file.write(img)
                id += 1
    #
    print('conout %d' % id)
if __name__ == '__main__':
    main()

