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
        dst_files=glob.glob('/fast_data/CleanPool/33/*/*.jpg')
        # print(dst_files[0])
    new_names=list(map(get_new_name,dst_files))
    for dir in glob.glob('/fast_data/CleanPool/33/*'):
        os.rename(dir,os.path.join(os.path.split(dir)[0],'clustered_'+os.path.split(dir)[1]))
    # print(new_names)

def get_new_name(dst_filepath):
    #8C75E7C9-017E-4F18-8AD0-D17579623B10_1_1_1610_3176_1847_3913
    list=os.path.split(dst_filepath)[1].split('.')[0].split('_',3)
    dst_filename='_'.join([list[0],list[1],list[2]])
    # print(list)
    for dict in dict_list_data:
        # print(dict['oldIndex'] ,dst_file)
        if dict['oldIndex'] == dst_filename:
            if len(list[3].split('_'))==4:
                list[3]=list[3]+'_0'
            new_name=os.path.join(os.path.split(os.path.split(dst_filepath)[0])[0],os.path.split(dst_filepath)[0].split('/')[-1],str(dict['newIndex'])+"_"+list[3]+os.path.splitext(dst_filepath)[1])
            # print(new_name)
            os.renames(dst_filepath,new_name)
            return dict['newIndex']

if __name__ == '__main__':
    main()