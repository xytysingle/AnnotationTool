from __future__ import division
import cv2
import os
import time
import numpy as np


save_dir = "/Users/lingmou/Desktop/python-script/img/"


def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))


# cap = cv2.VideoCapture(2)
# cap1 = cv2.VideoCapture(1)
capw = cv2.VideoCapture(0)

width = 3264
height = 2448
# cap.set(3, width)
# cap.set(4, height)
# cap1.set(3, width)
# cap1.set(4, height)
capw.set(3, width)
capw.set(4, height)
count = 0
smallSize = 5
while(1):
    # ret, frame = cap.read()
    # ret1, frame1 = cap1.read()
    retw, framew = capw.read()
    # frame = rotate_bound(frame, 270)
    # frame1 = rotate_bound(frame1,270)
    framew = rotate_bound(framew,270)
    #frame2 = cv2.flip(frame1, 1)
    t = int(round(time.time() * 1000))
    # frame2 = cv2.resize(frame, (height // smallSize, width // smallSize),interpolation=cv2.INTER_CUBIC)
    # frame3 = cv2.resize(frame1, (height // smallSize, width // smallSize),interpolation=cv2.INTER_CUBIC)
    frameww = cv2.resize(framew, (height // smallSize, width // smallSize),interpolation=cv2.INTER_CUBIC)
    # cv2.imshow("capture", frame2)
    # cv2.imshow("capture1", frame3)
    cv2.imshow("capture1", frameww)
    k=cv2.waitKey(1)

    if k & 0xFF == ord('q'):
        break
    elif k & 0xFF == ord('\r'):
    #     cv2.imwrite(save_dir + str(t) + "_1.jpg", frame)
    #     cv2.imwrite(save_dir + str(t) + "_2.jpg", frame1)
        cv2.imwrite(save_dir + str(t) + "_2.jpg", framew)
        count += 2

        print('第{}和{}张图片拍摄成功'.format(count-1, count), '总拍摄数为：{}张'.format(count))

# cap.release()
# cap1.release()
capw.release()
cv2.destroyAllWindows()


