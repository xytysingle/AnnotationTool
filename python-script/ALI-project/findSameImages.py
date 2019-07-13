import hashlib
from PIL import Image
import glob
from tqdm import tqdm
import json

# imagesPath = "/Users/lingmou/Desktop/ali/aImages/"
imagesPath = "/Users/lingmou/Desktop/陕西厂/sx/"
list_json = []

def main():
    md5_set = set()
    files_dict = {}
    files = glob.glob(imagesPath + "*/*.jpg")
    for f in tqdm(files):
        im = Image.open(f)
        md5 = hashlib.md5(im.tobytes()).hexdigest()
        files_dict.setdefault(md5, []).append(f)
        if md5 in md5_set:
            print('\n' + '=' * 20 + md5 + '=' * 20)
            for item in list_json:
                if item["md5"] == md5:
                    templist = []
                    for fd in files_dict[md5]:
                        print(fd)
                        templist.append(fd)
                    item["imagespath"] = templist





            print('Remove {}.'.format(f))
        else:
            md5_set.add(md5)
            list_json.append({
                "md5": md5,
                "imagespath":[f]
            })
    saveResultsByJson("same-image", list_json)

def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

if __name__ == '__main__':
    main()