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
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        ccep_data = json.load(f)
    for ccep in tqdm(ccep_data[:]):
        print(ccep['id'],ccep['sku_name'])
        try:
            if ccep['type_id']=='31':
                data.append([ccep['id'],ccep['sku_name']])
        except Exception as e:
            print(e)
    t = pds.DataFrame(columns=columns, data=data)
    # print(t)
    t.to_csv(os.path.join(dst_path, 'CCEP_Info.csv'), index=None)

if __name__ == '__main__':
    main()

