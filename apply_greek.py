#!/usr/bin/env python3
"""Apply the Greek translation to a fresh copy of the LADX disassembly.
Usage: python3 apply_greek.py <path-to-LADX-Disassembly> <greek_dialog.txt>
Resets the source files first, so it can be re-run safely."""
import re, sys, subprocess, pathlib, unicodedata
from PIL import Image

BETA = {'Α':'A','Β':'B','Γ':'G','Δ':'D','Ε':'E','Ζ':'Z','Η':'H','Θ':'Q','Ι':'I','Κ':'K',
        'Λ':'L','Μ':'M','Ν':'N','Ξ':'C','Ο':'O','Π':'P','Ρ':'R','Σ':'S','Τ':'T','Υ':'U',
        'Φ':'F','Χ':'X','Ψ':'Y','Ω':'W'}
PUNCT = set(" !,.-:;?'#&()0123456789")
TOKEN = re.compile(r'<[a-z0-9]+>')
SPECIAL = {'·': ':', '\u0387': ':', '’': "'", '᾿': "'", 'ʼ': "'", '\u1fbd': "'", '\u037e': ';', '…': '...'}

def to_ascii(text, ident=''):
    """Polytonic Greek -> capitals without marks -> Latin stand-in letters."""
    out = []
    for piece in re.split(r'(<[a-z0-9]+>)', text):
        if TOKEN.fullmatch(piece):
            out.append(piece); continue
        for ch in piece:
            ch = SPECIAL.get(ch, ch)
            base = ''.join(c for c in unicodedata.normalize('NFD', ch) if unicodedata.category(c) != 'Mn')
            for b in base.upper():
                if b in BETA: out.append(BETA[b])
                elif b in PUNCT or b == '.': out.append(b)
                else: raise SystemExit(f"Dialog{ident}: unexpected character {b!r} (U+{ord(b):04X}) - Latin look-alike?")
    return ''.join(out)

SHIFT = [2, 2, 1, 1, 1, 0, 0]
GLYPHS = {
 'G': ["#####","#....","#....","#....","#....","#....","#...."],
 'D': ["..#..",".#.#.",".#.#.","#...#","#...#","#...#","#####"],
 'Q': [".###.","#...#","#...#","#####","#...#","#...#",".###."],
 'L': ["..#..",".#.#.",".#.#.","#...#","#...#","#...#","#...#"],
 'C': ["#####",".....",".....",".###.",".....",".....","#####"],
 'P': ["#####","#...#","#...#","#...#","#...#","#...#","#...#"],
 'S': ["#####",".#...","..#..","...#.","..#..",".#...","#####"],
 'F': ["..#..",".###.","#.#.#","#.#.#",".###.","..#..","..#.."],
 'Y': ["#.#.#","#.#.#","#.#.#",".###.","..#..","..#..","..#.."],
 'W': [".###.","#...#","#...#","#...#",".#.#.",".#.#.","##.##"],
}
def box(letter):
    t = ord(letter) - 65
    x, y = (t % 16) * 8, (t // 16) * 8
    return (x, y, x + 8, y + 8)

def patch_font(path):
    im = Image.open(path)
    im.paste(im.crop(box('P')), box('R')[:2])   # Rho looks like Latin P
    im.paste(im.crop(box('Y')), box('U')[:2])   # Upsilon looks like Latin Y
    for letter, rows in GLYPHS.items():
        x0, y0, _, _ = box(letter)
        for j in range(8):
            for i in range(8): im.putpixel((x0 + i, y0 + j), 0)
        for j, row in enumerate(rows):
            for i, c in enumerate(row):
                if c == '#': im.putpixel((x0 + SHIFT[j] + i, y0 + j), 255)
    im.save(path)

def build_body(ident, spec):
    parts = [p.strip() for p in spec.split(' @@ ')]
    text, choices = parts[0], parts[1:]
    center = text.startswith('~')
    if center: text = text[1:].strip()
    args = []
    for line in text.split(' // '):
        a = to_ascii(line.strip(), ident)
        if center and len(a) < 16: a = ' ' * ((16 - len(a)) // 2) + a
        args.append(a)
    quoted = ', '.join(f'"{a}"' for a in args)
    if choices:
        assert len(choices) == 2, f"Dialog{ident}: need exactly two choices"
        c1, c2 = (to_ascii(c, ident) for c in choices)
        assert len(c1) <= 4 and len(c2) <= 7, f"Dialog{ident}: choice too long ({c1!r}, {c2!r})"
        return f'    dialog_string_wrapping {quoted}\n    dialog_ask_line "{c1}", "{c2}"\n'
    return f'    dialog_text {quoted}\n'

def apply_text(repo, entries):
    files = sorted((repo / 'src/text').glob('*.asm'))
    for ident, spec in entries:
        body = build_body(ident, spec)
        pat = re.compile(r'^(Dialog%s::[^\n]*\n)((?:[^\n]+\n)*)' % ident, re.M)
        for f in files:
            src = f.read_text()
            if pat.search(src):
                f.write_text(pat.sub(lambda m: m.group(1) + body, src, count=1)); break
        else:
            raise SystemExit(f"Dialog{ident}: label not found")

def main():
    repo = pathlib.Path(sys.argv[1]); txt = pathlib.Path(sys.argv[2])
    subprocess.check_call(['git', '-C', str(repo), 'checkout', '--', 'src'])
    entries = []
    for line in txt.read_text(encoding='utf-8').splitlines():
        if not line.strip() or line.startswith('#'): continue
        ident, spec = [s.strip() for s in line.split('|', 1)]
        entries.append((ident.upper(), spec))
    patch_font(repo / 'src/gfx/fonts/font.png')
    apply_text(repo, entries)
    print(f"Applied {len(entries)} entries and redrew {len(GLYPHS)+2} letters.")

if __name__ == '__main__':
    main()
