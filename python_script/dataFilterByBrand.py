#!/usr/bin/env python3
#!-*-coding:utf-8 -*-


import requests
import os
import json
import pandas as pds
import shutil
def main():
    data_src = '/data/tanx/res/data_src/0725品牌SKU.xlsx'
    pool_path = '/fast_data/CleanPool/41'
    categories=os.listdir(pool_path)
    pds.set_option('display.max_columns', 1000)
    pds.set_option('display.width', 1000)
    pds.set_option('display.max_colwidth', 1000)
    #读取其他数据
    data = pds.read_excel(data_src, header=0)
    #读取全品类分类
    filename = '/data/tanx/res/data_src/CleanPool2.json'
    with open(filename, 'r', encoding='utf-8') as file:
        dict_list_data = json.load(file)
    # print(dict_list_data[0])
    # print(data.head(0))
    # print(data.info())
    print(data.iloc[0, 0])
    # print(data.shape[0])
    # print(json.load(data.iloc[0][0])[0])
    others_data=[]
    main_data=[]
    # print(dir_name)
    #1.匹配其他数据
    # for category in categories:
    #     others_data.extend([ category for i in range(data.shape[0])  if category==  data.iloc[i,0].strip()])
    # # print(others_data)
    # #移动其他数据到pool_42
    # for item in others_data:
    #     print(os.path.join(pool_path,item),os.path.join(os.path.split(pool_path)[0],'42',item))
    #     shutil.move(os.path.join(pool_path,item),os.path.join(os.path.split(pool_path)[0],'42',item)+'/')
    #
    # print(os.path.join(pool_path, item), os.path.join(os.path.split(pool_path)[0], '42', item))

    #重新获取兵筛选移动后的数据
    remain_data=os.listdir(pool_path)
    #2.取剩下的数据匹配线上的数据
    for category in remain_data:
        main_data.extend([category for img_dict in dict_list_data if category == img_dict['sku_name']])
    # 移动匹配完线上的数据到pool_43
    for item in main_data:
        shutil.move(os.path.join(pool_path, item), os.path.join(os.path.split(pool_path)[0], '43', item))
    print(os.path.join(pool_path, item), os.path.join(os.path.split(pool_path)[0], '43', item))

if __name__ == '__main__':
    main()

