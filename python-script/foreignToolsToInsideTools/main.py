import requests
import json
import csv


def getLabelResults(index):
    anno_url = 'http://annotation-web.lingmou.ai:8000/index.php/annotation/view?image={}'.format(index)
    r_bboxes = []
    try:
        response = requests.get(anno_url).text
        response = json.loads(response)
        if response.__contains__("code") and response["code"] == 0:
            print("{}:没有标注结果".format(index))
        else:
            for item in response["bboxes"]:
                # print(item)
                # tempObj = {
                #     "className": item["className"],
                #     "score": 1,
                #     # "username": item["username"],
                #     "username": "jz",
                #     "truncated": item["truncated"],
                #     "x1": item["x1"],
                #     "x2": item["x2"],
                #     "y1": item["y1"],
                #     "y2": item["y2"]
                # }
                tempObj = {
                    "className": item["className"],
                    "score": 1,
                    # "username": item["username"],
                    "username": "jz",
                    "truncated": 0,
                    "points": item["points"]
                }
                r_bboxes.append(tempObj)
            uploadResults(index, r_bboxes)
    except Exception as e:
        print("获取失败:",e)


def uploadResults(index, r_bboxes):
    # print(response["username"], response["bboxes"])
    # submit_url = "http://annotation.lingmou.ai:8000/index.php/annotation/upsert"
    submit_url = "http://192.168.3.4:8000/index.php/annotation/upsert"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    submit_data = {
        "image": str(index),
        "rotate": 0,
        "sceneType": -1,
        "username": "jz",
        "bboxes": r_bboxes
    }
    submit_data = json.dumps(submit_data)
    # print(submit_data)
    response = requests.post(url=submit_url, data=submit_data, headers=headers)
    print(index, response.text)


if __name__ == "__main__":

    # 7001001
    # getLabelResults(20000473)
    for index in range(20000001, 20001001):
        getLabelResults(index)