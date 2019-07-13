from __future__ import print_function
import unittest
import os
import time

import image_store_cos


class ImageStoreCosTestCase(unittest.TestCase):
    def setUp(self):
        self.image_key = 'cooler.jpg'

    def test_cache(self):
        cache_path = os.path.join(image_store_cos.cache_dir, self.image_key)
        if os.path.exists(cache_path):
            os.remove(cache_path)
        t = time.time()
        data_no_cache = image_store_cos.get_as_raw(self.image_key)
        print('Took {}s from Cos'.format(time.time() - t))
        self.assertTrue(os.path.exists(cache_path))
        t = time.time()
        data_cache = image_store_cos.get_as_raw(self.image_key)
        print('Took {}s from Cache'.format(time.time() - t))
        self.assertEqual(data_no_cache, data_cache)
        os.remove(cache_path)
