import glob
import shutil
import os

BasePath = "/Users/lingmou/Desktop/clusterData/"

def main():
    smallImages = glob.glob(BasePath + "waitforNext/*/*.jpg")
    for smallImage in smallImages:
        print(smallImage)
        dirName = smallImage.split("/")[-2]
        image = smallImage.split("/")[-1]
        mkdir(BasePath + "processed/clustered_{}".format(dirName))
        shutil.copy(smallImage, BasePath + "processed/clustered_{}/".format(dirName) + image)




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


if __name__ == '__main__':
    main()