import json
import glob
import pandas as pd
from tqdm import tqdm
import shutil
import os

base_path = "/data/dongwei/"
target_path = "/data/datasets/coca/images/"

def main():
    images = glob.glob(base_path + "taigu_uncertain_process/target/numbered/*.jpg")
    for image in tqdm(images):
        # className = image.split("/")[-2].split("^")[1]
        # mkdir(target_path + "10/{}".format(className))
        shutil.move(image, target_path + "{}".format(image.split("/")[-1]))

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print("{}创建成功".format(path))
        return True
    else:
        # print("{}已存在".format(path))
        return False


if __name__ == '__main__':
    main()