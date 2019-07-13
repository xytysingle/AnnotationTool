import json




def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def saveResultsByJson(filename, data):
    with open("{}".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def main():
    bboxes = []
    count = 0
    datas = read_json("/Users/lingmou/Desktop/python-script/20ImageRecongnize/resource/report/2.json")
    datas = datas["data"]["report"]["result"]["class_detections"]
    print(datas)
    for item in datas:
        for obj in item["objects"]:
            count += 1
            tempObj = {
                "className": item["sku_name"],
                "x": int((obj["bl"][0] + obj["tr"][0])*3015 / 2),
                "y": int((obj["bl"][1] + obj["tr"][1])*2624 / 2),
            }
            bboxes.append(tempObj)
    print(count)
    saveResultsByJson("/Users/lingmou/Desktop/python-script/20ImageRecongnize/centerpoint/2.json", bboxes)
if __name__ == '__main__':
    main()