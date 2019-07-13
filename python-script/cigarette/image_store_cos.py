from __future__ import absolute_import
from __future__ import print_function

import os
import numpy as np
import cv2
import tempfile
import uuid
import traceback
import yaml
import time

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

DEBUG = False

cos = yaml.load(open('cos.yaml'))
bucket = cos['bucket']
config = CosConfig(Region=cos['region'], SecretId=cos['secret_id'], SecretKey=cos['secret_key'], Scheme='https')
client = CosS3Client(config)
cache_dir = cos['cache_dir']


def to_image_key(image_file, image_key_or_prefix):
    if image_key_or_prefix.endswith('_'):
        image_prefix = image_key_or_prefix
        image_key = image_prefix + str(uuid.uuid4())
    else:
        image_key = image_key_or_prefix
    if DEBUG:
        print('New image key: {}\n{}'.format(image_key, ''.join(traceback.format_stack())))
    with open(image_file, 'r') as f:
        client.put_object(
            Bucket=bucket,
            Body=f,
            Key=image_key,
            StorageClass='STANDARD',
            EnableMD5=False
        )
    return image_key


def get_as_raw(image_key):
    cache_path = os.path.join(cache_dir, image_key)
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            return f.read()
    else:
        raw_data = _get_as_raw(image_key, 3)
        with open(cache_path, 'w') as f:
            f.write(raw_data)
        os.chmod(cache_path, 0666)
        return raw_data


def _get_as_raw(image_key, retry):
    try:
        response = client.get_object(
            Bucket=bucket,
            Key=image_key,
        )
        fp = response['Body'].get_raw_stream()
        assert fp is not None, 'Image key not exist!'
        return fp.read()
    except Exception as e:
        if retry > 0:
            time.sleep(max(1, 4 - retry))
            retry -= 1
            return _get_as_raw(image_key, retry)
        else:
            raise e


def get_as_array(image_key):
    return np.frombuffer(get_as_raw(image_key), np.uint8)


def get_as_image(image_key):
    return cv2.imdecode(get_as_array(image_key), -1)


def get_as_file(image_key):
    raw = get_as_raw(image_key)
    tmp_file = os.path.join(tempfile.gettempdir(), image_key + '.jpg')
    suffix = 0
    while os.path.exists(tmp_file):
        suffix += 1
        tmp_file = os.path.join(tempfile.gettempdir(), '{}-{}.jpg'.format(image_key, suffix))
    with open(tmp_file, 'w') as f:
        f.write(raw)
    return tmp_file


def delete_image_key(image_key):
    client.delete_object(
        Bucket=bucket,
        Key=image_key
    )
