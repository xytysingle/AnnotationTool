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
    filename = '/fast_data/CCEP/resultsJson/imgIndexOldAndNew.json'
    with open(filename, 'r', encoding='utf-8') as file:
        dict_list_data = json.load(file)
        # print(dict_list_data)
        dst_files=glob.glob('/fast_data/CleanPool/32/*/*.jpg')
        print(dst_files)
    new_names=map(get_new_name,dst_files)
    print(new_names)
def get_new_name(dst_file):
    dst_file=os.path.split(dst_file)[1].split('.',3)
    print(dst_file)
    # for dict in tqdm(dict_list_data):
    #     if dict['oldIndex'] == dst_file:
    #         return dict['newIndex']

if __name__ == '__main__':
    main()

