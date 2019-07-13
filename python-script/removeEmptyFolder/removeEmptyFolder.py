import glob
import csv
import shutil
from tqdm import tqdm
import os


basePath = "/Users/lingmou/Desktop/cleanData/"

def main():
    count = 0
    images = glob.glob(basePath + "1/*/*.jpg")
    for image in tqdm(images):
        mkdir(basePath + "cleanedClassImages/" + image.split("/")[-2])
        try:
            shutil.copy(image, basePath + "cleanedClassImages/{}/{}".format(image.split("/")[-2], image.split("/")[-1]))
            count += 1
        except Exception as e:
            print(image + "-----------" + e)
    print(count)

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        # print("{}创建成功".format(path))
        return True
    else:
        # print("{}已存在".format(path))
        return False

if __name__ == '__main__':
    main()