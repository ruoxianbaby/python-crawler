#!/usr/bin/python
# -*- coding: UTF-8 -*-

from mysql import Db

class Base:
    def __init__(self):
        self.db = Db()

