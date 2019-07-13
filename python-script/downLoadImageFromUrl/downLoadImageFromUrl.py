import csv
import urllib.request
from tqdm import tqdm

csv_file = csv.reader(open('/Users/lingmou/Desktop/weita/Pic_Vitasoy_Crowdsourcing_KA_201904.csv', 'r', encoding='utf-8'))

count = 4941

def get_images(id, img_url):
    global count
    # image_name = img_url.rpartition('/')[2]
    image_name = id
    save_path = '/Users/lingmou/Desktop/weita/images/{}.jpg'.format(image_name)
    urllib.request.urlretrieve(img_url, save_path)
    # 'http://snapshot-api-sc.lingmouai.com//uploads/pbms/20180925/107964414.jpg'
    count = count + 1
    # print(count)

    # with open('./chunyue/{}'.format(image_name), 'wb') as f:
    #     f.write(imgage)

print(csv_file)
# i = 4941
i = 69847
index = 0
for line in tqdm(csv_file):
    index += 1
    # print(line)
    if index > 64906:
        i += 1
        img_url = line[2]
        print(i)
    # print(line[6])
    # image_name = img_url.rpartition('/')[2]
    # print(image_name)
        try:
            get_images(str(i), img_url)
        except:
            continue
