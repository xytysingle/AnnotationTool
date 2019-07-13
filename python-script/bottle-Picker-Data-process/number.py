import csv
import glob
import shutil


def read_csv(path):
    csv_file = csv.reader(open(path, "r", encoding='utf-8'))
    return csv_file


def main():
    global start_index
    target_json = []
    target = []
    targets = read_csv("target.csv")

    for item in targets:
        target.append(item[0])


    imagesList = glob.glob("/Users/lingmou/Desktop/traxResults/danping/20190410/*.jpg")
    jsonsList = glob.glob("/Users/lingmou/Desktop/bottlepicker/20190410json_1/*.json")
    for item in target:
        print(item)
        for image in imagesList:
            if item.split("/")[-1].split(".")[0] == image.split("/")[-1].split(".")[0]:
                shutil.copy(image, "/Users/lingmou/Desktop/bottlepicker/numbered/images/{}.jpg".format(str(start_index)))

        for json in jsonsList:
            if item.split("/")[-1].split(".")[0] == json.split("/")[-1].split(".")[0]:
                shutil.copy(json, "/Users/lingmou/Desktop/bottlepicker/numbered/json/{}.json".format(str(start_index)))
        print(start_index)
        start_index += 1






if __name__ == '__main__':
    start_index = 4000001
    main()