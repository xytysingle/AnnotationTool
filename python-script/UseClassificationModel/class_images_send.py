# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import time

# os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import cv2  # NOQA (Must import before importing caffe2 due to bug in cv2)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from tqdm import tqdm

from message_queue import clear, dequeue, enqueue

from image_store import to_image_key

# OpenCL may be enabled by default in OpenCV3; disable it because it's not
# thread safe and causes unwanted GPU memory allocations.
cv2.ocl.setUseOpenCL(False)

from matplotlib.font_manager import _rebuild
_rebuild()

matplotlib.rcParams['font.sans-serif'] = ['SimHei']


def parse_args():
    parser = argparse.ArgumentParser(description='End-to-end inference')
    parser.add_argument(
        '--output-dir',
        dest='output_dir',
        help='directory for visualization',
        default='/data/dongwei/modeldata/ali',
        type=str
    )
    parser.add_argument(
        '--image-ext',
        dest='image_ext',
        help='image file name extension (default: jpg)',
        default='jpg',
        type=str
    )
    parser.add_argument(
        '--image-folder',
        dest='image_folder',
        help='image or folder of images',
        default='/data/dongwei/dwclassImages/others',
        type=str
    )
    return parser.parse_args()


def vis_detections(im, detections, thresh, out_name, dpi=200, show_class=True):
    """Visual debugging of detections."""
    if detections is {}:
        fig = plt.figure(frameon=False)
        fig.set_size_inches(im.shape[1] / dpi, im.shape[0] / dpi)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.axis('off')
        fig.add_axes(ax)
        ax.imshow(im)
        fig.savefig(out_name, dpi=dpi)
        plt.close('all')
        return None, None

    color_list = colormap(rgb=True) / 255

    fig = plt.figure(frameon=False)
    fig.set_size_inches(im.shape[1] / dpi, im.shape[0] / dpi)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.axis('off')
    fig.add_axes(ax)
    ax.imshow(im)

    # Display in largest to smallest order to reduce occlusion
    for cls in detections:
        boxes = np.array(detections[cls])
        areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
        sorted_inds = np.argsort(-areas)

        for i in sorted_inds:
            bbox = boxes[i, :4]
            score = boxes[i, -1]
            if score < thresh:
                continue

            ax.add_patch(plt.Rectangle((bbox[0], bbox[1]),
                                       bbox[2] - bbox[0],
                                       bbox[3] - bbox[1],
                                       fill=True, edgecolor='g',
                                       linewidth=0.5, alpha=0.3))

            if show_class:
                ax.text(bbox[0], bbox[1] - 2,
                        unicode(cls.decode('utf-8') + '{:.2f}'.format(score).lstrip('0')),
                        fontsize=3,
                        bbox=dict(
                        facecolor='g', alpha=0.4, pad=0, edgecolor='none'),
                        color='white')

    fig.savefig(out_name, dpi=dpi)
    plt.close('all')


def main(args):
    folder = args.image_folder
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    im_files = []
    for dp, dn, files in os.walk(folder):
        for f in files:
            if f.endswith(args.image_ext) or f.endswith('.png'):
                im_files.append(os.path.join(dp, f))
    im_files.sort()
    for im_file in tqdm(im_files):
        out_name = im_file.replace(args.image_folder, args.output_dir)
        im = cv2.imread(im_file)

        data = {}
        queue = 'TEST_ALI_20190516'
        data['image_name'] = im_file
        data['image_file'] = to_image_key(im_file)
        data['output_queue'] = queue
        data['from_detectron'] = True
        data['others_threshold'] = 0.7
        data['save_root'] = args.output_dir
        data['save_folder'] = 'class_images'

        enqueue('ALI_CLASSIFICATION_TEST_INPUT_0', data)
        data = dequeue(queue)
        if data:
            print('\nDequeued from {}: {}'.format(queue, data))

    print('Inference done.')


if __name__ == '__main__':
    args = parse_args()
    main(args)
