import shutil
import glob
import pandas as pd
import json

BasePath = "/Users/lingmou/Desktop/bottle-box/"

def readText(path):
    labelJson = {}
    bboxes = []

    f = open(path, "r", encoding="utf-8")  # 设置文件对象 encoding="utf-8"
    # data = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    data = f.read().splitlines()
    f.close()
    # print(data[0].split(" ")[1])
    # print(data[0])
    if data[0].__contains__("rotate"):
        labelJson["rotate"] = int(data[0].split(" ")[1])
    else:
        print(path)

    # print(labelJson)
    # return labelJson

def main():

    labelTexts = glob.glob(BasePath + "annos/*.txt")

    for text in labelTexts:
        print(text)
        readText(text)



def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

if __name__ == '__main__':
    # readText("/Users/lingmou/Desktop/bottle-box/100298.txt")
    startIndex = 7500001
    main()