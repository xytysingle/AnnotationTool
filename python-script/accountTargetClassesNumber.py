import json
import glob

base_path = "/Users/lingmou/Desktop/dataset/"

def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def main():
    jsons = glob.glob(base_path + "jsons/*.json")
    h_list = []
    for j_data in jsons:
        data = read_json(j_data)
        horizontal_num = 0
        for item in data:
            if item["className"] == "can_horizontal" or item["className"] == "bottle_horizontal":
                horizontal_num += 1
        if horizontal_num > 5:
            h_list.append({
                "image": "{}.jpg".format(j_data.split("/")[-1].split(".")[0]),
                "horizontal_num": horizontal_num
            })
            

