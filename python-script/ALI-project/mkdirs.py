import os
import csv




def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print("{}创建成功".format(path))
        return True
    else:
        # print("{}已存在".format(path))
        return False

def read_csv(path):
    csv_file = csv.reader(open(path, "r", encoding='utf-8'))
    return csv_file

def main():

    dirNames = read_csv('/Users/lingmou/Desktop/ali/0515sku.csv')

    for dirname in dirNames:
        mkdir("/Users/lingmou/Desktop/ali/newdirs/{}".format(dirname[0]))
        # print(dirname[0])

if __name__ == '__main__':
    main()