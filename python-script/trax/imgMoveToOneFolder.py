import os
import shutil
import glob
from tqdm import tqdm

BasePath = "/Users/lingmou/Desktop/traxResults/"

def main():

    imgPath = glob.glob(BasePath + "/boxes/*/*.jpg")

    for img in tqdm(imgPath):
        shutil.copy(img, BasePath + "/one/{}".format(img.split("/")[-1]))


if __name__ == '__main__':
    main()