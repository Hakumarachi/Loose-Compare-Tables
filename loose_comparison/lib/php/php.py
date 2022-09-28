#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : php.py
# Author             : Aku
# Date created       : 11 Jun 2022

import itertools
from loose_comparison.utils import Comparator, get_image_tags, logger


class PHP(Comparator):
    def __init__(self, version):
        super(PHP, self).__init__('php', version)
        self.version = version
        self.title = f'PHP'

        self.comparator = '=='

    def execute(self, query):
        query = query.replace("'", '"')
        command = f"php -r '{query}'"
        logger.debug(f"Query : {command}")
        output = self.c.exec_run(command, tty=False).output.decode()
        output = output.split('\n')[:-1]
        output = [True if element == 'true' else False for element in output]
        logger.debug(f'Output : {output}')
        return output

    def tests(self) -> list:
        result = list()
        atempt = []
        query = ''
        for test in self.dataset:
            atempt.append([test[0], test[1]])
            query += f"""echo ({test[0]}{self.comparator}{test[1]}) ? "true\\n" : "false\\n";"""
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
        self.comparator = '==='
        self.dataset = itertools.product(self.value, repeat=2)
        r = self.tests()
        result[self.comparator] = r
        self.c.kill()
        return result


Language = PHP


def compare(options):
    filter = options.filter if options.filter else r'.*\d+-alpine$'
    versions = get_image_tags('php', filter)
    Comparator.compare(options, PHP, versions)
