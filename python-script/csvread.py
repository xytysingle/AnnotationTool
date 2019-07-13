import csv
import urllib.request

csv_file = csv.reader(open('/Users/lingmou/Desktop/mars1129.csv', 'r'))

def get_images(img_url):
    image_name = img_url.rpartition('/')[2]
    save_path = './chunyue/{}'.format(image_name)
    urllib.request.urlretrieve(img_url, save_path)
    'http://snapshot-api-sc.lingmouai.com//uploads/pbms/20180925/107964414.jpg'

    # with open('./chunyue/{}'.format(image_name), 'wb') as f:
    #     f.write(imgage)

print(csv_file)
for line in csv_file:
    img_url = line[6]
    print(img_url)
    # print(line[6])
    # image_name = img_url.rpartition('/')[2]
    # print(image_name)
    get_images(img_url)
