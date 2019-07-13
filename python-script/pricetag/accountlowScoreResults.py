import glob
import json
import csv

SCORE = 1

def accountLowScoreCount():
    json_paths = glob.glob("/Users/lingmou/Desktop/bottlepicker/20190410json_1/*.json")

    for json_path in json_paths:
        print(json_path)
        target_rect = 0
        input_data = read_json(json_path)
        image_name = input_data["image"]
        bboxes = input_data["bboxes"]
        for item in bboxes:
            if float(item["score"]) < SCORE:
                target_rect += 1
        save_data(image_name, target_rect)



def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data


def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def save_data(imagename, number):

    out = open('acountlowScorecount.csv', 'a', newline='', encoding='utf-8')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow([imagename, number])


if __name__ == '__main__':
    accountLowScoreCount()