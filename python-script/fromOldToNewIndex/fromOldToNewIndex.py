from pathlib import Path
from scipy import misc
import os
from os.path import join as pjoin
import pandas as pd
import csv
import re

# p = Path('/Users/lingmou/Desktop/python-script/movetoonefoler/sourcefolder')
p = Path('/Users/lingmou/Desktop/python-script/fromOldToNewIndex/sourcefolder')
data_dir = '/Users/lingmou/Desktop/python-script/fromOldToNewIndex/targetfolder'

def save_data(oldIndex, newIndex):
    print(oldIndex, newIndex)
    # pf = pd.DataFrame(dataList, columns=["old", "new"])
    # pf.to_csv("indexData.csv", index=False, encoding="utf-8")
    out = open('indexData.csv', 'a', newline='')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow([oldIndex, newIndex])

FileList = list(p.glob("**/*.jpg"))

count = 8000001
dataList = []
for file in FileList:
    # print(file, count)
    oldindex = re.search('/Users/lingmou/Desktop/python-script/fromOldToNewIndex/sourcefolder/(.*?).jpg', str(file)).group(1)

    save_data(oldindex, count)
    # dataList.append({file, count})
    filename = str(count) + '.jpg'
    img = misc.imread(file, mode='RGB')
    misc.imsave(pjoin(data_dir,filename), img)  # 将lfw中读取的每个文件夹中的图片存入指定的文件夹
    count = int(count) + 1
print('总文件数：',count)
# save_data(dataList)
