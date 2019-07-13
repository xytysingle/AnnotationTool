import glob
import json
import shutil

# Base_Path = "/Users/lingmou/Desktop/python-script/taigu_uncertain_process/target/"
Base_Path = "/data/dongwei/taigu_uncertain_process/target/"

def generateResults():
    classimages = glob.glob(Base_Path + "class_images/" + "*/*.jpg")
    for classimage in classimages:
        try:
            flag = 0
            classname = classimage.split("/")[-2].split("^")[1]
            results = classimage.split("/")[-1].split("_")
            # DETECTRON_IMAGE_0c4ec9a5-2e7d-48b8-a357-cab3361179fa.jpg
            # DETECTRON_IMAGE_0c4ec9a5-2e7d-48b8-a357-cab3361179fa_790_539_857_713(0.929259359837).jpg
            # DETECTRON_IMAGE_DEMO_IMAGE_f9b3f312dabfeb131e094ee8f094f9d5.jpg
            # DETECTRON_IMAGE_DEMO_IMAGE_f9b3f312dabfeb131e094ee8f094f9d5_1880_3328_2101_3895(0.769153892994).jpg
            # DETECTRON_IMAGE_SWIRE_SNAPSHOT_IMAGE5cc12c3adec3d8.38549025.jpg.jpg
            # DETECTRON_IMAGE_SWIRE_SNAPSHOT_IMAGE5cc12c3adec3d8.38549025.jpg_1071_654_1318_921(0.537285864353).jpg
            if len(results) == 9:
                original_img_name = "{}_{}_{}_{}_{}".format(results[0], results[1], results[2], results[3], results[4])
                x1 = results[5]
                y1 = results[6]
                x2 = results[7]
                if results[8].__contains__("("):
                    y2 = results[8].split("(")[0]
                    score = float(results[8].split("(")[1].split(")")[0])
                else:
                    y2 = results[8].split(".")[0]
                    score = 0.901

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
                                "truncated": 0

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
                                    "truncated": 0
                                }
                            ]
                        }
                    )

                print(classimage.split("/")[-2])
            elif len(results) == 7:
                original_img_name = "{}_{}_{}".format(results[0], results[1], results[2])
                print(results[6])
                x1 = results[3]
                y1 = results[4]
                x2 = results[5]

                if results[6].__contains__("("):
                    y2 = results[6].split("(")[0]
                    score = float(results[6].split("(")[1].split(")")[0])
                else:
                    y2 = results[6].split(".")[0]
                    score = 0.901

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
                                "truncated": 0

                            }
                        )
                if flag == 0:
                        all_data.append(
                            {
                                "image": original_img_name,
                                "bboxes":[
                                    {
                                        "className": classname,
                                        "x1": x1,
                                        "x2": x2,
                                        "y1": y1,
                                        "y2": y2,
                                        "score": score,
                                        "truncated": 0
                                    }
                                ]
                            }
                        )

                print(classimage.split("/")[-2])
        except Exception as e:
            print("格式不对：", e)



def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)




if __name__ == '__main__':
    all_data = []

    generateResults()

    saveResultsByJson(Base_Path + "resultsJson/results", all_data)