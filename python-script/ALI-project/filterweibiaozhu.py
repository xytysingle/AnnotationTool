import shutil
import glob
import json
from tqdm import tqdm

BasePath = "/Users/lingmou/Desktop/ali/"
imgList = [
    "1100158-1100284",
    "1300094-1300125",
    "1500094-1500156",
    "1600214-1600344",
    "2300181-2300276",
    "1800938-1801363",
    "1900196-1900313",
    "2101301-2101583"
]

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

def main():
    jsons = glob.glob(BasePath + "numbered/jsons/*.json")
    images = glob.glob(BasePath + "numbered/images/*.jpg")
    for json in tqdm(jsons):
        if len(read_json(json)["bboxes"]) == 0:
            shutil.move(json, BasePath + "numbered/jsonmove/{}".format(json.split("/")[-1]))
            for image in images:
                if image.split("/")[-1].split(".")[0] == json.split("/")[-1].split(".")[0]:
                    shutil.move(image, BasePath + "numbered/imagemove/{}".format(image.split("/")[-1]))


if __name__ == '__main__':
    main()