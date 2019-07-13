from __future__ import print_function
import sys
from message_queue import enqueue

q_name = sys.argv[1]
data = eval(sys.argv[2])
enqueue(q_name, data)
print('Enqueued to {}: {}'.format(q_name, data))
