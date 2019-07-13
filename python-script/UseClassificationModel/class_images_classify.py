#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import os
import shutil
import signal
import time

import cv2
import numpy as np

import image_store
import mxnet as mx
from classifier import (get_registered_classifier, load_classifier,
                        load_classifiers)
from logger import logger
from message_queue import *

os.environ['MXNET_CUDNN_AUTOTUNE_DEFAULT'] = '0'
os.environ['PYTHONUNBUFFERED'] = '1'

os.chdir(os.path.abspath(os.path.dirname(__file__)))

COUNT_PRIORITY_QUEUES = 3
H_FLIP_AUG = False
SCALE_720_AUG = False
runnable = True

SKU_LIST = [
]


def parse_args():
    parser = argparse.ArgumentParser(description='Ali Classification Server')
    parser.add_argument('--gpu', help='GPU device to use', default=0, type=int)
    args = parser.parse_args()
    return args


def transform(im, pixel_means):
    """
    transform into mxnet tensor,
    subtract pixel size and transform to correct format
    :param im: [height, width, channel] in BGR
    :param pixel_means: [B, G, R pixel means]
    :return: [batch, channel, height, width]
    """
    im_tensor = np.zeros((1, 3, im.shape[0], im.shape[1]))
    for i in range(3):
        im_tensor[0, i, :, :] = im[:, :, 2 - i] - pixel_means[2 - i]
    return im_tensor


def get_image_patch_padded(rgb_img, x1, y1, x2, y2):
    """
    Pad image patch with surrounding background
    :param rgb_img:
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    w = x2 - x1
    h = y2 - y1
    l = max(w, h)
    target = np.empty((l, l, 3), dtype=np.uint8)
    target[:, :, :] = [124, 117, 104]  # rgb
    x1_ = (x1 + x2 - l) / 2
    x2_ = (x1 + x2 + l) / 2
    y1_ = (y1 + y2 - l) / 2
    y2_ = (y1 + y2 + l) / 2

    org_h, org_w, _ = rgb_img.shape
    target[max(-y1_, 0):min(l - y2_ + org_h, l), max(-x1_, 0):min(l - x2_ + org_w, l), :] = \
        rgb_img[max(y1_, 0):min(y2_, org_h), max(x1_, 0):min(x2_, org_w)]
    return target


def resize(im, target_size, fit=False):
    """
    Resize the image to target size.
    :param im: RGB image
    :param target_size: target size.
    :param fit: fit or stretch fill
    :return:
    """
    if fit:
        if im.shape[0] > im.shape[1]:
            newsize = (im.shape[1] * target_size // im.shape[0], target_size)
        else:
            newsize = (target_size, im.shape[0] * target_size // im.shape[1])
        if newsize[0] == 0:
            newsize = (1, newsize[1])
        elif newsize[1] == 0:
            newsize = (newsize[0], 1)
        im = cv2.resize(im, newsize)
        target = np.empty((target_size, target_size, 3), dtype=np.uint8)
        # target[:, :, :] = [124, 117, 104]  # RGB order
        target[:, :, :] = [127, 127, 127]  # RGB order
        if im.shape[0] > im.shape[1]:
            start = (target_size - im.shape[1]) // 2
            target[:, start:start + im.shape[1], :] = im
        else:
            start = (target_size - im.shape[0]) // 2
            target[start:start + im.shape[0], :, :] = im
        im = target
    else:
        im = cv2.resize(im, (target_size, target_size))
    return im


def generate_patches(im, rgb_mean, pad_patch=False):
    im_array = transform(im, rgb_mean[::-1])[0]  # (c, h, w) RGB order
    rgb_img = im_array.transpose((1, 2, 0))  # (h, w, c)
    im_patch = resize(rgb_img, 224, True)
    patch_array = im_patch.transpose((2, 0, 1))[np.newaxis, :]  # (1, c, h, w)
    return [patch_array]


def generate_patches_h_flip(im, rgb_mean, bboxes, pad_patch=False):
    im_flipped = im[:, ::-1, :]
    width = im.shape[1]
    bboxes_flipped = np.array(bboxes).copy()
    oldx1 = bboxes_flipped[:, 0].copy()
    oldx2 = bboxes_flipped[:, 2].copy()
    bboxes_flipped[:, 0] = width - oldx2 - 1
    bboxes_flipped[:, 2] = width - oldx1 - 1
    assert (bboxes_flipped[:, 2] >= bboxes_flipped[:, 0]).all()
    bboxes_flipped = bboxes_flipped.tolist()
    return generate_patches(im_flipped, rgb_mean, bboxes_flipped, pad_patch)


def generate_patches_resize(im, rgb_mean, bboxes, target_size, pad_patch=False):
    height, width, _ = im.shape
    if min(width, height) < target_size:
        return []
    scale = float(target_size) / min(width, height)
    if height < width:
        newsize = (width * target_size // height, target_size)
    else:
        newsize = (target_size, height * target_size // width)
    im_resized = cv2.resize(im, newsize)
    bboxes_resized = np.array(bboxes) * scale
    bboxes_resized = bboxes_resized.astype(np.int).tolist()
    return generate_patches(im_resized, rgb_mean, bboxes_resized, pad_patch)


def generate_batch(patches):
    patches_array = np.concatenate(patches)
    data = [mx.nd.array(patches_array)]
    data_shapes = [('data', patches_array.shape)]
    return mx.io.DataBatch(data, provide_data=data_shapes, provide_label=None)


def classify_patches_per_batch(patches, classification_type, others_threshold):
    root_classifier = get_registered_classifier('ali')
    data_batch = generate_batch(patches)
    cls_names, scores = root_classifier.predict(data_batch)
    # 不满足置信度的都算作“其他”
    cls_names[np.where(scores < others_threshold)[0]] = '其他'
    # 不在SKU列表中的也算其他
    if SKU_LIST:
        cls_names[np.where(np.isin(cls_names, SKU_LIST, invert=True))] = '其他'

    return cls_names, scores


def classify_patches(patches, batch_size=128, others_threshold=0.5):
    patches = patches[::]
    cls_names, scores = classify_patches_per_batch(
        patches, 1, others_threshold)
    return cls_names[0], scores[0]


def save_patch(save_root, save_folder, cls_name, score, image_name):
    class_image_dir = os.path.join(save_root, save_folder, cls_name)
    if not os.path.exists(class_image_dir):
        os.makedirs(class_image_dir)
    class_image_path = os.path.join(class_image_dir, '{:.3f}_{}'.format(
        score, image_name.rpartition('/')[-1]))
    shutil.copy(image_name, class_image_path)


def main():
    args = parse_args()

    ctx = mx.gpu(args.gpu)
    load_classifier('model/ali', ctx)

    rgb_mean = [0, 0, 0]

    while True:
        try:
            if not runnable:
                logger.info('EXIT NOW!')
                break
            data = None
            for priority in range(COUNT_PRIORITY_QUEUES):
                queue = 'ALI_CLASSIFICATION_TEST_INPUT_{}'.format(priority)
                data = dequeue(queue, False)
                if data:
                    logger.info('Dequeued from {}: {}'.format(queue, data))
                    break
            if not data:
                time.sleep(0.1)
                continue

            image_key = data['image_file']
            context = data.get('context', None)
            image_name = data.get('image_name', '')
            output_queue = data.get('output_queue', '')
            from_detectron = data.get('from_detectron', False)
            others_threshold = data.get('others_threshold', 0.7)
            save_root = data.get('save_root', '')
            save_folder = data.get('save_folder', '')

            logger.info('Processing {}...'.format(image_key))

            result = {
                'context': context,
                'enqueue_at': time.time()
            }

            im = image_store.get_as_image(image_key)

            if im is None:
                continue

            patches = generate_patches(im, rgb_mean)

            cls_name, score = classify_patches(patches, 128, others_threshold)
            score = np.asscalar(score)
            save_patch(save_root, save_folder, cls_name, score, image_name)
            result['class_detections'] = {
                'image': image_name
            }
            logger.info('Enqueued to {}: {}'.format(output_queue, result))
            enqueue(output_queue, result)
        except Exception as e:
            logger.error(e, exc_info=True)


def signal_handler(signal, frame):
    global runnable
    runnable = False


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    main()
