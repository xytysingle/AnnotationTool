import requests
import glob
import os
import json

# 获取小图分类及原图，生成写入数据库的结果
def getClassImages(classImages_Path):
    global reults_list
    all_classimages = glob.glob(classImages_Path + '*/*.jpg')
    for item in all_classimages:
        path = os.path.split(item)
        className = path[0].split('/')[-1]
        results = path[1].split('_')
        photoIndex = results[0]
        x1 = results[1]
        x2 = results[3]
        y1 = results[2]
        y2 = results[4]

        flag = False
        for result in reults_list:

            if result['image'] == photoIndex:
                flag = True
                result['bboxes'].append(
                    {
                       "className": className,
                        "x1": x1,
                        "x2": x2,
                        "y1": y1,
                        "y2": y2
                    }
                )
                break
        if flag == False:
            reults_list.append(
                {
                    "image": photoIndex,
                    "bboxes": [
                        {
                            "className": className,
                            "x1": x1,
                            "x2": x2,
                            "y1": y1,
                            "y2": y2
                        }
                    ]
                }

            )

    # print(json.dumps(reults_list))
    for item in reults_list:
        print(item['image'])









if __name__ =='__main__':
    classImages_Path = './SourceFolder/classimages/'
    OrginPhotos_Path = './SourceFolder/photos/'
    reults_list = []
    getClassImages(classImages_Path)
