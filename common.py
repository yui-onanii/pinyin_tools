"""shared code, helper, utility funcs"""

import jieba
import pypinyin

def phrase2words(s: str) -> list[str]:
	"""split chinese words in a sentence"""
	return list(jieba.cut(s))

def word2pinyin(w: str) -> list[str]:
	"""return pinyin for each hanzi in a word"""
	pys = pypinyin.pinyin(w)
	res = []
	for x in pys:
		assert len(x) == 1
		res.extend(x)
	return res
