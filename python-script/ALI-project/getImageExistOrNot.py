import requests
import json
import glob
import shutil
import os
from tqdm import tqdm


images_url = "http://annotation.lingmou.ai:8000/index.php/image/list?token="

response = requests.get(images_url)
response = json.loads(response.text)

def main():
    notimages = []
    for i in tqdm(range(7500001, 7509084)):
        flag = 0
        for item in response:
            if str(i) == item.split(".")[0]:
                # print("存在")
                flag = 1
                break
        if flag == 0:
            print("图片不存在！")
            notimages.append(i)
    saveResultsByJson("notimages-1", notimages)


def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

if __name__ == '__main__':
    main()