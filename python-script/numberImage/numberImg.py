import glob
import shutil
from tqdm import tqdm

path = "/Users/lingmou/Desktop/traxResults/danping/20190412"

def main():
    startIndex = 8039548
    images = glob.glob(path + "/*.jpg")
    for image in tqdm(images):
        shutil.move(image, "/Users/lingmou/Desktop/numbered/{}.jpg".format(str(startIndex)))
        startIndex += 1

if __name__ == '__main__':
    main()