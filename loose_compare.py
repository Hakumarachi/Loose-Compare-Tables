#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : main.py
# Author             : Aku
# Date created       : 20 mai 2022

import argparse

from loose_comparison.utils import logger
from loose_comparison import lib


import importlib
import pkgutil


def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

discovered_plugins = {
    f'{name}'.split('.')[2]: importlib.import_module(name)
    for finder, name, ispkg
    in iter_namespace(lib)
}


def parse_args():
    parser = argparse.ArgumentParser(description="Description message")
    parser.add_argument("-l", "--language", default=None, help='select a specific language to test')
    parser.add_argument("--version", default=None, help='select a specific version of a language to test')
    parser.add_argument("--filter", default=None, help='select a specific filter to get version of a language to test')
    parser.add_argument("-L", "--list-languages", action='store_true', default=False, help='list available language')
    parser.add_argument("-q", "--quiet", action='store_true', default=False, help='avoid all messages')
    parser.add_argument("-v", "--verbose", default='info', help='Verbose mode. (default: False)')
    parser.add_argument("--all", action='store_true', default=False, help='parse all version')
    return parser.parse_args()


if __name__ == '__main__':
    options = parse_args()
    logger.set_verbosity(options.verbose.upper(), options.quiet)
    if options.list_languages:
        logger.info('All available languages :')
        for k in discovered_plugins.keys():
            logger.success(k, 1)
    elif options.language:
        if options.language in discovered_plugins:
            if options.version:
                test = discovered_plugins[options.language].Language(options.version)
                r = test.run()
                test.process(r, [test], options.verbose)
            else:
                discovered_plugins[options.language].compare(options)
        else:
            logger.error(f'Unable to find {options.language} language')
    else:
        for language in discovered_plugins:
            logger.info(f'Testing language : {language}')
            discovered_plugins[language].compare(options)
