import pandas as pd
import glob
import shutil
from tqdm import tqdm
import os
import requests
import json


base_path = "/Users/lingmou/Desktop/box-classes/"
allClassNameUrl = "http://annotation.lingmou.ai:8000/index.php/skus/get-all"

response = requests.get(allClassNameUrl)
response = json.loads(response.text)

def main():
    classImages = glob.glob(base_path + "target/*/*.jpg")
    # coca_box_skus = pd.read_csv(base_path + "coca_box_skus.csv")

    # df = pd.DataFrame(coca_box_skus)

    for classImage in tqdm(classImages):
        for item in response:
            if classImage.split("/")[-2] == item["sku_name"]:
                mkdir(base_path + "coca_skus-3/{}^{}".format(item["id"],classImage.split("/")[-2]))
                shutil.copy(classImage, base_path + "coca_skus-3/{}^{}/{}".format(item["id"], classImage.split("/")[-2], classImage.split("/")[-1]))
                break


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