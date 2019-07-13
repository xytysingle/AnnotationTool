import glob
import shutil


BasePath = "/Users/lingmou/Desktop/shujujiucuo/"

def main(index):
    jsonResults = glob.glob(BasePath + "results/*.json")
    images = glob.glob(BasePath + "images/*.jpg")
    for image in images:
        shutil.copy(image, BasePath + "numbered/images/{}.jpg".format(index))
        print("{}.jpg获取成功！".format(index))
        findResultsJson(index, image.split("/")[-1].split(".")[0], jsonResults)
        index += 1




def findResultsJson(index, name, jsonResults):
    # print(name)
    for json in jsonResults:
        if json.split("/")[-1].split(".")[0] == name:
            shutil.copy(json, BasePath + "numbered/results/{}.json".format(index))
            print("{}.json获取成功！".format(index))
            break


if __name__ == '__main__':
    start_index = 6006251
    main(start_index)