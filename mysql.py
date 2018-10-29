#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
from config import config

class Db:
    db = ""

    def __init__(self):
        if not self.db:
            self.connect_mysql(config['db'])
    
    def connect_mysql(self, db_config = False):
        if config:
            db = pymysql.connect(db_config['host'], db_config['username'], db_config['passwd'], db_config['dbname'], db_config['port'])
        else:
            db = pymysql.connect("127.0.0.1", "root", "", "my_data", 3306)
        self.db = db.cursor()

    def query(self, sql):
        self.query_status = self.db.execute(sql)
        return self.db.fetchone()

    def __del__(self):
        self.db.close()
        
