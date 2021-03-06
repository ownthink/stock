#!/usr/bin/env python3
# coding: utf-8
import time
from datetime import datetime
import re
import json
import requests
import smtplib
from email.header import Header
from email.mime.text import MIMEText


# from src.conf import Conf

def send_email(text):
    fromaddr = 'monitor@ownthink.com'
    password = 'Adeal.ggzy.gov.cn'
    toaddrs = ['denghaiai@ownthink.com', 'yener@ownthink.com']

    message = MIMEText(text, 'plain', 'utf-8')
    message['Subject'] = Header('投标交易公告', 'utf-8')
    message['From'] = Header("系统监测", 'utf-8')
    message['To'] = Header("查收", 'utf-8')

    try:
        server = smtplib.SMTP('smtp.mxhichina.com')
        server.login(fromaddr, password)
        server.sendmail(fromaddr, toaddrs, message.as_string())
        print('success')
        server.quit()
    except smtplib.SMTPException as e:
        print('error', e)


Regx = re.compile("(([1-9]\\d*[\\d,，]*\\.?\\d*)|(0\\.[0-9]+))(元|百万|万元|亿元|万|亿)")


def filter_money(html):
    '''
    todo...
    '''
    result = Regx.search(html)
    money_list = []
    if result != None:
        money_list.append(result.group())
    return money_list


def filter_html(text):
    biao = re.findall('<.*?>', text)
    for b in biao:
        text = text.replace(b, '')
    text = text.replace('&nbsp;', '').replace('）', '')
    return text


def deal_page(title, url):
    url_head = 'http://www.ggzy.gov.cn/information'

    # url = 'http://www.ggzy.gov.cn/information/html/a/440000/0201/201903/15/0044aa96457d9cc44ef6894964dab52f5272.shtml'
    # print(url)
    url = url.replace('/html/a/', '/html/b/')
    print(url)

    sess = requests.get(url)
    html = sess.text

    project_num = re.findall('项目编号：[\s\S]*?</p>', html)
    if project_num:
        project_num = filter_html(project_num[0])
    else:
        project_num = ''

    html = filter_html(html)
    result = filter_money(html)

    str_contens_ok = not_contents(html)

    money_ok = False
    print('ttttttttttttt')
    for res in result:

        if res.find('亿') >= 0:
            money_ok = True
            break
        elif res.find('万元') >= 0:
            if len(res.replace('万元', '').replace(',', '').split('.')[0]) > 4:
                money_ok = True
                break
        elif res.find('元') >= 0:
            if len(res.replace('元', '').replace(',', '').split('.')[0]) > 8:
                money_ok = True
                break



    if str_contens_ok and money_ok:
        text = 'title:%s \nurl:%s \nmoney:%s \nnum:%s\n' % (title, url, ' '.join(result), project_num)
        print(text)

        sendmessage(text)

    # sys.exit(0)
    else:
        # print('不发送')
        pass


def sendmessage(message):

    url ='https://oapi.dingtalk.com/robot/send?access_token=db64d570dd4d34c29488b0d2f205fe82081614d89c69a0d7c3a3adf32ba1a92e'
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    message = message
    String_textMsg = {
        "msgtype": "text",
        "text": {"content": message},
         "at": {
            "atMobiles": [
                "130xxxxxxxx"                                    #如果需要@某人，这里写他的手机号
            ],
            "isAtAll": 1                                         #如果需要@所有人，这些写1
        }
    }
    String_textMsg = json.dumps(String_textMsg)

    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)


def not_contents(html):
    if contentsStr(html):
        return True

    notList = ['勘探', '勘察', '市政工程', '建设用地', '建筑工程', '土地用途']

    for str in notList:
        print(html.find(str))
        if (html.find(str) > -1):
            return False

    return True



def contentsStr(html):


    list = ['贵州省德江']
    for str in list:
        print(html.find(str))
        if (html.find(str) > -1):
            return True
    return False


def now_time():
    localtime = time.localtime(time.time())
    date = datetime(localtime.tm_year, localtime.tm_mon, localtime.tm_mday, localtime.tm_hour, localtime.tm_min,
                    localtime.tm_sec)
    return date


def process():
    localtime = time.localtime(time.time())
    begin_date = '%s-%s-01' % (localtime.tm_year, localtime.tm_mon)
    end_date = '%s-%s-%s' % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday)

    head_data = {
        'TIMEBEGIN_SHOW': begin_date,
        'TIMEEND_SHOW': end_date,
        'TIMEBEGIN': begin_date,
        'TIMEEND': end_date,
        'SOURCE_TYPE': '1',
        'DEAL_TIME': '02',
        'DEAL_CLASSIFY': '00',
        'DEAL_STAGE': '0000',
        'DEAL_PROVINCE': '0',
        'DEAL_CITY': '0',
        'DEAL_PLATFORM': '0',
        'BID_PLATFORM': '0',
        'DEAL_TRADE': '0',
        'isShowAll': '1',
        'PAGENUMBER': '1',
        'FINDTXT': '',
        'validationCode': ''
    }

    url = 'http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp'
    sess = requests.post(url=url, data=head_data)
    result = sess.text
    result = json.loads(result)
    pageCount = result['ttlpage']





    for i in range(1, pageCount):
        dict2 = {'PAGENUMBER': i}
        head_data.update(dict2)
        print(head_data)
        sess = requests.post(url=url, data=head_data)
        result = sess.text
        result = json.loads(result)
        data = result['data']
        for info in data:
            deal_page(info['title'], info['url'])


if __name__ == '__main__':
    process()
