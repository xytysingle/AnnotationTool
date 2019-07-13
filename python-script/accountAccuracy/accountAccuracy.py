import shutil
import glob
from tqdm import tqdm

basePath = "/Users/lingmou/Desktop/ali/"

def main():
    yuce = glob.glob(basePath + "accountAccuracy/class_images/*/*.jpg")
    zhenshi = glob.glob(basePath + "accountAccuracy/10/*/*.jpg")
    allCount = len(yuce)
    rightCount = 0
    for ycitem in tqdm(yuce):
        for zsitem in zhenshi:
            res = ycitem.split("/")[-1].split("_")
            name = "{}_{}_{}_{}_{}_{}".format(res[1], res[2], res[3], res[4], res[5], res[6])
            # print(ycitem.split("/")[-1], zsitem.split("/")[-1], ycitem.split("/")[-2], zsitem.split("/")[-2])
            # print(name, zsitem.split("/")[-1])
            if name == zsitem.split("/")[-1]:
                if ycitem.split("/")[-2] == zsitem.split("/")[-2]:
                    rightCount += 1
                    print(rightCount)
                    break
    print(allCount, rightCount, rightCount / allCount)


if __name__ == '__main__':
    main()