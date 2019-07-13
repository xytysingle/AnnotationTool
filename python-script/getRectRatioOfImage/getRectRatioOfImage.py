# -*- coding: utf-8 -*-
import requests
import csv
import json
import numpy as np
import cv2
import urllib.request


Login_URL = 'http://ubuntu.zhixiang.co:8889/index.php/user/login'
getLabelInfo_Url = 'http://ubuntu.zhixiang.co:8889/index.php/annotation/view'
submitLabelInfo_Url = 'http://ubuntu.zhixiang.co:8889/index.php/annotation/upsert'
getImage_Url = 'http://annotation.lingmou.ai:8000/index.php/image/view?file='

s = requests.Session()
# print(s)
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
login_data = {
    'username': 'admin',
    'password': 'admin'
}

login_response = s.post(url=Login_URL, data=login_data, headers=headers)

csv_file_labelName = []

def getOldIndexAndNewIndex():
    csv_file_imgIndex = csv.reader(open('/Users/lingmou/Desktop/python-script/moveOldResultsToNewByIndex/sources/oldnewindex.csv', 'r'))
    # for line in csv_file_imgIndex:
    #     oldIndex = line[0]
    #     newIndex = line[1]
    #     print(oldIndex, newIndex)
    return csv_file_imgIndex
def getOldNameAndNewName():
    # global csv_file_labelName
    csv_file_labelName = csv.reader(open('/Users/lingmou/Desktop/python-script/moveOldResultsToNewByIndex/sources/oldnewname.csv', 'r', encoding='utf-8'))
    # print(csv_file_labelName)
    # for line in csv_file_labelName:
    #     oldName = line[0]
    #     newName = line[1]
    #     print(line)
    return csv_file_labelName

def getLabelInfoByIndex(oldIndex):

    getLabelInfo_data = {
        'image': oldIndex
    }
    labelInfo_response = s.get(url=getLabelInfo_Url, params=getLabelInfo_data, headers=headers)
    results = labelInfo_response.content.decode('utf-8')
    # print(results)
    results = json.loads(results)
    # print(results['bboxes'])

    return results
    # results = changeNameMiddleWare(results)
    # print(results['bboxes'])
    # submitLabelInfo(newIndex, results)

def submitLabelInfo(index, results):
    # print(type(results['bboxes']))
    # boxes = []
    # for item in results['bboxes']:
    #     boxes.append(item)
    #     print(item)
    boxes = np.array(results['bboxes'])
    # boxes = json.dumps(boxes.tolist())
    print(type(boxes), np.shape(boxes))
    boxes=boxes.tolist()
    print(boxes[0])
    submitLabelInfo_data = {
        'username': results['username'],
        'sceneType': results['sceneType'],
        'rotate': results['rotate'],
        'image': index,
        'bboxes': boxes,
    }

    # print(type(results['bboxes']))
    submitResponse = s.post(url=submitLabelInfo_Url, data=submitLabelInfo_data, headers=headers)
    print(submitResponse.content)
def changeNameMiddleWare(results):

    _bboxes = results['bboxes']
    # csv_file_labelName = getOldNameAndNewName()
    for item in _bboxes:
        for line in getOldNameAndNewName():
            # print('line[0]:', line[0], item['className'])
            if item['className'] == line[0]:
                # print('++++++++')
                item['className'] = line[1]
                # break
            else:
                continue
        # print('--------------------')
    print(results['bboxes'])
    return results

def getRectRatioOfImage(item, imgShape):

    width = int(item['x2']) - int(item['x1'])
    height = int(item['y2']) - int(item['y1'])
    rs = (width * height) / (imgShape[0] * imgShape[1])
    return rs

def getImageShape(image):
    # getImage_Url + index
    img = cv2.imread(image, 1)
    # imageW = img.shape[0]
    # imageH = img.shape[0]
    # print(img.shape[0])
    return img.shape

def get_images(id, img_url):
    # global count
    # image_name = img_url.rpartition('/')[2]
    image_name = id
    save_path = './images/{}.jpg'.format(image_name)
    urllib.request.urlretrieve(img_url, save_path)
    # 'http://snapshot-api-sc.lingmouai.com//uploads/pbms/20180925/107964414.jpg'
    # count = count + 1
    # print(count)
def save_data(imgIndex, advantage, samll, sku):
    print(imgIndex, advantage, samll)
    # pf = pd.DataFrame(dataList, columns=["old", "new"])
    # pf.to_csv("indexData.csv", index=False, encoding="utf-8")
    out = open('ratio.csv', 'a', newline='', encoding='utf-8')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow([imgIndex, advantage, samll, sku])

if __name__ =='__main__':
    # getImageShape()
    # 746642-746799
    for i in range(746642, 746799+1):
        # url = getImage_Url + str(i) + '.jpg'
        # get_images(str(i), url)
        print('正在处理第{}张'.format(i))
        imgShape = getImageShape('./images/{}.jpg'.format(i))
        results = getLabelInfoByIndex(str(i))
        # advantage = 0
        count = 0
        small = 1
        all = 0
        sku = ''
        for item in results['bboxes']:

            if item['className'] != '牙膏_侧面':
                # print(item)
                count += 1
                rs = getRectRatioOfImage(item, imgShape)
                all += rs
                if small > rs:
                    small = rs
                    sku = item['className']
            else:
                continue
        advantage = all / count
        save_data(i, advantage, small, sku)
