#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : php.py
# Author             : Aku
# Date created       : 11 Jun 2022

import itertools
from loose_comparison.utils import Comparator, get_image_tags, logger


class PERL(Comparator):
    def __init__(self, version):
        super(PERL, self).__init__('perl', version)
        self.version = version
        self.title = f'Perl'

        self.comparator = '=='

        self.value = [
            "1",
            "0",
            "-1",
            "'1'",
            "'0'",
            "'-1'",
            "''",
            "Null",
            "'John'",
            "'1Jhon'",
            "'0John'",
            "'-1John'",
            "'1e1'",
            "'0e1'",
            "'1e0'",
            "'-1e0'",
            "10",
            "[]",
            "[10]",
            "['1John']",
            "'*'",
            "42",
        ]
    def execute(self, query):
        query = query.replace("'", '"')
        command = f"perl -X -e '{query}'"
        logger.debug(f"Query : {command}")
        output = self.c.exec_run(command, tty=False).output.decode()
        logger.debug(f'Output : {output}')
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
            query += f"""print {test[0]}{self.comparator}{test[1]}? "true\\n" : "false\\n";"""
        try:
            response = self.execute(query)
            result = list(zip(atempt, response))
        except Exception:
            atempt.append('Error')
            result.append(atempt)
        return result

    def run(self):
        self.dataset = itertools.product(self.value, repeat=2)
        result = {}
        self.comparator = '=='
        r = self.tests()
        result[self.comparator] = r
        self.comparator = ' eq '
        self.dataset = itertools.product(self.value, repeat=2)
        r = self.tests()
        result[self.comparator] = r
        self.c.kill()
        return result


Language = PERL


def compare(options):
    filter = options.filter if options.filter else r'^\d+\.\d+\.\d+$'
    versions = get_image_tags('perl', filter)
    Comparator.compare(options, PERL, versions)
