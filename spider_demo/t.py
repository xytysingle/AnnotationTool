#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2019/3/9 20:50
#!@Author :SINGLE
#!@File   :t.py



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import  time
browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)

def get_page(index):
    browser.get('https://s.taobao.com/search?q=ipad')
    print(index)
    try:
        if index>1:
            input= wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form input')))
            commit_btn=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager div.form .J_Submit')))
            input.clear()
            input.send_keys(index)
            commit_btn.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager .items .active'),str(index)))
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
        get_products()
    except:
        index(index)


def get_products():
    items = browser.find_elements(By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')
    print(items)
    for item in items:
        print(item.find_element(By.CSS_SELECTOR,'.price strong').text,item.find_element(By.CSS_SELECTOR,'.title').text)

def main():
    for i in range(1,101):
        get_page(i)
        time.sleep(1)
if __name__ == '__main__':
    main()