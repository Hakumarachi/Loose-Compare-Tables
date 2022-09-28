#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : sql.py
# Author             : Aku
# Date created       : 10 Jun 2022

import psycopg2

from loose_comparison.utils import Comparator, get_image_tags


class Postgres(Comparator):
    def __init__(self, version='latest'):
        image = 'postgres'
        port = {"5432/tcp": 5432}
        self.environment = {
            'POSTGRES_PASSWORD': 'password',
            'POSTGRES_DB': 'test',
        }
        super(Postgres, self).__init__(image, version, port, self.environment)
        self.version = version
        self.title = "Postgres"
        self.conn = self.connect(5432)

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
                connect_str = f"dbname='{self.environment['POSTGRES_DB']}' user='postgres' host='localhost' " + \
                              f"password='{self.environment['POSTGRES_PASSWORD']}' port='{port}'"
                conn = psycopg2.connect(connect_str)
                return conn
            except psycopg2.OperationalError:
                pass


Language = Postgres


def compare(options):
    filter = options.filter if options.filter else r'.*\d+-alpine$'
    versions = get_image_tags('postgres', filter)
    Comparator.compare(options, Postgres, versions)
