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
import ssl
import yaml


ssl._create_default_https_context = ssl._create_unverified_context

def login():
    global lastPageScenceId


    # getLogin_url = 'https://services.trax-cloud.cn'
    getLogin_url = '{}'.format(config["login_url"])

    browser.get(getLogin_url)

    username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    # username = browser.find_element_by_name("username")
    # submit_next = browser.find_element_by_name("login")
    submit_next = wait.until(EC.presence_of_element_located((By.NAME, "login")))

    username.clear()
    # username.send_keys("chenqinghai@swirebev.com")
    print("input username")
    _username = input()
    # "shendan@swirebev.com"
    username.send_keys(_username)
    time.sleep(1)
    submit_next.click()

    # password_input = browser.find_element_by_name("password")
    # submit_login = browser.find_element_by_name("login")
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    submit_login = wait.until(EC.presence_of_element_located((By.NAME, "login")))
    print("input password")
    _password = input()

    password_input.clear()
    # Trax12345
    password_input.send_keys(_password)
    time.sleep(1)
    submit_login.click()


    Explorer = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ui-view/div/ui-view/div/div/div[1]/div[2]/a")))
    Explorer.click()

    # Explorer = browser.find_element_by_xpath("/html/body/ui-view/div/ui-view/div/div/div[1]/div[2]/a").click()
    # /html/body/ui-view/div/ui-view/div/div/div[1]/div[2]/a

    Scenes = browser.find_element_by_xpath("/html/body/ui-view/div/ui-view/ui-view/div/div[2]/div[2]").click()

    DateRange = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ui-view/div/ui-view/ui-view/ui-view/div/div[1]/div/ui-view/div/div/div/trax-date-picker/div/div"))).click()
                                                                    # "/html/body/ui-view/div/ui-view/ui-view/ui-view/div/div[1]/div/ui-view/div/div/div/trax-date-picker/div/div"
    # https://services.trax-cloud.cn/trax-one/api/projects/swirecn/explore/scenes/all/?limit=200&from=2019-02-01&to=2019-02-02&direction=first
    FromDate = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ui-view/div/ui-view/ui-view/ui-view/div/div[1]/div/ui-view/div/div/div/trax-date-picker/div/div[2]/div[1]/input[1]")))
                                                                    # "/html/body/ui-view/div/ui-view/ui-view/ui-view/div/div[1]/div/ui-view/div/div/div/trax-date-picker/div/div[2]/div[1]/input[1]"
    ToDate = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ui-view/div/ui-view/ui-view/ui-view/div/div[1]/div/ui-view/div/div/div/trax-date-picker/div/div[2]/div[1]/input[2]")))
    # '12 Mar, 2019' '14 Mar, 2019'  Mar  Feb  Jan                "/html/body/ui-view/div/ui-view/ui-view/ui-view/div/div[1]/div/ui-view/div/div/div/trax-date-picker/div/div[2]/div[1]/input[2]"
    FromDate.clear()

    # FromDate.send_keys("26  June, 2019")
    FromDate.send_keys("{}  {}, {}".format(_date.split("-")[-1], month_list["{}".format(_date.split("-")[1])], _date.split("-")[0]))

    ToDate.clear()
    # ToDate.send_keys("26 June, 2019")
    ToDate.send_keys("{}  {}, {}".format(_date.split("-")[-1], month_list["{}".format(_date.split("-")[1])], _date.split("-")[0]))
    time.sleep(1)
    Apply_btn = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ui-view/div/ui-view/ui-view/ui-view/div/div[1]/div/ui-view/div/div/div/trax-date-picker/div/div[2]/div[6]/button[2]")))
    Apply_btn.click()                                              #"/html/body/ui-view/div/ui-view/ui-view/ui-view/div/div[1]/div/ui-view/div/div/div/trax-date-picker/div/div[2]/div[6]/button[2]"
    #
    # page = browser.page_source

    # 进入场景
    time.sleep(5)
    getFirstScencesList()
    # getNextScencesList(lastPageScenceId)
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
    # print(key)
    res = browser.execute_script("return localStorage.getItem({})".format(key))
    return res
def getLabelResults(index):
    print('send request...')
    # base_url = 'https://services.trax-cloud.cn/trax-one/api/projects/swirecn/scene/' + str(index)
    base_url = 'https://services.traxretail.com/trax-one/api/projects/ccza/scene/' + str(index)

    # https://services.traxretail.com/trax-one/api/projects/ccza/scene/2460951
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

        # imagesList = rec_response["probeImages"]
        # for img in imagesList:
        #     img_url = 'https://services.traxretail.com/images/traxus' + img["probe_image_path"].partition('http://traxus.s3.amazonaws.com')[2] + '/original'
        #     img_name = img["probe_image_path"].split('/')[-1]
        #     try:
        #         saveimage(img_url, scence_path + "/{}.jpeg".format(img_name))
        #     except Exception as e:
        #         print("图片保存失败：", e)


        print('successful...')

    except:
        print("failed...")
    # time.sleep(2)
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
    global retryNum
    print('发起场景列表请求...')
    base_url = 'https://services.traxretail.com/trax-one/api/projects/ccza/explore/scenes/all/'
    # https://services.traxretail.com/trax-one/api/projects/ccza/scene/2460951
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
        print("run page:{} item:{},all pages:{}，all items:{}".format(pageNumber, i+1, totalPages, totalItemsCount))
        try:
            getLabelResults(index)
        except Exception as e:
            print('获取下个场景失败', e)
        if i == 199 and pageNumber <= totalPages:
            try:
                getNextScencesList(index)
            except Exception as e:
                retryNum += 1
                print('获取下个场景列表失败，正在重试', e)
                if retryNum <= 3:
                    getNextScencesList(index)
            except:
                print("重试三次后无效，请手动重启！")
                with open("lastIndex.txt", "w") as f:
                    f.write(index)




def getNextScencesList(last_known_primary_key):
    global pageNumber
    global totalPages
    global retryNum
    print('running...')
    # base_url = 'https://services.trax-cloud.cn/trax-one/api/projects/swirecn/explore/scenes/all/'
    base_url = 'https://services.traxretail.com/trax-one/api/projects/ccza/explore/scenes/all/'
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
        print("run page:{} item:{},all pages:{}，all items:{}".format(pageNumber, i + 1, totalPages, totalItemsCount))
        try:
            getLabelResults(index)
        except Exception as e:
            print('获取下个场景失败', e)
        if i == 199 and pageNumber <= totalPages:
            try:
                getNextScencesList(index)
            except Exception as e:
                retryNum += 1
                print('获取下个场景列表失败，正在重试', e)
                if retryNum <= 3:
                    getNextScencesList(index)
                else:
                    print("重试三次后无效，请手动重启！")
                    with open("lastIndex.txt", "w") as f:
                        f.write(index)



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
        print("{}created".format(path))
        return True
    else:
        print("{}已存在".format(path))
        return False

if __name__ == "__main__":
    month_list = {
        "01": "Jan",
        "02": "Feb",
        "03": "Mar",
        "04": "Apr",
        "05": "May",
        "06": "Jun",
        "07": "Jul",
        "08": "Aug",
        "09": "Sep",
        "10": "Oct",
        "11": "Nov",
        "12": "Dec",
    }
    print("input date, example:2019-07-11")
    _date = input()
    from_date = _date
    # from_date = '2019-06-26'
    to_date = _date
    # to_date = '2019-06-26'
    date = from_date.replace('-', '')
    # date_path = "./scence/{}".format(date)
    file = open("config.yaml", 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    # config = yaml.load(file_data)
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    date_path = "{}/{}".format(config["output_path"], date)
    lastPageScenceId = 9695981
    pageNumber = 0
    totalPages = 0
    retryNum = 0
    mkdir(date_path)
    chromeOptions = webdriver.ChromeOptions()
    # # chromeOptions.add_argument('--proxy-server=https://210.16.189.230:16816')
    # chromeOptions.add_argument("--headless")
    # browser = webdriver.Chrome(options=chromeOptions, executable_path="{}".format(config["chromedriver_path"]))
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 10)
    login()
#   garyj@penbev.co.za
#   Yellow!1
