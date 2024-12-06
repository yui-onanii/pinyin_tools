"""common code for writing SSA subtitle files"""

import datetime

# FIXME: i dont know what "Title" does, lets assume its just crap

# the resolution here doesnt matter, so leave it

# A default style is good enough for us

# the first two lines are template code for applying furigana

# FIXME: okay are all these shits in "Script Info" needed?

ASS_HEADER = r'''[Script Info]
; generated by pinyin_tools
Title: Unnamed subtitle file
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: None
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Microsoft YaHei,48,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Comment: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,template syl furi,{\pos($scenter,$smiddle)\an5\k!syl.start_time/10!\k$kdur}
'''

def escape_ssa_txt(s: str) -> str:
	"""currently just escapes all newline chars"""
	return s.replace('\n', '\\N')

def format_ssa_time(time: datetime.timedelta) -> str:
	"""example ==> 1:22:33.44"""
	assert not time.days  # ok, wtf?
	# init vars
	hr = 0
	min = 0
	sec = time.seconds
	ms = time.microseconds // 10000  # note SSA only show 2 digits of MS thus 10000

	# cvt units
	if sec >= 60:
		min = sec // 60
		sec = sec % 60
		if min >= 60:
			hr = min // 60
			min = min % 60

	# pad zeros for min, sec, and ms
	return f'{hr}:{min:02}:{sec:02}.{ms:02}'

class SSAWriter:
	"""note: currently u must handle the SSA tags urself"""

	def __init__(self, fp):
		"""pass a file pointer opened by open('path/to/save/filename.ass', 'r')"""
		self._fp = fp
		self._subs: list[tuple[datetime.timedelta, datetime.timedelta, str]] = []

	def add_sub_line(self, start: datetime.timedelta, end: datetime.timedelta, txt: str):
		"""using same time format as python-srt"""
		self._subs.append((start, end, txt))

	def write(self):
		self._fp.write(ASS_HEADER)
		for start, end, txt in self._subs:
			start_s = format_ssa_time(start)
			end_s = format_ssa_time(end)
			real_txt = escape_ssa_txt(txt)

			# note we are not using Layer, Name, MarginX or Effect
			self._fp.write(f'Dialogue: 0,{start_s},{end_s},Default,,0,0,0,,{real_txt}\n')
		self._fp.close()
