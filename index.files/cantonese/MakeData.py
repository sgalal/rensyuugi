#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from contextlib import closing
from itertools import repeat
import json
import sqlite3
import urllib.request

source_url = 'https://github.com/sgalal/lexi_can_crawler/releases/download/v1.1/data.json'
source = urllib.request.urlopen(source_url).read().decode('utf-8')
data = json.loads(source)

# Single characters

d = defaultdict(set)

for x in data:
	ch = x['ch']
	romanization = x['initial'] + x['rhyme'] + x['tone']
	d[ch].add(romanization)  

# Words

e = defaultdict(set)

for x in data:
	ch = x['ch']
	romanization = x['initial'] + x['rhyme'] + x['tone']
	words = x['words']

	def handle_current_char(current_char):
		if current_char == ch:
			return romanization
		elif len(d[current_char]) == 1:
			return next(iter(d[current_char]))
		else:
			return None

	def handle_word(word):
		res = [handle_current_char(x) for x in word]
		if all(x is not None for x in res):
			return ' '.join(res)
		else:
			return None

	for word in words:
		res = handle_word(word)
		if res is not None:
			e[word].add(res)

g = {k: sorted(v) for k, v in {**d, **e}.items()}

with open('data.json', 'w') as fout:
	print(json.dumps(g, ensure_ascii=False, sort_keys=True).replace('], ', '],\n'), file=fout)
