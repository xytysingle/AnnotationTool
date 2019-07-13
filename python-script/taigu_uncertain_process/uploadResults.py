import json
import requests
from tqdm import tqdm



def uploadResults(data):
    # submit_url = "http://annotation.lingmou.ai:8000/index.php/annotation/upsert"
    submit_url = "http://192.168.3.4:8000/index.php/annotation/upsert"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    submit_data = {
        "image": str(data["image"]),
        "rotate": 0,
        "sceneType": -1,
        "username": "dongwei",
        "bboxes": data["bboxes"]
    }
    # print(submit_data)
    submit_data = json.dumps(submit_data)
    try:
        response = requests.post(url=submit_url, data=submit_data, headers=headers)
        # print(data["image"], response.text)
    except:
        print("上传失败！")


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data


if __name__ == "__main__":

    BasePath = "/data/dongwei/taigu_uncertain_process/target/resultsJson/numbered_results.json"
    input_data = read_json(BasePath)

    for item in tqdm(input_data):
        uploadResults(item)
        # print(item)