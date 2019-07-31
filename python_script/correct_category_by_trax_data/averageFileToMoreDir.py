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
    filepaths = glob.glob('/data/tanx/test/1/2/*.json')
    total=len(filepaths)
    num=5
    interval=total//5

    for i in range(0+1,num):
        for filepath in filepaths[interval*i:interval*(i+1)]:
            dst_dir=f'/data/tanx/test/1/2_{i}/'
            if not os.path.exists(dst_dir):
                os.mkdir(dst_dir)
            shutil.move(filepath, dst_dir)


if __name__ == '__main__':
    main()

