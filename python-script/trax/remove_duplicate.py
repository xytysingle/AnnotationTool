# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   @Author: Kong Haiyang
   @Date: 2018-05-21 09:40:31
"""
from __future__ import absolute_import, division, print_function

import hashlib
import os
from os import walk
import time
from PIL import Image
from tqdm import tqdm

path1 = '/Users/lingmou/Desktop/堆头项目/duitou2/'
# path2 = '/home/konghaiyang/kong/scene_classifier/data/0827待跑场景分类图片_results_results/可口可乐旗下大包装堆头带托盘'

tt = time.time()

files = []
for dirpath, dirnames, filenames in walk(path1):

    if dirnames:
        continue

    _files = [os.path.join(dirpath, f) for f in os.listdir(dirpath)
              if f.endswith('.jpg') and not f.startswith('.')]
    files.extend(_files)

# for dirpath, dirnames, filenames in walk(path2):

#   if dirnames:
#     continue

#   _files = [os.path.join(dirpath, f) for f in os.listdir(dirpath)
#             if f.endswith('.jpg') and not f.startswith('.')]
#   files.extend(_files)

md5_set = set()
files_dict = {}
for f in tqdm(files):
    im = Image.open(f)
    md5 = hashlib.md5(im.tobytes()).hexdigest()
    files_dict.setdefault(md5, []).append(f)
    if md5 in md5_set:
        print('\n'+'='*20+md5+'='*20)
        for fd in files_dict[md5]:
            print(fd)
        files_dict[md5].remove(f)
        os.remove(f)
        print('Remove {}.'.format(f))
    else:
        md5_set.add(md5)

print(time.time()-tt)
