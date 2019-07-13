import glob
from tqdm import tqdm
import csv
import pandas as pd

basePath = "/Users/lingmou/Desktop/ali/"


def saveToExcel():
    allClasses = glob.glob(basePath + "0527/*")
    formdata = {}
    formdata["分类"] = []
    for item in tqdm(allClasses):
        formdata["分类"].append(item.split("/")[-1])
    writer = pd.ExcelWriter('ai_test2.xlsx')
    df1 = pd.DataFrame(data=formdata)
    df1.to_excel(writer, sheet_name='{}'.format("分类"))



    writer.save()

if __name__ == '__main__':
    saveToExcel()
