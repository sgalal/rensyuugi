#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from contextlib import closing
from itertools import repeat
import json
import sqlite3
import urllib.request

source_url = 'https://github.com/sgalal/lexi_can_crawler/releases/download/v1.0/data.json'
source = urllib.request.urlopen(source_url).read().decode('utf-8')
data = json.loads(source)

d = defaultdict(list)

# Processing

for x in data:
	character = x['character']
	romanization = x['romanization']
	d[character].append(romanization)  # Dump single characters

# Calculate words

with closing(sqlite3.connect(':memory:')) as conn:
	cur = conn.cursor()

	cur.execute('''
		CREATE TABLE 'characters'
		( 'id'           INTEGER PRIMARY KEY
		, 'character'    TEXT NOT NULL
		, 'romanization' TEXT NOT NULL
		);
		''')

	cur.executemany('INSERT INTO characters VALUES (?, ?, ?)', ((i, x['character'], x['romanization']) for i, x in enumerate(data)))

	conn.commit()

	def get_unique_pron(cur, ch):
		'''
		Return the unique romanization if it is unique,
		otherwise return None.
		'''
		try:
			pron_count = next(cur.execute(f"SELECT COUNT(*) FROM characters WHERE character = '{ch}' GROUP BY character;"))[0] == 1
		except StopIteration:
			pron_count = 0

		if pron_count == 1:  # Has unique pronunciation
			return next(cur.execute(f"SELECT romanization FROM characters WHERE character = '{ch}';"))[0]

	for i, x in enumerate(data):
		romanization = x['romanization']
		character = x['character']

		for word in x['words']:
			def process(ch):
				if ch == character:
					return romanization
				else:
					return get_unique_pron(cur, ch)

			res = [process(ch) for ch in word]

			if all(x is not None for x in res):
				pron = ' '.join(res)

				if pron not in d[word]:
					d[word].append(pron)  # Dump words

with open('data.json', 'w') as fout:
	print(json.dumps(d, ensure_ascii=False, sort_keys=True).replace('], ', '],\n'), file=fout)
