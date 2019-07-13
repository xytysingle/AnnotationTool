# -*- coding: utf-8 -*-
import requests
import csv
import json
import numpy as np


Login_URL = 'http://ubuntu.zhixiang.co:8889/index.php/user/login'
getLabelInfo_Url = 'http://ubuntu.zhixiang.co:8889/index.php/annotation/view'
submitLabelInfo_Url = 'http://ubuntu.zhixiang.co:8889/index.php/annotation/upsert'

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

def getLabelInfoByIndex(oldIndex, newIndex):

    getLabelInfo_data = {
        'image': oldIndex
    }
    labelInfo_response = s.get(url=getLabelInfo_Url, params=getLabelInfo_data, headers=headers)
    results = labelInfo_response.content.decode('utf-8')
    # print(results)
    results = json.loads(results)
    print(results['bboxes'])
    results = changeNameMiddleWare(results)
    # print(results['bboxes'])
    submitLabelInfo(newIndex, results)

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


if __name__ =='__main__':

    # index = '100001'
    i = 0
    csv_file_imgIndex = getOldIndexAndNewIndex()
    # getOldNameAndNewName()

    for line in csv_file_imgIndex:
        i += 1
        getLabelInfoByIndex(line[0], line[1])
        print(i)