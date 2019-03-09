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
t='''
   <dd>
                        <i class="board-index board-index-1">1</i>
    <a href="/films/1203" title="霸王别姬" class="image-link" data-act="boarditem-click" data-val="{movieId:1203}">
      <img src="//s0.meituan.net/bs/?f=myfe/mywww:/image/loading_2.e3d934bf.png" alt="" class="poster-default"/>
      <img data-src="https://p1.meituan.net/movie/20803f59291c47e1e116c11963ce019e68711.jpg@160w_220h_1e_1c" alt="霸王别姬" class="board-img"/>
    </a>
    <div class="board-item-main">
      <div class="board-item-content">
              <div class="movie-item-info">
        <p class="name"><a href="/films/1203" title="霸王别姬" data-act="boarditem-click" data-val="{movieId:1203}">霸王别姬</a></p>
        <p class="star">
                主演：张国荣,张丰毅,巩俐
        </p>
<p class="releasetime">上映时间：1993-01-01</p>    </div>
    <div class="movie-item-number score-num">
<p class="score"><i class="integer">9.</i><i class="fraction">5</i></p>        
    </div>

      </div>
    </div>

                </dd>
    '''
def parse_page(pageIndex):
    try:
        response = requests.get('https://maoyan.com/board/4', params={"offset":pageIndex*10})
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

            bs_parser = BeautifulSoup(response.text, 'lxml')
            # dds = bs_parser.find_all(name='dd')
            # for dd in dds:
            #     index=dd.find(class_='board-index').string
            #     img=dd.find(class_='board-img').attrs['data-src']
            #     title=dd.find(class_='name').find(name='a').string
            #     actor=dd.find(class_='star').string.strip()[3:]
            #     time=dd.find(class_='releasetime').string[5:]
            #     score=dd.find(class_='integer').string+dd.find(class_='fraction').string

            dds = bs_parser.select('dd')
            for dd in dds:
                index = dd.select_one('.board-index').string
                img=dd.select_one('.board-img').attrs['data-src']
                response = requests.get(img)
                title=dd.select_one('.name a').string
                # with open('img/%s.jpg' % title,'wb') as img_file:
                #     img_file.write(response.content)
                actor=dd.select_one('.star').string.strip()[3:]
                time=dd.select_one('.releasetime').string[5:]
                score=dd.select_one('.integer').string+dd.select_one('.fraction').string

                print(index,img,title,actor,time,score)
                # with open('..\data.csv', 'a', encoding='utf-8') as csvfile:
                #     fieldnames = ['index', 'img', 'title', 'actor','time','score']
                #     writer = csv.writer(csvfile)
                #     writer.writerow([index,img,title,actor,time,score])


    except RequestException:
        return None

if  __name__=='__main__':
    # if  not is_can_catch():
    #     return
    for i in range(10):
        parse_page(i)
