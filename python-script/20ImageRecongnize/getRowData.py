import json
import glob

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def saveResultsByJson(filename, data):
    with open("{}".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def main():

    jsons = glob.glob("/Users/lingmou/Desktop/python-script/20ImageRecongnize/centerpoint/*.json")
    for json in jsons:
        bboxes = read_json(json)
        for item in bboxes:
            item["x"] = int((item["x1"] + item["x2"])/2)
            item["y"] = int((item["y1"] + item["y2"])/2)
        saveResultsByJson("/Users/lingmou/Desktop/python-script/20ImageRecongnize/centerpoint/{}".format(json.split("/")[-1]), bboxes)

def getData(json):
    data = []
    bboxes = read_json(json)
    for item in bboxes:
        flag = False
        for rowData in data:
            if abs(item["y"] - rowData[0]["y"]) < dis:
                rowData.append(item)
                flag = True
                break
        if flag == False:
            data.append([item])

    data = sortRects(data)

    saveResultsByJson("/Users/lingmou/Desktop/python-script/20ImageRecongnize/target/jsons/{}".format(json.split("/")[-1]), data)

def sortRects(data):
    data.sort(key=lambda ele: ele[0]["y"])
    for rowdata in data:
        # for item in rowdata:
        rowdata.sort(key=lambda ele:ele["x"])
        print(rowdata)
    return data



if __name__ == '__main__':
    # main()
    bg = [
        6004073,
        6004074,
        6004077,
        6004080, # 补充一个空缺位
        6004083,
        6004086,
        6004102,
        6004104, #补两个空缺位
        6004106, #补两个空缺位
        6004111


    ]
    hj = [
        6004075,
        6004078,
        6004084, #两层罐装的需要调整
        6004089,
        6004092, #盒装罐装需要调整
        6004094,
        6004097, #两层罐装需要修改
        6004108, #两层罐装需要修改
        6004116,
        6004132


    ]
    item = 2
    dis = 50
    # for item in bg:
    getData("/Users/lingmou/Desktop/python-script/20ImageRecongnize/centerpoint/{}.json".format(str(item)))