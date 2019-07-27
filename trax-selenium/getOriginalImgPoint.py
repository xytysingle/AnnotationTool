# -*- coding: utf-8 -*-
from restorePoints import parse_json
import csv
import glob
import json
import math


def getAllJsonFile():
    path = "/Users/lingmou/Desktop/trax-selenium/scence/20190314/*/*.json"
    json_list = glob.glob(path)
    print(len(json_list))
    for json in json_list:
        print(json)
        getOriginalPoints(json)


def getAllImgPath():
    path = "/Users/lingmou/Desktop/trax-selenium/scence/20190314/*/*.jpeg"
    img_list = glob.glob(path)
    print(len(img_list))

def getOriginalPoints(json_path):
    global all_data
    try:
        results = parse_json(json_path)
        for result in results:
            img_path = result["file"]
            objects = result["objects"]
            bboxes = []
            for object in objects:
                # tempObj =[int(round(object[0])), int(round(object[1])), int(round(object[2]))]
                tempObj = {
                    "x": int(round(object[0])),
                    "y": int(round(object[1])),
                    "id": int(round(object[2]))
                }

                # tempObj = json.dumps(tempObj)
                bboxes.append(tempObj)
            print(bboxes)
            all_data.append(
                {
                    "img_path": img_path,
                    "bboxes": bboxes
                }
            )
    except:
        print("还原失败")
    # print(results)




def save_data(img_path, bboxes):
    out = open('20190313-1.csv', 'a', newline='', encoding='utf-8')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow([img_path, bboxes])

def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)



def read_csv():
    csv_file = csv.reader(open("duitouSKU.csv", "r"))
    return csv_file


def filterSKU():
    pass

if __name__ == "__main__":
    all_data = []
    # getOriginalPoints("/Users/lingmou/Desktop/python-script/trax-selenium/scence/20190313/9233287/9233287.json")
    getAllJsonFile()
    saveResultsByJson('20190314', all_data)
    # getAllImgPath()