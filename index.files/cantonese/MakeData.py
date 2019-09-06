#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import json
import urllib.request

source_url = 'https://github.com/sgalal/lexi_can_crawler/releases/download/v1.1/data.json'
source = urllib.request.urlopen(source_url).read().decode('utf-8')
data = json.loads(source)

# Single characters

d1 = defaultdict(set)
for x in data:
	ch = x['ch']
	romanization = x['initial'] + x['rhyme'] + x['tone']
	d1[ch].add(romanization)  

# Words

d2 = defaultdict(set)
for x in data:
	ch = x['ch']
	romanization = x['initial'] + x['rhyme'] + x['tone']
	words = x['words']

	def handle_current_char(current_char):
		if current_char == ch:
			return romanization
		elif len(d1[current_char]) == 1:  # Only one pronunciation
			return next(iter(d1[current_char]))

	def handle_word(word):
		res = [handle_current_char(x) for x in word]
		if all(res):
			return ' '.join(res)

	for word in words:
		res = handle_word(word)
		if res is not None:
			d2[word].add(res)

# Merge

d_merged = {k: sorted(v) for k, v in {**d1, **d2}.items()}
with open('data.json', 'w') as fout:
	print(json.dumps(d_merged, ensure_ascii=False, sort_keys=True).replace('], ', '],\n'), file=fout)
