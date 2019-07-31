#!/usr/bin/env python3
#!-*-coding:utf-8 -*-


import requests
import os
import json
import pandas as pds
from tqdm import tqdm
import shutil
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
def main():
        # print(f"{'321':0>7}")
        # print(os.path.join(r'\Users/michael', 'testdir'))
        filepath = './data_src/get_all.json'
        # filepath='/data/tanx/bin/correct_category_by_trax_data/res/products-penbev.json'
        # dst_path='/data/tanx/bin/correct_category_by_trax_data/dst/'
        dst_dir = 'D:\\xzz\\'
        columns = ['id', 'sku_name']
        ccep_data = []
        # with open(filepath, 'r', encoding='utf-8') as f:
        #     all_data = json.load(f)
        get_url='http://annotation.lingmou.ai:8000/index.php/skus/get-all'
        response=requests.get(get_url)
        all_data=response.json()

        # 下载图片,只用session进行操作。即只创建一个连接，并设置最大连接数或者重试次数。
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.keep_alive = False

        for sku_dict in tqdm(all_data):
            # try:
            if sku_dict['type_id']=='31' and sku_dict['url'] and 'Combo_' not in sku_dict['sku_name']:
                # ccep_data.append([sku_dict['id'],sku_dict['sku_name']])
                if sku_dict['url']:
                    logo_url='http://annotation.lingmou.ai:8000/'+sku_dict['url']
                    img_content = session.get(logo_url).content

                    #将sku_name作为windows文件夹名字命名时去掉首尾空格,换行符等符号
                    sku_name = sku_dict['sku_name'].strip()

                    save_dir=os.path.join(dst_dir, sku_name)
                    # print("判断文件夹是否存在..........")
                    if os.path.exists(save_dir):
                        # print("存在,删除中··········")
                        shutil.rmtree(save_dir)
                        # print("删除完毕！")
                    else:
                        # print("新建文件夹", save_dir, "中...........")
                        os.mkdir(save_dir)
                        # os.chdir(save_dir)
                        # print("新建完成..............")
                    with open(os.path.join(save_dir,sku_name+os.path.splitext(logo_url)[-1]),'wb') as f:
                        f.write(img_content)

            # except Exception as e:
            #         print(e)
            # t = pds.DataFrame(columns=columns, data=ccep_data)
            # print(t)
            # t.to_csv(os.path.join(dst_path, 'CCEP_Info_1.csv'), index=None,encoding='utf-8-sig')

if __name__ == '__main__':
    main()

