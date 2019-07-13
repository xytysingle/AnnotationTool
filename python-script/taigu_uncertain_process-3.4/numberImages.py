#-*- coding:utf-8 -*-
import json
import shutil
import glob



def numberImages():
    Base_Path = "./target/"
    start_index = int(read_text())
    imgIndexOldAndNew = []
    # global start_index
    images = glob.glob(Base_Path + "images/*.jpg")
    results_json = read_json(Base_Path + "resultsJson/results.json")
    for item in results_json:
        for path in images:
            if path.split("/")[-1] == str(item["image"]) + ".jpg":
                shutil.copy(path, Base_Path + "numbered/{}.jpg".format(start_index))
                imgIndexOldAndNew.append(
                    {
                        "oldIndex": item["image"],
                        "newIndex": start_index
                    }
                )
                item["image"] = start_index
                print(start_index)
                copyImageToimages(start_index)
                start_index += 1

    write_text(start_index)

    saveResultsByJson(Base_Path + "resultsJson/numbered_results.json", results_json)

    saveResultsByJson(Base_Path + "resultsJson/imgIndexOldAndNew.json", imgIndexOldAndNew)




def saveResultsByJson(filename, data):
    with open("{}".format(filename), 'w', encoding='utf-8') as json_file: #, encoding='utf-8'
        json.dump(data, json_file, ensure_ascii=False) #


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data


def read_text():
    with open("index.txt", "r") as f:
        index = f.read()
    return index

def write_text(index):
    with open("index.txt", "w") as f:
        f.write(str(index))

def copyImageToimages(index):
    shutil.copy("target/numbered/{}.jpg".format(index), "/data/datasets/coca/images/{}.jpg".format(index))

if __name__ == '__main__':
    numberImages()

