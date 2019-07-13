import json
import requests
import glob
from tqdm import tqdm
import shutil

BasePath = "/Users/lingmou/Desktop/cleanData/"

def uploadResults(data, index):
    # print(data)

    submit_url = "http://192.168.3.4:8000/index.php/annotation/upsert"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    submit_data = {
        "image": str(index),
        "rotate": 0,
        "sceneType": -1,
        "username": "dongwei",
        "bboxes": data
    }
    # print(submit_data)
    submit_data = json.dumps(submit_data)
    try:
        response = requests.post(url=submit_url, data=submit_data, headers=headers)
        # print(response)
        if len(response.text) > 0:
            res_data = json.loads(response.text)
            print(res_data)
            if(res_data["code"] == 0):
                print(index, response.text)
    except Exception as e:

        print(index, ":出错了！", e)


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def main():
    i = 0
    wrong = 0
    count = 0
    jsonResults = glob.glob(BasePath + r"tjy/20190514182931-2019-05-14/*.json")
    for item in tqdm(jsonResults):
        # imgIndex = item.split("\\")[-1].split(".")[0]
        # print(imgIndex)
        try:
            input_datas = read_json(item)
            # print(item)
            imgIndex = input_datas["image"].split(".")[0]
            bboxes = input_datas["bboxes"]
            for box in bboxes:
                count += 1
                # box["className"] = "其他"
                # box["truncated"] = 0
                # box["username"] = "jzt"
                if box["x1"] > box["x2"]:
                    x = box["x1"]
                    y = box["y1"]
                    box["x1"] = box["x2"]
                    box["y1"] = box["y2"]
                    box["x2"] = x
                    box["y2"] = y
                elif box["y1"] > box["y2"]:
                    x = box["x1"]
                    y = box["y1"]
                    box["x1"] = box["x2"]
                    box["y1"] = box["y2"]
                    box["x2"] = x
                    box["y2"] = y
                elif box["x1"] == box["x2"]:
                    bboxes.remove(box)
                    wrong += 1
                elif box["y1"] == box["y2"]:
                    bboxes.remove(box)
                    wrong += 1
            for box in bboxes:
                # box["className"] = "其他"
                # box["truncated"] = 0
                # box["username"] = "jzt"
                if box["x1"] > box["x2"]:
                    x = box["x1"]
                    y = box["y1"]
                    box["x1"] = box["x2"]
                    box["y1"] = box["y2"]
                    box["x2"] = x
                    box["y2"] = y
                elif box["y1"] > box["y2"]:
                    x = box["x1"]
                    y = box["y1"]
                    box["x1"] = box["x2"]
                    box["y1"] = box["y2"]
                    box["x2"] = x
                    box["y2"] = y
                elif box["x1"] == box["x2"]:
                    bboxes.remove(box)
                    wrong += 1
                elif box["y1"] == box["y2"]:
                    bboxes.remove(box)
                    wrong += 1
            for box in bboxes:
                box["className"] = "其他"
                box["truncated"] = 0
                box["username"] = "jzt"
            # if (imgIndex == "2704567"):
            #     print("找到该图片！")
            #     uploadResults(bboxes, imgIndex)

        except Exception as e:
            i += 1
            print(e)
            shutil.move(item, BasePath + "right/" + item.split("\\")[-1].split(".")[0] + ".json")
    print(i)
    print("wrong:", wrong)
    print("count:", count)



if __name__ == '__main__':
    main()