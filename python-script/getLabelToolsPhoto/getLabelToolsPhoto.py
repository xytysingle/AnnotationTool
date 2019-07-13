import requests
import pandas as pd


# http://annotation.lingmou.ai:8000/index.php/image/view?file=9102365.jpg
# BASEURL = 'http://annotation.lingmou.ai:8000/index.php/image/view?file='
BASEURL = 'http://192.168.3.4:8000/index.php/image/view?file='
TargetPath = "/Users/lingmou/Desktop/ali/aImages/"

def getImage(index):
    # BASEURL = 'http://annotation.lingmou.ai:8000/index.php/image/view?file='
    response = requests.get(BASEURL + index + '.jpg')
    with open(TargetPath + '{}.jpg'.format(index), 'wb') as f:
        f.write(response.content)

def readCsvFile():
    csv_file = pd.read_csv('/Users/lingmou/Desktop/python-script/getLabelToolsPhoto/sourceFiles/duitouxh20190217.csv')
    print(csv_file.shape)
    # imgIndexs = csv_file
    # print(csv_file.values[0][0])
    return csv_file

# indexs = readCsvFile()


if __name__ == '__main__':

    for i in range(2702278, 2705628):
        getImage(str(i))
        print('正在获取第{}张'.format(i))