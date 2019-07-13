import pandas as pd
import glob
import shutil
from tqdm import tqdm
import os


base_path = "/Users/lingmou/Desktop/box-classes/"

def main():
    classImages = glob.glob(base_path + "7/*/*.jpg")


    for classImage in tqdm(classImages):
        mkdir(base_path + "target/{}".format(classImage.split("/")[-2]))
        shutil.move(classImage, base_path + "target/{}/{}".format(classImage.split("/")[-2], classImage.split("/")[-1]))


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