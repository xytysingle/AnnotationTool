import os
import shutil
import glob
from tqdm import tqdm
import json


Base_Path = "/Users/lingmou/Desktop/ali/"

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

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def main():
    count = 0
    classimages = glob.glob(Base_Path + "class_images_original/*/*.jpg")
    indexDatas = read_json("/Users/lingmou/Desktop/python-script/ALI-project/indexChangeRecord.json")

    for classimage in tqdm(classimages):
        classname = classimage.split("/")[-2]
        results = classimage.split("/")[-1].split("_")

        # "0.914022445679_2704995_514_1469_611_1787_0.jpg"

        # score = results[0]
        original_img_name = results[1]
        # x1 = int(results[2])
        # y1 = int(results[3])
        # x2 = int(results[4])
        # y2 = int(results[5])
        mkdir(Base_Path + "alclassimges/" + classname)
        for index in indexDatas:
            if index["old"] == original_img_name:
                count += 1
                shutil.copy(classimage, Base_Path + "alclassimges/" + classname + "/{}_{}_{}_{}_{}_{}".format(index["new"], results[2], results[3], results[4], results[5], results[6]))
    print("总处理数：",count)
if __name__ == '__main__':
    main()