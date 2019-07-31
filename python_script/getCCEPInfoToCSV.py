#!/usr/bin/env python3
#!-*-coding:utf-8 -*-


import requests
import os
import json
import pandas as pds
from tqdm import tqdm
def main():
        # print(f"{'321':0>7}")
        # print(os.path.join(r'\Users/michael', 'testdir'))
        filepath = './data_src/get_all.json'
        dst_path = './dst/'
        # filepath='/data/tanx/bin/correct_category_by_trax_data/res/products-penbev.json'
        # dst_path='/data/tanx/bin/correct_category_by_trax_data/dst/'
        columns = ['id', 'sku_name']
        ccep_data = []
        # with open(filepath, 'r', encoding='utf-8') as f:
        #     all_data = json.load(f)
        get_url='http://annotation.lingmou.ai:8000/index.php/skus/get-all'
        response=requests.get(get_url)
        all_data=response.json()
        for sku_dict in tqdm(all_data):
            try:
                if sku_dict['type_id']=='31':
                    ccep_data.append([sku_dict['id'],sku_dict['sku_name']])
            except Exception as e:
                print(e)
        t = pds.DataFrame(columns=columns, data=ccep_data)
        # print(t)
        t.to_csv(os.path.join(dst_path, 'CCEP_Info_1.csv'), index=None,encoding='utf-8-sig')

if __name__ == '__main__':
    main()

