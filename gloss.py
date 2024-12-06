#!/usr/bin/env python3

"""gloss chinese sentences in pinyin, word by word"""

import common

def gloss(line: str) -> list[tuple[str, list[str]]]:
	"""gloss a line of text,
	output will be a list of ("word", ["pinyin for hanzi1", "pinyin for hanzi2", ...])"""
	words = common.phrase2words(line)
	res = []
	for word in words:
		pinyins = common.word2pinyin(word)
		res.append((word, pinyins))
	return res

def main():
	def PS():
		"""print an input prompt"""
		print('> ', end='', flush=True)

	PS()
	for line in sys.stdin:
		txt = line.strip()
		glosses = gloss(txt)
		for word, pinyins in glosses:
			# example: 你好 nǐ hǎo
			print(word, *pinyins)
		PS()

if __name__ == '__main__':
	import sys

	main()
