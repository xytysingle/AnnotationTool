import csv
import json
import shutil
import os



def read_csv(path):
    csv_file = csv.reader(open(path, "r", encoding='utf-8'))
    return csv_file

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def copyAndRename(path, filename):
    shutil.copy(path, filename)

def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print("{}创建成功".format(path))
        return True
    else:
        # print("{}已存在".format(path))
        return False

def main(scences, sl):
    global all_data
    global BasePath
    global date
    global TargetPath
    global count
    global scence_count
    global rect_count
    global resultsNum
    for scence in scences:
        scence_count += 1
        flag = 0
        flag2 = 0
        for rect in scence["bboxes"]:
            rect_count += 1
            for coca in cocal:
                if int(coca) == int(rect["id"]):
                    flag2 = 1
                    break
            if flag2 == 0:
                for sku in sl:

                    count += 1

                    if int(sku) == int(rect["id"]):
                        flag = 1
                        break

        if flag == 1 and flag2 == 0:
            try:
                img_name = scence["img_path"].split("/")[-1].split(".")[0] + ".jpg"

                if targetName == "dpz":
                # 大瓶装筛选
                    mkdir(TargetPath + "fewBottles/" + date)
                    copyAndRename(scence["img_path"], TargetPath + "fewBottles/" + date + "/" + img_name)

                elif targetName == "dt":
                    # 堆头筛选
                    mkdir(TargetPath + "boxes/" + date)
                    copyAndRename(scence["img_path"], TargetPath + "boxes/" + date + "/" + img_name)
                elif targetName == "dp":
                    # 单瓶筛选
                    mkdir(TargetPath + "danping/" + date)
                    copyAndRename(scence["img_path"], TargetPath + "danping/" + date + "/" + img_name)

                resultsNum += 1
                print("已找到{}张目标图片".format(resultsNum))
                all_data.append(
                    {
                        "image": img_name,
                        "bboxes": scence["bboxes"]
                    }
                )
            except:
                print("没有该图片")



if __name__ == "__main__":
    # BasePath = "/Users/lingmou/Desktop/trax-selenium/"
    sku_list = []
    BasePath = "/Users/lingmou/Desktop/traxResults/resultsJson/bottlesAndboxes/"
    TargetPath = "/Users/lingmou/Desktop/traxResults/"
    # targetName = "dt"
    targetName = "dt"
    date = "20190409"
    all_data = []
    count = 0
    scence_count = 0
    rect_count = 0
    resultsNum = 0

    if targetName == "dpz":
        # 大包装筛选
        sku_list = read_csv("traxsku/fewBottleSKUFilter_1.csv")
    elif targetName == "dt":
        # 堆头筛选
        sku_list = read_csv("traxsku/duitouSKUFilter-2.csv")

    elif targetName == "dp":
        # danping
        sku_list = read_csv("traxsku/danpingcanuse.csv")
    coca_list = read_csv("traxsku/doutouCoca.csv")
    sl = []
    for sku in sku_list:
        sl.append(sku[0])
    print(sl)

    cocal = []
    for sku in coca_list:
        cocal.append(sku[0])

    scences = read_json(BasePath + "bottlesAndboxes_{}.json".format(date))

    main(scences, sl)

    if targetName == "dpz":
        # 大包装筛选
        mkdir(TargetPath + "resultsJson/fewBottles/" + date)
        saveResultsByJson(TargetPath + "resultsJson/fewBottles/" + date + "/fewBottles_{}".format(date), all_data)
    elif targetName == "dt":
        # 堆头筛选
        mkdir(TargetPath + "resultsJson/boxes/" + date)
        saveResultsByJson(TargetPath + "resultsJson/boxes/" + date + "/boxes_{}".format(date), all_data)
    elif targetName == "dp":
        # danping
        mkdir(TargetPath + "resultsJson/danping/" + date)
        saveResultsByJson(TargetPath + "resultsJson/danping/" + date + "/danping_{}".format(date), all_data)


    print(scence_count, rect_count, count)
