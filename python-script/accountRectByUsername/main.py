import requests
import json
import csv
from tqdm import tqdm

def getLabels(index):
    global computerNum
    anno_url = 'http://annotation.lingmou.ai:8000/index.php/annotation/view?image={}'.format(index)
    # anno_url = 'http://192.168.3.4:8000/index.php/annotation/view?image={}'.format(index)
    try:
        response = requests.get(anno_url).text
        # print(response)

        response = json.loads(response)
    except:
        print("没有标注结果")

    # print(response)

    # print(response)
    try:
        imgCountsByUserName(response)
        bboxes = response["bboxes"]

        label_list = []
        for item in bboxes:

            if item.__contains__("username") == False or item["username"] == "":
                computerNum += 1

            else:
                flag = 0
                try:
                    # print(item["username"])
                    for label_item in label_list:
                        if item["username"] == label_item["username"]:
                            label_item["count"] += 1
                            flag = 1
                        # elif item["username"] == "":
                        #     # label_item["username"]
                        #     label_item["count"] += 1
                        #     flag = 1

                    if(flag == 0):
                        label_list.append({
                            "username": item["username"],
                            "count": 1
                        })
                except Exception as e:
                    print("该框没有用户名：", e)
                # computerNum += 1
        print(index, label_list)
        all_count(label_list)
    except Exception as e:
        print("没有标注结果:",e)
def write_csv(all_list, filename):
    headers = ['username', 'count']

    with open('{}.csv'.format(filename), 'w', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        for row in all_list:
            # print(row)
            writer.writerow(row)

def all_count(label_list):
    global all_list
    for label_item in label_list:
        flag = 0
        for all_item in all_list:
            if all_item["username"] == label_item["username"]:
                all_item["count"] += label_item["count"]
                flag = 1

        if (flag == 0):
            all_list.append({
                "username": label_item["username"],
                "count": label_item["count"]
            })
    print(all_list)


def imgCountsByUserName(response):
    global page_list
    flag = 0
    for page_item in page_list:
        if page_item["username"] == response["username"]:
            page_item["count"] += 1
            flag = 1
    if flag == 0:
        page_list.append(
            {
                "username": response["username"],
                "count": 1
            }
        )



if __name__ == "__main__":
    computerNum = 0
    all_list = []
    page_list = []
    for i in tqdm(range(7507001, 7509084)):
        getLabels(str(i))
    all_list.append({
        "username": "computer",
        "count": computerNum
    })
    write_csv(all_list, "labelRectCounts")
    write_csv(page_list, "imgCounts")

