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
    count = 0
    # classes = glob.glob(basePath +  "2/*")
    newdata = []
    wrong = []
    classes = readText()
    for item in tqdm(classes):
        flag = False
        for data in  response:
            if item.split("\n")[0] == data["sku_name"]:
                flag = True
                count += 1
                newdata.append("{}^{}".format(data["id"], item))
                break
        if flag == False:
            wrong.append(item)

    with open("/Users/lingmou/Desktop/python-script/classesnameAddId/target/wrong.txt", "w") as f:
        for i in wrong:
            f.writelines(i)
    saveText(newdata)
    print(count)
        # if flag == False:
        #     shutil.move(item, basePath + "error/{}".format(item.split("/")[-1]))

def readText():
    f = open("/Users/lingmou/Desktop/python-script/classesnameAddId/source/class_names.txt", "r")  # 设置文件对象
    data = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f.close()
    print(data)
    return data

def saveText(data):
    with open("/Users/lingmou/Desktop/python-script/classesnameAddId/target/class_names.txt", "w") as f:
        for i in data:
            f.writelines(i)

if __name__ == '__main__':
    main()
    # classes = readText()
    # # print(classes)
    # for item in classes:
    #     # print(item.rstrip("\n"))
    #     print(item.split(" ")[0])