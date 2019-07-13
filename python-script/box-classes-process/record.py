import glob
import json
from tqdm import tqdm

# base_path = "/Users/lingmou/Desktop/box-classes/"
base_path = "/data/dongwei/"

def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def main():
    boxImagesPath = []
    boxclassImages = glob.glob(base_path + "dwclassImages-5/*/*.jpg")
    for boxclassImage in tqdm(boxclassImages):
        boxImagesPath.append(boxclassImage)
    saveResultsByJson(base_path + "boxImagesPath-all", boxImagesPath)

if __name__ == '__main__':
    main()
