#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import cv2
import json
import os
import sys
import numpy as np
# from __future__ import unicode_literals


def str_hook(obj):
    # return {k.encode('utf-8') if isinstance(k, unicode) else k:
    #         v.encode('utf-8') if isinstance(v, unicode) else v
    #         for k, v in obj}
    return {k.encode('utf-8') if isinstance(k, str) else k:
                v.encode('utf-8') if isinstance(v, str) else v
            for k, v in obj}



def parse_json(input_file, draw=False):
    # , object_pairs_hook=str_hook
    with open(input_file, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
        # print(input_data)
        abs_path = os.path.abspath(input_file)
        abs_dir = os.path.dirname(abs_path)

        # read original images information
        images = []
        max_w = 0
        max_h = 0
        for probe in input_data['probeImages']:
            image = {}
            image['id'] = probe['probe_id']
            image_path = probe['probe_image_path']
            head, base = os.path.split(image_path)
            image['file'] = os.path.join(abs_dir, base + '.jpeg')
            w = image['w'] = probe['original_width']
            h = image['h'] = probe['original_height']
            for m in input_data['stitchingData']['molecules']:
                for d in m['data']:
                    if d['probe_pk'] == image['id']:
                        # print('find transform')
                        image['H'] = np.array(d['transform'], dtype=float)
                        break
            if 'H' not in image:
                #h = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
                image['H'] = np.eye(3, 3, dtype=float)

            #print(image)

            pts = np.float32(
                [[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, image['H'])
            rect = image['rect'] = cv2.boundingRect(dst)
            if max_w < (rect[0] + rect[2]):
                max_w = rect[0] + rect[2]
            if max_h < (rect[1] + rect[3]):
                max_h = rect[1] + rect[3]

            images.append(image)

        output = None
        imgs = [None, None]
        if draw:
            for i, image in enumerate(images):
                # print('{}'.format(image['file']))
                imgs[i] = cv2.imread(image['file'])
                output = cv2.warpPerspective(
                    imgs[i], image['H'], (image['w'], image['h']), output, borderMode=cv2.BORDER_TRANSPARENT)

        # draw products
        pts = None
        object_index = []
        points = []
        for p in input_data['products']:
            x = int(p['x'])
            y = int(p['y'])
            points.append([x, y])
            object_index.append([p['probe_id'], p['product_id']])
            if draw:
                cv2.circle(output, (x, y), 5, (0, 0, 255), 3)

        pts = np.float32(points).reshape(-1, 1, 2)
        for i, image in enumerate(images):
            objs = []
            H_inv = np.linalg.inv(image['H'])
            # print(image['H'])
            # print(H_inv)
            if len(points) > 0:
                dst = cv2.perspectiveTransform(pts, H_inv)
                for j, d_point in enumerate(dst):
                    x = d_point[0][0]
                    y = d_point[0][1]
                    if x < image['w'] and x >= 0 and y < image['h'] and y >= 0:
                        objs.append([x, y, object_index[j][1], object_index[j][0]])
                    if draw:
                        cv2.circle(imgs[i], (int(d_point[0][0]), int(
                            d_point[0][1])), 5, (0, 255, 255), 3)

            if draw:
                scale = 960. / float(imgs[i].shape[0])
                if scale < 1.0:
                    imgs[i] = cv2.resize(imgs[i], (0, 0), fx=scale, fy=scale)
                cv2.imshow("{}".format(i), imgs[i])
            images[i]['objects'] = objs

        # print(images)

        if draw:
            cv2.imshow("stitching", output)
            cv2.waitKey()

        return images


if __name__ == "__main__":

    for input_file in sys.argv[1:]:
        parse_json(input_file, draw=True)


'''
H1 = np.array([[0.24559931457042694, -0.06224933639168739, 286.8449401855469],
     [0.006159067153930664, 0.17961472272872925, 49.080711364746094],
     [0.00001644443182158284, -0.00009700922964839265, 1]], dtype=float)
H2 = np.array([
                    [0.148112952709198, -0.09270770102739334, 761.1323852539062],
                    [-0.020681526511907578, 0.16917912662029266, 53.60651779174805],
                    [-0.00006805119483033195, -0.00009501045133220032, 1]
                ], dtype=float)
img1 = cv2.imread('/home/alex/Downloads/scence/scence/9434046/original_1.jpeg')
img2 = cv2.imread('/home/alex/Downloads/scence/scence/9434046/original_2.jpeg')
h1,w1 = img1.shape[0:2]
h2,w2 = img2.shape[0:2]
pts1 = np.float32([[0, 0], [0, h1-1], [w1-1, h1-1], [w1-1, 0]]).reshape(-1, 1, 2)
pts2 = np.float32([[0, 0], [0, h2-1], [w2-1, h2-1], [w2-1, 0]]).reshape(-1, 1, 2)
dst1 = cv2.perspectiveTransform(pts1, H1)
dst2 = cv2.perspectiveTransform(pts2, H2)
bbox1 = cv2.boundingRect(dst1)
bbox2 = cv2.boundingRect(dst2)
w1 = bbox1[0] + bbox1[2]
h1 = bbox1[1] + bbox1[3]
w2 = bbox2[0] + bbox2[2]
y2 = bbox2[1] + bbox2[3]
w = w1 if w1 >= w2 else w2
h = h1 if h1 >= h2 else h2
warped = cv2.warpPerspective(img1, H1, (w, h))
warped = cv2.warpPerspective(img2, H2, (w, h), warped, borderMode=cv2.BORDER_TRANSPARENT)
cv2.imshow("warped", warped)
cv2.waitKey()
'''
