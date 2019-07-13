import json

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data


def main():
    datas = read_json("/Users/lingmou/Desktop/python-script/ALI-project/imagesJson.json")
    for data in datas:
        print(data)
        if len(data["imagespath"]) > 1:
            print(data)


if __name__ == '__main__':
    main()