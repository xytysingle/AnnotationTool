import csv
import cv2
import json


def read_csv(path):
    csv_file = csv.reader(open(path, "r", encoding='utf-8'))
    return csv_file

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def filterSKU(scences, sku_list):
    global start_index
    global all_data
    global count
    global scence_count
    global rect_count

    for scence in scences:
        scence_count += 1
        # print(scence)
        flag = 0
        for rect in scence["bboxes"]:
            # print(rect)
            rect_count += 1
            for sku in sku_list:
                # print(sku[0])
                count += 1
                if int(sku) == int(rect["id"]):
                    flag = 1
                    # print("+++")
                    continue
        if flag == 1:
            start_index += 1
            print(start_index)
            # readAndSaveImage(scence["img_path"], "./danping/" + str(start_index) + ".jpg")
            readAndSaveImage(scence["img_path"], "./duitou/" + str(start_index) + ".jpg")
            all_data.append(
                {
                    "image": start_index,
                    "bboxes": scence["bboxes"]
                }
            )



def readAndSaveImage(path, filename):
    img = cv2.imread(path)
    cv2.imwrite(filename, img)


def save_data(img_path, bboxes):
    out = open('duitou20190313.csv', 'a', newline='', encoding='utf-8')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow([img_path, bboxes])


def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


if __name__ == "__main__":
    count = 0
    scence_count = 0
    rect_count = 0
    sku_list = read_csv("duitouSKU.csv")
    # sku_list = read_csv("danpingSKU.csv")
    sl = []
    for sku in sku_list:
        sl.append(sku[0])
    print(sku_list)
    scences = read_json("20190314.json")

    all_data = []
    start_index = 324400
    filterSKU(scences, sl)
    print(scence_count, rect_count, count)
    saveResultsByJson("duitou20190314", all_data)
