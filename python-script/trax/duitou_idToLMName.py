import json
import csv


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data


def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def read_csv(path):
    csv_file = csv.reader(open(path, "r", encoding='utf-8'))
    return csv_file

def idToName():
    global sku_list
    duitou = read_json("/Users/lingmou/Desktop/trax-selenium/duitou20190315.json")

    for scence in duitou:
        for item in scence["bboxes"]:

            for sku in sku_list:
                # print(sku)
                if int(item["id"]) == int(sku["id"]):
                    print("+++++")
                    item["name"] = sku["name"]
                    item["attribute"] = sku["attribute"]
                    print(item)
    saveResultsByJson("duitou20190315name", duitou)



if __name__ == "__main__":
    skus = read_csv("/Users/lingmou/Desktop/trax-selenium/traxsku/duitoucanuse.csv")
    sku_list = []
    for sku in skus:
        # print(sku)
        sku_list.append({
            "id": sku[0],
            "name": sku[3],
            "attribute": sku[4]

        })
    idToName()