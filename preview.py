#!/usr/bin/env python3
"""preview.py font.png greek_dialog.txt out.png [ID ...]  -- approximate picture of dialogue lines in the game font."""
import sys, re
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from apply_greek import to_ascii
from PIL import Image
font = Image.open(sys.argv[1])
def tile(t): return font.crop(((t % 16) * 8, (t // 16) * 8, (t % 16) * 8 + 8, (t // 16) * 8 + 8))
PT = {' ':0x7e,'!':0x3d,',':0x3a,'-':0x3f,'.':0x3b,':':0x42,';':0x43,'?':0x3c,"'":0x40,'#':0x7e}
def t_of(ch):
    if 'A' <= ch <= 'Z': return ord(ch) - 65
    if ch.isdigit(): return 0x70 + int(ch)
    return PT.get(ch, 0x7e)
def wrap(s, n=16):
    lines, cur = [], ''
    for w in s.split(' '):
        if len(cur) + len(w) + (1 if cur else 0) <= n: cur = (cur + ' ' + w) if cur else w
        else: lines.append(cur); cur = w
    return lines + [cur]
wanted = set(a.upper() for a in sys.argv[4:]) or {'000', '016', '056', '07D', '092'}
blocks = []
for line in open(sys.argv[2], encoding='utf-8'):
    if line.startswith('#') or '|' not in line: continue
    ident, spec = [x.strip() for x in line.split('|', 1)]
    if ident not in wanted: continue
    parts = [p.strip() for p in spec.split(' @@ ')]
    text, ch = parts[0], parts[1:]
    center = text.startswith('~'); text = text.lstrip('~').strip()
    rows = []
    for seg in text.split(' // '):
        a = to_ascii(seg.strip(), ident)
        if center: a = ' ' * ((16 - len(a)) // 2) + a
        rows += wrap(a) if len(a) > 16 else [a]
    if ch: rows.append('    ' + to_ascii(ch[0]).ljust(5) + to_ascii(ch[1]))
    blocks.append(rows)
SC, LH = 3, 9
h = sum(len(b) * LH + 8 for b in blocks) + 8
img = Image.new('L', (16 * 8 + 16, h), 0); y = 6
for b in blocks:
    for ln in b:
        for i, ch in enumerate(ln[:16]): img.paste(tile(t_of(ch)), (8 + i * 8, y))
        y += LH
    y += 8
img.resize((img.width * SC, img.height * SC), Image.NEAREST).save(sys.argv[3])
