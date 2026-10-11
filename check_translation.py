#!/usr/bin/env python3
"""check_translation.py source.txt gemini_output.txt [--glossary glossary.txt] [--merge greek_dialog.txt]
Checks a batch translation against the English source, reports problems, and (with --merge) adds the clean entries."""
import re, sys, pathlib, collections
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from apply_greek import to_ascii

def parse_source(text):
    lines = [l.strip() for l in text.splitlines()]
    idx = [(i, m.group(1).upper(), m.group(2)) for i, l in enumerate(lines)
           if (m := re.match(r'^Dialog([0-9A-Fa-f]{3})::\s*;?\s*(.*)$', l))]
    out = {}
    for n, (i, ident, speaker) in enumerate(idx):
        end = idx[n + 1][0] if n + 1 < len(idx) else len(lines)
        body, keep, seen_if = lines[i + 1:end], True, False
        eng, ask = [], False
        for l in body:
            if re.match(r'^IF\b', l): seen_if = True; continue
            if re.match(r'^ELSE\b', l): keep = False; continue
            if re.match(r'^ENDC\b', l): keep = True; continue
            if not keep: continue
            l = re.sub(r'^:\s*', '', l)
            if l.startswith('dialog_ask_line'): ask = True; continue
            if re.match(r'^(dialog_text|dialog_string_wrapping|db)\b', l):
                eng += re.findall(r'"((?:[^"\\]|\\.)*)"', l)
        if eng:
            e = ' '.join(s.strip() for s in eng)
            out[ident] = dict(speaker=speaker, english=e, ask=ask, args=[x.strip('\x00') for x in eng])
    return out

def parse_output(text):
    ents, terms, dup = {}, [], []
    for l in text.splitlines():
        m = re.match(r'^\s*(?:Dialog)?([0-9A-Fa-f]{3})\s*\|\s*(.+?)\s*$', l)
        if m:
            i = m.group(1).upper()
            if i in ents: dup.append(i)
            ents[i] = m.group(2); continue
        m = re.match(r'^\s*TERM:\s*(.+?)\s*$', l)
        if m and m.group(1).lower() != 'none': terms.append(m.group(1))
    return ents, terms, dup

def load_glossary(path):
    rows = []
    for l in open(path, encoding='utf-8'):
        if l.startswith('#') or '|' not in l: continue
        eng, grk, stem = [x.strip() for x in l.split('|')]
        rows.append(([a.strip() for a in eng.split('/')], grk, to_ascii(stem)))
    return rows


def _units(s): return re.findall(r'<[a-z0-9]+>|.', s)
def est_bytes(args, ask=None):
    """Bytes the game's dialog macros would use for one entry (lines padded to 16, '@' terminator)."""
    total = last = 0
    for a in args:
        u = _units(a)
        while True:
            total += (16 - last) % 16; last = 0
            if len(u) <= 16: last = len(u); total += last; break
            ll = cut = None
            for i in range(16):
                if u[i] == ' ': ll, cut = i, i + 1
                elif u[i] == '-': ll, cut = i + 1, i + 1
            if u[16] == ' ': ll, cut = 16, 17
            if ll is None: return 9999
            last = ll; total += ll; u = u[cut:]
    return total + ((16 - last) % 16 + 10 + len(_units(ask[1]))) if ask else total + 1

def seg_len(a): return len(re.sub(r'<[a-z0-9]+>', 'x', a))

def main():
    args = sys.argv[1:]
    src = parse_source(open(args[0], encoding='utf-8').read())
    ents, terms, dup = parse_output(open(args[1], encoding='utf-8').read())
    gl = load_glossary(args[args.index('--glossary') + 1]) if '--glossary' in args else []
    errors, warns, good = collections.defaultdict(list), collections.defaultdict(list), {}
    for d in dup: errors[d].append('duplicate ID in output')
    for i in sorted(src):
        if i not in ents: errors[i].append('missing from output')
    for i in sorted(ents):
        if i not in src: errors[i].append('ID not in source (shared label or typo?)'); continue
        spec, s = ents[i], src[i]
        parts = [p.strip() for p in spec.split(' @@ ')]
        text, choices = parts[0], parts[1:]
        if s['ask'] and len(choices) != 2: errors[i].append('source has choices; output needs exactly " @@ first @@ second"')
        if not s['ask'] and choices: errors[i].append('output has choices but source has none')
        if len(choices) == 2:
            try:
                c1, c2 = to_ascii(choices[0], i), to_ascii(choices[1], i)
                if len(c1) > 4: errors[i].append(f'first choice too long ({len(c1)}>4): {choices[0]}')
                if len(c2) > 7: errors[i].append(f'second choice too long ({len(c2)}>7): {choices[1]}')
            except SystemExit as e: errors[i].append(str(e))
        centre = text.startswith('~'); body = text.lstrip('~').strip()
        asc = None
        try: asc = ' // '.join(to_ascii(x.strip(), i) for x in body.split(' // '))
        except SystemExit as e: errors[i].append(str(e).replace(f'Dialog{i}: ', ''))
        if asc is not None:
            for seg in asc.split(' // '):
                if centre and seg_len(seg) > 16: errors[i].append(f'centred line over 16 letters: {seg}')
                for w in seg.split(' '):
                    if seg_len(w) > 16: errors[i].append(f'word over 16 letters: {w}')
            eng_len = len(re.sub(r'\s+', ' ', s['english']))
            if len(asc) > 1.5 * eng_len and len(asc) > 30: warns[i].append(f'long: {len(asc)} vs English {eng_len} letters')
        if s['speaker'].strip().lower() == 'map' and not centre: warns[i].append('speaker is Map: expected ~ label format')
        tk = lambda t: sorted(re.findall(r'#####|<[a-z0-9]+>', t))
        if tk(s['english']) != tk(text): errors[i].append(f'symbols differ: English {tk(s["english"])} vs Greek {tk(text)}')
        dg = lambda t: sorted(re.findall(r'\d+', t))
        if s['speaker'].strip().lower() != 'map' and dg(s['english']) != dg(text): warns[i].append(f'numbers differ: {dg(s["english"])} vs {dg(text)}')
        if asc is not None:
            for engs, grk, stem in gl:
                if any(re.search(r'\b' + re.escape(a) + r'\b', re.sub(r'<[a-z0-9]+>', '', s['english']), 0 if a.isupper() else re.I) for a in engs) and stem not in asc.replace(' // ', ' '):
                    warns[i].append(f'glossary: English has "{engs[0]}" but Greek lacks {stem}')
        if i not in errors: good[i] = spec
    from apply_greek import build_body
    eb = gb = 0; grow = []
    for i in good:
        body = build_body(i, ents[i]); g_args = re.findall(r'"((?:[^"\\]|\\.)*)"', body.split('dialog_ask_line')[0])
        ask = re.findall(r'"([^"]*)"', body.split('dialog_ask_line')[1]) if 'dialog_ask_line' in body else None
        e_args = src[i]['args']; e_ask = ['', ''] if src[i]['ask'] else None
        g, e = est_bytes(g_args, ask), est_bytes(e_args, e_ask); gb += g; eb += e; grow.append((g - e, i))
        if g - e >= 16: warns[i].append(f'uses {(g - e) // 16} more line(s) than the English ({g - e:+d} bytes): shorten')
    print(f'Estimated game bytes for this batch: English {eb}, Greek {gb} ({gb - eb:+d}, {100 * (gb - eb) / max(eb, 1):+.1f}%). Each bank has only a little spare room: aim for Greek <= English.')
    if gb > eb:
        print('Biggest growers (shorten these first): ' + ', '.join(f'{i} ({d:+d})' for d, i in sorted(grow, reverse=True)[:8]))
    print(f'Source entries: {len(src)}   Output entries: {len(ents)}   Clean: {len(good)}   With errors: {len(errors)}   Warnings on: {len(warns)}')
    for i in sorted(errors): print(f'ERROR {i}: ' + '; '.join(errors[i]))
    for i in sorted(warns): print(f'warn  {i}: ' + '; '.join(warns[i]))
    for t in terms: print('NEW TERM: ' + t)
    if '--merge' in args:
        p = pathlib.Path(args[args.index('--merge') + 1]); head, cur = [], {}
        for l in p.read_text(encoding='utf-8').splitlines():
            m = re.match(r'^([0-9A-F]{3}) \| (.*)$', l)
            if m: cur[m.group(1)] = m.group(2)
            elif l.strip(): head.append(l)
        cur.update(good)
        p.write_text('\n'.join(head) + '\n' + '\n'.join(f'{k} | {cur[k]}' for k in sorted(cur, key=lambda x: int(x, 16))) + '\n', encoding='utf-8')
        print(f'Merged {len(good)} clean entries into {p.name} (now {len(cur)} entries).')
    sys.exit(1 if errors else 0)
main()
