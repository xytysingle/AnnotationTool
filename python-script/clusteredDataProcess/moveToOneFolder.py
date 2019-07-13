import glob
import shutil
from tqdm import tqdm

imagesPath = "/Users/lingmou/Desktop/clusterData/"

images = glob.glob(imagesPath + "clusteredImages/*/*.jpg")

# index = 2705230
for image in tqdm(images):
    # print(index)
    shutil.move(image, imagesPath + "waitForClustered/{}".format(image.split("/")[-1]))

# Combo_Coca-Cola Can 330 ml_Plastic Film 6 Can
    # index += 1