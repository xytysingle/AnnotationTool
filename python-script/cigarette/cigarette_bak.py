# -*- coding: utf-8 -*-
'''
   @Author: Kong Haiyang
   @Date: 2019-03-10 11:32:12
'''
from __future__ import absolute_import, division, print_function

import argparse
import datetime
import os
import shutil
import signal
import time

import cv2
import numpy as np
import tensorflow as tf

import image_store
import image_store_cos
from logger import setup_logging
from message_queue import dequeue, enqueue

os.environ['PYTHONUNBUFFERED'] = '1'

SAVE = False
SAVE_THRESHOLD = 0.5
SAVE_PATH = 'saved_images'

runnable = True


def parse_args():
    parser = argparse.ArgumentParser(description='CIGARETTE Server')
    parser.add_argument('--model_path', help='path of cigarette model',
                        default='models/model.pb', type=str)
    parser.add_argument('--classes', help='path of cigarette classes',
                        default='classes.txt', type=str)
    parser.add_argument('--classes_mapping', help='path of classes mapping',
                        default='classes_mapping.txt', type=str)
    parser.add_argument('--gpu', help='GPU device to use', default=0, type=int)
    parser.add_argument('--gpu_fraction', help='GPU amount to use', default=0.8, type=float)
    args = parser.parse_args()
    return args


def process_image(path):

    try:
        img = cv2.imread(path)

        image = np.zeros((224, 224, 3), dtype=float)
        image[:, :, :] = [104, 117, 124]
        height = img.shape[0]
        width = img.shape[1]
        if max(height, width) > 224:
            if height > width:
                ratio = 224 / height
                width = int(ratio * width)
                img = cv2.resize(img, (width, 224))
            else:
                ratio = 224 / width
                height = int(ratio * height)
                img = cv2.resize(img, (224, height))
        height = img.shape[0]
        width = img.shape[1]
        if height >= width:
            ratio = 224 / height
            width = int(ratio * width)
            img = cv2.resize(img, (width, 224))
            image[:, int((224 - width) / 2):int((224 - width) / 2) + width, :] = img
        else:
            ratio = 224 / width
            height = int(ratio * height)
            img = cv2.resize(img, (224, height))
            image[int((224 - height) / 2):int((224 - height) / 2) + height, :, :] = img
    except IOError:
        print('Read image `{}` error.'.format(path))
        return None

    image = 2 * (image / 255. - 0.5)

    return image


def main():

    args = parse_args()

    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu)

    with open(args.classes) as f:
        classes = [c.strip() for c in f.readlines()]
    label_map = {i: v for i, v in enumerate(classes)}

    with open(args.classes_mapping) as f:
        cm = [c.strip() for c in f.readlines()]
    class2id = {v: i for i, v in enumerate(cm)}

    cigarette_graph = tf.Graph()
    with cigarette_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(args.model_path, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = args.gpu_fraction
    with cigarette_graph.as_default():
        sess = tf.Session(graph=cigarette_graph, config=config)
        image_tensor1 = cigarette_graph.get_tensor_by_name('input1:0')
        image_tensor2 = cigarette_graph.get_tensor_by_name('input2:0')
        image_tensor3 = cigarette_graph.get_tensor_by_name('input3:0')
        is_training = cigarette_graph.get_tensor_by_name('is_training:0')
        prob = cigarette_graph.get_tensor_by_name('prob:0')
        soft = tf.nn.softmax(prob)
        prediction = tf.argmax(soft, axis=1)
        score = tf.reduce_max(soft, reduction_indices=[1])[0]

    logger.info('CIGARETTE Server started!')

    try:
        while True:
            if not runnable:
                logger.info('EXIT CIGARETTE SERVER!')
                break
            data = None
            data = dequeue('CIGARETTE_INPUT', False)
            if data:
                logger.info('Dequeued from CIGARETTE_INPUT: {}'.format(data))
            else:
                time.sleep(1)
                continue

            if not isinstance(data, dict):
                logger.error('Dequeued data format is not correct.')
                continue
            image_oris = data.get('images', None)
            im_keys = data.get('image_files', None)
            context = data.get('context', None)
            output_queue = data.get('output_queue', None)
            if im_keys is None:
                logger.error('im_keys is None.')
                continue
            if not isinstance(im_keys, list):
                logger.error('im_keys is not a list.')
                continue
            if output_queue is None:
                logger.error('output queue is None.')
                continue

            logger.info('Processing {}, {} and {}...'.format(im_keys[0], im_keys[1], im_keys[2]))

            try:
                _im_file1 = image_store.get_as_file(im_keys[0], True)
                _im_file2 = image_store.get_as_file(im_keys[1], True)
                _im_file3 = image_store.get_as_file(im_keys[2], True)
            except Exception:
                logger.error('Get file from im_key failed: {}, {} or {}.'.format(
                    im_keys[0], im_keys[1], im_keys[2]))
                _im_file1 = _im_file2 = _im_file3 = None

            try:
                image1 = process_image(_im_file1)
                image2 = process_image(_im_file2)
                image3 = process_image(_im_file3)
            except Exception:
                logger.error('Read image failed: {}, {} or {}.'.format(
                    _im_file1, _im_file2, _im_file3))
                image1 = image2 = image3 = None

            if image1 is None or image2 is None or image3 is None:
                result = {
                    'image': image_oris,
                    'context': context,
                    'type': str(-1),
                    'score': str(-1)
                }
                result['enqueue_at'] = time.time()
                logger.info('Enqueue to {}'.format(output_queue))
                enqueue(output_queue, result)
            else:
                image1 = np.expand_dims(image1, axis=0)
                image2 = np.expand_dims(image2, axis=0)
                image3 = np.expand_dims(image3, axis=0)
                pred, sc = sess.run([prediction, score], feed_dict={
                    image_tensor1: image1, image_tensor2: image2, image_tensor3: image3, is_training: False})
                print(pred)
                print(sc)
                try:
                    result = {
                        'image': image_oris,
                        'context': context,
                        'type': str(class2id[label_map[int(pred)]]),
                        'score': float(round(sc, 3))
                    }
                except Exception:
                    print(label_map[int(pred)])
                    result = {
                        'image': image_oris,
                        'context': context,
                        'type': str(-1),
                        'score': str(-1)
                    }
                result['enqueue_at'] = time.time()
                print('Enqueue to {}'.format(output_queue))
                enqueue(output_queue, result)
                if SAVE and sc <= SAVE_THRESHOLD:
                    folder = os.path.join(SAVE_PATH,
                                          datetime.datetime.now().strftime('%Y%m%d'),
                                          label_map[int(pred)])
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                    shutil.copy(_im_file1,
                                os.path.join(folder, '{:.3f}_'.format(sc)+os.path.basename(_im_file1)))
                    shutil.copy(_im_file2,
                                os.path.join(folder, '{:.3f}_'.format(sc)+os.path.basename(_im_file2)))
                    shutil.copy(_im_file3,
                                os.path.join(folder, '{:.3f}_'.format(sc)+os.path.basename(_im_file3)))
                if _im_file1 is not None and os.path.exists(_im_file1):
                    os.remove(_im_file1)
                if _im_file2 is not None and os.path.exists(_im_file2):
                    os.remove(_im_file2)
                if _im_file3 is not None and os.path.exists(_im_file3):
                    os.remove(_im_file3)
    except Exception as e:
        logger.error(e, exc_info=True)
    except:
        logger.error('Unknown error occurred!')


def signal_handler(signal, frame):
    global runnable
    runnable = False


if __name__ == '__main__':
    logger = setup_logging(os.path.basename(__file__)[:-3])
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()
