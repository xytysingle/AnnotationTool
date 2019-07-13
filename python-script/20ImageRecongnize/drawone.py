import cv2
import json

# imgIndex = "6004073"
point_size = 10
point_color = (48,48,255)
thickness = -1

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

        return input_data

def drawOneCircle(point):
    pass

def main(imgIndex):
    # datas = read_json("/Users/lingmou/Desktop/python-script/20ImageRecongnize/target/jsons/{}.json".format(imgIndex))
    img = cv2.imread("/Users/lingmou/Desktop/python-script/20ImageRecongnize/resource/pjImages/1.jpg")
    # for data in datas:
    #     for item in data:
    #         point = (item["x"], item["y"])
    cv2.circle(img, (2386, 1088), point_size, point_color, thickness)
    cv2.imwrite("/Users/lingmou/Desktop/python-script/20ImageRecongnize/target/images/{}.jpg".format(imgIndex), img)


if __name__ == '__main__':
    bg = [
        6004073,
        6004074,
        6004077,
        6004080,  # 补充一个空缺位
        6004083,
        6004086,
        6004102,
        6004104,  # 补两个空缺位
        6004106,  # 补两个空缺位
        6004111

    ]
    hj = [
        6004075,
        6004078,
        6004084,  # 两层罐装的需要调整
        6004089,
        6004092,  # 盒装罐装需要调整
        6004094,
        6004097,  # 两层罐装需要修改
        6004108,  # 两层罐装需要修改
        6004116,
        6004132

    ]
    # for imgIndex in hj:
    main(str(1))