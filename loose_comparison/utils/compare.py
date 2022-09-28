#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : compare.py
# Author             : Aku
# Date created       : 10 Jun 2022


import itertools
import docker
import os
import shutil
import json

import rich.terminal_theme
from rich.console import Console, CONSOLE_SVG_FORMAT
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn, MofNCompleteColumn
from rich.terminal_theme import MONOKAI
from .logger import logger, console
from abc import ABC, abstractmethod

client = docker.from_env()
logo = open("./logo.svg").read()
CONSOLE_SVG_FORMAT2 = """\
<svg width="{total_width}" height="{total_height}" viewBox="0 0 {total_width} {total_height}"
     xmlns="http://www.w3.org/2000/svg">
    <style>
        @font-face {{
            font-family: "{font_family}";
            src: local("FiraCode-Regular"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Regular.woff2") format("woff2"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Regular.woff") format("woff");
            font-style: normal;
            font-weight: 400;
        }}
        @font-face {{
            font-family: "{font_family}";
            src: local("FiraCode-Bold"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Bold.woff2") format("woff2"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Bold.woff") format("woff");
            font-style: bold;
            font-weight: 700;
        }}
        .{classes_prefix}-terminal-wrapper span {{
            display: inline-block;
            white-space: pre;
            vertical-align: top;
            font-size: {font_size}px;
            font-family:'{font_family}','Cascadia Code',Monaco,Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace;
        }}
        .{classes_prefix}-terminal-wrapper a {{
            text-decoration: none;
            color: inherit;
        }}
        .{classes_prefix}-terminal-body .blink {{
           animation: {classes_prefix}-blinker 1s infinite;
        }}
        @keyframes {classes_prefix}-blinker {{
            from {{ opacity: 1.0; }}
            50% {{ opacity: 0.3; }}
            to {{ opacity: 1.0; }}
        }}
        .{classes_prefix}-terminal-wrapper {{
            padding: {margin}px;
            padding-top: 100px;
        }}
        .{classes_prefix}-terminal {{
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: {theme_background_color};
            border-radius: 14px;
            box-shadow: 0 0 0 1px #484848;
        }}
        .{classes_prefix}-terminal-header {{
            position: relative;
            width: 100%;
            background-color: #2e2e2e;
            margin-bottom: 12px;
            font-weight: bold;
            border-radius: 14px 14px 0 0;
            color: {theme_foreground_color};
            font-size: 18px;
            box-shadow: inset 0px -1px 0px 0px #4e4e4e,
                        inset 0px -4px 8px 0px #1a1a1a;
        }}
        .{classes_prefix}-terminal-title-tab {{
            display: inline-block;
            margin-top: 14px;
            margin-left: 124px;
            font-family: sans-serif;
            padding: 14px 28px;
            border-radius: 6px 6px 0 0;
            background-color: {theme_background_color};
            box-shadow: inset 0px 1px 0px 0px #4e4e4e,
                        0px -4px 4px 0px #1e1e1e,
                        inset 1px 0px 0px 0px #4e4e4e,
                        inset -1px 0px 0px 0px #4e4e4e;
        }}
        .{classes_prefix}-terminal-traffic-lights {{
            position: absolute;
            top: 24px;
            left: 20px;
        }}
        .{classes_prefix}-terminal-link {{
            position: absolute;
            top: 24px;
            right: 20px;
            font-family: sans-serif;
            color: #fff
        }}
        .{classes_prefix}-terminal-logo {{
            position: absolute;
            top: 14px;
            right: 150px;
            border-radius: 15px;
            width : 40px;
            height: 40px;
        }}
        .{classes_prefix}-terminal-body {{
            line-height: {line_height}px;
            padding: 14px;
        }}
        {stylesheet}
    </style>
    <foreignObject x="0" y="0" width="100%" height="100%">
        <body xmlns="http://www.w3.org/1999/xhtml">
            <div class="{classes_prefix}-terminal-wrapper">
                <div class="{classes_prefix}-terminal">
                    <div class="{classes_prefix}-terminal-header">
                        <svg class="{classes_prefix}-terminal-traffic-lights" width="90" height="21" viewBox="0 0 90 21" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="14" cy="8" r="8" fill="#ff6159"/>
                            <circle cx="38" cy="8" r="8" fill="#ffbd2e"/>
                            <circle cx="62" cy="8" r="8" fill="#28c941"/>
                        </svg>
                        """ + logo + """
                        <div class="{classes_prefix}-terminal-link" x="0" y="15">@Akumarachi</div>
                        <div class="{classes_prefix}-terminal-title-tab">{title}</div>
                    </div>
                    <div class="{classes_prefix}-terminal-body">
                        {code}
                    </div>
                </div>
            </div>
        </body>
    </foreignObject>
</svg>
        """
class Comparator(ABC):
    def __init__(self, image=None, version='latest', port={}, environment={}, volume=False):
        logger.debug(image)
        self.image = f'{image}:{version}'
        self.value = [
            "True",
            "False",
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
        self.volume = None
        if image:
            if volume:
                self.volume = f'/tmp/{image}-{version}'
                try:
                    os.mkdir(self.volume)
                except FileExistsError as e:
                    logger.error(e)
            volume = [f'{self.volume}:/tmp'] if volume else []
            logger.debug(f'Creating container {self.image}')
            self.c = client.containers.run(
                self.image,
                tty=True, detach=True,
                remove=True, ports=port,
                environment=environment,
                volumes=volume
            )

        self.template = {
            True: '[green]%s[/green]',
            False: '[red]%s[/red]',
            'err': '[purple]Error[/purple]',
            None: '[blue]Null[/blue]'
        }

        self.title = 'Comparator'
        self.table = dict()

        self.dataset = itertools.product(self.value, repeat=2)

    def process(self, result, version, verbose):
        for comparator in result:
            self.__process(result[comparator])
            self.__print_table(comparator=comparator, languages=version, verbose=verbose)
            self.__save_json(result, version[0].version)

    def __process(self, result=None):
        self.table = dict()
        for atempt in result:
            p1 = atempt[0][0]
            p2 = atempt[0][1]
            r = atempt[1]
            if r == 1:
                r = True
            elif r == 0:
                r = False
            if r is not None:
                if r == 1:
                    r = self.template[p1 == p2] % r
                elif r == 0:
                    if p1 == p2:
                        r = self.template[False] % r
                    else:
                        r = 'False'
                else:
                    r = self.template['err']
            else:
                r = self.template[r]
            if p1 in self.table:
                self.table[p1].append(r)
            else:
                self.table[p1] = [r]

    def __save(self, console, languages, comparator):
        path = os.path.join("results", self.title, languages[0].version)
        os.makedirs(path, exist_ok=True)
        console.save_svg(f"{os.path.join(path, self.title)}_{languages[0].version}_{comparator}.svg",
                         title=f"{self.title}", theme=MONOKAI, code_format=CONSOLE_SVG_FORMAT2)

    def __save_json(self, result, version):
        path = os.path.join("results", self.title, version)
        os.makedirs(path, exist_ok=True)
        with open(f'{os.path.join(path, self.title)}_{version}.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

    def __print_table(self, comparator=None, languages=None, verbose=False):
        title = f'{self.title} [bold green]{languages[0].version}[/bold green]' if len(languages) == 1 else self.title
        title = f'{title} with {comparator}' if comparator else title
        table = Table(title=title)
        table.add_column("", justify="center", style="bold")
        for v in self.table:
            table.add_column(v, justify="center")
        for k in self.table:
            table.add_row(*([k] + self.table[k]))
        console = Console(record=True)
        console.print(table, justify="center")
        self.__save(console, languages, comparator)
        logger.info(f'{len(languages)} version of [bold green]{self.title}[/bold green] match this array')
        logger.verbose_json([v.version for v in languages])

    def __del__(self):
        if self.volume:
            pass
            # shutil.rmtree(self.volume)

    @abstractmethod
    def tests(self):
        raise NotImplementedError('This method should be implemented by subclass')

    def run(self):
        result = self.tests()
        return result

    @staticmethod
    def compare(options, Language, versions=None):
        client = docker.from_env()
        if versions is None:
            versions = ['latest']
        logger.debug_json(versions)
        result = []
        images = []
        with Progress(SpinnerColumn(),
                      *Progress.get_default_columns(),
                      TimeElapsedColumn(), MofNCompleteColumn()) as progress:
            t = progress.add_task("", total=len(versions))
            for version in versions:
                progress.update(description=f'Processing version [blue]{version}[/blue]', task_id=t)
                try:
                    language = Language(version)
                    images.append(language.image)
                    while len(images) > 1:
                        logger.debug_json(images)
                        client.images.remove(images.pop(0), True)
                    r = language.run()
                    filtered = None
                    if not options.all:
                        filtered = list(filter(lambda test: test['result'] == r, result))
                    if not filtered:
                        result.append({'version': [language], 'result': r})
                        if options.all:
                            language.process(r, [language], options.verbose)
                    else:
                        filtered[0]['version'] += [language]
                except Exception as e:
                    logger.error(e)
                progress.advance(t)

        if not options.all:
            for r in result:
                r['version'][0].process(r['result'], r['version'], options.verbose)
