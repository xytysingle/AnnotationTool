# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   @Author: Kong Haiyang
   @Date: 2018-05-17 09:29:23
"""
from __future__ import absolute_import, division, print_function

import os
import subprocess
import sys

from tqdm import tqdm

if len(sys.argv) == 1:
    sys.argv.extend(
        '../detectron/datasets/data/ali0904191400 /data/datasets/coca/images \
          False . False .'.split())

if len(sys.argv) < 3:
    print('Usage: python gen_annos_from_class_images.py root_dir source_images \
            [ is_filter_out remain_skus is_mapping mapping_file ]')

print(len(sys.argv))

if len(sys.argv) == 3:
    root_dir, source_images = sys.argv[1:]
    is_filter_out = False
    remain_skus = None
    is_mapping = False
    mapping_file = None
elif len(sys.argv) == 5:
    root_dir, source_images, is_filter_out, remain_skus = sys.argv[1:]
    is_filter_out = True if is_filter_out == 'True' or is_filter_out == 'true' else False
    is_mapping = False
    mapping_file = None
elif len(sys.argv) == 7:
    root_dir, source_images, is_filter_out, remain_skus, is_mapping, mapping_file = sys.argv[1:]
    is_filter_out = True if is_filter_out == 'True' or is_filter_out == 'true' else False
    is_mapping = True if is_mapping == 'True' or is_mapping == 'true' else False

root_dir = os.path.abspath(root_dir)
class_images_folder = os.path.join(root_dir, 'class_images')

target_annos = os.path.join(root_dir, 'annos')
if not os.path.exists(target_annos):
    os.makedirs(target_annos)

if is_filter_out:
    if os.path.exists(remain_skus):
        remains = []
        with open(remain_skus) as f:
            remains = [line.strip() for line in f.readlines()]
    else:
        raise IOError('remain_skus file not exist.')

if is_mapping:
    if os.path.exists(mapping_file):
        mappings = {}
        with open(mapping_file) as f:
            lines = [line.strip() for line in f.readlines()]
            for line in lines:
                if line:
                    c, m = line.split()
                    mappings[c] = m
    else:
        raise IOError('mapping_file not exist.')


_anno_dict = {}
anno_count = {}

folders = [os.path.join(class_images_folder, anno) for anno in os.listdir(class_images_folder)
           if not anno.startswith('.') and os.path.isdir(os.path.join(class_images_folder, anno))]

for folder in tqdm(folders):
    annos = [anno for anno in os.listdir(folder) if anno.endswith('.jpg')]
    name = folder.rpartition('/')[-1]

    if is_mapping:
        if name in mappings:
            name = mappings[name]
        else:
            print('No mapping, remain original: {}'.format(name))

    if name not in anno_count:
        anno_count[name] = len(annos)
    else:
        anno_count[name] += len(annos)

    for anno in annos:
        parts = anno[:-4].split('_')
        image_name = os.path.join(source_images, '{}.jpg'.format(parts[0]))
        if not os.path.exists(image_name):
            continue
        _anno_dict.setdefault(parts[0], []).append([name] + parts[1:])

anno_dict = {}
key2id = {}
for k, values in _anno_dict.items():
    image_key = subprocess.check_output(['md5sum', '{}/{}.jpg'.format(source_images, k)])
    if image_key not in key2id:
        key2id[image_key] = k
        anno_dict[k] = values
    else:
        anno_dict[key2id[image_key]].extend(anno_dict[k])

for k, values in anno_dict.items():
    with open(os.path.join(target_annos, '{}.txt'.format(k)), 'w') as f:
        for v in values:
            f.write('{} {} {} {} {} {}\n'.format(v[0], v[1], v[2], v[3], v[4], v[5]))

count_list = [[k, v] for k, v in anno_count.items()]
count_list = sorted(count_list, key=lambda x: int(x[1]), reverse=True)
with open('{}/counts.txt'.format(root_dir), 'w') as f:
    for cl in count_list:
        f.write('{} {}\n'.format(cl[0], cl[1]))

with open('{}/classes.txt'.format(root_dir), 'w') as f:
    for cl in count_list:
        f.write('{}\n'.format(cl[0]))
