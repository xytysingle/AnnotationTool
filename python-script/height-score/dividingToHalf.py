import cv2
import glob
import os

Base_Path = "/Users/lingmou/Desktop/halfImages/"

images = glob.glob(Base_Path + "sourceImages/*/*.jpg")


def main():
    # for image in images:
    image = Base_Path + "sourceImages/Watsons屈臣氏饮用水瓶装4500毫升/8034148_1518_1972_1697_2362_0.jpg"
    img = cv2.imread(image)
    imgH = img.shape[0]
    imgW = img.shape[1]

    crop_imgUp = img[0:int(imgH/2), 0:int(imgW)]
    crop_imgDown = img[int(imgH/2):imgH, 0:int(imgW)]

    mkdir(Base_Path + "targetImages/{}".format(image.split("/")[-2]))
    cv2.imwrite(Base_Path + "targetImages/{}/{}_up.jpg".format(image.split("/")[-2], image.split("/")[-1].split(".")[0]), crop_imgUp)
    cv2.imwrite(Base_Path + "targetImages/{}/{}_down.jpg".format(image.split("/")[-2], image.split("/")[-1].split(".")[0]), crop_imgDown)


    print(imgH, imgW )



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