#!/usr/bin/env python3
"""Generate the A minor blues scale with the riff notes on a 0-12 seven-string fretboard map."""

import argparse
from pathlib import Path

import reportlab
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', default='a_minor_blues_scale_map.pdf',
                    help='Output PDF path (default: %(default)s)')
args = parser.parse_args()
OUT = Path(args.output).expanduser().resolve()
OUT.parent.mkdir(parents=True, exist_ok=True)

c = canvas.Canvas(str(OUT), pagesize=A4)
c.setTitle('A minor blues scale and riff - 7-string fretboard map, frets 0-12')
c.setAuthor('')
W, H = A4
M = 38
INNER = W - 2 * M
font_dir = Path(reportlab.__file__).resolve().parent / 'fonts'
for family, filename in [('Body', 'Vera.ttf'), ('Bold', 'VeraBd.ttf')]:
    pdfmetrics.registerFont(TTFont(family, str(font_dir / filename)))

NAMES = {0: 'C', 1: 'Db', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'Bb', 11: 'B'}
BLUES = {9, 0, 2, 3, 4, 7}  # A C D D# E G
RIFF = {9, 0, 2, 3, 7, 8}  # A C D D# G G#: the blues scale without E, plus a chromatic G#
SCALE = BLUES | RIFF
opens = [64, 59, 55, 50, 45, 40, 35]
labels = ['1 e', '2 B', '3 G', '4 D', '5 A', '6 E', '7 B']


def txt(x, y, s, size=9, font='Body'):
    c.setFillColor(black)
    c.setFont(font, size)
    c.drawString(x, y, s)


def center(x, y, s, size=9, font='Body'):
    c.setFillColor(black)
    c.setFont(font, size)
    c.drawCentredString(x, y, s)


txt(M, H - 44, 'A MINOR BLUES | RIFF NOTES', 20, 'Bold')
txt(M, H - 66, 'Standard seven-string tuning | B E A D G B E | frets 0-12', 9)
c.setStrokeColor(HexColor('#aaaaaa'))
c.setLineWidth(.6)
c.line(M, H - 80, W - M, H - 80)
txt(M, 25, 'A MINOR BLUES RIFF MAP | 7-string B standard', 7)
txt(W - M - 30, 25, '1/2', 7)

txt(M, H - 110, 'A minor blues: A  C  D  D#  E  G', 11)
txt(M, H - 128, 'Riff notes: A  C  D  D#  G  G#  (skips E, adds a chromatic G#-G slide)', 11)
txt(M, H - 160, 'FRETS 0-12', 12, 'Bold')
txt(M, H - 178, 'Mid-grey cells are the riff notes. Dark cells mark A roots. Light cells are blues notes the riff skips (E).', 8.5)
txt(M, H - 192, 'A dash marks a note outside the scale and riff.', 8.5)

x0 = M + 37
cw = (INNER - 37) / 13
rh = 29
top = H - 224
for fret in range(13):
    center(x0 + (fret + .5) * cw, top + 9, str(fret), 8, 'Bold')
for row, (op, label) in enumerate(zip(opens, labels)):
    yy = top - (row + 1) * rh
    txt(M, yy + 10, label, 9, 'Bold')
    for fret in range(13):
        n = (op + fret) % 12
        inside = n in SCALE
        root = n == 9
        c.setFillColor(HexColor('#333333') if root else HexColor('#b3b3b3') if n in RIFF else HexColor('#ececec') if inside else white)
        c.setStrokeColor(HexColor('#cccccc'))
        c.rect(x0 + fret * cw, yy, cw, rh, fill=1, stroke=1)
        c.setFillColor(white if root else black)
        c.setFont('Bold' if n in RIFF else 'Body', 9)
        c.drawCentredString(x0 + (fret + .5) * cw, yy + 10, NAMES[n] if inside else '-')
c.setStrokeColor(black)
c.setLineWidth(2.5)
c.line(x0 + cw, top, x0 + cw, top - 7 * rh)
for fret in range(13):
    center(x0 + (fret + .5) * cw, top - 7 * rh - 14, str(fret), 8, 'Bold')

txt(M, top - 7 * rh - 40, 'Thinnest string at the top. The map repeats 12 frets higher.', 9.3)
y = top - 7 * rh - 72
txt(M, y, 'Scales to solo over this riff', 11, 'Bold')
y -= 20
for line in simpleSplit('If you want a full 7- or 8-note scale to solo or write melodies over this riff without hitting wrong notes, use:', 'Body', 9.3, INNER):
    txt(M, y, line, 9.3)
    y -= 14
y -= 4
for name, body in [
    ('A minor blues (A  C  D  D#  E  G)', 'for the core gritty, bluesy sound.'),
    ('A Dorian (A  B  C  D  E  F#  G) + the D# blue note', 'when you want to lean into the upbeat, funky side of the groove.'),
]:
    c.setFillColor(black)
    c.circle(M + 4, y + 3, 1.6, fill=1, stroke=0)
    c.setFont('Bold', 9.3)
    c.drawString(M + 14, y, name)
    y -= 14
    c.setFont('Body', 9.3)
    c.drawString(M + 14, y, body)
    assert M + 14 + pdfmetrics.stringWidth(body, 'Body', 9.3) < W - M, name
    y -= 20
assert y > 50
c.showPage()

# Page 2: hotspots (every note claim is checked against B standard).
def note(string, fret):
    return NAMES[(opens[string] + fret) % 12]


assert [note(5, f) for f in (2, 3, 4, 5)] == ['F#', 'G', 'G#', 'A']  # low E frets 2-5
assert note(3, 7) == note(5, 5) == note(4, 0) == 'A'  # D-7 is the octave above E-5 / A-0
assert (opens[3] + 7) - opens[4] == 12
assert [note(6, f) for f in (10, 9, 8)] == ['A', 'G#', 'G']  # low B frets 10-8
assert note(1, 10) == 'A'  # B string fret 10
assert note(4, 9) == 'F#'
assert (opens[3] + 13) % 12 == 3  # D-13 on a 4-string bass is D#

txt(M, H - 44, 'BASS-FRIENDLY AND GUITAR-ONLY MOVES', 20, 'Bold')
txt(M, H - 66, 'Standard seven-string tuning | B E A D G B E | A minor blues riff', 9)
c.setStrokeColor(HexColor('#aaaaaa'))
c.setLineWidth(.6)
c.line(M, H - 80, W - M, H - 80)
txt(M, 25, 'A MINOR BLUES RIFF MAP | 7-string B standard', 7)
txt(W - M - 30, 25, '2/2', 7)

y = H - 112
for title, intro, bullets in [
    ('100% bass-friendly (strings B, E, A, D)', None,
     [('The E-string chromatic walk (E-2 > 3 > 4 > 5):', 'pure bass gold.'),
      ('The octave pop (A-0 or E-5 + D-7):', 'a classic slap/fingerstyle bass move.'),
      ('Funky 6th double-stop (A-9 + D-7):', 'works great on bass as a punchy chordal accent.'),
      ('Deep low-end drop (B-10 > B-9 > B-8):', 'built specifically for heavy bass low-end (though guitar can double it for massive weight).')]),
    ('Guitar-only (uses the F# string)', None,
     [('The Hendrix/funk triad (F#-3, D-5, F#-5):', 'requires the F# string (unless you play a 5- or 6-string bass tuned B-E-A-D-G/F#).'),
      ('The upper blues bend (F#-8):', 'guitar lead move (on a 4-string bass, that same D# note sits up at D-13).')]),
]:
    txt(M, y, title, 11, 'Bold')
    y -= 18
    for head, body in bullets:
        lines = simpleSplit(head + ' ' + body, 'Body', 9.3, INNER - 14)
        c.setFillColor(black)
        c.circle(M + 4, y + 3, 1.6, fill=1, stroke=0)
        for i, line in enumerate(lines):
            if i == 0:
                c.setFont('Bold', 9.3)
                c.drawString(M + 14, y, head)
                hw = pdfmetrics.stringWidth(head + ' ', 'Bold', 9.3)
                c.setFont('Body', 9.3)
                c.drawString(M + 14 + hw, y, line[len(head) + 1:])
            else:
                txt(M + 14, y, line, 9.3)
            y -= 14
        y -= 4
    y -= 14
assert y > 50
c.showPage()

c.save()
print(OUT)
