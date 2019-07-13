import glob
import cv2
from tqdm import tqdm

base_path ="/Users/lingmou/Desktop/gouzao/"

images = glob.glob(base_path + "imgs/*.jpg")
print(images)

for img in tqdm(images):
    _img = cv2.imread(img)
    cv2.imwrite(base_path + "target/{}".format(img.split("/")[-1]), _img)

