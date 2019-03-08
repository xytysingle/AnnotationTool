#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/10/3 17:20
#!@Author :SINGLE
#!@File   :BaseApp.py
from urllib.robotparser import RobotFileParser
import re,json,requests,time
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import  csv
def is_can_catch():
    rp=RobotFileParser('http://www.maoyan.com/robots.txt')
    rp.read()
    print(rp.can_fetch('*','https://maoyan.com/board/4?offset=0'))
def parse_page(pageIndex):
    try:
        response = requests.get('http://8d30guhytpv0pl9m.cy1234.xyz:3103/VMDIR5EC28CF91FE3CE9423378'
                                'CF92F79D8AE/20190307/NAnbS8ls/800kb/hls/g5mO68770%02d.ts' % pageIndex, timeout=60)
        if response.status_code==200:
            # doc=pq(response.text)
            # items= doc('dd').items()
            # for item in items:
            #     index=item.find('.board-index').text()
            #     img = item.find('.board-img').attr('data-src')
            #     title = item.find('.name a ').text()
            #     actor = item.find('.star').text()[3:]
            #     time = item.find('.releasetime').text().lstrip()[5:]
            #     score=item.find('.integer').text()+item.find('.fraction').text()

            # bs_parser = BeautifulSoup(response.text, 'lxml')
            # dds = bs_parser.find_all(name='dd')
            # for dd in dds:
            #     index=dd.find(class_='board-index').string
            #     img=dd.find(class_='board-img').attrs['data-src']
            #     title=dd.find(class_='name').find(name='a').string
            #     actor=dd.find(class_='star').string.strip()[3:]
            #     time=dd.find(class_='releasetime').string[5:]
            #     score=dd.find(class_='integer').string+dd.find(class_='fraction').string

            # dds = bs_parser.select('dd')
            # for dd in dds:
            #     index = dd.select_one('.board-index').string
            #     img=dd.select_one('.board-img').attrs['data-src']
            #     response = requests.get(img)
            #     title=dd.select_one('.name a').string
            #     with open('img/%s.jpg' % title,'wb') as img_file:
            #         img_file.write(response.content)
            #     actor=dd.select_one('.star').string.strip()[3:]
            #     time=dd.select_one('.releasetime').string[5:]
            #     score=dd.select_one('.integer').string+dd.select_one('.fraction').string

                # print(index,img,title,actor,time,score)

            return  response.content


    except RequestException:
        return None

if  __name__=='__main__':
    # if  not is_can_catch():
    #     return
    with open('data.mp4', 'wb+', ) as csvfile:
        for i in range(32):
            csvfile.write(parse_page(i))
http://8d30guhytpv0pl9m.cy1234.xyz:3103/VMDIR5EC28CF91FE3CE9423378CF92F79D8AE/20190307/NAnbS8ls/800kb/hls/g5mO6877003.ts
http://8d30guhytpv0pl9m.cy1234.club:3103/VMDIR5EC28CF91FE3CE9423378CF92F79D8AE/20190307/yVy0O9Ka/800kb/hls/uhiwz25701000.ts