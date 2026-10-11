#!/usr/bin/env python3
"""build_prompt.py glossary.txt prompt_template.txt out.txt -- inserts the glossary into the Gemini prompt."""
import sys
rows = []
for l in open(sys.argv[1], encoding='utf-8'):
    l = l.rstrip('\n')
    if not l.strip(): continue
    if l.startswith('#'): rows.append('\n' + l.lstrip('# ').strip().upper()); continue
    eng, grk, _stem = [x.strip() for x in l.split('|')]
    rows.append(f'{eng} = {grk}')
open(sys.argv[3], 'w', encoding='utf-8').write(open(sys.argv[2], encoding='utf-8').read().replace('{{GLOSSARY}}', '\n'.join(rows).strip()))
