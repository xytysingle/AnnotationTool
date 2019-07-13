import glob
import json


def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def main():
    bottleJsons = glob.glob("/Users/lingmou/Desktop/bottlepicker/numbered/json/*.json")
    boxJsons = glob.glob("/Users/lingmou/Desktop/bottlepicker/boxjsons/*.json")
    for item in bottleJsons:
        nowIndex = item.split("/")[-1].split(".")[0]
        data = read_json(item)
        orginalIndex = data["image"].split("/")[-1].split(".")[0]
        for box_item in boxJsons:
            if orginalIndex == box_item.split("/")[-1].split(".")[0]:
                box_data = read_json(box_item)
                for box in box_data["bboxes"]:
                    data["bboxes"].append(box)

                saveResultsByJson("/Users/lingmou/Desktop/bottlepicker/numbered/addboxJson/{}".format(nowIndex), data)

                print("处理成功：", nowIndex)

if __name__ == '__main__':
    main()