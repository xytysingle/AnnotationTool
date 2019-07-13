import requests
import json



def getRect(index):
    anno_url = 'http://annotation.lingmou.ai:8000/index.php/annotation/view?image={}'.format(index)
    try:
        response = requests.get(anno_url).text
        response = json.loads(response)
        if response.__contains__("code") and response["code"] == 0:
            print("{}:没有标注结果".format(index))
        else:
            saveResultsByJson("results/{}".format(index), response["bboxes"])

    except Exception as e:
        print("获取失败:",e)


def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

def main():
    for index in range(6004073, 6004134):
        print(index)
        getRect(str(index))

if __name__ == '__main__':
    main()