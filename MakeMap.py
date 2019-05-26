#!/usr/bin/env python3

import re
from collections import defaultdict
import json

d = defaultdict(list)
with open('kunyomi.txt', 'r', encoding='utf-8') as fin:
    for line in re.finditer(r'^([^ ]) (.+)$', fin.read(), re.MULTILINE):
        word = line[1]
        yomikata = line[2]
        d[word].append(yomikata)
print(json.dumps(d, ensure_ascii=False, sort_keys=True).replace('], ', '],\n'))
