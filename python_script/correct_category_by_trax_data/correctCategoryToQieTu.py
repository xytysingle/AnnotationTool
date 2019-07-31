#!/usr/bin/env python3
#!-*-coding:utf-8 -*-
import glob
import json
import os
import requests
import shutil
import pandas as pds
from tqdm import tqdm
def main():
    img_index=52000001
    data=[]
    project_dir='/data/tanx/project/ARCA/'
    original_imgs_filelist = glob.glob(f'{project_dir}/Cooler/*.jpg')
    dst_dir_imgs=f'{project_dir}/original_imgs_named'
    dst_dir_json=f'{project_dir}/original_imgs_bboxes_json'

    dst_file_csv= f'{project_dir}/imgIndexOld&New.csv'
    #检出的bbox
    imgs_info_filelist = glob.glob(f'{project_dir}/out0730/*.json')

    for imgs_info_file in tqdm(imgs_info_filelist):
        imgs_info_dict = read_json(imgs_info_file)
        #当前图片名
        img_name=os.path.splitext(imgs_info_dict['image'])[0].split('/')[-1]
        #图片中没有bbox被检出
        if len(imgs_info_dict["bboxes"])==0:
            continue
        #遍历某一张图片的bbox
        for bbox in imgs_info_dict["bboxes"]:
            bbox["className"] = "其他"
            # print(bbox)
        #json另存为
        with open(os.path.join(dst_dir_json,str(img_index)+'.json'),'w',encoding='utf-8') as file:
            json.dump(imgs_info_dict,file)
        # print(imgs_info_dict)
        #原图另存为
        # print(img_name)
        for img_file in original_imgs_filelist:
            if img_name in img_file:
                shutil.copy(img_file,os.path.join(dst_dir_imgs,str(img_index)+'.jpg'))
                break
                # print(img_file,os.path.join(dst_dir_imgs,str(img_index)+'.jpg'))
        # print(img_index)
        #备份新旧名字为csv
        data.append([img_name,img_index])
        img_index+=1
    t=pds.DataFrame(columns=['oldIndex','newIndex'],data=data)
    # print(t)
    t.to_csv(dst_file_csv,index=None)

    # uploadResults(index, r_bboxes)


def uploadResults(index, r_bboxes):
    submit_url = "http://annotation.lingmou.ai:8000/index.php/annotation/upsert"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    submit_data = {
        "image": index,
        "rotate": 0,
        "sceneType": -1,
        "username": "tttt",
        "bboxes": r_bboxes
    }
    submit_data = json.dumps(submit_data)
    response = requests.post(url=submit_url, data=submit_data, headers=headers)
    print(index, response.text)

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    return input_data


if __name__ == "__main__":
    main()
