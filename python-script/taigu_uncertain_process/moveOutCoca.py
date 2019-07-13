import requests
import json
import glob
import shutil
import os
from tqdm import tqdm


basePath = "/data/dongwei/dwclassImages/"
allClassNameUrl = "http://annotation.lingmou.ai:8000/index.php/skus/get-all"

response = requests.get(allClassNameUrl)
response = json.loads(response.text)

def main():
    count = 0
    smallImages = glob.glob(basePath +  "*/*.jpg")
    # newdata = []
    # wrong = []
    # classes = readText()
    for item in tqdm(smallImages):
        # print(item.split("/")[-2])
        for data in response:
            if item.split("/")[-2] == data["sku_name"] and data["group_id"] == "94":
                count += 1
                mkdir("data/dongwei/Coca-Cola/{}".format(item.split("/")[-2]))
                shutil.move(item, "/data/dongwei/Coca-Cola/{}/{}".format(item.split("/")[-2], item.split("/")[-1]))
                if count % 100 == 0:
                    print(count)
                break




    print("总数为：", count)
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
