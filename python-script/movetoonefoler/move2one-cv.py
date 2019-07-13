from pathlib import Path
from scipy import misc
import os
from os.path import join as pjoin
import cv2
import sys

# p = Path('/Users/lingmou/Desktop/python-script/movetoonefoler/sourcefolder')
p = Path('/Users/lingmou/Desktop/python-script/movetoonefoler/sourcefolder/')
data_dir = '/Users/lingmou/Desktop/python-script/movetoonefoler/targetfolder'


FileList = list(p.glob("**/*.jpg"))

count = 1
useful_image_count = 0
all_image_count = 0


def getImageSize(image):
    image_storage_size = os.path.getsize(image)  # 获取图片字节大小

    return image_storage_size

for file in FileList:
    all_image_count += 1
    filename = str(count) + '.jpg'
    # img = misc.imread(file, mode='RGB')
    # misc.imsave(pjoin(data_dir,filename), img)  # 将lfw中读取的每个文件夹中的图片存入指定的文件夹
    imgSize = getImageSize(str(file))
    print(file, count, imgSize)
    if(imgSize >= 240800):
        useful_image_count = useful_image_count +1
        img = cv2.imread(str(file), 1)
        cv2.imwrite(pjoin(data_dir,filename), img)
        count = int(count) + 1
    else:
        continue

print('总文件数：',all_image_count,'有效文件数：', useful_image_count)


