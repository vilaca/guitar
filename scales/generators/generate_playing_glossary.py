#!/usr/bin/env python3
"""Generate the shared playing glossary for the seven-string scale guides."""

import argparse
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas


def make_pdf(path):
    entries = [
        ('Eighth-note hits',
         'Two evenly spaced attacks per beat. Count 1 & 2 & 3 & 4 &. For a stop before a chord change, play on 1 & 2 &, rest on 3 & 4 &, then land on beat 1.'),
        ('Half-time feel',
         'A slower-feeling backbeat at the same tempo. In 4/4, move the main snare accent from beats 2 and 4 to beat 3 while the guitar keeps its original pulse.'),
        ('Loose drums and warm keys',
         'Loose drums use small variations in timing and attack. Warm keys have a mellow tone with softer high frequencies. Leave space between bass notes and bring in an echo or a high note gradually.'),
        ('Swung offbeats',
         'The & counts fall between the numbered beats. Delay each & slightly to create a long-short bounce. Try short chord stabs on those delayed offbeats.'),
        ('Two-step groove',
         'A syncopated drum pattern common in UK garage. Start with snares on 2 and 4, leave gaps in the kick pattern, and let the bass answer short offbeat chords.'),
    ]
    width, height = A4
    margin = 40
    c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle('Playing glossary for seven-string scale guides')
    c.setFont('Helvetica-Bold', 23)
    c.drawString(margin, height - 52, 'PLAYING GLOSSARY')
    c.setFont('Helvetica', 11)
    c.drawString(margin, height - 74, 'Rhythm, articulation and synth terms for the seven-string scale guides')
    y = height - 122
    for term, explanation in entries:
        c.setFont('Helvetica-Bold', 13)
        c.drawString(margin, y, term)
        y -= 20
        c.setFont('Helvetica', 10.5)
        for line in simpleSplit(explanation, 'Helvetica', 10.5, width - 2 * margin):
            c.drawString(margin, y, line)
            y -= 15
        y -= 24
    assert y > margin
    c.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('playing_glossary.pdf'))
    path = parser.parse_args().output.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    make_pdf(path)
    print(path)
