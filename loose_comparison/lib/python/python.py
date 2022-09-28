#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : python.py
# Author             : Aku
# Date created       : 11 Jun 2022

import itertools
from loose_comparison.utils import Comparator, get_image_tags, logger


class Python(Comparator):
    def __init__(self, version):
        super(Python, self).__init__('python', version)
        self.version = version
        self.title = f'Python'

        self.comparator = '=='

    def execute(self, query):
        query = query.replace("'", '"')
        query = query.replace('Null','None')
        command = f"python -W ignore -c '{query}'"
        logger.debug(f"Query : {command}")
        output = self.c.exec_run(command, tty=False).output.decode()
        logger.debug(output)
        output = output.split('\n')[:-1]
        output = [True if a == 'True' else False for a in output if a == "True" or a == 'False']
        logger.debug(f'Output : {output}')
        return output

    def tests(self) -> list:
        result = list()
        atempt = []
        query = ''
        for test in self.dataset:
            atempt.append([test[0], test[1]])
            query += f"""print({test[0]}{self.comparator}{test[1]});"""
        try:
            response = self.execute(query)
            result = list(zip(atempt, response))
        except Exception:
            atempt.append('Error')
            result.append(atempt)
        return result

    def run(self):
        result = {}
        self.comparator = '=='
        r = self.tests()
        result[self.comparator] = r
        self.comparator = ' is '
        self.dataset = itertools.product(self.value, repeat=2)
        r = self.tests()
        result[self.comparator] = r
        self.c.kill()
        return result


Language = Python


def compare(options):
    filter = options.filter if options.filter else r'.*\d+-alpine$'
    versions = get_image_tags('python', filter)
    Comparator.compare(options, Python, versions)
