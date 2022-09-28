#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : sql.py
# Author             : Aku
# Date created       : 10 Jun 2022

import pymysql

from loose_comparison.utils import Comparator, get_image_tags


class Mysql(Comparator):
    def __init__(self, version='latest'):
        image = 'mysql'
        port = {"3306/tcp": 3306}
        self.environment = {
            'MYSQL_ROOT_PASSWORD': 'password',
            'MYSQL_DATABASE': 'test',
        }
        super(Mysql, self).__init__(image, version, port, self.environment)
        self.version = version
        self.title = image.capitalize()
        self.conn = self.connect(3306)

    def tests(self) -> list:
        result = list()
        for test in self.dataset:
            atempt = [[test[0], test[1]]]
            query = f"select {test[0]}={test[1]}"
            c = self.conn.cursor()
            try:
                c.execute(query)
                response = c.fetchall()
                for r in response:
                    atempt.append(r[0])
                    result.append(atempt)
            except Exception:
                atempt.append('Error')
                result.append(atempt)
            self.conn.commit()
            c.close()
        return result

    def run(self):
        result = {}
        r = self.tests()
        result['='] = r
        self.c.kill()
        return result

    def connect(self, port):
        conn = None
        while not conn:
            try:
                conn = pymysql.connect(
                    host='127.0.0.1',
                    user='root',
                    password=self.environment['MYSQL_ROOT_PASSWORD'],
                    db=self.environment['MYSQL_DATABASE'],
                    port=port
                )
                return conn
            except pymysql.OperationalError:
                pass


Language = Mysql


def compare(options):
    filter = options.filter if options.filter else r'.*\d+-debian$'
    versions = get_image_tags('mysql', filter)
    Comparator.compare(options, Mysql, versions)
