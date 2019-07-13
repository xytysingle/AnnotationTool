from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import json
import os
import math
from urllib import request



def login():
    global lastPageScenceId


    getLogin_url = 'https://services.trax-cloud.cn'



    username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    # username = browser.find_element_by_name("username")
    # submit_next = browser.find_element_by_name("login")
    submit_next = wait.until(EC.presence_of_element_located((By.NAME, "login")))

    username.clear()
    username.send_keys("chenqinghai@swirebev.com")
    time.sleep(1)
    submit_next.click()

    # password_input = browser.find_element_by_name("password")
    # submit_login = browser.find_element_by_name("login")
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    submit_login = wait.until(EC.presence_of_element_located((By.NAME, "login")))

    password_input.clear()
    password_input.send_keys("Trax12345")
    time.sleep(1)
    submit_login.click()


    Explorer = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ui-view/div/ui-view/div/div/div[1]/div[2]/a")))
    Explorer.click()

    # Explorer = browser.find_element_by_xpath("/html/body/ui-view/div/ui-view/div/div/div[1]/div[2]/a").click()
    # /html/body/ui-view/div/ui-view/div/div/div[1]/div[2]/a

    Scenes = browser.find_element_by_xpath("/html/body/ui-view/div/ui-view/ui-view/div/div[2]/div[2]").click()

    DateRange = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ui-view/div/ui-view/ui-view/ui-view/div/div[1]/div/ui-view/div/div/trax-date-picker/div/div"))).click()

    # https://services.trax-cloud.cn/trax-one/api/projects/swirecn/explore/scenes/all/?limit=200&from=2019-02-01&to=2019-02-02&direction=first
    FromDate = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ui-view/div/ui-view/ui-view/ui-view/div/div[1]/div/ui-view/div/div/trax-date-picker/div/div[2]/div[1]/input[1]")))
    ToDate = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ui-view/div/ui-view/ui-view/ui-view/div/div[1]/div/ui-view/div/div/trax-date-picker/div/div[2]/div[1]/input[2]")))
    # '12 Mar, 2019' '14 Mar, 2019'  Mar  Feb  Jan
    FromDate.clear()
    FromDate.send_keys("13  Mar, 2019")

    ToDate.clear()
    ToDate.send_keys("13 Mar, 2019")
    time.sleep(1)
    Apply_btn = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ui-view/div/ui-view/ui-view/ui-view/div/div[1]/div/ui-view/div/div/trax-date-picker/div/div[2]/div[6]/button[2]")))
    Apply_btn.click()
    #
    # page = browser.page_source

    # 进入场景
    time.sleep(5)
    # getFirstScencesList()
    getNextScencesList(lastPageScenceId)
def saveCookies():
    cookies = browser.get_cookies()
    jsonCookies = json.dumps(cookies)
    with open('cookies.json', 'w') as f:
        f.write(jsonCookies)
    print(cookies)

# 获取cookies
def getCookies():
    with open('cookies.json', 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
    cookie = [item["name"] + "=" + item["value"] for item in listCookies]
    cookiestr = '; '.join(item for item in cookie)

    return cookiestr

# 获取localStorage
def getLocalStorage(key):
    # getItem = 'localStorage.getItem("temp2")'
    print(key)
    res = browser.execute_script("return localStorage.getItem({})".format(key))
    return res
def getLabelResults(index):
    print('发起请求...')
    base_url = 'https://services.trax-cloud.cn/trax-one/api/projects/swirecn/scene/' + str(index)
    headers = {
        "authentication_token": getLocalStorage("'authentication_token'"),
        "authorization_token": getLocalStorage("'authorization_token'"),
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "refresh_token": getLocalStorage("'refresh_token'"),
        "cookie": getCookies()
    }
    try:
        rec_response = requests.get(base_url, headers=headers).text
        rec_response = json.loads(rec_response)
        scence_path = date_path + "/{}".format(str(index))
        mkdir(scence_path)
        # saveResults(scence_path + "/{}".format(str(index)), rec_response)
        saveResultsByJson(scence_path + "/{}".format(str(index)), rec_response)
        imagesList = rec_response["probeImages"]
        for img in imagesList:
            img_url = 'https://services.traxretail.com/images/traxus' + img["probe_image_path"].partition('http://traxus.s3.amazonaws.com')[2] + '/original'
            img_name = img["probe_image_path"].split('/')[-1]
            try:
                saveimage(img_url, scence_path + "/{}.jpeg".format(img_name))
            except Exception as e:
                print("图片保存失败：", e)
        print('爬取成功...')
    except:
        print("爬取失败")
    time.sleep(2)
    # print(rec_response)

def goToNextPage():
    # span.xp-navigate-description.trax-tst-pagination-paging-summary
    page_location =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.xp-navigate-description.trax-tst-pagination-paging-summary')))
    print('page_location:', page_location.text)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[title="next"]'))).click()
    # 进入场景
    time.sleep(5)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href^="trax-one/swirecn/explore/scene/"]'))).click()


def getNextSence():

    scence_location = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > ui-view > div > ui-view > ui-view > div > div.is-subheader.is-viewer-subheader.sp-flex-shrink > span.is-subheader-center > ui-view > div > siblings-navigator > span > span > span.items-list.trax-tst-viewer-serializationText')))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > ui-view > div > ui-view > ui-view > div > div.is-subheader.is-viewer-subheader.sp-flex-shrink > span.is-subheader-center > ui-view > div > siblings-navigator > span > span > span.trax-icons.trax-icons-page-back.rotated-to-down-arrow.trax-tst-viewer-next'))).click()
    scence_index = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > ui-view > div > ui-view > ui-view > div > div.is-subheader.is-viewer-subheader.sp-flex-shrink > span.is-subheader-left > ui-view > div > span > span:nth-child(4)')))
    print('scence_location:', scence_location.text, 'scence_index:', scence_index.text)

def getFirstScencesList():
    global pageNumber
    global totalPages
    print('发起场景列表请求...')
    base_url = 'https://services.trax-cloud.cn/trax-one/api/projects/swirecn/explore/scenes/all/'
    headers = {
        "authentication_token": getLocalStorage("'authentication_token'"),
        "authorization_token": getLocalStorage("'authorization_token'"),
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "refresh_token": getLocalStorage("'refresh_token'"),
        "cookie": getCookies()
    }
    request_data = {
        "limit": 200,
        "from": from_date,
        "to": to_date,
        "direction": 'first',
        # "last_known_primary_key": last_known_primary_key
    }

    scencesList_res = requests.get(url=base_url, headers=headers, params=request_data).text
    scencesList_res = json.loads(scencesList_res)
    saveResultsByJson(date_path +'/' + date + '_' + str(pageNumber + 1), scencesList_res)
    print(scencesList_res)
    totalItemsCount = scencesList_res["totalItems"]["total_items"]
    items = scencesList_res["items"]
    print("totalItemsCount:",totalItemsCount, "items:", items)
    pageNumber += 1
    totalPages = math.ceil(int(totalItemsCount) / 200)
    for i in range(0, 200):
        index = items[i]["scene_id"]
        print("正在爬取第{}页的第{}条,共{}页，共{}条".format(pageNumber, i+1, totalPages, totalItemsCount))
        try:
            getLabelResults(index)
            if i == 199 and pageNumber <= totalPages:
                getNextScencesList(index)
        except Exception as e:
            print('获取下个场景失败', e)


def getNextScencesList(last_known_primary_key):
    global pageNumber
    global totalPages
    print('发起场景列表请求...')
    base_url = 'https://services.trax-cloud.cn/trax-one/api/projects/swirecn/explore/scenes/all/'
    headers = {
        "authentication_token": getLocalStorage("'authentication_token'"),
        "authorization_token": getLocalStorage("'authorization_token'"),
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "refresh_token": getLocalStorage("'refresh_token'"),
        "cookie": getCookies()
    }
    request_data = {
        "limit": 200,
        "from": from_date,
        "to": to_date,
        "direction": 'next',
        "last_known_primary_key": last_known_primary_key
    }

    scencesList_res = requests.get(url=base_url, headers=headers, params=request_data).text
    scencesList_res = json.loads(scencesList_res)

    # print(scencesList_res)
    # saveResultsByJson(str(2019), scencesList_res)
    saveResultsByJson(date_path + '/' + date + '_' + str(pageNumber + 1), scencesList_res)
    print(scencesList_res)
    totalItemsCount = scencesList_res["totalItems"]["total_items"]
    items = scencesList_res["items"]
    print("totalItemsCount:", totalItemsCount, "items:", items)
    pageNumber += 1
    totalPages = math.ceil(int(totalItemsCount) / 200)
    for i in range(0, 200):
        index = items[i]["scene_id"]
        print("正在爬取第{}页的第{}条,共{}页，共{}条".format(pageNumber, i + 1, totalPages, totalItemsCount))
        try:
            getLabelResults(index)
            if i == 199 and pageNumber <= totalPages:
                getNextScencesList(index)
        except Exception as e:
            print('获取下个场景失败', e)


def saveimage(imgUrl, imgPath):
    request.urlretrieve(imgUrl, imgPath)

def saveResults(filename, data):
    with open("{}.json".format(filename), "w", encoding='utf-8') as f:
        f.write(data)

def saveResultsByJson(filename, data):
    with open("{}.json".format(filename), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print("{}创建成功".format(path))
        return True
    else:
        print("{}已存在".format(path))
        return False

if __name__ == "__main__":
    from_date = '2019-03-13'
    to_date = '2019-03-13'
    date = from_date.replace('-', '')
    date_path = "./scence/{}".format(date)
    lastPageScenceId = 9237427
    pageNumber = 5
    totalPages = 0
    mkdir(date_path)
    # chromeOptions = webdriver.ChromeOptions()
    # chromeOptions.add_argument('--proxy-server=https://210.16.189.230:16816')
    # browser = webdriver.Chrome(chrome_options=chromeOptions)
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 10)
    login()
