import os
import math

imgst_kb = math.ceil(os.stat('if7.jpg').st_size / 1024)
print(imgst_kb,'KB')