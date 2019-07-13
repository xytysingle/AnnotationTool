import os
import shutil
import cv2
import glob
from tqdm import tqdm


# Source_Path = "/Users/lingmou/Desktop/uncertain/"
Source_Path = "/data/datasets/uncertain/"
Target_Path = "/data/dongwei/taigu_uncertain_process/"


def main():
    images = glob.glob(Source_Path + date + "/images/*.jpg")


    # print(images)
    for item in tqdm(images):
        img = cv2.imread(item)
        img_size = img.shape
        img_name = item.split("/")[-1]
        if img_size[1] > 1000:
            # print(img_size[1])

            shutil.copy(item, Target_Path +  "target/images/" + img_name)
            # print(img_name.split(".")[0])
            getUsefulClassimages(img_name.rpartition(".")[0])
        # item.split()

    # DETECTRON_IMAGE_0c4ec9a5-2e7d-48b8-a357-cab3361179fa.jpg
    # DETECTRON_IMAGE_0c4ec9a5-2e7d-48b8-a357-cab3361179fa_790_539_857_713(0.929259359837).jpg
    # DETECTRON_IMAGE_DEMO_IMAGE_f9b3f312dabfeb131e094ee8f094f9d5.jpg
    # DETECTRON_IMAGE_DEMO_IMAGE_f9b3f312dabfeb131e094ee8f094f9d5_1880_3328_2101_3895(0.769153892994).jpg
    # DETECTRON_IMAGE_SWIRE_SNAPSHOT_IMAGE5cc12c3adec3d8.38549025.jpg.jpg
    # DETECTRON_IMAGE_SWIRE_SNAPSHOT_IMAGE5cc12c3adec3d8.38549025.jpg_1071_654_1318_921(0.537285864353).jpg
def getUsefulClassimages(img_name):
    for classimage in classimages:

        results = classimage.split("/")[-1].split("_")
        if len(results) == 9:
            original_img_name = "{}_{}_{}_{}_{}".format(results[0], results[1], results[2], results[3], results[4])
            # print(original_img_name)
            if img_name == original_img_name:
                classname = classimage.split("/")[-2]
                mkdir(Target_Path + "target/class_images/" + classname)
                shutil.copy(classimage, Target_Path + "target/class_images/" + classname + "/" + classimage.split("/")[-1])
        elif len(results) == 7:
            original_img_name = "{}_{}_{}".format(results[0], results[1], results[2])
            # print(original_img_name)
            if img_name == original_img_name:
                classname = classimage.split("/")[-2]
                mkdir(Target_Path + "target/class_images/" + classname)
                shutil.copy(classimage, Target_Path +  "target/class_images/" + classname + "/" + classimage.split("/")[-1])


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
    for i in range(20190625, 20190626):
        print(i)
        date = str(i)
        classimages = glob.glob(Source_Path + date + "/class_images/*/*.jpg")
        main()