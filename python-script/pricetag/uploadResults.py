import json
import requests



def uploadResults(data, index):
    submit_url = "http://annotation.lingmou.ai:8000/index.php/annotation/upsert"
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
    print(submit_data)
    submit_data = json.dumps(submit_data)
    response = requests.post(url=submit_url, data=submit_data, headers=headers)
    print(response.text)
    # print(data["image"], response.text)


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data


if __name__ == "__main__":

    BasePath = "/Users/lingmou/Desktop/pricetag/numbered/jsons/7003674.json"
    input_data = read_json(BasePath)
    for item in input_data["bboxes"]:
        item["className"] = "价签"
        item["score"] = float(item["score"])
    uploadResults(input_data["bboxes"], 7003674)