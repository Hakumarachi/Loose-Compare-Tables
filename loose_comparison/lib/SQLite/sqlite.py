#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : sql.py
# Author             : Aku
# Date created       : 10 Jun 2022

import sqlite3

from loose_comparison.utils import Comparator, logger


class SQLite(Comparator):
    def __init__(self, version):
        self.version = sqlite3.version
        super(SQLite, self).__init__()
        self.title = 'SQLite'
        self.conn = self.connect()

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
            except Exception as e:
                atempt.append('Error')
                result.append(atempt)
            self.conn.commit()
            c.close()
        return result

    def connect(self):
        conn = sqlite3.connect('test.db')
        return conn

    def run(self):
        result = {}
        r = self.tests()
        result['='] = r
        return result


Language = SQLite


def compare(options):
    Comparator.compare(options, SQLite)
