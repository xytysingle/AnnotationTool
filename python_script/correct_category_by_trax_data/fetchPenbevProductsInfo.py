#!/usr/bin/env python3
#!-*-coding:utf-8 -*-


import requests
import os
import json
import pandas as pds
from tqdm import  tqdm
def main():

    filepath='./res/products-penbev.json'
    dst_path='./dst/'
    # filepath='/data/tanx/bin/correct_category_by_trax_data/res/products-penbev.json'
    # dst_path='/data/tanx/bin/correct_category_by_trax_data/dst/'
    columns=['id','name','size','sizeUnit','category','brand','images','level1','level2','designChanges']
    data=[]
    with open(filepath,'r',encoding='utf-8') as f:
        product_data=json.load(f)
    for product in tqdm(product_data['data'][:]):
        print(product['id'])
        try:
            data.append([product['id'],product['name'],product['size'],product['sizeUnit'],product['category']['name']
                            ,product['brand']['name']])
            #product['level1']['name'],product['level2']['logo']
            path_url = product['images'][0]['path']
            path_url=path_url.replace(path_url[0:path_url.find('ccza')],
                             'https://services.traxretail.com/images/traxus/')
            data[-1].append(path_url+'/original')
            if 'level1' in product.keys():
                data[-1].append(product['level1']['name'])
            if 'level2' in product.keys() :
                logo_url = product['level2']['logo']
                logo_url=logo_url.replace(logo_url[0:logo_url.find('ccza')],
                                          'https://services.traxretail.com/images/traxus/')
                data[-1].append(logo_url+'/original')
            if product['designChanges']:
                designChanges_url = product['designChanges'][0]['images'][0]['path']
                designChanges_url=designChanges_url.replace(designChanges_url[0:designChanges_url.find('ccza')], 'https://services.traxretail.com/images/traxus/')
                data[-1].append(designChanges_url+'/original')
        except Exception as e:
             print(e)
             break
    t = pds.DataFrame(columns=columns, data=data)
    # print(t)
    t.to_csv(os.path.join(dst_path,'fetchPenbevProductsInfo.csv'), index=None)
if __name__ == '__main__':
    main()

