#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Base import Base
import re
from bs4 import BeautifulSoup
import urllib.request
import requests
import json
import time

class index(Base):
    url = "http://www.btbtdy.net/btdy/"
    url_param = 399
    douban_url = "http://api.douban.com/v2/movie/search?q="
    
    def __init__(self):
        Base.__init__(self)

    def main(self):
        for i in range(10000):
            try:
                self.execute()
            except:
                print(self.url_param)
                self.url_param = self.url_param + 1
                self.main()

    def execute(self):
        url = self.createUrl()
        html_doc = urllib.request.urlopen(url)
        error = ''
        if html_doc:
            soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
            if soup:
                res = soup.title.get_text().split("-")[0]
                if res != '提示信息':
                    query_url = self.douban_url + res + '&start=0&count=1'
                    content = requests.get(query_url).json()
                    if content:
                        if content['subjects'][0]['id']:
                            self.url_param = self.url_param + 1
                            print('ok')
                        else:
                          error = ["content['subjects'][0]['id']", res + '豆瓣没搜索到这条记录', self.url_param]
                    else:
                        error = ['requests.get(query_url).json()执行失败', query_url + '未正确返回--豆瓣,可能ip问题', self.url_param]
                else:
                   error = ['bt电影-资源已被移除', url + '的页面不存在', self.url_param]
            else:
                error = ['BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")执行失败', '', self.url_param]                
        else:
            error = ['urllib.request.urlopen(url)执行失败', 'urllib.request.urlopen(url),url为:' + url, self.url_param]
        if error != '':
            self.error_log(error)

    def createUrl(self):
        url = self.url + 'dy' + str(self.url_param) + '.html'
        return url

    def datetime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    def error_log(self, error):
        sql = "INSERT INTO `error_log` (error_type, error_message, error_num) VALUES ('%s', '%s', '%s') " % (error[0], error[1], error[2])
        print(sql)
        # res = self.db.query(sql)
        # if res:
        #     print("error success")

    def __del__(self):
        print("end and exit")

index = index()
index.main()
