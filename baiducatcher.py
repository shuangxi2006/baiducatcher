# -*- coding: utf-8 -*-
# !/usr/bin/ python3
"""
Created on Mon Nov 26 08:48:32 2018
catcher 捕捉Baidu新闻关注词
@author: shuangxi2006
"""
import sys
import requests
import pymysql
import lxml.html
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from warnings import filterwarnings

def sendmail(mailtext,subject):
        #使用 163 smtp 以及基本信息赋值
        mail_host = 'smtp.163.com'
        mail_user = ''  # 您的邮箱账户
        mail_pass = ''  # 您的邮箱密码 
        sender = ''     # 您的邮箱地址
        receivers = []  # 收件人, 列表类型, 可以发给多个收件人
        #建立邮件对象
        #smtpObj = smtplib.SMTP()
        #smtpObj.connect(mail_host,465) # 163.com 的邮箱SMTP使用 SSL连接 端口 465 或 994
        smtpObj = smtplib.SMTP_SSL(mail_host,465)
        #登陆邮箱
        smtpObj.login(mail_user,mail_pass)
        message = MIMEText(mailtext,'plain','utf-8')
        #邮件主题
        message['Subject'] = Header(subject)
        #发送人
        message['From']= Header(sender)
        message['To'] = Header(receivers[0])
        smtpObj.sendmail(sender,receivers,message.as_string())
        smtpObj.quit()

db=pymysql.connect(host='localhost',port=3306,user='test',passwd='',db='test',charset='utf8')
cursor = db.cursor()
filterwarnings('error', category = pymysql.Warning)
content=err=''
if len(sys.argv) > 1:
    keyword = sys.argv[1]
else:
    keyword = 'python社区'
print('正在拼命寻找有关 {} 的资讯...'.format(keyword))

head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
mailtext="""
{}

started at:{}

""".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),keyword)

print("Reading...",end="")

for index in range(19):
    url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word={}&x_bfe_rqs=03E80&x_bfe_tjscore=0.004571&tngroupname=organic_news&pn={}'.format(keyword,index*10)
    print(".",end="")
    con = requests.get(url,headers = head)
    con.encoding = 'utf-8'
    content = content + str(con.text)
    content = content.replace('<em>','').replace('</em>','')


sel = lxml.html.fromstring(content)

for i in sel.xpath('//div[@class="result"]'):
    title="".join(i.xpath('./h3/a/text()'))

    if len("".join(i.xpath('./div[1]/text()')))<18:
        summary = "".join(i.xpath('./div[1]/div[2]/text()'))
        mc=i.xpath('./div[1]/div[2]/p/text()')
    else:
        summary="".join(i.xpath('./div[1]/text()'))
        mc=i.xpath('./div[1]/p/text()')

    if len(mc)>1:
        mc=mc[-1].replace('\xa0\xa0',',')
    else:
        mc=mc[0].replace('\xa0\xa0',',')

    mc="".join(mc.split())
    mc=mc.split(',')
    media = mc[0]
    date = mc[1]


    curl="".join(i.xpath('./h3/a/@href'))
    data = ("".join(title.split()), "".join(summary.split()), media, date, curl)
    sql = "INSERT ignore INTO catcher(title,summary,media,date,url)\
    VALUES(%s,%s,%s,%s,%s)"
    try:
        cursor.execute(sql,data)
        err=err+'0'
        mailtext = mailtext+"标题:"+"".join(title.split())+"\n"+"摘要:"+"".join(summary.split())+"\n"+"媒体:"+media+"\n"+"日期: "+date+"\n"+"链接: "+curl+"\n\n"
        db.commit()
    except pymysql.Warning:
        err=err+'1'

if '0' in err:sendmail(mailtext,keyword+'新闻')
cursor.close()
db.close()
print("Done!")
print(err)
