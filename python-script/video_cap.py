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


cap = cv2.VideoCapture(0)
# cap1 = cv2.VideoCapture(2)



width = 3264
height = 2448
cap.set(3, width)
cap.set(4, height)
# cap1.set(3, width)
# cap1.set(4, height)


while(1):
    ret, frame = cap.read()
    if ret == True:
    # ret1, frame1 = cap1.read()
        frame = rotate_bound(frame, 90)
        # frame1 = rotate_bound(frame1,90)
        # frame2 = cv2.flip(frame1, 1)
        t = int(round(time.time() * 1000))
        # cv2.imshow("capture", frame2)
        cv2.imshow("capture", frame)
        k=cv2.waitKey(1)

        if k & 0xFF == ord('q'):
            break
        elif k & 0xFF ==ord('s'):
            # cv2.imwrite(save_dir + str(t) + ".jpg", frame2)
            cv2.imwrite(save_dir + str(t) + "1.jpg", frame)

cap.release()
cv2.destroyAllWindows()


