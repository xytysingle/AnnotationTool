#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/10/3 17:20
#!@Author :SINGLE
#!@File   :BaseApp.py
from urllib.robotparser import RobotFileParser
import re,json,requests,time
from requests.exceptions import RequestException

def is_can_catch():
    rp=RobotFileParser('http://www.maoyan.com/robots.txt')
    rp.read()
    print(rp.can_fetch('*','https://maoyan.com/board/4?offset=0'))
def parse_page(pageIndex):
    try:
        t='''
            <dd>
                        <i class="board-index board-index-1">1</i>
    <a href="/films/1203" title="霸王别姬" class="image-link" data-act="boarditem-click" data-val="{movieId:1203}">
      <img src="//s0.meituan.net/bs/?f=myfe/mywww:/image/loading_2.e3d934bf.png" alt="" class="poster-default" />
      <img data-src="https://p1.meituan.net/movie/20803f59291c47e1e116c11963ce019e68711.jpg@160w_220h_1e_1c" alt="霸王别姬" class="board-img" />
    </a>
    <div class="board-item-main">
      <div class="board-item-content">
              <div class="movie-item-info">
        <p class="name"><a href="/films/1203" title="霸王别姬" data-act="boarditem-click" data-val="{movieId:1203}">霸王别姬</a></p>
        <p class="star">
                主演：张国荣,张丰毅,巩俐
        </p>
<p class="releasetime">上映时间：1993-01-01</p>    </div>
        '''
        #star.*?：(.*?).*?</p>.*?releasetime.*?：(.*?)</p>
        response = requests.get('https://maoyan.com/board/4', data='{"offset":' + str(pageIndex) + '}')
        if response.status_code==200:
            pattern=re.compile('board-index-(\d+).*?data-src="(.*?)".*?movie-item-info.*?title="(.*?)".*?star.*?：(.*?)\n.*?</p>.*?releasetime.*?：(.*?)</p>',re.S)
            items=re.findall(pattern,response.text)
            return items
            for item in items:
                return {'actor':item[0],'time':item[1]}
    except RequestException:
        return None

if  __name__=='__main__':
    # if  not is_can_catch():
    #     return
    page = parse_page(0)
    print(page)
