import requests
import json
import glob

def downLoadAnnoResults(index):
    jsonData = {}
    bboxes = []
    # anno_url = 'http://annotation.lingmou.ai:8000/index.php/annotation/view?image={}'.format(index)
    anno_url = 'http://192.168.3.4:8000/index.php/annotation/view?image={}'.format(index)
    try:
        response = requests.get(anno_url).text
        # print(response)

        response = json.loads(response)
        jsonData["image"] = response["image"]
        for item in response["bboxes"]:
            bboxes.append({
                "className": "box",
                "score": 1,
                "truncated": 0,
                "username": "sc",
                "x1": item["x1"],
                "x2": item["x2"],
                "y1": item["y1"],
                "y2": item["y2"],
            })

        jsonData["bboxes"] = bboxes

        saveResultsByJson("/Users/lingmou/Desktop/bottlepicker/boxjsons/{}".format(index), jsonData)
    except Exception as e:
        print("没有获取到标注结果：", e)
        with open("yc.txt", "a") as f:
            f.write(index + '\n')


def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

if __name__ == '__main__':
    imagesList = glob.glob("/Users/lingmou/Desktop/bottlepicker/yubiaozhu/detection/*.jpg")
    for image in imagesList:
        index = image.split("/")[-1].split(".")[0]
        print("正在下载：", index)
        downLoadAnnoResults(index)