import json
import requests
import glob

BasePath = "/Users/lingmou/Desktop/bottle-box/"

def uploadResults(data, index, rotate):

    submit_url = "http://annotation.lingmou.ai:8000/index.php/annotation/upsert"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    submit_data = {
        "image": str(index),
        "rotate": rotate,
        "sceneType": -1,
        "username": "dongwei",
        "bboxes": data
    }
    # print(submit_data)
    submit_data = json.dumps(submit_data)
    try:
        response = requests.post(url=submit_url, data=submit_data, headers=headers)
        print(index, response.text)
    except Exception as e:
        with open("yc.txt", "a") as f:
            f.write(str(index) + ':' + str(e) + '\n')


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def main():
    jsonResults = glob.glob(BasePath + "numbered/json/*.json")
    for item in jsonResults:
        input_data = read_json(item)
        rotate = input_data["rotate"]
        uploadResults(input_data["bboxes"], item.split("/")[-1].split(".")[0], rotate)


if __name__ == '__main__':
    main()