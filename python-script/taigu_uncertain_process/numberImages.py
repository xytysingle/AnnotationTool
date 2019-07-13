import json
import shutil
import glob

Base_Path = "/data/dongwei/taigu_uncertain_process/target/"


def main():
    global start_index
    images = glob.glob(Base_Path + "images/*.jpg")
    results_json = read_json(Base_Path + "resultsJson/results.json")
    numbered_results = []
    for path in images:
        for item in results_json:

            if path.split("/")[-1] == str(item["image"]) + ".jpg":
                shutil.copy(path, Base_Path + "numbered/{}.jpg".format(start_index))
                imgIndexOldAndNew.append(
                    {
                        "oldIndex": item["image"],
                        "newIndex": start_index
                    }
                )
                item["image"] = start_index
                numbered_results.append(item)

                print(start_index)
                start_index += 1


    saveResultsByJson(Base_Path + "resultsJson/numbered_results", numbered_results)





def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data


if __name__ == '__main__':
    start_index = 9133980
    imgIndexOldAndNew = []
    main()
    saveResultsByJson(Base_Path + "resultsJson/imgIndexOldAndNew", imgIndexOldAndNew)
