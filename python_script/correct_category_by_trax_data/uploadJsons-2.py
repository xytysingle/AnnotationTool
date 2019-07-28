import json
import requests
import glob
from tqdm import tqdm

#/fast_data/Drink_China/Construct-images/0724_jsons/
BasePath = "/data/tanx/project/PenBev/original_imgs_bboxes_json/"

def uploadResults(data, index):

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
    jsonResults = glob.glob(BasePath + "*.json")
    # jsonResults = glob.glob('/data/tanx/project/PenBev/original_imgs_bboxes_json/51000002.json')
    for item in tqdm(jsonResults):
        print(item)
        # input_data = read_json(item)
    # item = "/Users/lingmou/Desktop/python-script/ALI-project/51000001.json"
        input_data = read_json(item)
    # if input_data.__contains__("bboxes"):
    #     bboxes = input_data["bboxes"]
        bboxes = input_data["bboxes"]
        for box in bboxes:
            # box["score"] = float(box["score"])
            box["truncated"] = 0
            box["score"] = float(box["score"])

        uploadResults(bboxes, item.split("/")[-1].split(".")[0])


if __name__ == '__main__':
    main()