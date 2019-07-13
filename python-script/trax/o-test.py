from urllib import request
import re
import csv

path="/Users/lingmou/Desktop/trax-selenium/scence/20190315/9327227/20190315125641-35979bb3-9999-4223-a531-941e3a92d6ba.jpeg"

res = path.split("/")[-1].split(".")[0]
print(res)
