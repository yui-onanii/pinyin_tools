#!/usr/bin/env python3

"""attach pinyin on top of SRT subtitle lines (WIP)
note, this parses SRT and turns it into SSA format,
currently it will only work for trivial cases."""

import argparse
import sys

import srt

import ass_common
import common
import gloss

ap = argparse.ArgumentParser()
ap.add_argument('SUB_FILE', type=argparse.FileType('r'))
args = ap.parse_args()

subs = common.parse_srt(args.SUB_FILE)
ssa = ass_common.SSAWriter(sys.stdout)

for sub in subs:
	new_txt = []
	for og_txt, pinyins in gloss.gloss(sub.content):
		if len(pinyins) == 1 and og_txt == pinyins[0]:
			new_txt.append(og_txt)
			continue

		pinyin = ' '.join(pinyins)
		new_txt.append(f'{og_txt}|<{pinyin}')
	ssa.add_sub_line(sub.start, sub.end, r'{\k0}'.join(new_txt))

ssa.write()
