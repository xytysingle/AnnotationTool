import glob
import json
import shutil
from tqdm import tqdm

Base_Path = "/Users/lingmou/Desktop/ali/"

def generateResults():
    classimages = glob.glob(Base_Path  + "ceshiji/class_images/*/*.jpg")
    for classimage in tqdm(classimages):
        try:
            flag = 0
            classname = classimage.split("/")[-2]
            results = classimage.split("/")[-1].split("_")

            # "0.914022445679_2704995_514_1469_611_1787_0.jpg"

            score = float(results[0])
            original_img_name = results[1]
            x1 = int(results[2])
            y1 = int(results[3])
            x2 = int(results[4])
            y2 = int(results[5])
            for item in all_data:
                if item["image"] == original_img_name:
                    flag = 1
                    item["bboxes"].append(
                        {
                            "className": classname,
                            "x1": x1,
                            "x2": x2,
                            "y1": y1,
                            "y2": y2,
                            "score": score,
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
                                "x1": x1,
                                "x2": x2,
                                "y1": y1,
                                "y2": y2,
                                "score": score,
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

    saveResultsByJson(Base_Path + "ceshiji/resultsJson/results", all_data)