import requests
import json






def getLabelResults(index):
    anno_url = 'http://annotation.lingmou.ai:8000/index.php/annotation/view?image={}'.format(index)
    r_bboxes = []
    try:
        response = requests.get(anno_url).text
        response = json.loads(response)
        if response.__contains__("code") and response["code"] == 0:
            print("{}:没有标注结果".format(index))
        else:
            for item in response["bboxes"]:
                # print(item)
                flag = 0
                if item["score"] <= 0.95:
                    flag = 1
                    tempObj = {
                        "className": item["className"],
                        "score": item["score"],
                        "username": "lingmou",
                        "truncated": item["truncated"],
                        "x1": item["x1"],
                        "x2": item["x2"],
                        "y1": item["y1"],
                        "y2": item["y2"]
                    }
                    r_bboxes.append(tempObj)

                saveResultsByJson(BasePath + "/{}/{}".format("results", index), r_bboxes)

                if flag == 1:
                    getImage(index)

    except Exception as e:
        print("获取失败:",e)


def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def getImage(index):
    BASEURL = 'http://annotation.lingmou.ai:8000/index.php/image/view?file='
    response = requests.get(BASEURL + index + '.jpg')
    with open(BasePath + '/images/{}.jpg'.format(index), 'wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    BasePath = "/Users/lingmou/Desktop/shujujiucuo"
    for index in range(8005001, 8019845):
        print("正在处理第{}张".format(index))
        getLabelResults(str(index))