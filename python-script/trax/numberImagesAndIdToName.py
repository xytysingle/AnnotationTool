import json
import csv
import glob
import shutil



def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

def read_csv(path):
    csv_file = csv.reader(open(path, "r", encoding='utf-8'))
    return csv_file

def idToName(bboxes):
    global sku_list
    for item in bboxes:
        for sku in sku_list:
            if int(item["id"]) == int(sku["id"]):
                item["name"] = sku["name"]
    return bboxes
def numberImages():
    pass

def getAllImages():
    global BasePath
    allImagesPath = glob.glob(BasePath + "waitForNumber/*/*.jpg")
    return allImagesPath

def copyAndRename(path, filename):
    shutil.copy(path, filename)

if __name__ == "__main__":
    start_index = 8000001

    # targetName = "dt"
    targetName = "dp"

    BasePath = "/Users/lingmou/Desktop/traxResults/"
    TargetPath = "/Users/lingmou/Desktop/traxResults/"
    all_data = []

    if targetName == "dpz":
        # 单瓶
        skus = read_csv("traxsku/danpingcanuse.csv")
    elif targetName == "dt":
        # 堆头
        skus = read_csv("traxsku/duitoucanuse.csv")
    elif targetName == "dp":
        # 堆头
        skus = read_csv("traxsku/duitoucanuse.csv")

    sku_list = []

    for sku in skus:
        sku_list.append({
            "id": sku[0],
            "name": sku[3]
        })

    allImagesPath = getAllImages()
    for image in allImagesPath:
        img_name = image.split("/")[-1]
        img_date = image.split("/")[-2]

        if targetName == "dpz":
            #大瓶装
            Json_data = read_json(BasePath + "resultsJson/fewBottles/{}/fewBottles_{}.json".format(img_date, img_date))

        elif targetName == "dt":
            # 堆头
            Json_data = read_json(BasePath + "resultsJson/boxes/{}/boxes_{}.json".format(img_date, img_date))

        elif targetName == "dp":
            # 堆头
            Json_data = read_json(BasePath + "resultsJson/danping/{}/danping_{}.json".format(img_date, img_date))

        for item in Json_data:
            if img_name == item["image"]:

                copyAndRename(image, TargetPath + "numbered/{}.jpg".format(str(start_index)))
                _bboxes = idToName(item["bboxes"])
                all_data.append({
                    "image": start_index,
                    "bboxes": _bboxes,
                    "oldName":img_name
                })
                print("已处理：", start_index)
                start_index += 1


    saveResultsByJson(TargetPath + "resultsJson/numbered/numbered".format(start_index), all_data)