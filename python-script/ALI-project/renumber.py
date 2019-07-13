import glob
import shutil
import json


imagesPath = "/Users/lingmou/Desktop/ali/"

def main():
    # images = glob.glob(imagesPath + "*.jpg")
    index = 7900001
    data = read_json("/Users/lingmou/Desktop/python-script/ALI-project/annotationJson.json")
    for item in data:
        print(index)
        shutil.copy(item["image"], imagesPath + "numbered/images/{}.jpg".format(str(index)))
        saveResultsByJson(imagesPath + "numbered/jsons/{}".format(str(index)), item)
        index += 1



def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

if __name__ == '__main__':
    main()