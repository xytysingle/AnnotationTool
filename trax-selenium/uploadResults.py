import requests
from selenium import webdriver
# '''代理IP地址（高匿）'''
proxy = {
  # 'http': 'http://210.16.189.230:16816',
  'https': 'https://210.16.189.230:16816'
}
'''head 信息'''
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
       'Connection': 'keep-alive'}
'''http://icanhazip.com会返回当前的IP地址'''
p = requests.get('https://icanhazip.com', headers=head, proxies=proxy)
print(p.text)

# chromeOptions = webdriver.ChromeOptions()
# # chromeOptions.add_argument('--proxy-server=https://210.16.189.230:16816')
# # browser = webdriver.Chrome(chrome_options=chromeOptions)
# # res = browser.get("https://icanhazip.com")
# # print(res)