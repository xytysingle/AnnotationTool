import requests
import csv
import json




def save_data(sku):
    print(sku)
    # pf = pd.DataFrame(dataList, columns=["old", "new"])
    # pf.to_csv("indexData.csv", index=False, encoding="utf-8")
    out = open('duitousku.csv', 'a', newline='', encoding="utf-8")
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow([sku])


if __name__ == '__main__':
    response = requests.get("http://annotation.lingmou.ai:8000/index.php/skus/list?type=%20+%2022&token=").text
    print(response)
    response = json.loads(response)
    for item in response["data"]["skus"]:
        save_data(item["sku_name"])
