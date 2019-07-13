
import os
import shutil
import cv2
import glob
import time
# from PIL import Image
from GenerateResults import generateResults
from numberImages import numberImages
from uploadResults import run_uploads


Source_Path = "/data/datasets/uncertain/"
now_date = time.strftime("%Y%m%d %H:%M:%S", time.localtime()).split(" ")[0]
now_date = "20190425"

date = now_date


classimages = glob.glob(Source_Path + date + "/class_images/*/*.jpg")

def main():
    images = glob.glob(Source_Path + date + "/images/*.jpg")
    record_list = read_text()

    print(images)
    for item in images:
        img = cv2.imread(item)
        # img = Image.open(item)
        img_size = img.shape
        img_name = item.split("/")[-1]
        flag = 0
        for record in record_list:
            if img_name == record:
                flag = 1
                break
        if flag == 0:
            if img_size[1] > 1500:
                # print(img_size[1])

                shutil.copy(item, "target/images/" + img_name)
                write_text(img_name)
                # print(img_name.split(".")[0])
                getUsefulClassimages(img_name.rpartition(".")[0])
        # item.split()
    # DETECTRON_IMAGE_128d33b3-f882-4117-9b0f-2052bf2671a9_233_244_285_362
    # DETECTRON_IMAGE_128d33b3-f882-4117-9b0f-2052bf2671a9
def getUsefulClassimages(img_name):
    for classimage in classimages:

        results = classimage.split("/")[-1].split("_")
        if len(results) == 9:
            original_img_name = "{}_{}_{}_{}_{}".format(results[0], results[1], results[2], results[3], results[4])
            print(original_img_name)
            if img_name == original_img_name:
                classname = classimage.split("/")[-2]
                mkdir("target/class_images/" + classname)
                shutil.copy(classimage, "target/class_images/" + classname + "/" + classimage.split("/")[-1])
        elif len(results) == 7:
            original_img_name = "{}_{}_{}".format(results[0], results[1], results[2])
            print(original_img_name)
            if img_name == original_img_name:
                classname = classimage.split("/")[-2]
                mkdir("target/class_images/" + classname)
                shutil.copy(classimage, "target/class_images/" + classname + "/" + classimage.split("/")[-1])

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        # print("{}创建成功".format(path))
        return True
    else:
        # print("{}已存在".format(path))
        return False

def read_text():
    with open("record/{}/record.txt".format(date), "r") as f:
        data_list = []
        data = f.readlines()
        for item in data:
            data_list.append(item.split("\n")[0])
    return data_list

def write_text(index):
    with open("record/{}/record.txt".format(date), "a") as f:
        f.write(index + "\n")


if __name__ == '__main__':
    if os.path.exists("target"):
        shutil.rmtree("target")
    mkdir("target/resultsJson")
    mkdir("target/numbered")
    mkdir("target/images")
    mkdir("target/class_images")
    # if os.path.exists("target/numbered"):
    #     shutil.rmtree("target/numbered")
    # if os.path.exists("target/images"):
    #     shutil.rmtree("target/images")
    # if os.path.exists("target/class_images"):
    #     shutil.rmtree("target/class_images")
    mkdir("record/{}".format(date))
    write_text("")
    main()
    generateResults()
    numberImages()
    run_uploads()