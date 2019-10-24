#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import json
import re
import urllib.request

source_url = 'https://raw.githubusercontent.com/sugina-dev/sugina/943741f8417e20ec15256aadcd6254009d13127b/config/hanja.txt'
d = defaultdict(list)
for line in re.finditer(r'^([^ ]{2,}) (.+)$', urllib.request.urlopen(source_url).read().decode('utf-8'), re.MULTILINE):
    word = line[1]
    yomikata = line[2]
    d[word].append(yomikata)
with open('data.json', 'w') as fout:
    print(json.dumps(d, ensure_ascii=False, sort_keys=True).replace('], ', '],\n'), file=fout)
