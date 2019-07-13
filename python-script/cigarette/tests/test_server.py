from __future__ import absolute_import
from __future__ import print_function
import time
import sys

import unittest

sys.path.insert(0, '.')

from message_queue import *

images = {
    2: 'tests/images/budweiser.jpg'
}


class ServerTestCase(unittest.TestCase):
    def test_budweiser(self):
        scene_type = 2
        output_queue = 'BUDWEISER_OUTPUT_TEST_{}'.format(scene_type)
        image = images[scene_type]
        enqueue('BUDWEISER_INPUT_0', {
            'image_files': [image],
            'type': scene_type,
            'output_queue_qc': output_queue,
            'enqueue_at': time.time()
        })
        result = dequeue(output_queue)
        print(result)
        clear(output_queue)
        self.assertIn('image_results', result)
        self.assertGreater(len(result['image_results']), 0)
        self.assertIn('bottles', result['image_results'][0])
        self.assertGreater(len(result['image_results'][0]['bottles']), 0)
        self.assertIn('gates', result['image_results'][0])
        self.assertGreater(len(result['image_results'][0]['gates']), 0)
        self.assertIn('tiers', result['image_results'][0])
        self.assertGreater(len(result['image_results'][0]['tiers']), 0)


if __name__ == '__main__':
    unittest.main()
