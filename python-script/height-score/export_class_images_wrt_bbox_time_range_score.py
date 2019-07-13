#!/usr/bin/env python

import os
import sys
import cv2
import numpy as np
import pymongo
from tqdm import tqdm

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.coca

if len(sys.argv) == 4:
    print('Using default time range and score to export...')
    begin_index, end_index, target_dir = sys.argv[1:]
    start_time = -1
    end_time = np.inf
    score = np.inf
elif len(sys.argv) == 5:
    print('Using default time range to export...')
    begin_index, end_index, target_dir, score = sys.argv[1:]
    score = float(score)
    start_time = -1
    end_time = np.inf
elif len(sys.argv) == 6:
    print('Using default score to export...')
    begin_index, end_index, target_dir, start_time, end_time = sys.argv[1:]
    start_time = int(start_time)
    end_time = int(end_time)
    score = np.inf
elif len(sys.argv) == 7:
    print('Have set all parameters...')
    begin_index, end_index, target_dir, start_time, end_time, score = sys.argv[1:]
    start_time = int(start_time)
    end_time = int(end_time)
    score = float(score)
else:
    print('Usage: python export_class_images_from_db.py begin_index end_index target_dir start_time end_time score')
    print('Eg: python export_class_images_from_db.py 800000 801000 test 1533638157 1533638161 0.5')
    print('Or: "python export_class_images_from_db.py 800000 801000 test 1533638157 1533638161" to use default score')
    print('Or: "python export_class_images_from_db.py 800000 801000 test 0.5" to use default time range')
    print('Or: "python export_class_images_from_db.py 800000 801000 test" to use default time range and score')
    raise ValueError("Must have 3, 4, 5 or 6 Parameters!")

if not os.path.exists(target_dir):
    os.mkdir(target_dir, 0777)

begin = int(begin_index)
end = int(end_index) + 1

for i in tqdm(range(begin, end)):
    index = '{:06d}'.format(i)
    print('Extracting ' + index)
    annotation = db.annotations.find_one({'image': index, 'deleted': False})
    if not annotation:
        print 'Annotation not found!'
        continue
    rotate = annotation['rotate']
    fname = os.path.join('/data/datasets/coca/images', index + '.jpg')
    if not os.path.exists(fname):
        print (fname, "not found")
        continue
    im = cv2.imread(fname)
    if rotate != 0:
        rot_mat = cv2.getRotationMatrix2D((im.shape[1] / 2, im.shape[0] / 2), rotate, 1)
        im = cv2.warpAffine(im, rot_mat, (im.shape[1], im.shape[0]))
    height, width = im.shape[:-1]

    for i, bbox in enumerate(annotation['bboxes']):
        if bbox.get('score', 0.0) > score:
            cls = bbox['className'].encode('utf-8')
            x1 = int(bbox['x1'])
            y1 = int(bbox['y1'])
            x2 = int(bbox['x2'])
            y2 = int(bbox['y2'])
            x1 = x1 if x1 >= 0 else 0
            y1 = y1 if y1 >= 0 else 0
            x2 = x2 if x2 <= width else width
            y2 = y2 if y2 <= height else height
            truncated = bbox['truncated']
            attribute = bbox.get('attribute', None)
            if attribute:
                cls = '{}|{}'.format(cls, attribute.encode('utf-8'))
            crop_img = im[y1:y2, x1:x2]
            class_path = os.path.join(target_dir, cls)
            if not os.path.exists(class_path):
                os.mkdir(class_path, 0777)
            cv2.imwrite(os.path.join(class_path, '{}_{}_{}_{}_{}_{}.jpg'.format(
                index, x1, y1, x2, y2, truncated)), crop_img)

        if not (start_time == -1 and end_time == np.inf):
            time = bbox.get('time', None)
            if time is None or not (start_time <= time <= end_time):
                continue

