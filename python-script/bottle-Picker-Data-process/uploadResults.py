import json
import requests
import glob

BasePath = "/Users/lingmou/Desktop/bottlepicker/"

def uploadResults(data, index):
    _data = []
    submit_url = "http://192.168.3.4:8000/index.php/annotation/upsert"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    for item in data:
        tempObj = {
            "className": item["className"],
            "x2": item["x2"],
            "y2": item["y2"],
            "score": float(item["score"]),
            "truncated": 0,
            "y1": item["y1"],
            "x1": item["x1"],

        }
        _data.append(tempObj)

    submit_data = {
        "image": str(index),
        "rotate": 0,
        "sceneType": -1,
        "username": "dongwei",
        "bboxes": _data
    }
    print(submit_data)
    submit_data = json.dumps(submit_data)
    response = requests.post(url=submit_url, data=submit_data, headers=headers)
    print(index, response.text)


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def main():
    jsonResults = glob.glob(BasePath + "numbered/addboxJson/*.json")
    for item in jsonResults:
        input_data = read_json(item)
        uploadResults(input_data["bboxes"], item.split("/")[-1].split(".")[0])


if __name__ == '__main__':
    main()
    # uploadResults(read_json("/Users/lingmou/Desktop/bottlepicker/numbered/addboxJson/7600002.json")["bboxes"], 7600002)