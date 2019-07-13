import csv
import glob
import shutil


def read_csv(path):
    csv_file = csv.reader(open(path, "r", encoding='utf-8'))
    return csv_file


def main():
    global start_index

    imagesList = glob.glob("/Users/lingmou/Desktop/bottlepicker/yubiaozhu/detection/*.jpg")
    jsonsList = glob.glob("/Users/lingmou/Desktop/bottlepicker/yubiaozhu/detection_results/*.json")
    for image in imagesList:
        for json in jsonsList:
            if image.split("/")[-1].split(".")[0] == json.split("/")[-1].split(".")[0]:
                shutil.copy(image, "/Users/lingmou/Desktop/bottlepicker/numbered/images/{}.jpg".format(str(start_index)))
                shutil.copy(json, "/Users/lingmou/Desktop/bottlepicker/numbered/json/{}.json".format(str(start_index)))
                print(start_index)
                start_index += 1






if __name__ == '__main__':
    start_index = 7600001
    main()