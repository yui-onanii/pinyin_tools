#!/usr/bin/env python3

"""rewrite SRT sub lines with pinyin and print to stdout"""

import argparse

import srt

import gloss

SEPS = '\n 　~～!！(（)）-—「」【】『』〖〗［］〚〛<>«»‹›《》«»‹›⟨⟩〈〉:：;；"“”\'‘’,，.。?？%％#№&$￥*＊+=\\＼/／|｜、·・'

def pad_spaces(frags: list[str]):
	"""like ' '.join(frags) but avoid adding space where a separator already exist"""
	res = []
	last = ''
	for frag in frags:
		if last and not frag in SEPS and not last in SEPS:
			res.append(' ')
		res.append(frag)
		last = frag
	return ''.join(res)

ap = argparse.ArgumentParser()
ap.add_argument('SUB_FILE', type=argparse.FileType('r'))
args = ap.parse_args()

# N.B. srt.parse() returns an generator
subs = list(srt.parse(args.SUB_FILE))

for sub in subs:
	# gloss.gloss() returns list[tuple[str, list[str]]]
	# the tuple contains ("word", ["pinyin for hanzi1", "pinyin for hanzi2", ...])
	pinyins = []
	for _, pinyins_for_word in gloss.gloss(sub.content):
		pinyins.extend(pinyins_for_word)

	pinyin = pad_spaces(pinyins)

	# example:
	#   pinyin for text line 1
	#   original text line 1
	#   pinyin for text line 2
	#   original text line 2
	new_lines = []
	for pinyin_line, sub_line in zip(pinyin.split('\n'), sub.content.split('\n')):
		new_lines.append(pinyin_line + '\n' + sub_line)
	sub.content = '\n'.join(new_lines)

new_srt_contents = srt.compose(subs)
print(new_srt_contents)
