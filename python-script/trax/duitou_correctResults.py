import json
import requests


def downloadResults(index):
    anno_url = 'http://annotation.lingmou.ai:8000/index.php/annotation/view?image={}'.format(index)
    response = requests.get(anno_url).text
    response = json.loads(response)
    try:
        bboxes = response["bboxes"]
        t_bboxes = getTraxResults(index)
        r_bboxes = []

        for item in bboxes:
            # print(item)
            flag = 0
            for t_item in t_bboxes:
                if item["x1"] < t_item["x"] < item["x2"] and item["y1"] < t_item["y"] < item["y2"]:
                    try:
                        item["className"] = t_item["name"]
                        item["attribute"] = t_item["attribute"]
                        item["username"] = "trax"
                        item["score"] = 0.901
                    except:
                        print("没有对应名称")
                    # print("---:", t_item["name"])
                    # if(t_item["name"]):

            r_bboxes.append(item)

        uploadResults(index, r_bboxes)
    except:
        print(index + "该序号没有图片")


def uploadResults(index, r_bboxes):
    submit_url = "http://annotation.lingmou.ai:8000/index.php/annotation/upsert"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    submit_data = {
        "image": index,
        "rotate": 0,
        "sceneType": -1,
        "username": "trax",
        "bboxes": r_bboxes
    }
    submit_data = json.dumps(submit_data)
    response = requests.post(url=submit_url, data=submit_data, headers=headers)
    print(index, response.text)

def getTraxResults(index):
    global all_data
    for item in all_data:
        # print(item)
        if str(index) == str(item["image"]):
            return item["bboxes"]


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data


if __name__ == "__main__":

    all_data = read_json("duitou20190315name.json")
    print(all_data)

    # 324401～324755
    for index in range(326722, 328131):

        downloadResults(str(index))
    # uploadResults("100001", data)