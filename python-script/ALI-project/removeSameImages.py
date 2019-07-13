import os
import json

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def main():
    data = read_json("/Users/lingmou/Desktop/python-script/ALI-project/imagesJson.json")
    for item in data:
        images = item["imagespath"]
        if len(images) == 2:
            results = images[1].split("/")
            results[5] = "aImages"
            rpath = ''
            for p in results[1:]:
                rpath = rpath + "/" + p
            os.remove(rpath)
            print("removed", rpath)

# "/Users/lingmou/Desktop/ali/aImagesyl/1700025.jpg"
if __name__ == '__main__':
    main()