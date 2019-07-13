import json
import glob
import pandas as pd



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

def saveDataToExcel(json):
   datas = read_json(json)
   maxnum = 0
   for rowdata in datas:
       if len(rowdata) > maxnum:
           maxnum = len(rowdata)


   formdata = {}
   for i in range(maxnum):
       formdata["{}".format(i)] = []
   print(len(formdata))

   for rowdata in datas:
       i = 0
       for j in range(len(formdata)):
           # print(j)

           if i < len(rowdata):
               # print(len(rowdata), i)
               formdata[str(j)].append(rowdata[i]["className"])
           else:
               formdata[str(j)].append('')
           i += 1

   writer = pd.ExcelWriter('lmrecognnition.xlsx')
   df1 = pd.DataFrame(data=formdata)
   df1.to_excel(writer, sheet_name='{}'.format(json.split("/")[-1].split(".")[0]))

   writer.save()


def sortRects(data):
    data.sort(key=lambda ele: ele[0]["y"])
    for rowdata in data:
        # for item in rowdata:
        rowdata.sort(key=lambda ele:ele["x"])
        print(rowdata)
    return data



if __name__ == '__main__':
    bg = [
        6004073,
        6004074,
        6004077,
        6004080,  # 补充一个空缺位
        6004083,
        6004086,
        6004102,
        6004104,  # 补两个空缺位
        6004106,  # 补两个空缺位
        6004111

    ]
    hj = [
        6004075,
        6004078,
        6004084,  # 两层罐装的需要调整
        6004089,
        6004092,  # 盒装罐装需要调整
        6004094,
        6004097,  # 两层罐装需要修改
        6004108,  # 两层罐装需要修改
        6004116,
        6004132

    ]

    # for item in bg:
    # main()
    item = 2
    saveDataToExcel("/Users/lingmou/Desktop/python-script/20ImageRecongnize/target/jsons/{}.json".format(str(item)))
