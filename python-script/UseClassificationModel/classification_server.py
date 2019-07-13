#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import mxnet as mx
import cv2
import time
import argparse
import numpy as np
import signal
import datetime

from message_queue import *
from classifier import load_classifiers, load_classifier, get_registered_classifier
import image_store
from logger import logger

os.environ['MXNET_CUDNN_AUTOTUNE_DEFAULT'] = '0'
os.environ['PYTHONUNBUFFERED'] = '1'

os.chdir(os.path.abspath(os.path.dirname(__file__)))

COUNT_PRIORITY_QUEUES = 3
H_FLIP_AUG = True
SCALE_720_AUG = True
runnable = True

SKU_LIST = [
]


def parse_args():
    parser = argparse.ArgumentParser(description='Shapshot Classification Server')
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


def generate_patches(im, rgb_mean, bboxes, pad_patch=False):
    im_array = transform(im, rgb_mean[::-1])[0]  # (c, h, w) RGB order
    rgb_img = im_array.transpose((1, 2, 0))  # (h, w, c)
    list_patch_array = []
    for bbox in bboxes:
        if pad_patch:
            im_patch = get_image_patch_padded(rgb_img, bbox[0], bbox[1], bbox[2], bbox[3])
            im_patch = resize(im_patch, 224, False)
        else:
            im_patch = rgb_img[bbox[1]:bbox[3], bbox[0]:bbox[2], :]
            im_patch = resize(im_patch, 224, True)
        patch_array = im_patch.transpose((2, 0, 1))[np.newaxis, :]  # (1, c, h, w)
        list_patch_array.append(patch_array)
    return list_patch_array


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
    # im_resized = cv2.imread('/home/fallingdust/Pictures/20180731025027592412_720.jpg')
    # print 'LOADED'
    bboxes_resized = np.array(bboxes) * scale
    bboxes_resized = bboxes_resized.astype(np.int).tolist()
    # bboxes_resized = bboxes
    return generate_patches(im_resized, rgb_mean, bboxes_resized, pad_patch)


def generate_batch(patches):
    patches_array = np.concatenate(patches)
    data = [mx.nd.array(patches_array)]
    data_shapes = [('data', patches_array.shape)]
    return mx.io.DataBatch(data, provide_data=data_shapes, provide_label=None)


def classify_patches_per_batch(patches, classification_type, others_threshold):
    # root_classifier = get_registered_classifier('bottle' if classification_type == 1 else 'box')
    assert classification_type == 1
    root_classifier = get_registered_classifier('bottle')
    data_batch = generate_batch(patches)
    cls_names, scores = root_classifier.predict(data_batch)
    # 不满足置信度的都算作“其他”
    cls_names[np.where(scores < others_threshold)[0]] = '其他'
    # 不在SKU列表中的也算其他
    if SKU_LIST:
        cls_names[np.where(np.isin(cls_names, SKU_LIST, invert=True))] = '其他'

    # 遍历所有bbox的分类，检查是否需要进一步分类
    # classifiers = {}  # {Classifier: [bbox indexes]
    # for i, cls in enumerate(cls_names):
    #     classifier = get_registered_classifier(cls)
    #     if classifier is None:
    #         continue
    #     # 在保证rgb mean一致的情况下，能复用data_batch
    #     assert root_classifier.rgb_mean == classifier.rgb_mean
    #     classifiers.setdefault(classifier, []).append(i)
    #
    # for classifier, bbox_indexes in classifiers.iteritems():
    #     logger.info('Calling sub classifier {}'.format(classifier.name))
    #     sub_data = data_batch.data[0].take(mx.nd.array(bbox_indexes))
    #     sub_data_batch = mx.io.DataBatch([sub_data], provide_data=[('data', sub_data.shape)], provide_label=None)
    #     sub_class_names, sub_scores = classifier.predict(sub_data_batch)
    #     cls_names[bbox_indexes] = sub_class_names
    #     scores[bbox_indexes] = sub_scores

    return cls_names, scores


def classify_patches(patches, classification_type, batch_size=128, others_threshold=0.5):
    patches = patches[::]
    cls_names = None
    scores = None
    while len(patches) > 0:
        _patches = patches[:batch_size]
        patches = patches[batch_size:]
        _cls_names, _scores = classify_patches_per_batch(_patches, classification_type, others_threshold)
        if cls_names is None:
            cls_names = _cls_names
            scores = _scores
        else:
            cls_names = np.append(cls_names, _cls_names)
            scores = np.append(scores, _scores)
    return cls_names, scores


def merge_groups(cls_names, scores, count_groups):
    count_bboxes = len(cls_names) / count_groups
    max_scores = []
    max_cls_names = []
    for i in range(count_bboxes):
        max_score = 0
        max_cls_name = None
        for j in range(count_groups):
            idx = count_bboxes * j + i
            if scores[idx] > max_score:
                max_score = scores[idx]
                max_cls_name = cls_names[idx]
        max_scores.append(max_score)
        max_cls_names.append(max_cls_name)
    return np.array(max_cls_names), np.array(max_scores)


def save_patch(image_key, im, bbox, cls_name, score):
    save_root = os.path.join('uncertain', datetime.datetime.now().strftime('%Y%m%d'))
    if not os.path.exists(save_root):
        os.mkdir(save_root)
        os.mkdir(os.path.join(save_root, 'images'))
        os.mkdir(os.path.join(save_root, 'class_images'))
    image_path = os.path.join(save_root, 'images', image_key + '.jpg')
    if not os.path.exists(image_path):
        cv2.imwrite(image_path, im)
    class_image_dir = os.path.join(save_root, 'class_images', cls_name)
    if not os.path.exists(class_image_dir):
        os.mkdir(class_image_dir)
    x1, y1, x2, y2 = bbox
    class_image_path = os.path.join(class_image_dir, '{}_{}_{}_{}_{}({}).jpg'.format(image_key, x1, y1, x2, y2, score))
    im_patch = im[y1:y2, x1:x2, ::]
    cv2.imwrite(class_image_path, im_patch)


def main():
    args = parse_args()

    ctx = mx.gpu(args.gpu)
    # load_classifiers('model', ctx)
    load_classifier('model/bottle', ctx)
    # load_classifier('model/box', ctx)

    rgb_mean = [0, 0, 0]

    while True:
        try:
            if not runnable:
                logger.info('EXIT NOW!')
                break
            data = None
            for priority in range(COUNT_PRIORITY_QUEUES):
                queue = 'SNAPSHOT_CLASSIFICATION_INPUT_{}'.format(priority)
                data = dequeue(queue, False)
                if data:
                    logger.info('Dequeued from {}: {}'.format(queue, data))
                    break
            if not data:
                time.sleep(0.1)
                continue

            image_key = data['image_file']
            bboxes = data['bboxes']
            context = data.get('context', None)
            classification_type = data.get('type', 1)  # 1: bottle, 2: box
            output_queue = data['output_queue']
            from_detectron = data.get('from_detectron', False)
            others_threshold = data.get('others_threshold', 0.7)

            logger.info('Processing {}...'.format(image_key))

            result = {
                'context': context,
                'enqueue_at': time.time()
            }

            im = image_store.get_as_image(image_key)

            if im is None:
                continue

            if len(bboxes) == 0:
                result['detections'] = []
            else:
                if not from_detectron:  # 标注工具结果
                    rotate = data.get('rotate', 0)
                    if rotate != 0:
                        rot_mat = cv2.getRotationMatrix2D((im.shape[1] / 2, im.shape[0] / 2), rotate, 1)
                        im = cv2.warpAffine(im, rot_mat, (im.shape[1], im.shape[0]))

                    bboxes_ = []
                    for bbox in bboxes:
                        bbox[0] = min(max(bbox[0], 0), im.shape[1])
                        bbox[1] = min(max(bbox[1], 0), im.shape[0])
                        bbox[2] = min(max(bbox[2], 0), im.shape[1])
                        bbox[3] = min(max(bbox[3], 0), im.shape[0])
                        if bbox[2] - bbox[0] > 0 and bbox[3] - bbox[1] > 0:
                            bboxes_.append(bbox)
                    bboxes = bboxes_
                    patches = []
                    patches += generate_patches(im, rgb_mean, bboxes)
                    if H_FLIP_AUG:
                        patches += generate_patches_h_flip(im, rgb_mean, bboxes)
                    if SCALE_720_AUG:
                        patches += generate_patches_resize(im, rgb_mean, bboxes, 720)

                    cls_names, scores = classify_patches(patches, classification_type, 128, others_threshold)
                    count_groups = len(patches) / len(bboxes)
                    if count_groups > 1:
                        cls_names, scores = merge_groups(cls_names, scores, count_groups)
                    detections = []
                    for i, bbox in enumerate(bboxes):
                        detections.append(bbox + [cls_names[i]] + [np.asscalar(scores[i])])
                    result['detections'] = detections
                else:  # Detectron检出后进一步分类
                    patches = []
                    patches += generate_patches(im, rgb_mean, bboxes)
                    if H_FLIP_AUG:
                        patches += generate_patches_h_flip(im, rgb_mean, bboxes)
                    if SCALE_720_AUG:
                        patches += generate_patches_resize(im, rgb_mean, bboxes, 720)

                    cls_names, scores = classify_patches(patches, classification_type, 128, others_threshold)
                    count_groups = len(patches) / len(bboxes)
                    if count_groups > 1:
                        cls_names, scores = merge_groups(cls_names, scores, count_groups)
                    cls_dets = {}
                    for i, bbox in enumerate(bboxes):
                        score = np.asscalar(scores[i])
                        cls_dets.setdefault(cls_names[i], []).append(bbox + [score])
                        if score < 0.95:
                            save_patch(image_key, im, bbox, cls_names[i], score)
                    # if classification_type != 1 and '其他' in cls_dets:  # box中过滤“其他”，很有可能是错误检出
                    #     del cls_dets['其他']
                    result['class_detections'] = cls_dets

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
