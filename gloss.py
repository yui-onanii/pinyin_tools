#!/usr/bin/env python3

"""gloss chinese sentences in pinyin, word by word"""

import sys
import readline

import common

def PS():
	"""print an input prompt"""
	print('> ', end='', flush=True)

PS()
for line in sys.stdin:
	txt = line.strip()
	words = common.phrase2words(txt)
	for word in words:
		py = common.word2pinyin(word)
		# example: 你好 nǐ hǎo
		print(word, *py)
	PS()
