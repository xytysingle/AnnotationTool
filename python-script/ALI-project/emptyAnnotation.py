import json
import requests
import glob
from tqdm import tqdm

BasePath = "/Users/lingmou/Desktop/ali/"
imgList = [
    "1100158-1100284",
    "1300094-1300125",
    "1500094-1500156",
    "1600214-1600344",
    "2300181-2300276",
    "1800938-1801363",
    "1900196-1900313",
    "2101301-2101583"
]

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
    # print(submit_data)
    submit_data = json.dumps(submit_data)
    try:
        response = requests.post(url=submit_url, data=submit_data, headers=headers)
        print(index, response.text)
    except:
        print("....", index)


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def main():
    for item in tqdm(imgList):

        # startIndex = item.split("-")[0]
        # endIndex = item.split("-")[1]
        # print(startIndex, endIndex)
        emptyList = read_json("/Users/lingmou/Desktop/python-script/ALI-project/notimages-1.json")
        for i in tqdm(emptyList):
            uploadResults([], str(i))
            print('正在清空第{}张'.format(i))


if __name__ == '__main__':
    main()
    # uploadResults([], str(1100158))