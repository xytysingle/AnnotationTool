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
            fenlei = getyubiaoResults(index)
            for item in response["bboxes"]:
                # print(item)
                flag = 0
                for fl_item in fenlei:
                    if item["x1"] < fl_item["centerpointX"] < item["x2"] and item["y1"] < fl_item["centerpointY"] < item["y2"]:
                        flag = 1
                        tempObj = {
                            "className": fl_item["className"],
                            "score": 0.960,
                            "username": "lingmou",
                            "truncated": item["truncated"],
                            "x1": item["x1"],
                            "x2": item["x2"],
                            "y1": item["y1"],
                            "y2": item["y2"]
                        }
                        r_bboxes.append(tempObj)
                        break
                if flag == 0:
                    tempObj = {
                        "className": item["className"],
                        "score": 1,
                        "username": item["username"],
                        "truncated": item["truncated"],
                        "x1": item["x1"],
                        "x2": item["x2"],
                        "y1": item["y1"],
                        "y2": item["y2"]
                    }
                    r_bboxes.append(tempObj)

            uploadResults(index, r_bboxes)
    except Exception as e:
        print("获取失败:",e)

def getyubiaoResults(index):
    anno_url = 'http://annotation.lingmou.ai:8000/index.php/annotation/view?image={}'.format(index)
    fenlei = []
    try:
        response = requests.get(anno_url).text
        response = json.loads(response)
        if response.__contains__("code") and response["code"] == 0:
            print("{}:没有标注结果".format(index))
        else:
            for item in response["bboxes"]:
                # print(item)
                tempObj = {
                    "className": item["className"],
                    "score": 1,
                    "username": "lingmou",
                    "centerpointX": int((item["x1"] + item["x2"]) / 2),
                    "centerpointY": int((item["y1"] + item["y2"]) / 2),
                }
                fenlei.append(tempObj)
            # uploadResults(index, fenlei)
        return fenlei
    except Exception as e:
        print("获取失败:",e)

def uploadResults(index, r_bboxes):
    # print(response["username"], response["bboxes"])
    submit_url = "http://annotation.lingmou.ai:8000/index.php/annotation/upsert"
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

    for index in range(336306, 339062):
        getLabelResults(index)