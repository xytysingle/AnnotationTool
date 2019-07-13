import glob
import shutil
import json
from tqdm import tqdm


BasePath = "/Users/lingmou/Desktop/ali/"

def main():
    # images = glob.glob(imagesPath + "*.jpg")
    indexChangeRecord = []
    index = 7900001
    jsons = glob.glob(BasePath + "oldJsons/*.json")
    images = glob.glob(BasePath + "aImages/*.jpg")
    for json in tqdm(jsons):
        for image in images:
            if image.split("/")[-1].split(".")[0] == json.split("/")[-1].split(".")[0]:
                indexObject = {
                    "old": image.split("/")[-1].split(".")[0],
                    "new": index
                }
                indexChangeRecord.append(indexObject)
                shutil.copy(image, BasePath + "target/images/{}.jpg".format(str(index)))
                shutil.copy(json, BasePath + "target/jsons/{}.json".format(str(index)))
                index += 1

    saveResultsByJson("indexChangeRecord", indexChangeRecord)
def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

if __name__ == '__main__':
    main()