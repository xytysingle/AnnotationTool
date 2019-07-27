import json
import csv
import re

def processJson():
    file_path = "/Users/lingmou/Desktop/python-script/trax-selenium/products.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        categories = json.loads(f.read())["categories"]
        print(len(categories))
        for categorie in categories:
            print(len(categorie["brands"]))
            brands = categorie["brands"]
            for brand in brands:
                brand_name = brand["name"]
                products = brand["products"]
                for product in products:
                    id =  product["id"]
                    traxName =  product["name"]
                    # result = re.findall("https://traxus.s3.amazonaws.com/swirecn-prod", product["imagePath"])

                    results = product["imagePath"].split('/')
                    print(results)

                    smallImgUrl = "https://services.traxretail.com/images/traxoregon/swirecn/{}/{}/small".format(
                            results[4], results[5])


                    save_data(id, traxName, brand_name)
    # nameList = []
    # for item in categories:
    #     # sku = {
    #     #     "id": item["id"],
    #     #     "traxName": item["localName"],
    #     #     "imageUrl": item["images"][0]["path"]
    #     # }
    #     save_data(item["id"], item["localName"], item["images"][0]["path"])
    #     # nameList.append(sku)

def save_data(id, traxName, brand_name):
    # print(imgIndex, advantage, samll)
    # pf = pd.DataFrame(dataList, columns=["old", "new"])
    # pf.to_csv("indexData.csv", index=False, encoding="utf-8")
    out = open('traxProduct.csv', 'a', newline='', encoding='utf-8')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow([id, traxName, brand_name])




if __name__ == "__main__":
    processJson()