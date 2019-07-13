import glob
import shutil
import json
from tqdm import tqdm

basePath = "/Users/lingmou/Desktop/ali/"


def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def main():
    count = 0
    oldLabels = glob.glob(basePath + "jsons/old/*.json")
    newAddDatas = read_json(basePath + "resultsJson/results.json")
    for datapath in tqdm(oldLabels):
        imgIndex = datapath.split("/")[-1].split(".")[0]
        jsondata = read_json(datapath)
        for newdata in newAddDatas:
            if imgIndex == newdata["image"]:
                print(imgIndex)
                bboxes = jsondata["bboxes"]
                for old_item in bboxes:
                    for item in newdata["bboxes"]:
                        if old_item["x1"] == item["x1"] and old_item["x2"] == item["x2"] and old_item["y1"] == item["y1"] and old_item["y2"] == item["y2"]:
                            old_item["className"] = item["className"]
                            old_item["username"] = "lm"
                            count += 1
                            # bboxes.append(item)
        saveResultsByJson(basePath + "jsons/new/{}".format(imgIndex), jsondata)

    print("总更改分类数：", count)

if __name__ == '__main__':
    main()


