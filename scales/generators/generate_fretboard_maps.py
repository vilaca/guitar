#!/usr/bin/env python3
"""Generate B-standard seven-string fretboard maps (frets 0-24), one page per scale."""

import argparse
from pathlib import Path

import reportlab
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', default='fretboard_maps_7_string_standard.pdf',
                    help='Output PDF path (default: %(default)s)')
args = parser.parse_args()
OUT = Path(args.output).expanduser().resolve()
OUT.parent.mkdir(parents=True, exist_ok=True)

c = canvas.Canvas(str(OUT), pagesize=A4)
c.setTitle('B scales - 7-string fretboard maps, frets 0-24')
c.setAuthor('')
W, H = A4
M = 38
font_dir = Path(reportlab.__file__).resolve().parent / 'fonts'
for family, filename in [('Body', 'Vera.ttf'), ('Bold', 'VeraBd.ttf')]:
    pdfmetrics.registerFont(TTFont(family, str(font_dir / filename)))


def txt(x, y, s, size=10, font='Body'):
    c.setFillColor(black)
    c.setFont(font, size)
    c.drawString(x, y, s)


opens = [35, 40, 45, 50, 55, 59, 64]
labels = ['7', '6', '5', '4', '3', '2', '1']
FRETS = 24

# title, note names by pitch class, formula, scale-note count per string
SCALES = [
    ('B PHRYGIAN DOMINANT',
     {11: 'B', 0: 'C', 3: 'D#', 4: 'E', 6: 'F#', 7: 'G', 9: 'A'},
     '1  b2  3  4  5  b6  b7', 4, 'four'),
    ('B PHRYGIAN',
     {11: 'B', 0: 'C', 2: 'D', 4: 'E', 6: 'F#', 7: 'G', 9: 'A'},
     '1  b2  b3  4  5  b6  b7', 4, 'four'),
    ('B MINOR PENTATONIC',
     {11: 'B', 2: 'D', 4: 'E', 6: 'F#', 9: 'A'},
     '1  b3  4  5  b7', 3, 'three'),
]


def page(number, title, note_names, formula, per_string, count_word):
    # Diagonal route: scale notes per string, starting on open B (string 7).
    scale = [n for n in range(opens[0], 110) if n % 12 in note_names]
    route = set()
    for i, open_pitch in enumerate(opens):
        route |= {(i, n - open_pitch) for n in scale[i * per_string:(i + 1) * per_string]}
    assert len(route) == 7 * per_string
    assert all(fret <= FRETS for _, fret in route), title

    size = 20
    while pdfmetrics.stringWidth(title, 'Bold', size) > W - 2 * M:
        size -= .5
    txt(M, H - 44, title, size, 'Bold')
    txt(M, H - 66, 'Standard seven-string tuning | B E A D G B E | frets 0-24', 9)
    c.setStrokeColor(HexColor('#aaaaaa'))
    c.setLineWidth(.6)
    c.line(M, H - 80, W - M, H - 80)
    txt(M, 25, 'B SCALE FRETBOARD MAPS | 7-string B standard', 7)
    txt(W - M - 30, 25, f'{number}/{len(SCALES)}', 7)

    ordered = sorted(note_names, key=lambda pc: (pc - 11) % 12)
    txt(M, H - 110, title.title().replace('B ', 'B ', 1) + ': ' + '  '.join(note_names[pc] for pc in ordered), 11)
    txt(M, H - 128, 'Formula from B: ' + formula, 11)
    txt(M, H - 160, 'FRETS 0-24 | DIAGONAL ROUTE', 12, 'Bold')
    txt(M, H - 178, f'Shaded cells are the diagonal route: {count_word} scale notes per string, starting on open B.', 8.5)
    txt(M, H - 192, 'Dark cells mark B roots on it. A dash marks a note outside the scale.', 8.5)

    left = M + 16
    cell = (W - M - left) / (FRETS + 1)
    row_h = 29
    top = H - 224
    c.setFillColor(black)
    c.setFont('Bold', 8)
    for fret in range(FRETS + 1):
        c.drawCentredString(left + (fret + .5) * cell, top + 9, str(fret))
    for row, (label, pitch) in enumerate(zip(reversed(labels), reversed(opens))):
        string = 6 - row
        y = top - (row + 1) * row_h
        txt(M, y + 10, label, 9, 'Bold')
        for fret in range(FRETS + 1):
            note = note_names.get((pitch + fret) % 12, '-')
            on_route = (string, fret) in route
            root = on_route and note == 'B'
            x = left + fret * cell
            c.setFillColor(HexColor('#333333') if root else HexColor('#d9d9d9') if on_route else white)
            c.setStrokeColor(HexColor('#cccccc'))
            c.rect(x, y, cell, row_h, fill=1, stroke=1)
            c.setFillColor(white if root else black)
            c.setFont('Bold' if on_route else 'Body', 9)
            c.drawCentredString(x + cell / 2, y + 10, note)
    c.setStrokeColor(black)
    c.setLineWidth(2.5)
    c.line(left + cell, top, left + cell, top - 7 * row_h)
    c.setFillColor(black)
    c.setFont('Bold', 8)
    for fret in range(FRETS + 1):
        c.drawCentredString(left + (fret + .5) * cell, top - 7 * row_h - 14, str(fret))
    c.showPage()


for number, (title, note_names, formula, per_string, count_word) in enumerate(SCALES, 1):
    page(number, title, note_names, formula, per_string, count_word)
c.save()
print(OUT)
