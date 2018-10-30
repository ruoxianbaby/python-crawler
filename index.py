#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import sys
import urllib.request
import requests
import json
import time
from bs4 import BeautifulSoup
from Base import Base

class index(Base):
    url = "http://www.btbtdy.net/btdy/"
    url_param = 1
    proxy = ""
    ip_error = 0
    proxy_num = 0
    douban_url = "http://api.douban.com/v2/movie/search?q="

    def __init__(self):
        Base.__init__(self)
        self.init_url_param()

    def init_url_param(self):
        sql = "select param from exit_status order by id desc limit 0,1"
        res = self.db.query(sql)
        if res:
            self.url_param = int(res[0]) + 1
            print(self.url_param)

    def main(self):
        for i in range(10000):
            self.execute()

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
                    # content = requests.get(query_url).json()
                    content = self.http_douban(query_url)
                    if content:
                        content = content.json()
                        # print(content)
                        try:
                            content['total']
                            if content['total'] == 0:
                                error = ["content.total为0", res + '--豆瓣没搜索到这条记录', self.url_param]
                            else:
                                doubane_id = content['subjects'][0]['id']
                                self.write_record(content, doubane_id, res)
                                self.url_param = self.url_param + 1
                                self.ip_error = 0
                        except:
                            error = ['请求失败', 'ip限制,或者其他权限问题或者反斜杠的问题 或者豆瓣没正确返回--' + res , self.url_param]
                            self.error_log(error)
                            if self.ip_error > 5:
                                sys.exit()
                            self.ip_error += 1                     
                            
                    else:
                        error = ['http_douban(query_url)执行失败', query_url + '代理IP可能有问题,网络未正确返回--豆瓣', self.url_param]
                else:
                    print('bt电影-资源已被移除')
                    error = ['bt电影-资源已被移除', url + '的页面不存在', self.url_param]
            else:
                error = ['BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")执行失败', '', self.url_param]                
        else:
            error = ['urllib.request.urlopen(url)执行失败', 'urllib.request.urlopen(url),url为:' + url, self.url_param]
        if error != '':
            self.error_log(error)

    def write_record(self, content, doubane_id, messages):
        cc = json.dumps(content)
        create_time = self.datetime()
        sql = "insert into `bt_douban_result` (bt_type, bt_num, douban_id, result, create_time) values ('%s', '%s','%s','%s','%s')" % ('film', self.url_param, doubane_id, cc, create_time)
        res = self.db.query(sql)
        if res != None:
            print("写入失败: ", messages)
            error = ('sql写入失败,标题是: ' + messages, '错误的sql: ' + sql, self.url_param)
            self.error_log(error)
        else:
            print("success: ", messages)

    def http_douban(self, query_url):
        retry_count = 3 # 连续4次IP都不行退出
        proxy = ""
        while retry_count > 0:
            try:
                proxy = self.get_proxy()
                print(proxy)
                html = requests.get(query_url, proxies={"http": "http://{}".format(proxy)}, timeout=8)
                return html
            except Exception:
                self.delete_proxy(proxy)
                retry_count -= 1
        return False

    def get_proxy(self):
        if not self.proxy or self.proxy_num > 50:
            self.proxy_num = 0
            self.proxy = requests.get("http://127.0.0.1:5010/get/").text
        else:
            self.proxy_num += 1
        return self.proxy
    
    def delete_proxy(self, proxy):
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

    def createUrl(self):
        url = self.url + 'dy' + str(self.url_param) + '.html'
        return url

    def datetime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    def error_log(self, error):
        sql = "INSERT INTO `error_log` (error_type, error_message, error_num) VALUES ('%s', '%s', '%s') " % (error[0], error[1], error[2])
        res = self.db.query(sql)
        if res:
            print("error success")
        self.url_param = self.url_param + 1

    def __del__(self):
        sql = "insert into exit_status (param) values ('%s')" % (self.url_param)
        self.db.query(sql)
        print("last param is: %s" % (self.url_param))
        print("end and exit")

index = index()
index.main()
