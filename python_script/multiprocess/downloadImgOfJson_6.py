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
    data_src = r'G:\trax_data\20190717\*\*.json'
    file_paths = glob.glob(data_src)

    for file_path in file_paths:
        img_output_dir=os.path.dirname(file_path)
        print(img_output_dir)
        with open(file_path, 'r', encoding='utf-8') as file:
            dict_data = json.load(file)
            img_dict_data=dict_data['stitchingData']['probes']
            for item in img_dict_data:
                probe_url=item['probe_url']
                url=probe_url.replace(probe_url[0:probe_url.find('ccza')],'https://services.traxretail.com/images/traxus/')
                # print(url)
                # 下载图片,只用session进行操作。即只创建一个连接，并设置最大连接数或者重试次数。
                session = requests.Session()
                retry = Retry(connect=3, backoff_factor=0.5)
                adapter = HTTPAdapter(max_retries=retry)
                session.mount('http://', adapter)
                session.mount('https://', adapter)
                session.keep_alive = False

                response = session.get(url + '/original')
                img = response.content
                img_name = probe_url.split('/')[-1]
                # print(os.path.join(img_output_dir,f'{img_name}.jpg'))
                with open(os.path.join(img_output_dir, f'{img_name}.jpg'), 'wb') as file:
                    file.write(img)

if __name__ == '__main__':
    main()

