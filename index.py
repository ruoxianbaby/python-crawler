#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Base import Base

class index(Base):
    def __init__(self):
        Base.__init__(self)

    def main(self):
        sql = "select version()"
        return self.db.query(sql)
        
index = index()
print(index.main())