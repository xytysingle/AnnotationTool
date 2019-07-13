import os  #打开文件时需要
from PIL import Image
import re

Start_path = '/Volumes/NO NAME/场景构造9.7/'
Out_path = '/Users/dw/Desktop/1080P/'
new_width = 1080
# new_high = 1080
list = os.listdir(Start_path)
#print list
count = 0
for pic in list:
    path = Start_path+pic
    print(path)
    im = Image.open(path)
    w, h = im.size

    print(pic)
    print("图片名称为" + pic + "图片被修改")
    h_new = int(h/w*new_width)
    w_new = new_width
    count = count + 1
    out = im.resize((w_new, h_new), Image.ANTIALIAS)
    new_pic = re.sub(pic[:-4], pic[:-4] + '_new', pic)
    # print new_pic
    new_path = Out_path + new_pic
    out.save(new_path)


