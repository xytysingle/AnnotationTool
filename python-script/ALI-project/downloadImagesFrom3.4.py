import requests
import pandas as pd
from tqdm import tqdm

# http://annotation.lingmou.ai:8000/index.php/image/view?file=9102365.jpg
BASEURL = 'http://192.168.3.4/index.php/image/view?file='


def getImage(index):
    BASEURL = 'http://192.168.3.4:8000/index.php/image/view?file='
    response = requests.get(BASEURL + index + '.jpg')
    with open('/Users/lingmou/Desktop/pricetag/images/{}.jpg'.format(index), 'wb') as f:
        f.write(response.content)

def readCsvFile():
    csv_file = pd.read_csv('/Users/lingmou/Desktop/python-script/getLabelToolsPhoto/sourceFiles/duitouxh20190217.csv')
    print(csv_file.shape)
    # imgIndexs = csv_file
    # print(csv_file.values[0][0])
    return csv_file

# indexs = readCsvFile()

def main():
    # imagesList = [
    #     "1100158-1100284",
    #     "1300094-1300125",
    #     "1500094-1500156",
    #     "1600214-1600344",
    #     "2300181-2300276",
    #     "1800938-1801363",
    #     "1900196-1900313",
    #     "2101301-2101583",
    #     "1000040-1000064",
    #     "1200783-1201138",
    #     "1300082-1300093",
    #     "1400109-1400172",
    #     "2000250-2000416",
    #     "2400152-2400251"
    #
    # ]
    # imagesList2 = [
    #     "1200001-1200225"
    # ]
    # for item in imagesList:
    #
    #     startIndex = item.split("-")[0]
    #     endIndex = item.split("-")[1]
    #     print(startIndex, endIndex)
    for i in tqdm(range(7000001, 7003674)):
        getImage(str(i))
        # print('正在获取第{}张'.format(i))

if __name__ == '__main__':
    main()

    # for i in range(746143, 746262):
    #     getImage(str(i))
    #     print('正在获取第{}张'.format(i))