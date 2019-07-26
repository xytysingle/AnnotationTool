#!/usr/bin/env python3
#!-*-coding:utf-8 -*-

import glob
import shutil
import requests
import os
from tqdm import tqdm
import json
import pandas as pds
def main():
    global dict_list_data
    filename = '/data/tanx/res/data_src/CleanPool2.json'
    categories=os.listdir('/fast_data/Beer/CleanPool/2/')
    with open(filename, 'r', encoding='utf-8') as file:
        dict_list_data = json.load(file)
        # print(dict_list_data)
    sku_names=[]
    for category in categories:
        for img_dict in dict_list_data:
            if category==img_dict['sku_name'] and (int(img_dict['brand_id'])==303 or int(img_dict['brand_id'])==183):
                sku_names.append((img_dict['id'], img_dict['sku_name']))
    print(sku_names,len(sku_names))
    

    for sku_name_tuple in sku_names:
        shutil.copytree(os.path.join('/fast_data/Beer/CleanPool/2/',sku_name_tuple[1]),os.path.join('/fast_data/Drink_China/waitfortrain/',sku_name_tuple[0]+'^'+sku_name_tuple[1]))
        # print(os.path.join('/fast_data/Beer/CleanPool/2/',sku_name_tuple[1]),os.path.join('/fast_data/Drink_China/waitfortrain/',sku_name_tuple[0]+'^'+sku_name_tuple[1]))



if __name__ == '__main__':
    main()