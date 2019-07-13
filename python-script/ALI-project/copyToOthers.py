import pandas as pd
import shutil
import glob
import os
from tqdm import tqdm

base_path = "/data/dongwei/"

def main():
    count = 0
    dy = pd.read_csv("ai2others.csv")
    pf = pd.DataFrame(dy)
    # print(len(pf), pf["others"][0])
    smallImages = glob.glob(base_path + "dwclassImages-2/*/*.jpg")
    for image in tqdm(smallImages):
        for i in range(len(pf)):
            if pf["sku_name"][i] == image.split("/")[-2]:
                mkdir(base_path + "bin/alToOthers/target/{}".format(pf["others"][i]))
                shutil.copy(image, base_path + "bin/alToOthers/target/{}/{}".format(pf["others"][i], image.split("/")[-1]))
                if count % 100 == 0:
                    print("find:", count)
                count += 1
                break
    print("共找到:", count)

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