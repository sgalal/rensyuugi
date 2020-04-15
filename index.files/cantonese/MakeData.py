#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import json
import os
import re
import sys
import urllib.request

here = os.path.dirname(os.path.abspath(__file__))

def skip_header(response):
    it = iter(response.readlines())
    while True:
        if next(it).decode('utf-8') == '...\n':
            break
    next(it)
    for line in it:
        str = line.decode('utf-8')
        if str and str[0] != '#':
            yield str

source_url = 'https://raw.githubusercontent.com/rime/rime-cantonese/15b9bb92187653ef9ae6439f15b83deb987608c0/jyut6ping3.dict.yaml'
d = defaultdict(list)
pattern = re.compile(r'^([^\t\n]+)\t([^\t\n]+)')

for line in skip_header(urllib.request.urlopen(source_url)):
    match = pattern.match(line)
    try:
        word = match[1]
        yomikata = match[2]
        if len(word) > 1:
            d[word].append(yomikata)
    except TypeError:
        print(line, file=sys.stderr)

with open(os.path.join(here, 'data.json'), 'w') as fout:
    print(json.dumps(d, ensure_ascii=False, sort_keys=True).replace('], ', '],\n'), file=fout)
