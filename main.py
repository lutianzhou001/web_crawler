#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from urllib import request
from bs4 import BeautifulSoup
import os
import time
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

file_handle = open('latest.txt','r')
latestProject = file_handle.read()
print("初始化成功")
print(latestProject)
file_handle.close()
while True:
    localtime = time.asctime( time.localtime(time.time()) )
    print("[START]",localtime)
    url="https://www.jxsggzy.cn/web/jyxx/002001/002001001/jyxx.html"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(url,headers=headers)
    page_info = request.urlopen(page).read().decode('utf-8')#打开Url,获取HttpResponse返回对象并读取其ResposneBody
    # 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
    soup = BeautifulSoup(page_info, 'html.parser')
    # 以格式化的形式打印html
    res = soup.find_all(name='a', attrs={"class": "ewb-list-name"})
    print(res[0].text)
    if res[0].text != latestProject:
        file_handle = open('latest.txt','w')
        latestProject = res[0].text
        file_handle.write(latestProject)
        file_handle.close()
        url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"
        payload = "{\"personalizations\": [{\"to\": [{\"email\": \"540854429@qq.com\"},{\"email\": \"840436489@qq.com\"}],\"subject\": \"" + latestProject + "\"}],\"from\": {\"email\": \"lutianzhou@sjtu.edu.cn\"},\"content\": [{\"type\": \"text/plain\",\"value\": \"Hello, World!\"}]}"
        headers = {'content-type': "application/json",'x-rapidapi-host': "rapidprod-sendgrid-v1.p.rapidapi.com",'x-rapidapi-key': "ae2ad23146msh06a431323e86027p11a924jsn731ce3762748"}
        response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)
        print(response.text)
    time.sleep(3)

