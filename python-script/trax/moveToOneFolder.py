import glob
import shutil
from tqdm import tqdm

imagesPath = "/Users/lingmou/Desktop/traxResults/"

images = glob.glob(imagesPath + "OrginalImages/20190523/*/*.jpeg")

# index = 2705230
for image in tqdm(images):
    # print(index)
    shutil.move(image, imagesPath + "one/20190523/{}".format(image.split("/")[-1]))
    # index += 1