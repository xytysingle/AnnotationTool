import numpy as np
import cv2

# img = np.zeros((320, 320, 3), np.uint8)  # 生成一个空灰度图像
# print
# img.shape  # 输出：(480, 480, 3)

# point_size = 1
# point_color = (0, 0, 255)  # BGR
# thickness = 4  # 可以为 0 、4、8
#
# # 要画的点的坐标
# points_list = [(160, 160), (136, 160), (150, 200), (200, 180), (120, 150), (145, 180)]
#
# for point in points_list:
#     cv.circle(img, point, point_size, point_color, thickness)
#
# # 画圆，圆心为：(160, 160)，半径为：60，颜色为：point_color，实心线
# cv.circle(img, (160, 160), 60, point_color, 0)
#
# cv.namedWindow("image")
# cv.imshow('image', img)
# cv.waitKey(10000)  # 显示 10000 ms 即 10s 后消失
# cv.destroyAllWindows()
img = cv2.imread("/Users/lingmou/Desktop/python-script/20ImageRecongnize/resource/pjImages/2.jpg")
print(img.shape)
h = img.shape[0]
w = img.shape[1]
print(h,w)

y = h * (0.37637897469176 + 0.33030499675535) / 2
x = w * (0.70223253116845 + 0.68164685416063) / 2

print(int(x),int(y))