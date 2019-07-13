import glob
import shutil
import os


BasePath = "/Users/lingmou/Desktop/python-script/filterClassimages/classImages/"
TargetPath = "/Users/lingmou/Desktop/python-script/filterClassimages/target/"
startIndex = 6000662
endIndex = 6000882

def filterClassImages(imagePath):
    # 814044_1480_1813_1552_2060_0.jpg
    orginImageIndex = imagePath.split("/")[-1].split("_")[0]
    for index in range(startIndex, endIndex + 1):
        if int(orginImageIndex) == index:
            # print(imagePath.split("/")[-2])
            mkdir(TargetPath + imagePath.split("/")[-2])
            shutil.move(imagePath, TargetPath + imagePath.split("/")[-2] + "/" + imagePath.split("/")[-1])
            break


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print("{}创建成功".format(path))
        return True
    else:
        # print("{}已存在".format(path))
        return False


def main():

    all_images = glob.glob(BasePath + "*/*.jpg")
    for item in all_images:
        # print(item)
        filterClassImages(item)



if __name__ == '__main__':

    main()