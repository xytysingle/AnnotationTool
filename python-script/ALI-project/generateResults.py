import glob
import json
import shutil
from tqdm import tqdm

# Base_Path = "/Users/lingmou/Desktop/cleanData/"
Base_Path = "/data/work/www/snapshot_partner/api/web/baiwei/"
# "/data/work/www/snapshot_partner/api/web/baiwei/after_cls/10^ALLEGRA钻典天然矿泉水瓶装330毫升"

def generateResults():
    classimages = glob.glob(Base_Path  + "after_cls/*/*.jpg")
    for classimage in tqdm(classimages):
        try:
            flag = 0
            classname = classimage.split("/")[-2].split("^")[1]
            results = classimage.split("/")[-1].split("_")

            # "0.914022445679_2704995_514_1469_611_1787_0.jpg"

            # score = float(results[0])
            original_img_name = results[0]
            x1 = int(results[1])
            y1 = int(results[2])
            x2 = int(results[3])
            y2 = int(results[4])
            for item in all_data:
                if item["image"] == original_img_name:
                    flag = 1
                    item["bboxes"].append(
                        {
                            "className": classname,
                            # "className": "其他",
                            "x1": x1,
                            "x2": x2,
                            "y1": y1,
                            "y2": y2,
                            "score": 1.00,
                            "truncated": 0,
                            "username": "lm"

                        }
                    )
            if flag == 0:
                all_data.append(
                    {
                        "image": original_img_name,
                        "bboxes": [
                            {
                                "className": classname,
                                # "className": "其他",
                                "x1": x1,
                                "x2": x2,
                                "y1": y1,
                                "y2": y2,
                                "score": 1.00,
                                "truncated": 0,
                                "username": "lm"
                            }
                        ]
                    }
                )

            # if len(results) == 9:
            #     original_img_name = "{}_{}_{}_{}_{}".format(results[0], results[1], results[2], results[3], results[4])
            #     x1 = results[5]
            #     y1 = results[6]
            #     x2 = results[7]
            #     if results[8].__contains__("("):
            #         y2 = results[8].split("(")[0]
            #         score = float(results[8].split("(")[1].split(")")[0])
            #     else:
            #         y2 = results[8].split(".")[0]
            #         score = 0.901
            #
            #     for item in all_data:
            #         if item["image"] == original_img_name:
            #             flag = 1
            #             item["bboxes"].append(
            #                 {
            #                     "className": classname,
            #                     "x1": x1,
            #                     "x2": x2,
            #                     "y1": y1,
            #                     "y2": y2,
            #                     "score": score,
            #                     "truncated": 0
            #
            #                 }
            #             )
            #     if flag == 0:
            #         all_data.append(
            #             {
            #                 "image": original_img_name,
            #                 "bboxes": [
            #                     {
            #                         "className": classname,
            #                         "x1": x1,
            #                         "x2": x2,
            #                         "y1": y1,
            #                         "y2": y2,
            #                         "score": score,
            #                         "truncated": 0
            #                     }
            #                 ]
            #             }
            #         )
            #
            #     print(classimage.split("/")[-2])
            # elif len(results) == 7:
            #     original_img_name = "{}_{}_{}".format(results[0], results[1], results[2])
            #     print(results[6])
            #     x1 = results[3]
            #     y1 = results[4]
            #     x2 = results[5]
            #
            #     if results[6].__contains__("("):
            #         y2 = results[6].split("(")[0]
            #         score = float(results[6].split("(")[1].split(")")[0])
            #     else:
            #         y2 = results[6].split(".")[0]
            #         score = 0.901
            #
            #     for item in all_data:
            #         if item["image"] == original_img_name:
            #             flag = 1
            #             item["bboxes"].append(
            #                 {
            #                     "className": classname,
            #                     "x1": x1,
            #                     "x2": x2,
            #                     "y1": y1,
            #                     "y2": y2,
            #                     "score": score,
            #                     "truncated": 0
            #
            #                 }
            #             )
            #     if flag == 0:
            #             all_data.append(
            #                 {
            #                     "image": original_img_name,
            #                     "bboxes":[
            #                         {
            #                             "className": classname,
            #                             "x1": x1,
            #                             "x2": x2,
            #                             "y1": y1,
            #                             "y2": y2,
            #                             "score": score,
            #                             "truncated": 0
            #                         }
            #                     ]
            #                 }
            #             )
            #
            #     print(classimage.split("/")[-2])
        except Exception as e:
            print("格式不对：", e)



def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)




if __name__ == '__main__':
    all_data = []
    # 106246
    generateResults()

    saveResultsByJson("/data/dongwei/modeldata/Beers/resultsJson/results", all_data)