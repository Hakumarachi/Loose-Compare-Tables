#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : utils.py
# Author             : Aku
# Date created       : 15 juin 2022

import requests
import json
import re
import rich.spinner
from .logger import console, logger


def get_image_tags(image, filter=''):
    url = f'https://registry.hub.docker.com/v2/repositories/library/{image}/tags?page_size=1024'
    tags = []
    page_number = 1
    with console.status(f"Loading {image} tags (page {page_number})...") as a:
        while url is not None:
            response = requests.get(url)
            response = json.loads(response.content.decode())
            tags += response['results']
            url = response['next']
            page_number += 1 if url is not None else 0
            a.update(f"Loading {image} tags (page {page_number})...")

    logger.debug_json(len(tags))

    tags = [tag['name'] for tag in tags if re.match(filter, tag['name'])]
    logger.info(f"Found {len(tags)} tags that match '{filter}' pattern")

    return tags
