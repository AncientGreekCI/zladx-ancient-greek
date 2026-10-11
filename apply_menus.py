#!/usr/bin/env python3
"""apply_menus.py <repo>  -- Greek menus. Run AFTER apply_greek.py (which resets the source tree).
1. File-menu word tilemaps (erase / copy / command strip): Greek letters via the dialogue-font tiles (tile id = beta letter - 'A').
2. The two big headings (PLAYER SELECT, YOUR NAME?): new lettering drawn into the menu tile sheet."""
import sys, pathlib
repo = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(repo / 'tools')); sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib.background_coder import BackgroundCoder
from apply_greek import to_ascii
from PIL import Image, ImageDraw, ImageFont

BLANK = 0x7E
PUNCT_TILE = {' ': BLANK, '?': 0x3C, '!': 0x3D, ',': 0x3A, '.': 0x3B, '-': 0x3F, ':': 0x42, ';': 0x43}
def tiles(text):
    out = []
    for ch in to_ascii(text):
        out.append(ord(ch) - 65 if 'A' <= ch <= 'Z' else PUNCT_TILE[ch])
    return out

BG = repo / 'src/data/backgrounds'
def load(name):
    raw = (BG / f'{name}.tilemap.encoded').read_bytes()
    data = BackgroundCoder.decode(raw, 20, 0x7E, True)
    again = BackgroundCoder.decode(BackgroundCoder.encode(bytes(data), 0x9800, 20, 0x7E, True), 20, 0x7E, True)
    assert bytes(again) == bytes(data), f'{name}: re-encoding changes the picture'
    return [bytearray(data[i:i + 20]) for i in range(0, len(data), 20)]
def save(name, rows):
    (BG / f'{name}.tilemap.encoded').write_bytes(BackgroundCoder.encode(bytes(b''.join(rows)), 0x9800, 20, 0x7E, True))
def put(rows, r, c, text, clear_to=None):
    if clear_to is not None:
        for i in range(c, clear_to + 1): rows[r][i] = BLANK
    t = tiles(text); assert c + len(t) <= 19, (text, c, len(t))
    for i, v in enumerate(t): rows[r][c + i] = v

# --- erase screen
rows = load('menu_file_erase')
put(rows, 2, 2, 'ΤΙΝΑ ΑΡΩ;', clear_to=18)     # "Whom shall I remove?"
put(rows, 4, 10, '', clear_to=18)               # old second line ("PLAYER ?") removed
put(rows, 15, 4, 'ΕΠΑΝΕΛΘΕ', clear_to=18)       # "Return"
save('menu_file_erase', rows)
# --- copy screen
rows = load('menu_file_copy')
put(rows, 2, 2, 'ΜΙΜΟΥ ΤΙΝΑ;', clear_to=18)     # "Copy whom?"
put(rows, 4, 3, '-ΑΠΟ-', clear_to=9); put(rows, 4, 13, '-ΕΙΣ-', clear_to=17)
put(rows, 15, 4, 'ΕΠΑΝΕΛΘΕ', clear_to=18)
save('menu_file_copy', rows)
# --- command strip on the file-select screen (arrows stay at the original columns: erase starts col 6, copy col 13)
strip = tiles('ΑΡΟΝ') + [BLANK] * 3 + tiles('ΜΙΜΟΥ')
(BG / 'menu_file_selection_commands.tilemap.encoded').write_bytes(bytes([0x99, 0xE6, len(strip) - 1]) + bytes(strip))

# --- big headings
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 40)
def letter(ch, w, h):
    big = Image.new('L', (80, 80), 0); ImageDraw.Draw(big).text((10, 5), ch, font=FONT, fill=255)
    box = big.getbbox(); g = big.crop(box).resize((w, h), Image.LANCZOS)
    return g.point(lambda v: 255 if v > 110 else 0)
def heading(lines, width_px, line_h=11):
    im = Image.new('L', (width_px, 24), 0)
    for k, text in enumerate(lines):
        n = len(text); cell = width_px // 6 if n > 4 else 8
        cell = min(8, width_px // max(n, 1)); w = cell - 1
        for i, ch in enumerate(text):
            im.paste(letter(ch, w, line_h), (i * cell, k * 12 + 1))
    return im
def paint(sheet_path, layout, art):
    sheet = Image.open(sheet_path).convert('L')
    for j, row in enumerate(layout):
        for i, tid in enumerate(row):
            n = tid - 0x80; x, y = (n % 16) * 8, (n // 16) * 8
            sheet.paste(art.crop((i * 8, j * 8, i * 8 + 8, j * 8 + 8)), (x, y))
    sheet.save(sheet_path)
SEL = [[0x80,0x81,0x82,0x83,0x84,0x89],[0x90,0x91,0x92,0x93,0x94,0xAA],[0x8A,0x8B,0x8C,0x8D,0x8E,0xAF]]
NAM = [[0x85,0x86,0x87,0x88],[0x95,0x96,0x97,0x98,0x99],[0x9A,0x9B,0x9C,0x9D,0x9E]]
art_sel = heading(['ΕΚΛΟΓΗ', 'ΗΡΩΟΣ'], 48)
art_nam = heading(['ΣΟΝ', 'ΟΝΟΜΑ'], 40)
for variant in ('cgb', 'dmg'):
    p = repo / f'src/gfx/menus/menu.{variant}.png'
    paint(p, SEL, art_sel); paint(p, NAM, art_nam)
print('menus applied')

# ======================= in-game Save menu and Game Over screen =======================
M5 = {  # 5x7 Greek capitals for the small menu font
 'Α': [".###.","#...#","#...#","#####","#...#","#...#","#...#"], 'Β': ["####.","#...#","#...#","####.","#...#","#...#","####."],
 'Γ': ["#####","#....","#....","#....","#....","#....","#...."], 'Δ': ["..#..",".#.#.",".#.#.","#...#","#...#","#...#","#####"],
 'Ε': ["#####","#....","#....","####.","#....","#....","#####"], 'Ζ': ["#####","....#","...#.","..#..",".#...","#....","#####"],
 'Η': ["#...#","#...#","#...#","#####","#...#","#...#","#...#"], 'Θ': [".###.","#...#","#...#","#####","#...#","#...#",".###."],
 'Ι': [".###.","..#..","..#..","..#..","..#..","..#..",".###."], 'Κ': ["#...#","#..#.","#.#..","##...","#.#..","#..#.","#...#"],
 'Λ': ["..#..",".#.#.",".#.#.","#...#","#...#","#...#","#...#"], 'Μ': ["#...#","##.##","#.#.#","#.#.#","#...#","#...#","#...#"],
 'Ν': ["#...#","##..#","#.#.#","#..##","#...#","#...#","#...#"], 'Ξ': ["#####",".....",".....",".###.",".....",".....","#####"],
 'Ο': [".###.","#...#","#...#","#...#","#...#","#...#",".###."], 'Π': ["#####","#...#","#...#","#...#","#...#","#...#","#...#"],
 'Ρ': ["####.","#...#","#...#","####.","#....","#....","#...."], 'Σ': ["#####","#....",".#...","..#..",".#...","#....","#####"],
 'Τ': ["#####","..#..","..#..","..#..","..#..","..#..","..#.."], 'Υ': ["#...#","#...#",".#.#.","..#..","..#..","..#..","..#.."],
 'Φ': ["..#..",".###.","#.#.#","#.#.#",".###.","..#..","..#.."], 'Χ': ["#...#",".#.#.","..#..","..#..","..#..",".#.#.","#...#"],
 'Ψ': ["#.#.#","#.#.#","#.#.#",".###.","..#..","..#..","..#.."], 'Ω': [".###.","#...#","#...#","#...#",".#.#.",".#.#.","##.##"],
 '(': ["..#..",".#...",".#...",".#...",".#...",".#...","..#.."], ')': ["..#..","...#.","...#.","...#.","...#.","...#.","..#.."],
}
def word_bitmap(text, ntiles):
    im = Image.new('L', (ntiles * 8, 8), 255)
    for k, ch in enumerate(text):
        if ch == ' ': continue
        for j, row in enumerate(M5[ch]):
            for i, c in enumerate(row):
                if c == '#': im.putpixel((k * 6 + i, 1 + j), 0)
    return im
POOL = list(range(0xA9, 0xAE)) + list(range(0xB0, 0xBE)) + list(range(0xC0, 0xCE))
words = [('ΣΩΣΟΝ ΚΑ', 6), ('Ι ΠΡΟΑΓΕ', 6), ('Ι ΠΑΥΣΑΙ', 6), ('ΠΡΟΑΓΕ', 5), ('(ΜΗ ΣΩΣΑΣ)', 8)]
assert sum(n for _, n in words) <= len(POOL)
alloc, pos = [], 0
for text, n in words: alloc.append(POOL[pos:pos + n]); pos += n
PREFIX, TAIL_CONT, TAIL_QUIT, L_CONT, L_NOSAVE = alloc
TITLE_FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 40)
def gameover_art():
    art = Image.new('L', (64, 16), 170)
    for k, ch in enumerate('ΤΕΛΟΣ'):
        big = Image.new('L', (80, 80), 0); ImageDraw.Draw(big).text((10, 5), ch, font=TITLE_FONT, fill=255)
        g = big.crop(big.getbbox()).resize((10, 13), Image.LANCZOS).point(lambda v: 0 if v > 110 else 170)
        art.paste(g, (2 + k * 12, 1))
    return art
for variant in ('cgb', 'dmg'):
    p = repo / f'src/gfx/menus/save_menu.{variant}.png'
    sheet = Image.open(p).convert('L')
    def place(ids, bmp):
        for i, tid in enumerate(ids):
            n = tid - 0x80; sheet.paste(bmp.crop((i * 8, 0, i * 8 + 8, 8)), ((n % 16) * 8, (n // 16) * 8))
    place(PREFIX, word_bitmap(words[0][0], 6)); place(TAIL_CONT, word_bitmap(words[1][0], 6)); place(TAIL_QUIT, word_bitmap(words[2][0], 6))
    place(L_CONT, word_bitmap(words[3][0], 5)); place(L_NOSAVE, word_bitmap(words[4][0], 8))
    art = gameover_art()
    for r in range(2):
        for c in range(8):
            n = (0x80 + r * 8 + c) - 0x80; sheet.paste(art.crop((c * 8, r * 8, c * 8 + 8, r * 8 + 8)), ((n % 16) * 8, (n // 16) * 8))
    sheet.save(p)
def setrow(rows, r, ids):
    for c in range(3, 15): rows[r][c] = 0x7F
    for i, t in enumerate(ids): rows[r][3 + i] = t
rows = load('game_over')
setrow(rows, 6, PREFIX + TAIL_CONT); setrow(rows, 8, PREFIX + TAIL_QUIT); setrow(rows, 10, L_CONT); setrow(rows, 11, L_NOSAVE)
save('game_over', rows)
rows = load('menu_file_save')
setrow(rows, 3, L_CONT); setrow(rows, 5, PREFIX + TAIL_QUIT)
save('menu_file_save', rows)
print('save menu / game over applied')
