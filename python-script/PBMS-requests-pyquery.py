import requests
import re
import pytesseract
from PIL import Image
from pyquery import PyQuery as pq
from urllib.parse import urljoin
import datetime
from retrying import retry
# 引入模块
import os
import sys
import logging

# print(sys.argv[0])          #sys.argv[0] 类似于shell中的$0,但不是脚本名称，而是脚本的路径
# print(sys.argv[1])



dirname = os.path.dirname(__file__)
# targetdate = '2018-09-15'
def getYesterday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return str(yesterday)

def captcha_rec(captchapicfile):
    captcha_str = pytesseract.image_to_string(Image.open(captchapicfile))
    captcha_str = ''.join(re.findall(r'\d+', captcha_str))
    return captcha_str

def after_login(s, headers, visit_record_response):
    global list
    global lastrecordnum
    global total_page
    vrdoc = pq(visit_record_response.text)
    total_record = int(vrdoc('#ctl00_ContentPlaceHolder1_gv_List font:nth-child(2)').text())
    # '#ctl00_ContentPlaceHolder1_gv_List font:nth-child(2)'
    total_page = int(vrdoc('#ctl00_ContentPlaceHolder1_gv_List font:nth-child(4)').text())
    # '#ctl00_ContentPlaceHolder1_gv_List font:nth-child(4)'
    print("总条数为：", total_record)
    print("总页数为：", total_page)
    print('正在爬取第 1 页')
    lastrecordnum = total_record % 15
    after_login_viewstate_value = vrdoc('#__VIEWSTATE').attr("value")
    # print('after_login_viewstate_value:', after_login_viewstate_value)
    # total_customer_code = vrdoc('td:nth-child(2):contains(S)')

    if flag == 1:
        total_customer_code = vrdoc('td:nth-child(2):contains(S)')
    elif flag == 2:
        total_customer_code = vrdoc('td:nth-child(2):contains(R)')
    # print(customer_code)
    total_detail_link = vrdoc('a:contains(查看详细)')

    if total_page == 1:
        recordnum = lastrecordnum
    else:
        recordnum = 15
    picturecssnum = 1
    for i in range(0, recordnum):
        print("共 {totalpage} 页, 正在爬取页第 {page} 页 {i} 条记录".format(totalpage=total_page, page = 1, i=i + 1))
        picturecssnum = picturecssnum + 1
        if picturecssnum < 10:
            picturecss = '#ctl00_ContentPlaceHolder1_gv_List_ctl0{ii}_lb_PictureCount'.format(ii=picturecssnum)
        else:
            picturecss = '#ctl00_ContentPlaceHolder1_gv_List_ctl{ii}_lb_PictureCount'.format(ii=picturecssnum)
        picamount = int(vrdoc(picturecss).text())

        if picamount == 0:
            continue
        else:
            customer_code = total_customer_code.eq(i).text()

            detail_url = BASE_URL + '/PBMS/SubModule/PBM/Visit/' + total_detail_link.eq(i).attr("href")
            detail_get_response = s.get(detail_url)
            dgrdoc = pq(detail_get_response.text)
            dgrviewstate_value = dgrdoc('#__VIEWSTATE').attr("value")
            dgrdata = {
                '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$MCSTabControl1',
                '__EVENTARGUMENT': '2',
                '__VIEWSTATE': dgrviewstate_value,
                '__VIEWSTATEENCRYPTED': ''
            }
            target_result = s.post(url=detail_url, data=dgrdata, headers=headers)
            # print(target_result)
            detdoc = pq(target_result.text)
            get_informations(detdoc, customer_code)
            # 去图片后半部分URL和图片对应名称
            for j in range(0, picamount):
                if j <= 4:
                    imgurllastcss = '#ctl00_ContentPlaceHolder1_UploadFile1_lv_list_ctrl0_ctl0{j}_ProductLink'.format(
                        j=j)
                    imgnamecss = '#ctl00_ContentPlaceHolder1_UploadFile1_lv_list_ctrl0_ctl0{j}_lb_name'.format(j=j)
                else:
                    imgurllastcss = '#ctl00_ContentPlaceHolder1_UploadFile1_lv_list_ctrl1_ctl0{j}_ProductLink'.format(
                        j=j - 5)
                    imgnamecss = '#ctl00_ContentPlaceHolder1_UploadFile1_lv_list_ctrl1_ctl0{j}_lb_name'.format(j=j - 5)
                imgurllast = detdoc(imgurllastcss).attr('href')
                # print(j, imgurllast)
                imgname = detdoc(imgnamecss).text()
                # print(imgname)
                getimages(imgurllast, imgname, s)
            del list
    next_viewstate_value = after_login_viewstate_value
    for page in range(2, total_page + 1):
        next_viewstate_value = next_page(page, next_viewstate_value, s, headers)


def get_informations(detdoc, customer_code):
    global list
    list = []
    vistor = detdoc('#ctl00_ContentPlaceHolder1_VST_WorkList_RelateStaff').text()
    roadline = detdoc('#ctl00_ContentPlaceHolder1_VST_WorkList_Route').text()
    customername = detdoc('#ctl00_ContentPlaceHolder1_VST_WorkList_Client').text()
    starttime = detdoc('#ctl00_ContentPlaceHolder1_VST_WorkList_BeginTime').text()
    visttype = detdoc('#ctl00_ContentPlaceHolder1_VST_WorkList_WorkingClassify').text()

    list.append(vistor)
    list.append(roadline)
    if customer_code == '':
        customer_code = 1
    list.append(customer_code)
    list.append(customername)
    list.append(starttime)
    list.append(visttype)
    print("业代:", vistor)
    print("线路:", roadline)
    print("客户编码:", customer_code)
    print("客户名称:", customername)
    print("开始时间:", starttime)
    print("类别:", visttype)
    # viewstate_value = detdoc('#__VIEWSTATE').attr("value")
    # return viewstate_value


def getimages(imgurllast, imgname, s):
    global list
    try:
        # datePath = re.search('(\d+)-(\d+)-(\d+)', targetdate)
        # datePath = datePath.group(1) + datePath.group(2) + datePath.group(3)
        # file_path = dirname
        file_path_middle = 'PBMS/{datePath}/{province}/'.format(datePath=datePath, province=province)
        # mkfile_path_middle = os.path.join(dirname, 'PBMS/{datePath}/{province}/'.format(datePath=datePath, province=province))
        # mkdir(mkfile_path_middle)
        imgurl_pre = BASE_URL + '/PBMS/SubModule/'
        imgurllast = re.match('../../(.*)', imgurllast).group(1)
        imgurl = urljoin(imgurl_pre, imgurllast)
        print(imgurl)
        # imgurl = parse.urlencode(imgurl).encode('utf-8')
        # imgresquest = request.Request(imgurl)

        imgres = s.get(url=imgurl, timeout=5)


        list.append(file_path_middle+imgname)
        try:
            with open(os.path.join(dirname, "{}{}".format(file_path_middle, imgname)), "wb") as f:
                f.write(imgres.content)
        except:
            print("保存图片出错")
        try:
            with open(os.path.join(dirname, 'PBMS/pbmstxt/{}_{}.txt'.format(province, datePath)), 'a') as f:
                for line in list:
                    f.write(line + '|')
                f.write('\n')
        except:
            print("写入txt出错")
        del list[-1]
    except:
        print("获取图片响应超时失败")


# @retry(stop_max_attempt_number=3)
def main():
    # global targetdate
    # global datePath


    login_url = BASE_URL + '/PBMS/SubModule/Login/index.aspx'
    captcha_url = BASE_URL + '/PBMS/VerifyCode.aspx?'
    visit_record_url = BASE_URL + '/PBMS/SubModule/PBM/Visit/VisitWorkList.aspx'
    # User-Agent信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    mkdir(os.path.join(dirname, 'captchaimagepath/'))
    captcha_image_path = os.path.join(dirname, 'captchaimagepath/captcha.png')
    # 定义维持会话的cookies
    s = requests.Session()
    # 获取第一次VIEWSTATE
    getres = s.get(url=login_url, headers=headers)
    getdoc = pq(getres.text)
    login_viewstate_value = getdoc('#__VIEWSTATE').attr("value")



    captcha_res = s.get(captcha_url)
    print(captcha_res.status_code)
    with open(captcha_image_path, 'wb') as f:
        f.write(captcha_res.content)
    captcha_value = captcha_rec(captcha_image_path)
    if len(captcha_value) != 4:
        captcha_res = s.get(captcha_url)
        print(captcha_res.status_code)
        with open(captcha_image_path, 'wb') as f:
            f.write(captcha_res.content)
        captcha_value = captcha_rec(captcha_image_path)
        print("自动识别验证码为：", captcha_value)
    else:
        print("自动识别验证码为：", captcha_value)


    if flag == 1:
        # 陕西
        Login_Data = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': '',
            # 陕西
            # '__VIEWSTATE': '/wEPDwUKMTUyNDQ2MjM1Nw8WAh4HTWFjQWRkcmUWAgIDD2QWAmYPPCsACgEADxYCHghVc2VyTmFtZQUJ55m95pmT552/ZBYCZg9kFgICAw8PFgIeBFRleHQFCeeZveaZk+edv2RkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBRNMb2dpbjEkSW1hZ2VCdXR0b24xM1yR2flVMGXD9quSHV07opC1HEI=',
            '__VIEWSTATE': '{}'.format(login_viewstate_value),
            'Login1$ImageButton1.x': '193',
            'Login1$ImageButton1.y': '12',
            'Login1$Password': 'zxc**123',
            'Login1$tbx_VerifyCode': captcha_value,
            'Login1$UserName': '白晓睿',
        }
    elif flag == 2:
        # 山西
        Login_Data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            # 山西
            # '__VIEWSTATE': '/wEPDwUKMTUyNDQ2MjM1Nw8WAh4HTWFjQWRkcmUWAgIDD2QWAmYPPCsACgEADxYCHghVc2VyTmFtZQUJ5YiY5pmT6ZuFZBYCZg9kFgICAw8PFgIeBFRleHQFCeWImOaZk+mbhWRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBRNMb2dpbjEkSW1hZ2VCdXR0b24xnCC8poK7Mv9yf7hpufVWIb3C7Yk=',
            # '__VIEWSTATEGENERATOR': 'CA4CC9A8',
            '__VIEWSTATE': '{}'.format(login_viewstate_value),
            'Login1$ImageButton1.x': '168',
            'Login1$ImageButton1.y': '8',
            'Login1$Password': 'abc123..',
            'Login1$tbx_VerifyCode': captcha_value,
            'Login1$UserName': '刘晓雅',
        }
    else:
        print('省份错误')
        return



    # response = requests.post("http://httpbin.org/post", data=data, headers=headers)
    loginres = s.post(url=login_url, data=Login_Data, headers=headers)
    print(loginres.status_code)
    if loginres.status_code != 200:
        main()
        print('未登录成功')
        return
    else:
        visit_record_res = s.get(visit_record_url)
        vrphdoc = pq(visit_record_res.text)
        viewstate_value = vrphdoc('#__VIEWSTATE').attr("value")
        print(viewstate_value)


    # print("请输入要爬取的日期：")
    # targetdate = input()

    # if len(sys.argv) == 1:
    #     targetdate = getYesterday()
    # else:
    #     if len(sys.argv[1]) == 10 :
    #         targetdate = sys.argv[1]
    #     else:
    #         targetdate = getYesterday()
    # print("即将爬取的图片日期为", targetdate)
    datePath = re.search('(\d+)-(\d+)-(\d+)', targetdate)
    datePath = datePath.group(1) + datePath.group(2) + datePath.group(3)
    mkimgpath = os.path.join(dirname, 'PBMS/{}/{}'.format(datePath, province))
    mktxtpath = os.path.join(dirname, 'PBMS/pbmstxt')
    mkdir(mkimgpath)
    mkdir(mktxtpath)
    visit_record_data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': viewstate_value,
        '__VIEWSTATEENCRYPTED': '',
        'ctl00$ContentPlaceHolder1$bt_Find': '查 找',
        'ctl00$ContentPlaceHolder1$tbx_begin': '{}'.format(targetdate),
        'ctl00$ContentPlaceHolder1$tbx_end': '{}'.format(targetdate),
        'ctl00$ContentPlaceHolder1$select_Staff$select_StaffSelect_txt_Value': '',
        'ctl00$ContentPlaceHolder1$tbx_RouteCode': '',
        'ctl00$ContentPlaceHolder1$tbx_Retailer': '',
        'ctl00$ContentPlaceHolder1$tbx_Offset': '0',
        'ctl00$ContentPlaceHolder1$ddl_EQCondition': '0',
        'ctl00$ContentPlaceHolder1$ddl_IsInPlan': '0',
        'ctl00$ContentPlaceHolder1$ddl_JdType': '0',
        'ctl00$ContentPlaceHolder1$tbx_PhotoRemark': '',
        'ctl00$ContentPlaceHolder1$gv_List$ctl18$_tbx_page_go': '1',
        # 'ctl00$ContentPlaceHolder1$gv_List$ctl18$ctl05': 'GO'
    }

    visit_record_response = s.post(url=visit_record_url, data=visit_record_data, headers=headers)
    # print(visit_record_response.text)
    after_login(s, headers, visit_record_response)

def next_page(page, next_viewstate_value, s, headers):
    global list
    nextpageurl = BASE_URL + '/PBMS/SubModule/PBM/Visit/VisitWorkList.aspx'
    nextpage_data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': next_viewstate_value,
        '__VIEWSTATEENCRYPTED': '',
        # 'ctl00$ContentPlaceHolder1$bt_Find': '查 找',
        'ctl00$ContentPlaceHolder1$tbx_begin': '{}'.format(targetdate),
        'ctl00$ContentPlaceHolder1$tbx_end': '{}'.format(targetdate),
        'ctl00$ContentPlaceHolder1$select_Staff$select_StaffSelect_txt_Value': '',
        'ctl00$ContentPlaceHolder1$tbx_RouteCode': '',
        'ctl00$ContentPlaceHolder1$tbx_Retailer': '',
        'ctl00$ContentPlaceHolder1$tbx_Offset': '0',
        'ctl00$ContentPlaceHolder1$ddl_EQCondition': '0',
        'ctl00$ContentPlaceHolder1$ddl_IsInPlan': '0',
        'ctl00$ContentPlaceHolder1$ddl_JdType': '0',
        'ctl00$ContentPlaceHolder1$tbx_PhotoRemark': '',
        'ctl00$ContentPlaceHolder1$gv_List$ctl18$_tbx_page_go': '{i}'.format(i=page),
        'ctl00$ContentPlaceHolder1$gv_List$ctl18$ctl05': 'GO'
    }
    nextpage_response = s.post(url=nextpageurl, data=nextpage_data, headers=headers)
    nextpagedoc = pq(nextpage_response.text)
    next_viewstate_value = nextpagedoc('#__VIEWSTATE').attr("value")
    if flag == 1:
        total_customer_code = nextpagedoc('td:nth-child(2):contains(S)')
    elif flag ==2:
        total_customer_code = nextpagedoc('td:nth-child(2):contains(R)')
    # #ctl00_ContentPlaceHolder1_gv_List > tbody > tr:nth-child(2) > td:nth-child(2)
    total_detail_link = nextpagedoc('a:contains(查看详细)')

    if page == total_page :
        recordnum = lastrecordnum
    else:
        recordnum = 15
    picturecssnum = 1
    for i in range(0, recordnum):
        print("共 {totalpage} 页, 正在爬取页第 {page} 页 {i} 条记录".format(totalpage=total_page, page=page, i=i + 1))
        picturecssnum = picturecssnum + 1
        if picturecssnum < 10:
            picturecss = '#ctl00_ContentPlaceHolder1_gv_List_ctl0{ii}_lb_PictureCount'.format(ii=picturecssnum)
        else:
            picturecss = '#ctl00_ContentPlaceHolder1_gv_List_ctl{ii}_lb_PictureCount'.format(ii=picturecssnum)
        picamount = int(nextpagedoc(picturecss).text())

        if picamount == 0:
            continue
        else:
            customer_code = total_customer_code.eq(i).text()
            # print("客户编码：", customer_code)
            detail_url = BASE_URL + '/PBMS/SubModule/PBM/Visit/' + total_detail_link.eq(i).attr("href")
            detail_get_response = s.get(detail_url)
            dgrdoc = pq(detail_get_response.text)
            dgrviewstate_value = dgrdoc('#__VIEWSTATE').attr("value")
            dgrdata = {
                '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$MCSTabControl1',
                '__EVENTARGUMENT': '2',
                '__VIEWSTATE': dgrviewstate_value,
                '__VIEWSTATEENCRYPTED': ''
            }
            target_result = s.post(url=detail_url, data=dgrdata, headers=headers)
            # print(target_result)
            detdoc = pq(target_result.text)
            get_informations(detdoc, customer_code)
            # 去图片后半部分URL和图片对应名称
            for j in range(0, picamount):
                if j <= 4:
                    imgurllastcss = '#ctl00_ContentPlaceHolder1_UploadFile1_lv_list_ctrl0_ctl0{j}_ProductLink'.format(
                        j=j)
                    imgnamecss = '#ctl00_ContentPlaceHolder1_UploadFile1_lv_list_ctrl0_ctl0{j}_lb_name'.format(j=j)
                else:
                    imgurllastcss = '#ctl00_ContentPlaceHolder1_UploadFile1_lv_list_ctrl1_ctl0{j}_ProductLink'.format(
                        j=j - 5)
                    imgnamecss = '#ctl00_ContentPlaceHolder1_UploadFile1_lv_list_ctrl1_ctl0{j}_lb_name'.format(j=j - 5)
                imgurllast = detdoc(imgurllastcss).attr('href')
                # print(j, imgurllast)
                imgname = detdoc(imgnamecss).text()
                # print(imgname)
                getimages(imgurllast, imgname, s)
            del list
    return next_viewstate_value

def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("/")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False

def logSave():
    pass

if __name__ =='__main__':
    global datePath
    global targetdate
    global flag # 1 陕西；2 山西
    global BASE_URL
    global province
    if len(sys.argv) == 1:
        targetdate = getYesterday()
        flag = 1

        # BASE_URL = 'http://58.56.179.242:8198'  # 山西
    elif len(sys.argv) == 2:
        if sys.argv[1] == '陕西' :
            targetdate = getYesterday()
            flag = 1
        elif sys.argv[1] == '山西':
            targetdate = getYesterday()
            flag = 2
    elif len(sys.argv) == 3:
        if sys.argv[1] == '陕西':
            flag = 1
            targetdate = sys.argv[2]
        elif sys.argv[1] == '山西':
            targetdate = sys.argv[2]
            flag = 2
    else:
        print('传参错误：参数1：省份 参数2：yyyy-mm-dd')


    if flag == 1:
        print("即将爬取省份为陕西")
        BASE_URL = 'http://58.56.179.242:8488'  # 陕西
        province = 'sx'
    elif flag == 2:
        print("即将爬取省份为山西")
        BASE_URL = 'http://58.56.179.242:8198'  # 山西
        province = 's1x'
    print("即将爬取的图片日期为:", targetdate)

    print('省份代号：', province)
    try:
        datePath = re.search('(\d+)-(\d+)-(\d+)', targetdate)
        datePath = datePath.group(1) + datePath.group(2) + datePath.group(3)
        print(datePath)
        main()
        # os.system('cd /home/fallingdust/data/www/snapshot_{}' + '&&' + './yii pbms/get-txt /home/fallingdust/data/PBMS/pbmstxt/{}_{}.txt'.format(province, province, datePath))  # datePath

    except:
        print('爬取{}图片出错'.format(targetdate))

    print(datePath)
    print('cd /home/fallingdust/data/www/snapshot_{}'.format(province) + '&&' + './yii pbms/get-txt /home/fallingdust/data/PBMS/pbmstxt/{}_{}.txt'.format(province, datePath))
    os.system('cd /home/fallingdust/data/www/snapshot_{}'.format(province) + '&&' + './yii pbms/get-txt /home/fallingdust/data/PBMS/pbmstxt/{}_{}.txt'.format(province, datePath))  # datePath




