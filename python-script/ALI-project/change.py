import json
import glob
from tqdm import tqdm


BasePath = "/Users/lingmou/Desktop/ali/"

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data


def saveResultsByJson(filename, data):
    with open("{}".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def main():
    jsons = glob.glob(BasePath + "test_images_jsons/*.json")

    for json in tqdm(jsons):
        data = read_json(json)
        # print(data)
        saveResultsByJson(BasePath + "ali_test_images_jsons/{}".format(json.split("/")[-1]), data)


if __name__ == '__main__':
    main()