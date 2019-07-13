import glob
import shutil
import json
import os
from tqdm import tqdm


base_path = "/Users/lingmou/Desktop/box-classes/"

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def main():
    count = 0
    nowClasses = glob.glob(base_path + "box/train/其他/*.jpg")
    targetClasses = read_json(base_path + "boxImagesPath-all.json")
    for item in  tqdm(nowClasses):
        for target in targetClasses:
            if item.split("/")[-1] == target.split("/")[-1]:
                count += 1
                mkdir(base_path + "target/{}".format(target.split("/")[-2]))
                shutil.move(item, base_path + "target/{}/{}".format(target.split("/")[-2], item.split("/")[-1]))
                break
    print(count)


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


if __name__ == '__main__':
    main()