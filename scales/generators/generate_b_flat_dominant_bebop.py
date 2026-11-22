#!/usr/bin/env python3
"""Bb dominant bebop: guitar, piano and 45 progressions

Install: python -m pip install reportlab
Run: python generate_b_flat_dominant_bebop.py --output my_guide.pdf
"""

from pathlib import Path
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import argparse

parser = argparse.ArgumentParser(description='Bb dominant bebop: guitar, piano and 45 progressions')
parser.add_argument('--output', default='b_flat_dominant_bebop_7_string_and_piano.pdf',
                    help='Output PDF path (default: %(default)s)')
args = parser.parse_args()
OUT = Path(args.output).expanduser().resolve()
OUT.parent.mkdir(parents=True, exist_ok=True)

import reportlab
font_dir = Path(reportlab.__file__).resolve().parent / 'fonts'
for family, filename in [('Body', 'Vera.ttf'), ('Bold', 'VeraBd.ttf')]:
    pdfmetrics.registerFont(TTFont(family, str(font_dir / filename)))
c=canvas.Canvas(str(OUT),pagesize=A4)
c.setTitle('Bb Dominant Bebop with a G-centred Riff - 7-string guitar, piano and 45 progressions')
W,H=A4; M=38; INNER=W-2*M; TOTAL=14
ALLOWED={10,0,2,3,5,7,8,9}
NAMES={0:'C',1:'Db',2:'D',3:'Eb',4:'E',5:'F',6:'F#',7:'G',8:'Ab',9:'A',10:'Bb',11:'B'}
PITCH={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}

def midi(s):
    m=re.fullmatch(r'([A-G])([b#]?)(-?\d+)',s)
    assert m,s
    return (int(m[3])+1)*12+PITCH[m[1]]+({'b':-1,'#':1,'':0}[m[2]])

def txt(x,y,s,size=9,font='Body',color=black):
    c.setFillColor(color);c.setFont(font,size);c.drawString(x,y,s)

def center(x,y,s,size=9,font='Body'):
    c.setFillColor(black);c.setFont(font,size);c.drawCentredString(x,y,s)

def paragraph(y,s,size=9.3,leading=14):
    for line in simpleSplit(s,'Body',size,INNER):
        txt(M,y,line,size);y-=leading
    return y

def header(page,title,subtitle):
    size=20
    while pdfmetrics.stringWidth(title,'Bold',size)>INNER:size-=.5
    txt(M,H-44,title,size,'Bold')
    txt(M,H-66,subtitle,9)
    c.setStrokeColor(HexColor('#aaaaaa'));c.setLineWidth(.6);c.line(M,H-80,W-M,H-80)
    txt(M,25,'Bb DOMINANT BEBOP | guitar + piano / synth',7)
    txt(W-M-30,25,f'{page}/{TOTAL}',7)

def lines(y,rows,size=9,leading=15):
    for r in rows:
        txt(M,y,r,size);y-=leading
    return y

def table(y,heads,widths,rows,height=26,size=9):
    xs=[M]
    for w in widths:xs.append(xs[-1]+w)
    assert sum(widths)<=INNER+.01
    for i,row in enumerate([heads]+list(rows)):
        yy=y-i*height
        if i==0:
            c.setFillColor(HexColor('#eeeeee'));c.rect(M,yy-height+5,sum(widths),height,fill=1,stroke=0)
        for j,s in enumerate(row):
            assert pdfmetrics.stringWidth(str(s),'Bold' if i==0 else 'Body',size)<widths[j]-8,(s,widths[j])
            txt(xs[j]+4,yy-12,str(s),size,'Bold' if i==0 else 'Body')
        c.setStrokeColor(HexColor('#cccccc'));c.setLineWidth(.4);c.line(M,yy-height+5,xs[-1],yy-height+5)
    return y-(len(rows)+1)*height

# Page 1: pitch collection, original riff and map.
header(1,'Bb DOMINANT BEBOP WITH A G-CENTRED RIFF','Standard seven-string tuning | B E A D G B E')
def section(y,title,paras):
    txt(M,y,title,11,'Bold');y-=20
    for p in paras:y=paragraph(y,p,9.5,15)-3
    return y-12
y=H-110
y=paragraph(y,'Bb dominant bebop: Bb  C  D  Eb  F  G  Ab  A',11,18)
y=paragraph(y,'Formula from Bb: 1  2  3  4  5  6  b7  7',11,18)
y=H-150
y=paragraph(y,'Starting this collection on G gives G Ab A Bb C D Eb F: G Phrygian with an added natural 2nd (A).',9.5,15)
y=paragraph(y,'The name identifies the collection; most loops keep G, the centre of your riff, as the point of rest.',9.5,15)
txt(M,H-210,'STANDARD 7-STRING | FRETS 0-12',12,'Bold')
txt(M,H-228,'Dark cells mark your riff positions; bold G marks the tonal centre. A dash marks a note outside the scale.',9)
opens=[64,59,55,50,45,40,35]
labels=['1 e','2 B','3 G','4 D','5 A','6 E','7 B']
highlights={(5,0),(5,3),(5,5),(5,6),(6,3),(6,4)}
x0=M+37;cw=(INNER-37)/13;rh=29;top=H-262
for fret in range(13):center(x0+(fret+.5)*cw,top+9,str(fret),8,'Bold')
for row,(op,label) in enumerate(zip(opens,labels)):
    yy=top-(row+1)*rh
    txt(M,yy+10,label,9,'Bold')
    for fret in range(13):
        n=(op+fret)%12;selected=(row+1,fret) in highlights
        c.setFillColor(HexColor('#333333') if selected else white)
        c.setStrokeColor(HexColor('#cccccc'));c.rect(x0+fret*cw,yy,cw,rh,fill=1,stroke=1)
        s=NAMES[n] if n in ALLOWED else '-'
        c.setFillColor(white if selected else black)
        c.setFont('Bold' if selected or n==7 else 'Body',9)
        c.drawCentredString(x0+(fret+.5)*cw,yy+10,s)
y=top-7*rh-28
y=paragraph(y,'Thinnest string at the top. The map repeats 12 frets higher.',9)-14
y=section(y,'Your riff',['Low E frets 3-4 = G-Ab; A string frets 0-3-5-6 = A-C-D-Eb.'])
y=section(y,'Using A natural intentionally',['Over a Bb7 vamp, A is often used briefly between Bb and Ab rather than held as a resting note. In G-centred music, A can also be the 9th of Gm9, or a chord tone in Dm and F.','Ab is G\'s dark b2; A is its natural 2. You do not need every scale note in every chord.'])
assert y>50
c.showPage()

header(2, 'GUITAR PATTERNS', 'Bb dominant bebop | Standard B E A D G B E')
def route(per_string):
    opens = [35, 40, 45, 50, 55, 59, 64]
    notes = [n for n in range(35, 100) if n % 12 in ALLOWED]
    rows, i = [], 0
    for open_pitch, count in zip(opens, per_string):
        rows.append([n - open_pitch for n in notes[i:i + count]])
        i += count
    return rows


def pattern(top, title, frets):
    txt(M, top, title, 13, 'Bold')
    opens = [35, 40, 45, 50, 55, 59, 64]
    labels = ['7 B', '6 E', '5 A', '4 D', '3 G', '2 B', '1 e']
    left = M + 38
    step = (W - M - 12 - left) / (sum(map(len, frets)) + 1)
    played = []

    def draw_row(y, label, open_pitch, row, start):
        txt(M, y - 3, label, 8, 'Bold')
        c.setStrokeColor(HexColor('#888888'))
        c.setLineWidth(.5)
        c.line(left - 10, y, W - M, y)
        scale_frets = [f for f in range(25) if (open_pitch + f) % 12 in ALLOWED]
        first = scale_frets.index(row[0])
        assert row == scale_frets[first:first + len(row)]
        for i in range(max(0, first - 1), min(len(scale_frets), first + len(row) + 1)):
            fret = scale_frets[i]
            neighbor = i < first or i >= first + len(row)
            label = f'({fret})' if neighbor else str(fret)
            size = 9 if neighbor else 11
            font = 'Bold' if (open_pitch + fret) % 12 == 7 else 'Body'
            x = left + (start + 1 + i - first) * step
            width = c.stringWidth(label, font, size) + 1
            c.setFillColor(white)
            c.rect(x - width / 2, y - 6, width, 12, fill=1, stroke=0)
            c.setFillColor(black)
            c.setFont(font, size)
            c.drawCentredString(x, y - 3, label)

    for string, row in enumerate(frets):
        y = top - 42 - (6 - string) * 26
        draw_row(y, labels[string], opens[string], row, len(played))
        played.extend(opens[string] + f for f in row)
    return played

diagonal = route([4] * 7)
played = pattern(H-120, 'DIAGONAL | start on string 7, fret 1 (C)', diagonal)
assert played == [n for n in range(36, 78) if n % 12 in ALLOWED]
assert all(a <= b for a, b in zip([r[0] for r in diagonal], [r[0] for r in diagonal][1:]))
y = H-350
for instruction in [
    'Read left to right. Bold numbers mark G. Parentheses show the neighboring scale frets on the same string. Skip them when playing the run.',
    'Diagonal: the open seventh string is B, which is outside the scale, so start on the first scale note above it, C at fret 1. Play four notes per string and shift up the neck. Finish on F5 (string 1, fret 13).',
]:
    y = paragraph(y, instruction, 9.3) - 10
assert y > 45
c.showPage()

# Chord spelling checks underpin all diagrams and original progressions.
CH={
 'Gm':'G Bb D','Ab':'Ab C Eb','Bb':'Bb D F','Cm':'C Eb G','Dm':'D F A','Ddim':'D F Ab',
 'Eb':'Eb G Bb','Fm':'F Ab C','F':'F A C',
 'Gm7':'G Bb D F','Gm9':'G Bb D F A','Abmaj7':'Ab C Eb G','Bb7':'Bb D F Ab',
 'Bbmaj7':'Bb D F A','Cm7':'C Eb G Bb','Dm7':'D F A C','Ebmaj7':'Eb G Bb D',
 'Fm7':'F Ab C Eb','F7':'F A C Eb','Bbadd9':'Bb C D F',
 'G5':'G D','Ab5':'Ab Eb','Bb5':'Bb F','Eb5':'Eb Bb','F5':'F C'}
def pcs(notes):return {midi(n+'3')%12 for n in notes.split()}
for name,ns in CH.items():assert pcs(ns)<=ALLOWED,(name,ns)

def piano(y,lh,rh):
    whites=[n for n in range(41,72) if n%12 in {0,2,4,5,7,9,11}]
    kw=(INNER-6)/len(whites);kh=40;bh=25;bw=kw*.58;x0=M+3
    targets={**{midi(n):'L' for n in lh.split()},**{midi(n):'R' for n in rh.split()}}
    assert len(targets)==len(lh.split())+len(rh.split())
    assert all(41<=n<=71 for n in targets)
    for j,n in enumerate(whites):
        x=x0+j*kw;c.setFillColor(HexColor('#dddddd') if n in targets else white)
        c.setStrokeColor(black);c.setLineWidth(.4);c.rect(x,y,kw,kh,fill=1,stroke=1)
        center(x+kw/2,y-9,NAMES[n%12]+str(n//12-1),6.5)
        if n in targets:
            c.setFillColor(white);c.circle(x+kw/2,y+10,6,fill=1,stroke=1)
            center(x+kw/2,y+7,targets[n],7,'Bold')
    for j,n in enumerate(whites[:-1]):
        if n%12 not in {0,2,5,7,9}:continue
        nn=n+1;x=x0+(j+1)*kw-bw/2
        c.setFillColor(black);c.rect(x,y+kh-bh,bw,bh,fill=1,stroke=1)
        if nn in targets:
            c.setFillColor(white);c.circle(x+bw/2,y+kh-bh+8,5.5,fill=1,stroke=0)
            center(x+bw/2,y+kh-bh+5.5,targets[nn],7,'Bold')

def verify_voicing(ch,lh,rh):
    assert {midi(n)%12 for n in (lh+' '+rh).split()}==pcs(CH[ch]),ch

triads=[('Gm','G2','Bb3 D4 G4'),('Ab','Ab2','C4 Eb4 Ab4'),('Bb','Bb2','Bb3 D4 F4'),
        ('Cm','C3','C4 Eb4 G4'),('Dm','D3','A3 D4 F4'),('Eb','Eb3','Bb3 Eb4 G4'),
        ('Fm','F2','Ab3 C4 F4'),('F','F2','A3 C4 F4')]
header(3,'PIANO KEYS | BASIC CHORDS','L = left-hand bass | R = right-hand chord | C4 = middle C')
txt(M,H-105,'Play each L and all three R keys together. Shading also marks the selected white keys.',9)
degrees=['i','bII','bIII','iv','v','bVI','bvii','bVII']
labels3=[ch+' ('+d+')' for (ch,_,_),d in zip(triads,degrees)]
lh_x=max(pdfmetrics.stringWidth(l,'Bold',11) for l in labels3)+14
for i,((ch,lh,rh),label) in enumerate(zip(triads,labels3)):
    verify_voicing(ch,lh,rh);top=H-128-i*80
    txt(M,top,label,11,'Bold');txt(M+lh_x,top,'LH: '+lh+'     RH: '+rh,10)
    piano(top-48,lh,rh)
txt(M,49,'All notes fit Bb dominant bebop. Fm uses Ab; F uses A natural.',9)
c.showPage()

full=[('Gm7','G2 D3','Bb3 D4 F4 G4'),('Abmaj7','Ab2 Eb3','C4 Eb4 G4 Ab4'),
      ('Bb7','Bb2 F3','Ab3 Bb3 D4 F4'),('Cm7','C3 G3','Bb3 C4 Eb4 G4'),
      ('F7','F2 C3','A3 C4 Eb4 F4'),('Gm9','G2 D3','A3 Bb3 D4 F4')]
header(4,'PIANO KEYS | FULLER CHORDS','L = left-hand root + fifth | R = right-hand chord | C4 = middle C')
lines(H-103,['Use these richer chords in loops 05-10 and wherever their symbols appear.','The keyboard shows every played key. Move a voicing up an octave if the bass gets muddy.'],9,15)
txt(M,60,'All notes belong to the scale. Gm9 makes A natural audible as an added colour above G minor.',9)
for i,(ch,lh,rh) in enumerate(full):
    verify_voicing(ch,lh,rh);top=H-137-i*95
    txt(M,top,ch,11,'Bold');txt(M+93,top,'LH: '+lh+'     RH: '+rh,10)
    piano(top-49,lh,rh)
paragraph(77,'For more weight, replace a left-hand fifth with a bass octave, such as G2-G3. If the low register becomes crowded, move the right-hand chord up an octave.',9)
c.showPage()

header(5,'START HERE | FOUR LOOPS','Each box is one bar in 4/4. Try 70-100 BPM and repeat each loop.')
variations = {
    '22': ('Variation 31 - Digital bloom / Hyperpop | 140-180 BPM, or half-time feel',
           'Layer a pluck with a pad; strip back to bass before the final chord.'),
    '19': ('Variation 33 - Ash descent / Black metal | 140-200 BPM, or slower atmospheric feel',
           'Use fast repeated notes; let each moving bass root sustain below them.'),
    '02': ('Variation 39 - Broken signal / Dubstep | around 140 BPM, half-time feel',
           'Use a sparse half-time groove and syncopated bass replies between chords.'),
    '32': ('Variation 44 - Techno | 125-140 BPM',
           'Repeat short chord stabs over eight bars.'),
}

def draw_variation(y, title):
    variation = variations.get(title[:2])
    if variation:
        name, direction = variation
        txt(M + 10, y, name, 8.5, 'Bold')
        y -= 12
        for line in simpleSplit(direction, 'Body', 8.5, W - 2 * M - 10):
            txt(M + 10, y, line, 8.5)
            y -= 12
    return y

core=[('01  Your original dark centre',['Gm','Ab','Gm','Gm'],
       'G is home. Emphasize Ab-G in the melody when Ab returns to Gm.'),
      ('02  Hear A natural',['Gm','Dm','Ab','Gm'],
       'Dm contains A. Compare that natural 2 with the Ab in the following chord.'),
      ('03  Bb7-oriented vamp',['Bb7','Cm7','Fm7','Bb7'],
       'Treat Bb7 as the recurring anchor. Try a short melody Bb-A-Ab, then G-F.'),
      ('04  Fuller G-centred colour',['Gm9','F7','Abmaj7','Gm9'],
       'Move bass G-F-Ab-G. Use the fuller two-hand piano voicings on page 4.')]

def sequence(y,seq,size=10):
    s='| '+' | '.join(seq)+' |'
    while pdfmetrics.stringWidth(s,'Courier',size)>INNER:size-=.3
    txt(M,y,s,size,'Courier')

txt(M,H-110,'One chord per bar in 4/4. Follow the roots in the bass and resolve to Gm or Gm7.',10)
yy = H - 128
for title,seq,desc in core:
    assert all(ch in CH for ch in seq)
    txt(M,yy,title,11,'Bold');sequence(yy-23,seq)
    txt(M,yy-43,desc,8.8)
    yy = draw_variation(yy-56, title) - 12
txt(M,389,'ADDITIONAL CHORD SPELLINGS',12,'Bold')
table(368,['Chord','Notes','Useful colour'],[94,160,INNER-254],[
 ('Dm7','D F A C','A natural'),('Ebmaj7','Eb G Bb D','Soft major seventh'),
 ('Fm7','F Ab C Eb','Ab, the darker option'),('Bbadd9','Bb C D F','Open C above Bb'),
 ('Bbmaj7','Bb D F A','A rather than Ab'),('Ddim','D F Ab','Compact tension')],height=25,size=8.8)
y=170
for p in ['Power chords: G5 = G D; Ab5 = Ab Eb; Bb5 = Bb F; Eb5 = Eb Bb; F5 = F C.',
          'The A and Ab options mean there is no single seven-chord diatonic harmonization. The palettes here are selected familiar chords whose notes all fit the eight-note scale.',
          'Scale membership does not make every sustained note equally settled over every chord. Use your ear, chord tones and the destination of each phrase.']:
    y=paragraph(y,p,9)-8
assert y>45
c.showPage()

def style_page(page,title,subtitle,groups,variation_guide=None):
    header(page,title,subtitle)
    txt(M,H-108,'1 bar per chord | Keys pp3-4 | Chords p5 | Tips p14',9)
    y=H-140
    for group,loops in groups:
        txt(M,y,group,14,'Bold');y-=29
        for label,seq,desc in loops:
            assert all(ch in CH for ch in seq),seq
            assert pdfmetrics.stringWidth(desc,'Body',8.7)<=INNER,desc
            txt(M,y,label,10,'Bold');sequence(y-22,seq)
            txt(M,y-42,desc,8.7)
            y = draw_variation(y-58, label) - 18
        y-=23
    if variation_guide:
        txt(M, 60, variation_guide, 9)
    assert y>60
    c.showPage()

style_page(6,'AMBIENT & ETHEREAL','Bb dominant bebop loops | Let the harmony breathe.',[
 ('Ambient | 50-75 BPM',[
  ('05  Slow drift',['Gm7','Abmaj7','Cm7','Gm7'],'Sustain soft pads; let each chord last two bars if you want a slower change.'),
  ('06  Quiet return',['Gm9','Cm7','Abmaj7','Gm9'],'Use soft attacks and leave gaps; hear A natural in Gm9.'),
  ('07  Wide horizon',['Gm7','Ebmaj7','Abmaj7','Gm7'],'Spread chord notes across octaves, with a gentle moving bass below.')]),
 ('Ethereal | 65-95 BPM',[
  ('08  Floating light',['Gm9','Bbadd9','Abmaj7','Gm9'],'Play right-hand notes one at a time; add quiet delay and reverb.'),
  ('09  Falling through',['Gm7','Dm7','Cm7','Abmaj7','Gm9','Gm9'],'Use a high, sparse melody; let the final Gm9 last two bars.'),
  ('10  Glass motion',['Gm9','Ebmaj7','F7','Abmaj7','Gm9','Gm9'],'Let shared notes ring; keep the bass changes distinct.')])])

style_page(7,'METAL & ROCK','Bb dominant bebop loops | Make the rhythm carry the weight.',[
 ('Metal | 85-140 BPM',[
  ('11  Half-step pressure',['G5','Ab5','G5','F5'],'Strike root-plus-fifth pairs briefly, then release. Tip 2, p14.'),
  ('12  Climb and collapse',['G5','Ab5','Bb5','Ab5','G5','G5'],'Hit twice per beat, then stop early before returning to G5. Glossary: eighth-note hits.'),
  ('13  Heavy descent',['G5','Eb5','F5','Ab5','G5','G5'],'Use a strong snare on beat 3; add low bass octaves. Glossary: half-time feel.')]),
 ('Rock | 95-140 BPM',[
  ('14  Open drive',['Gm','Eb','Bb','Ab','Gm','Gm'],'Play all three chord notes together, twice per beat. Tip 3, p14.'),
  ('15  Angular lift',['Gm','Dm','F','Ab','Gm','Gm'],'Repeat a melody ending Ab-G when Ab returns to Gm. Tip 4, p14.'),
  ('16  Dark release',['Gm','Cm','Eb','Ab','Gm','Gm'],'Start with G3-Bb3; later spread Gm as G2-D3-Bb3-G4. Tip 5, p14.')])])

style_page(8,'POP & CINEMATIC','Bb dominant bebop loops | Brighter A natural and darker Ab can coexist.',[
 ('Pop / dark pop | 85-120 BPM',[
  ('17  Dark chorus',['Gm','Eb','Bb','F','Ab','Gm'],'Use a steady groove and repeating melody; save Ab-G for the closing turn.'),
  ('18  Bright surface',['Gm','Dm','Eb','Ab'],'Build a short hook around G-Bb-A; resolve the melody to G on the repeat.'),
  ('19  Stepwise shade',['Gm','Fm','Eb','Ab'],'Bass moves G-F-Eb-Ab. Try offbeat stabs; compare Fm with F on a later repeat.')]),
 ('Cinematic / tension | 55-90 BPM',[
  ('20  Unstable shadow',['Gm','Ddim','Ab','Gm'],'Use Ddim briefly. Its Ab links to the next chord before the return to Gm.'),
  ('21  Long scene',['Gm','Gm','Cm','Ab','Eb','Fm','Ab','Gm'],'Build layers over eight bars, then return to a clear G bass.'),
  ('22  Suspended scene',['Gm9','Dm7','Abmaj7','Cm7','Abmaj7','Gm9'],'Use slow broken chords and sustain the final Gm9 before repeating.')])])

style_page(9,'ELECTRO & ELECTROPOP','Bb dominant bebop loops | Suggested starting tempos, not genre rules.',[
 ('Electro | 110-135 BPM',[
  ('23  Machine steps',['Gm','Ab','Cm','Gm'],'Use syncopated drum-machine kicks, short chord stabs and a dry octave bass.'),
  ('24  Metallic circuit',['G5','Bb5','Ab5','G5'],'Sequence short bass bursts, leaving gaps around the snare hits.'),
  ('25  Cold transmission',['Gm7','Dm7','Abmaj7','Gm9'],'Use a glassy pluck or vocal-like pad; put chord stabs between the main beats.')]),
 ('Electropop | 100-125 BPM',[
  ('26  Neon refrain',['Gm','Eb','F','Ab'],'Use a steady kick and bright stabs, with a short melody that returns to G.'),
  ('27  Glass chorus',['Gm9','Bbadd9','Dm7','Abmaj7'],'Repeat a clear melody; let A in Dm7 contrast with Ab before returning to Gm9.'),
  ('28  Night drive',['Gm','Cm','F','Ab'],'Try octave bass pulses and a wide pad behind a simple lead melody.')])])

style_page(10,'HYPERPOP & BLACK METAL','Bb dominant bebop loops | Let texture and articulation define the contrast.',[
 ('Hyperpop | 140-180 BPM, or half-time feel',[
  ('29  Sugar and static',['Gm9','Ebmaj7','Bbadd9','Abmaj7'],'Use bright layered synths, sudden stops and a melody doubled an octave higher.'),
  ('30  Pixel jump',['Gm','Ab','Bb','F','Ab','Gm'],'Chop the chords into quick bursts; jump registers between phrases.'),
  ]),
 ('Black metal | 140-200 BPM, or slower atmospheric feel',[
  ('32  Frost line',['Gm','Ab','Gm','Cm'],'Rapidly repeat upper chord tones over a thin pad and relentless drums.'),
  ('34  Distant ruin',['Gm','Ddim','Cm','Ab','Gm','Gm'],'Use the diminished chord for friction; contrast fast notes with a long final Gm.')])],
    variation_guide='Hyperpop and black metal variations: 31 and 33 on p8.')

style_page(11,'DUB & DUBSTEP','Bb dominant bebop loops | Leave space for bass, rhythm and effects.',[
 ('Dub | 65-85 BPM',[
  ('35  Echo chamber',['Gm7','Cm7','Abmaj7','Gm7'],'Play short offbeat chord chops, melodic bass and occasional echo repeats.'),
  ('36  Half-step skank',['Gm','Ab','Gm','F7'],'Keep the chords brief; answer them with bass phrases rather than held roots.'),
  ('37  Empty space',['Gm9','Fm7','Cm7','Abmaj7'],'Omit some chord hits on later repeats; let bass and echoes fill the gaps.')]),
 ('Dubstep | around 140 BPM, half-time feel',[
  ('38  Sub pressure',['G5','Ab5','G5','Eb5'],'Keep the deep sub simple; put rhythmic filter changes on a separate mid bass.'),
  ('40  Weightless drop',['Gm9','Ebmaj7','F7','Abmaj7'],'Begin with airy pads, then shorten the chords to open room for the bass drop.')])],
    variation_guide='Dubstep variation: 39 on p5.')

header(12,'BLUES | SCALE EXCEPTIONS','Bb dominant bebop blues | Outside notes are explicitly marked')
y=H-108
y=paragraph(y,'Only example 41 stays entirely inside Bb dominant bebop. Examples 42-43 borrow notes.',9,16)
y=paragraph(y,'G minor blues melody: G Bb C Db D F. Db is outside the scale.',9,16)
txt(M,H-173,'41  Scale-based blues-inspired loop | 65-95 BPM',11,'Bold')
sequence(H-198,['Gm7','Cm7','Gm7','Ab','Gm7','Gm7'])
paragraph(H-220,'This is a six-bar modal sketch, not a traditional 12-bar blues. Use a long-short shuffle rhythm and short melody phrases that answer each other.',9)
borrow={'G7':'G B D F','C7':'C E G Bb','D7':'D F# A C'}
assert pcs(borrow['G7'])-ALLOWED=={11}
assert pcs(borrow['C7'])-ALLOWED=={4}
assert pcs(borrow['D7'])-ALLOWED=={6}
minor=['Gm7']*4+['Cm7']*2+['Gm7']*2+['D7','Cm7','Gm7','D7']
dominant=['G7','C7','G7','G7','C7','C7','G7','G7','D7','C7','G7','D7']
for yy,title,seq,desc in [
 (H-300,'42  Minor 12-bar blues | borrowed D7',minor,'D7 adds F#. Follow that raised note when the harmony calls for it.'),
 (H-463,'43  Dominant 12-bar blues | outside this scale',dominant,'G7 adds B; C7 adds E; D7 adds F#. This is a different harmonic palette.')]:
    assert len(seq)==12
    txt(M,yy,title,11,'Bold')
    for row in range(3):sequence(yy-25-row*22,seq[row*4:row*4+4],11)
    paragraph(yy-99,desc,9)
txt(M,211,'BORROWED CHORD SPELLINGS',11,'Bold')
table(190,['Chord','Notes','Outside this scale'],[90,180,INNER-270],[('G7','G B D F','B'),('C7','C E G Bb','E'),('D7','D F# A C','F#')],height=26)
paragraph(61,'The scale-only rule is relaxed on this page: match the harmony rather than forcing every note into the original collection.',8.7,12)
c.showPage()

style_page(13,'MORE ELECTRONIC DIRECTIONS','Bb dominant bebop loops | Techno, house, industrial and breakbeat arrangements.',[
 ('Techno / house / industrial',[
  ('45  House | 118-128 BPM',['Gm9','Cm7','F7','Abmaj7'],'Delay offbeat stabs; move bass each beat. Glossary: swung offbeats. Bass: tip 1, p14.'),
  ('46  Industrial | 100-135 BPM',['G5','Ab5','Eb5','G5'],'Play G+D as clipped stabs; add metallic percussion and repeating bass. Tip 2, p14.')]),
 ('Drum & bass / UK garage / trip-hop',[
  ('47  Drum & bass | 165-175 BPM',['Gm9','Bbadd9','Cm7','Abmaj7'],'Let chords last a bar or two over fast breaks, with space for a clean sub bass.'),
  ('48  UK garage | 128-138 BPM',['Gm7','Dm7','Cm7','Abmaj7'],'Delay offbeat stabs; add syncopated kicks and snares on 2 and 4. Glossary: two-step groove.'),
  ('49  Trip-hop | 65-95 BPM',['Gm9','Abmaj7','Fm7','Gm9'],'Loosen drums; vary mellow keys over sparse bass. Glossary: loose drums and warm keys.')])],
    variation_guide='Techno variation: 44 on p10.')

header(14,'PLAYING EXAMPLES','Bass, chords and melodic phrasing for Bb dominant bebop')
tips = [

    ('1  Walking bass', 'Play one note per beat: G-Ab-Bb-D over Gm7, landing on C for Cm7.'),
    ('2  Clipped fifths', 'Strike G and D together and release immediately.'),


    ('3  Full triads', 'Sound all three chord tones together: G-Bb-D for Gm. A power chord leaves out the third.'),
    ('4  Melodic hook', 'Repeat a short phrase ending Ab-G as Ab returns to Gm.'),
    ('5  Wider voicings', 'Begin with G3-Bb3, add D4, then spread Gm across G2-D3-Bb3-G4.'),
]
y = H - 111
for title, direction in tips:
    txt(M, y, title, 11, 'Bold')
    y -= 17
    for line in simpleSplit(direction, 'Body', 9.3, W - 2 * M):
        txt(M, y, line, 9.3)
        y -= 13
    y -= 22
txt(M, y - 12, 'Shared rhythm and production terms', 11, 'Bold')
txt(M, y - 32, 'See Playing glossary (playing_glossary.pdf), supplied with the scale guides.', 9)
c.linkURL('playing_glossary.pdf', (M, y - 36, M + 320, y - 20), relative=0, kind='GoToR')
assert y > 85
c.showPage()
c.save()
print(OUT)
