#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import os
import sys
import time

import numpy as np

sys.path.insert(0, '.')

import image_store as image_store
from message_queue import clear, dequeue, enqueue

image_file = 'tests/images/budweiser.jpg'
output_queue = 'CIGARETTE_TEST_{:.6f}'.format(np.random.random())
enqueue('CIGARETTE_INPUT', {
    'image_file': image_store.to_image_key(image_file, 'BUD'),
    'output_queue': output_queue,
    'context': os.path.basename(image_file),
    'enqueue_at': time.time()
})
result = dequeue(output_queue)
clear(output_queue)
print(result)
