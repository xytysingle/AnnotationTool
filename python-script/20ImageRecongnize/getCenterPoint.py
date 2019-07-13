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
    jsons = glob.glob("/Users/lingmou/Desktop/python-script/20ImageRecongnize/resource/jsons/*.json")
    for json in jsons:
        bboxes = read_json(json)
        for item in bboxes:
            item["x"] = int((item["x1"] + item["x2"])/2)
            item["y"] = int((item["y1"] + item["y2"])/2)
        saveResultsByJson("/Users/lingmou/Desktop/python-script/20ImageRecongnize/centerpoint/{}".format(json.split("/")[-1]), bboxes)

if __name__ == '__main__':
    main()