#!/usr/bin/env python3
#!-*-coding:utf-8 -*-

import requests
import time
import json
import os
import io
import glob
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
def main():
    #20190705-20190709
    data_src = r'G:\trax_data\20190716\*\*.json'
    file_paths = glob.glob(data_src)
    data=[]
    for file_path in file_paths:
        img_output_dir=os.path.dirname(file_path)
        # print(img_output_dir)
        with open(file_path, 'r', encoding='utf-8') as file:
            dict_data = json.load(file)
            img_dict_data=dict_data['stitchingData']['probes']
            data.append((img_output_dir,img_dict_data))
    for item in data:
        print(item[0])
        for img_dict in item[1]:
            probe_url=img_dict['probe_url']
            url = probe_url.replace(probe_url[0:probe_url.find('ccza')],
                                    'https://services.traxretail.com/images/traxus/')
            # 下载图片,只用session进行操作。即只创建一个连接，并设置最大连接数或者重试次数。
            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            session.keep_alive = False

            response = session.get(url+'/original')
            img = response.content
            img_name=probe_url.split('/')[-1]
            # print(os.path.join(img_output_dir,f'{img_name}.jpg'))
            with open(os.path.join(item[0],f'{img_name}.jpg'), 'wb') as file:
                file.write(img)

    # print(os.path.split(data_src))
    # id=0
    # dir_name=os.path.join('/data/tanx/res/output/',os.path.split(data_src)[1].split('.')[0]+'_'+time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
    # #print(dir_name)
    # os.mkdir(dir_name)
    # if os.path.exists(dir_name):
    #     for i in range(data.shape[0]):
    #         #读取指定行列
    #         print(id,id == 15)
    #         # if id > 5:
    #         #     break
    #         img_urls = json.loads(data.iloc[i,0])
    #         # 遍历获取图片链接并下载到本地
    #         for img_url in img_urls:
    #             response = requests.get(img_url)
    #             img = response.content
    #             img_name=time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
    #             with open(os.path.join(dir_name,f'{img_name}.jpg'), 'wb') as file:
    #                 file.write(img)
    #             id += 1
    #
    # print('conout %d' % id)
if __name__ == '__main__':
    main()

