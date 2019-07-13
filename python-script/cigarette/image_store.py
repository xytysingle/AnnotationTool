from __future__ import print_function

import os
import numpy as np
import cv2
import tempfile
import uuid
import traceback

from message_queue import r

DEBUG = False


def to_image_key(image_file, image_key_or_prefix):
    if image_key_or_prefix.endswith('_'):
        image_prefix = image_key_or_prefix
        image_key = image_prefix + str(uuid.uuid4())
    else:
        image_key = image_key_or_prefix
    if DEBUG:
        print('New image key: {}\n{}'.format(image_key, ''.join(traceback.format_stack())))
    with open(image_file, 'r') as f:
        r.set(image_key, f.read())
    return image_key


def get_as_raw(image_key, delete=True):
    raw = r.get(image_key)
    assert raw is not None, 'Image key not exist!'
    if delete:
        if DEBUG:
            print('Delete image key: {}\n{}'.format(image_key, ''.join(traceback.format_stack())))
        r.delete(image_key)
    return raw


def get_as_array(image_key, delete=True):
    return np.frombuffer(get_as_raw(image_key, delete), np.uint8)


def get_as_image(image_key, delete=True):
    return cv2.imdecode(get_as_array(image_key, delete), -1)


def get_as_file(image_key, delete=True):
    raw = get_as_raw(image_key, delete)
    tmp_file = os.path.join(tempfile.gettempdir(), image_key + '.jpg')
    with open(tmp_file, 'w') as f:
        f.write(raw)
    return tmp_file


def delete_image_key(image_key):
    r.delete(image_key)
