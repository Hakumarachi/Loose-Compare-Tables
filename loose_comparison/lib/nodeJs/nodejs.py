#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : nodejs.py
# Author             : Aku
# Date created       : 11 Jun 2022

import itertools
from loose_comparison.utils import Comparator, get_image_tags, logger


class NodeJS(Comparator):
    def __init__(self, version):
        super(NodeJS, self).__init__('node', version)
        self.version = version
        self.title = f'NodeJS'

        self.comparator = '=='

    def execute(self, query):
        query = query.replace("'", '"')
        command = f"node -e '{query}'"
        logger.debug(command)
        output = self.c.exec_run(command, tty=False).output.decode()
        output = output.split('\n')[:-1]
        logger.debug(output)
        output = [True if element == 'true' else False for element in output]
        return output

    def tests(self) -> list:
        result = list()
        atempt = []
        query = ''
        for test in self.dataset:
            atempt.append([test[0], test[1]])
            query += f"console.log({test[0].lower()}{self.comparator}{test[1].lower()});"
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
        self.c.remove(force=True)
        return result


Language = NodeJS


def compare(options):
    filter = options.filter if options.filter else r'.*\d+-alpine$'
    versions = get_image_tags('node', filter)
    Comparator.compare(options, NodeJS, versions)
