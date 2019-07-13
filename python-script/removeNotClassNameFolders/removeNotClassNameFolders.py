import requests
import json
import glob
import shutil
import os
from tqdm import tqdm

basePath = "/Users/lingmou/Desktop/cleanData/"
allClassNameUrl = "http://annotation.lingmou.ai:8000/index.php/skus/get-all"

response = requests.get(allClassNameUrl)
response = json.loads(response.text)

def main():
    classes = glob.glob(basePath +  "weita/*/*.jpg")
    for item in tqdm(classes):
        flag = False
        for data in  response:
            if item.split("/")[-2] == data["sku_name"]:
                # print("results/{}:{}".format(data["id"], item.split("/")[-2]))
                mkdir( basePath + "results/{}^{}".format(data["id"], item.split("/")[-2]))
                flag = True
                shutil.move(item, basePath + "results/{}^{}/{}".format(data["id"], item.split("/")[-2], item.split("/")[-1]))
                
        # if flag == False:
        #     shutil.move(item, basePath + "error/{}".format(item.split("/")[-1]))

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