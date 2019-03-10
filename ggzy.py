import time
from datetime import datetime
import re
import json
import requests
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def send_email(text):
	fromaddr = 'monitor@ownthink.com'
	password = 'Adeal.ggzy.gov.cn'
	toaddrs = ['14476239@qq.com', '158760520@qq.com']
	 
	message = MIMEText(text, 'plain','utf-8')  
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
	result = Regx.search(html)
	money_list = []
	if result != None:
		money_list.append(result.group())
	return money_list
		
def deal_page(title, url):
	url_head = 'http://www.ggzy.gov.cn/information'
	sess = requests.get(url)
	html = sess.text
	detail_url = re.findall('''onclick="showDetail\(this, '.*?','(.*?)'\)">''', html)
	for detail in detail_url:
		url = url_head + detail
		sess = requests.get(url)
		html = sess.text
		result = filter_money(html)
		if result != []:
			text = 'title:%s \nurl:%s \nmoney:%s \n'%(title, '手工根据title检索url', ' '.join(result))
			
			print(text)
			
			send_email(text)
			
			sys.exit(0)
			
def now_time():
	localtime = time.localtime(time.time())
	date = datetime(localtime.tm_year, localtime.tm_mon, localtime.tm_mday, localtime.tm_hour, localtime.tm_min, localtime.tm_sec)
	return date
	
def process():
	localtime = time.localtime(time.time())
	date = '%s-%s-%s'%(localtime.tm_year, localtime.tm_mon, localtime.tm_mday)
	
	data = {
		'TIMEBEGIN_SHOW': date,
		'TIMEEND_SHOW': date,
		'TIMEBEGIN': date,
		'TIMEEND': date,
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
	sess = requests.post(url=url, data=data)
	result = sess.text
	result = json.loads(result)
	data = result['data']
	for info in data:
		print(info['title'])
		continue
		deal_page(info['title'], info['url'])

if __name__ == '__main__':
	process()
