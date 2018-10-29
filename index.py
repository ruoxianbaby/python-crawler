#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Base import Base
import re
from bs4 import BeautifulSoup
import urllib.request
import requests
import json

class index(Base):
    url = "http://www.btbtdy.net/btdy/"
    url_param = 1
    douban_url = "http://api.douban.com/v2/movie/search?q="
    def __init__(self):
        Base.__init__(self)

    def main(self):
        for i in range(100):
            try:
                self.execute()
            except:
                print(self.url_param - 1)
                return False

    def execute(self):
        url = self.createUrl()
        print(url)
        html_doc = urllib.request.urlopen(url)
        if html_doc:
            soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
            # print(soup)
            if soup:
                # soup.prettify()
                res = soup.title.get_text().split("-")[0]
                print(res)
                if res != '提示信息':
                    query_url = self.douban_url + res + '&start=0&count=1'
                    content = requests.get(query_url).json()
                    if content:
                        print(content['title'])
                        if content['subjects'][0]['id']:
                            print('ok')
                        else:
                          self.error_log()
                    else:
                        self.error_log()
                else:
                   self.error_log() 
            else:
                self.error_log()
        else:
            self.error_log()

    def createUrl(self):
        url = self.url + 'dy' + str(self.url_param) + '.html'
        self.url_param = self.url_param + 1
        return url

    def error_log(self):
        print('error')

    def __del__(self):
        print("end and exit")

index = index()
index.main()




    # def test(self):
    #     sql = "select version()"
    #     return self.db.query(sql)
        
