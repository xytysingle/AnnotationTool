import cv2
import glob
import shutil
from tqdm import tqdm


# basePath = "/Users/lingmou/Desktop/clusterData/"
basePath = "/Users/lingmou/Desktop/ali/"

def main():
    images = glob.glob(basePath + "moveToOne/target/*/*.jpg")
    for image in tqdm(images):
        img = cv2.imread(image)
        imgShape = img.shape
        # print(imgShape[0],imgShape[1])
        if imgShape[0] <= 20 or imgShape[1] <= 20:
            shutil.move(image, basePath + "error/{}".format(image.split("/")[-1]))

if __name__ == '__main__':
    main()