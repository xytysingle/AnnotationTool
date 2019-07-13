import glob
import shutil
from tqdm import tqdm

imagesPath = "/Volumes/Samsung_T5/trax原图/"

images = glob.glob(imagesPath + "20190523/*/*.jpeg")

# index = 2705230
for image in tqdm(images):
    # print(index)
    shutil.move(image,  "/Users/lingmou/Desktop/traxResults/one/{}.jpg".format(image.split("/")[-1].split(".")[0]))
    # index += 1