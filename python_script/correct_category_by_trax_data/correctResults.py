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
    img_index=51000001
    data=[]
    root_dir = '/data/tanx/project/ccza/20190710-20'
    original_imgs_filePathList = glob.glob(f'{root_dir}/original_imgs_init/*.jpg')
    dst_dir_imgs=f'{root_dir}/original_imgs_named'
    dst_dir_json=f'{root_dir}/original_imgs_bboxes_json'
    dst_file_csv= f'{root_dir}/imgIndexOld&New.csv'
    #检出的bbox
    imgs_info_filelist = glob.glob(f'{root_dir}/out0729/*.json')
    #trax中心点坐标
    trax_point_data = read_json(f'{root_dir}/point.json')
    # fetch name of trax by id
    trax_products = read_json('/data/tanx/bin/correct_category_by_trax_data/res/products-penbev.json')
    # print(len(trax_products['data']))
    isExistId=False
    #trax中心点坐标json数据示例
    # [{"img_path": "E:\\CCZA\\20190701\\2425032\\20190701070219-cfd542ba-a251-41dc-9456-324bc51ff5cd.jpeg",
    #   "bboxes": [{"x": 2028, "y
    for imgs_info_file in tqdm(imgs_info_filelist[0:3]):
        imgs_info_dict = read_json(imgs_info_file)
        #当前图片名
        img_name=os.path.splitext(imgs_info_dict['image'])[0].split('/')[-1]
        trax_img_index=0
        #找到trax对应图片索引
        for i,v in enumerate(trax_point_data):
            trax_img_name=os.path.splitext(v['img_path'])[0].split('\\')[-1]
            if trax_img_name==img_name:
                trax_img_index=i
        #图片中没有bbox被检出
        if len(imgs_info_dict["bboxes"])==0:
            print(f'{img_name} no bboxes',imgs_info_dict["bboxes"])
            continue
        #遍历某一张图片的bbox
        for bbox in imgs_info_dict["bboxes"]:
            # 遍历trax某一张图片的point
            for trax_bbox in trax_point_data[trax_img_index]['bboxes']:
                if trax_bbox["x"] in range(bbox["x1"] , bbox["x2"]+1) and trax_bbox["y"] in range(bbox["y1"] , bbox["y2"]+1):

                    #通过id获取trax的className
                    for trax_product in trax_products['data']:
                        print(trax_product['id'])
                        if 3689==trax_product['id']:
                            isExistId=True
                            bbox["className"] = trax_product["name"]
                            bbox['score']=1.0
            # print(isExistId)
            isExistId=False

            # print(bbox)

        #json另存为
        with open(os.path.join(dst_dir_json,str(img_index)+'.json'),'w',encoding='utf-8') as file:
            json.dump(imgs_info_dict,file)
        # print(imgs_info_dict)
        #原图另存为
        # print(img_name)
        for img_file in original_imgs_filePathList:
            if img_name in img_file:
                shutil.copy(img_file,os.path.join(dst_dir_imgs,str(img_index)+'.jpg'))
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
