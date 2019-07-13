import shutil
import glob
import pandas as pd
import json

BasePath = "/Users/lingmou/Desktop/bottle-box/"

def readText(path):
    labelJson = {}
    bboxes = []

    f = open(path, "r", encoding="utf-8")  # 设置文件对象
    # data = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    data = f.read().splitlines()
    f.close()
    # print(data[0].split(" ")[1])
    if data[0].__contains__("rotate"):
        labelJson["rotate"] = int(data[0].split(" ")[1])
    # labelJson["rotate"] = int(data[0].split(" ")[1])
        for item in data[1:]:
            # print(item)
            results = item.split(" ")
            if results[0].__contains__("堆头"):
                results[0] = "box"
            elif results[0] == "box":
                results[0] = "box"
            else:
                results[0] = "bottle"
            bboxes.append(
                {
                    "className": results[0],
                    "x1": int(results[1]),
                    "x2": int(results[3]),
                    "y1": int(results[2]),
                    "y2": int(results[4]),
                    "truncated": int(results[5]),
                }
            )
    else:
        labelJson["rotate"] = 0
        for item in data:
            # print(item)
            results = item.split(" ")
            if results[0].__contains__("堆头"):
                results[0] = "box"
            elif results[0] == "box":
                results[0] = "box"
            else:
                results[0] = "bottle"
            bboxes.append(
                {
                    "className": results[0],
                    "x1": int(results[1]),
                    "x2": int(results[3]),
                    "y1": int(results[2]),
                    "y2": int(results[4]),
                    "truncated": int(results[5]),
                }
            )
    labelJson["bboxes"] = bboxes

    print(labelJson)
    return labelJson

def main(index):
    images = glob.glob(BasePath + "targetImages/*.jpg")
    labelTexts = glob.glob(BasePath + "annos/*.txt")
    for image in images:
        oldnameI = image.split("/")[-1].split(".")[0]
        for text in labelTexts:
            oldnameT = text.split("/")[-1].split(".")[0]
            if oldnameI == oldnameT:
                labelJson = readText(text)
                shutil.copy(image, BasePath + "numbered/images/{}.jpg".format(index))
                saveResultsByJson(BasePath + "numbered/json/{}".format(index), labelJson)
        print("已处理：", index)
        index += 1


def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

if __name__ == '__main__':
    # readText("/Users/lingmou/Desktop/bottle-box/806571.txt")
    startIndex = 7503227
    main(startIndex)