#!/usr/bin/env python3
#!-*-coding:utf-8 -*-
import shutil

import requests
import os
import json
import pandas as pds
from tqdm import tqdm
import glob
def main():
    # print(f"{'321':0>7}")
    # print(os.path.join(r'\Users/michael', 'testdir'))
    filepaths = glob.glob('/fast_data/Arca/clustered_300000/*/*.jpg')
    total=len(filepaths)
    print('total:'+str(total))
    interval=int(input('请输入平均数:'))
    num=total//interval
    # remain=total%num
    index=51
    for i in tqdm(list(range(0,num))):
        for filepath in filepaths[interval*i:interval*(i+1)]:
            sku_name=os.path.dirname(filepath).split('/')[-1]
            dst_dir=f'/fast_data/CleanPool/{index}/{sku_name}/'
            print(filepath,dst_dir)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            shutil.move(filepath, dst_dir)
        index+=1

    remain = glob.glob('/fast_data/Arca/clustered_300000/*/*.jpg')
    print(len(remain))
    for filepath in remain:
        sku_name = os.path.dirname(filepath).split('/')[-1]
        dst_dir = f'/fast_data/CleanPool/{index-1}/{sku_name}/'
        print(filepath, dst_dir)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        shutil.move(filepath, dst_dir)


def renameDir():
    for dir in tqdm(glob.glob('/fast_data/Arca/clustered_300000/*')):
        # print(dir+'==='+os.path.join(os.path.split(dir)[0],'clustered_'+os.path.split(dir)[1].zfill(4)))
        os.rename(dir,os.path.join(os.path.split(dir)[0],'clustered_'+os.path.split(dir)[1].zfill(4)))
def copyTo():
    for dir in tqdm(glob.glob('/fast_data/Arca/clustered_300000/*')):
        shutil.copytree(dir,'/fast_data/CleanPool/50/')
if __name__ == '__main__':
    main()
    # renameDir()
    # copyTo()

