import glob
import shutil
from tqdm import tqdm


images = glob.glob("/data/tanx/project/PenBev/original_imgs_named/*.jpg")
# images = glob.glob("/data/tanx/project/PenBev/original_imgs_named/51000002.jpg")

for image in tqdm(images):
    shutil.move(image, "/data/datasets/coca/images/{}".format(image.split("/")[-1]))

