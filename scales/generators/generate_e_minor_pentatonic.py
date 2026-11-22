#!/usr/bin/env python3
"""E minor pentatonic: guitar, piano and 46 progressions

Install: python -m pip install reportlab
Run: python generate_e_minor_pentatonic.py --output my_guide.pdf
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

parser = argparse.ArgumentParser(description='E minor pentatonic: guitar, piano and 46 progressions')
parser.add_argument('--output', default='e_minor_pentatonic_7_string_and_piano.pdf',
                    help='Output PDF path (default: %(default)s)')
args = parser.parse_args()
OUT = Path(args.output).expanduser().resolve()
OUT.parent.mkdir(parents=True, exist_ok=True)

import reportlab
font_dir = Path(reportlab.__file__).resolve().parent / 'fonts'
for family, filename in [('Body', 'Vera.ttf'), ('Bold', 'VeraBd.ttf')]:
    pdfmetrics.registerFont(TTFont(family, str(font_dir / filename)))
c=canvas.Canvas(str(OUT),pagesize=A4)
c.setTitle('E Minor Pentatonic - 7-string guitar, piano and 46 progressions')
W,H=A4; M=38; INNER=W-2*M; TOTAL=14
ALLOWED={4,7,9,11,2}
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
    txt(M,25,'E MINOR PENTATONIC | guitar + piano / synth',7)
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



header(1,'E MINOR PENTATONIC','Standard seven-string tuning | B E A D G B E')
def section(y,title,paras):
    txt(M,y,title,11,'Bold');y-=20
    for p in paras:y=paragraph(y,p,9.5,15)-3
    return y-12
y=H-110
y=paragraph(y,'E minor pentatonic: E  G  A  B  D',11,18)
y=paragraph(y,'Formula from E: 1  b3  4  5  b7',11,18)
y=H-150
y=paragraph(y,'E is the tonal centre: the note where a phrase feels settled. The first note you play need not be E.',9.5,15)
y=paragraph(y,'It leaves out F# and C from E natural minor; both can still appear in the accompaniment.',9.5,15)
txt(M,H-210,'STANDARD 7-STRING | FRETS 0-12',12,'Bold')
txt(M,H-228,'Dark cells mark E roots. A dash marks a note outside the scale.',9)
opens=[64,59,55,50,45,40,35];labels=['1 e','2 B','3 G','4 D','5 A','6 E','7 B']
x0=M+37;cw=(INNER-37)/13;rh=29;top=H-262
for fret in range(13):center(x0+(fret+.5)*cw,top+9,str(fret),8,'Bold')
for row,(op,label) in enumerate(zip(opens,labels)):
    yy=top-(row+1)*rh;txt(M,yy+10,label,9,'Bold')
    for fret in range(13):
        n=(op+fret)%12;root=n==4
        c.setFillColor(HexColor('#333333') if root else white)
        c.setStrokeColor(HexColor('#cccccc'));c.rect(x0+fret*cw,yy,cw,rh,fill=1,stroke=1)
        c.setFillColor(white if root else black);c.setFont('Bold' if root else 'Body',9)
        c.drawCentredString(x0+(fret+.5)*cw,yy+10,NAMES[n] if n in ALLOWED else '-')
y=top-7*rh-28
y=paragraph(y,'Thinnest string at the top. The map repeats 12 frets higher.',9)-14
y=section(y,'Root rule',['E is the root on open strings 6 and 1, and on string 7 at fret 5. All seven open strings fit E minor pentatonic.'])
y=section(y,'Using the notes',['E is home. G is the minor third that gives the scale its minor sound; A, B and D are the fourth, fifth and minor seventh.','You do not need every scale note in every chord.'])
assert y>45
c.showPage()

header(2,'GUITAR PATTERNS','E minor pentatonic | Standard B E A D G B E')
standard = [[5, 8, 10], [7, 10, 12], [10, 12, 14], [12, 14, 17], [14, 16, 19], [17, 20, 22], [19, 22, 24]]
assert len(standard) == 7 and all(len(row) == 3 for row in standard)
open_b_diagonal = [[0, 3, 5], [3, 5, 7], [5, 7, 10], [7, 9, 12], [9, 12, 14], [12, 15, 17], [15, 17, 19]]

def tab(top,title,frets):
    txt(M, top, title, 13, 'Bold')
    left = M + 37
    step = (W - M - 12 - left) / (sum(map(len, frets)) + 1)
    seq = []
    for s, row in enumerate(frets):
        yy = top - 42 - (6 - s) * 26
        txt(M, yy - 3, labels[6 - s], 8, 'Bold')
        c.setLineWidth(.5)
        c.setStrokeColor(HexColor('#888888'))
        c.line(left - 10, yy, W - M, yy)

        open_pitch = opens[6 - s]
        start_x = left + (len(seq) + 1) * step
        markers = [(i, fret, False) for i, fret in enumerate(row)]
        if len(row) == 3:
            scale_frets = [f for f in range(25) if (open_pitch + f) % 12 in ALLOWED]
            first = scale_frets.index(row[0])
            assert scale_frets[first:first + 3] == row
            if first > 0:
                markers.insert(0, (-1, scale_frets[first - 1], True))
            if first + 3 < len(scale_frets):
                markers.append((3, scale_frets[first + 3], True))

        for offset, fret, neighbor in markers:
            x = start_x + offset * step
            label = f'({fret})' if neighbor else str(fret)
            font = 'Bold' if (open_pitch + fret) % 12 == 4 else 'Body'
            size = 9 if neighbor else 11
            width = pdfmetrics.stringWidth(label, font, size) + 1
            c.setFillColor(white)
            c.rect(x - width / 2, yy - 6, width, 12, fill=1, stroke=0)
            center(x, yy - 3.2, label, size, font)
        seq.extend(open_pitch + fret for fret in row)
    assert all(n%12 in ALLOWED for n in seq)
    assert all(a<b for a,b in zip(seq,seq[1:]))
    return seq

open_run = tab(H-120,'DIAGONAL | start on open B, string 7',open_b_diagonal)
diagonal_run = tab(H-366,'DIAGONAL | start on E at string 7, fret 5',standard)
assert open_run == [n for n in range(midi('B1'), midi('B5') + 1) if n % 12 in ALLOWED]
assert diagonal_run == [n for n in range(midi('E2'), midi('E6') + 1) if n % 12 in ALLOWED]
for pattern in (open_b_diagonal, standard):
    starting_frets = [row[0] for row in pattern if row]
    assert all(a < b for a, b in zip(starting_frets, starting_frets[1:]))
y=H-594
for p in ['Play the plain fret numbers from left to right (0 = open). Parentheses mark the nearest scale fret on either side of a three-note group on that string, wherever it falls within frets 0-24. Skip these markers when playing the run.',
          'Open-B run: start on the open seventh string, B1. Play three notes on each of the seven strings, shifting up the neck at each crossing. Finish on B5 (string 1, fret 19).',
          'Seventh-string run: start on E2 at string 7, fret 5. Play three notes on each of the seven strings. The full four-octave run ends on E6 at fret 24.']:
    y=paragraph(y,p,9.3)-10
assert y>45
c.showPage()

CH={
 'Em':'E G B','G':'G B D','Esus4':'E A B','Asus2':'A B E','Asus4':'A D E',
 'Dsus4':'D G A','Em7':'E G B D','G6':'G B D E','Gadd9':'G A B D',
 'A7sus4':'A D E G','D6sus4':'D G A B','Em7(add11)':'E G B D A',
 'E5':'E B','G5':'G D','A5':'A E','D5':'D A',
 'C':'C E G','D':'D F# A','Am':'A C E','Am7':'A C E G','Bm7':'B D F# A',
 'B7':'B D# F# A','Cmaj7':'C E G B','Em9':'E G B D F#','Gmaj7':'G B D F#',
 'F':'F A C','C5':'C G','B5':'B F#'}
def pcs(notes):return {midi(n+'3')%12 for n in notes.split()}
OUTSIDE={ch:pcs(ns)-ALLOWED for ch,ns in CH.items()}
STRICT={ch for ch in CH if not OUTSIDE[ch]}
assert {'Em','G','Esus4','Asus2','Asus4','Dsus4','Em7','G6','Gadd9','A7sus4','D6sus4','Em7(add11)','E5','G5','A5','D5'}==STRICT

def piano(y,lh,rh):
    whites=[n for n in range(36,72) if n%12 in {0,2,4,5,7,9,11}]
    kw=(INNER-6)/len(whites);kh=40;bh=25;bw=kw*.58;x0=M+3
    targets={**{midi(n):'L' for n in lh.split()},**{midi(n):'R' for n in rh.split()}}
    assert len(targets)==len(lh.split())+len(rh.split())
    assert all(36<=n<=71 for n in targets)
    for j,n in enumerate(whites):
        x=x0+j*kw;c.setFillColor(HexColor('#dddddd') if n in targets else white)
        c.setStrokeColor(black);c.setLineWidth(.4);c.rect(x,y,kw,kh,fill=1,stroke=1)
        center(x+kw/2,y-9,NAMES[n%12]+str(n//12-1),6.2)
        if n in targets:
            c.setFillColor(white);c.circle(x+kw/2,y+10,5.5,fill=1,stroke=1)
            center(x+kw/2,y+7,targets[n],6.8,'Bold')
    for j,n in enumerate(whites[:-1]):
        if n%12 not in {0,2,5,7,9}:continue
        nn=n+1;x=x0+(j+1)*kw-bw/2
        c.setFillColor(black);c.rect(x,y+kh-bh,bw,bh,fill=1,stroke=1)
        if nn in targets:
            c.setFillColor(white);c.circle(x+bw/2,y+kh-bh+8,5,fill=1,stroke=0)
            center(x+bw/2,y+kh-bh+5.5,targets[nn],6.8,'Bold')

def verify(ch,lh,rh):
    assert {midi(n)%12 for n in (lh+' '+rh).split()}==pcs(CH[ch]),ch

basic=[('Em','E2','G3 B3 E4'),('G','G2','G3 B3 D4'),('Esus4','E2','A3 B3 E4'),
       ('Asus2','A2','A3 B3 E4'),('Dsus4','D3','A3 D4 G4'),('Asus4','A2','A3 D4 E4'),
       ('C','C3','G3 C4 E4'),('D','D3','A3 D4 F#4')]
header(3,'PIANO KEYS | BASIC CHORDS','L = left-hand bass | R = right-hand chord | C4 = middle C')
txt(M,H-105,'Play each L and all three R keys together. Shading also marks the selected white keys.',9)
degrees=['i','bIII','i sus4','IV sus2','bVII sus4','IV sus4','bVI','bVII']
labels3=[ch+('*' if OUTSIDE[ch] else '')+' ('+d+')' for (ch,_,_),d in zip(basic,degrees)]
lh_x=max(pdfmetrics.stringWidth(l,'Bold',11) for l in labels3)+14
for i,((ch,lh,rh),label) in enumerate(zip(basic,labels3)):
    verify(ch,lh,rh);top=H-128-i*80
    txt(M,top,label,11,'Bold');txt(M+lh_x,top,'LH: '+lh+'     RH: '+rh,10)
    piano(top-48,lh,rh)
txt(M,49,'The first six chords are [P]. C* adds C natural; D* adds F#. Suspended chords replace the third.',9)
c.showPage()

full=[('Em7','E2 B2','D4 E4 G4 B4'),('G6','G2 D3','B3 D4 E4 G4'),
      ('Gadd9','G2 D3','A3 B3 D4 G4'),('A7sus4','A2 E3','G3 A3 D4 E4'),
      ('D6sus4','D3 A3','B3 D4 G4 A4'),('Em7(add11)','E2 B2','D4 E4 G4 A4')]
header(4,'PIANO KEYS | FULLER CHORDS','L = left-hand root + fifth | R = right-hand chord | C4 = middle C')
lines(H-103,['Use these richer chords in loops 05-10 and wherever their symbols appear.','The keyboard shows every played key. Move a voicing up an octave if the bass gets muddy.'],9,15)
txt(M,60,'[P] Every played note belongs to E minor pentatonic. Em7(add11) uses all five scale notes.',9)
for i,(ch,lh,rh) in enumerate(full):
    verify(ch,lh,rh);assert ch in STRICT
    top=H-137-i*95;txt(M,top,ch,11,'Bold')
    txt(M+115,top,'LH: '+lh+'     RH: '+rh,10);piano(top-49,lh,rh)
paragraph(77,'For more weight, use a left-hand octave such as E2-E3. Keep dense chords above the low bass. C4 is middle C; octave names can vary between synth manufacturers.',9)
c.showPage()

def mark(ch):return ch+('*' if OUTSIDE.get(ch) else '')
def sequence(y,seq,size=10):
    s='| '+' | '.join(mark(ch) for ch in seq)+' |'
    while pdfmetrics.stringWidth(s,'Courier',size)>INNER:size-=.3
    txt(M,y,s,size,'Courier')

header(5,'START HERE | FOUR LOOPS','Each box is one bar in 4/4. Try 70-100 BPM and repeat each loop.')
variations = {
    '02': ('Variation 05 - Slow drift / Ambient | 50-75 BPM',
           'Sustain soft pads; give each chord two bars if you want slower harmony.'),
    '01': ('Variation 23 - Machine steps / Electro | 110-135 BPM',
           'Use syncopated drum-machine kicks, short chord stabs and a dry octave bass.'),
    '04': ('Variation 47 - Drum & bass | 165-175 BPM',
           'Let chords last a bar or two over fast breaks, with space for a clean sub bass.'),
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

core=[('01  [P] Open pentatonic motion',['Em','Dsus4','Asus2','Em'],
       'Move bass E-D-A-E. Let the last Em feel settled.'),
      ('02  [P] Fuller colour',['Em7','G6','A7sus4','Em7'],
       'Use the fuller piano voicings on page 4. Keep the melody on E-G-A-B-D.'),
      ('03  [H] Familiar E minor harmony',['Em','C','G','D'],
       'C* adds C; D* adds F#. The lead melody can still start with E minor pentatonic.'),
      ('04  [H] Stronger return',['Em9','Cmaj7','Am7','B7'],
       'B7* adds D# and F#. Let D# rise to E when the loop returns to Em9*.')]
txt(M,H-110,'One chord per bar in 4/4. Follow the roots in the bass and resolve to Em or Em7.',10)
yy = H-126
for title,seq,desc in core:
    txt(M,yy,title,11,'Bold');sequence(yy-21,seq)
    txt(M,yy-33,desc,8.6)
    yy = draw_variation(yy-46, title) - 12
txt(M,398,'WIDER-HARMONY REFERENCE',11,'Bold')
extra=['C','D','Am','Am7','Bm7','B7','Cmaj7','Em9','Gmaj7','F','C5','B5']
table(378,['Chord','Complete notes','Outside E minor pentatonic'],[87,170,INNER-257],
      [(ch+'*',CH[ch],', '.join(n for n in CH[ch].split() if midi(n+'3')%12 not in ALLOWED)) for ch in extra],height=20,size=8.5)
paragraph(86,'[P] = every chord note belongs to the five-note scale. [H] = wider harmony; an asterisk marks added notes, not an augmented chord. The pentatonic scale remains a useful starting palette for the melody. Match the current chord when a clash sounds unwanted.',8.5,12)
c.showPage()

def style_page(page,title,subtitle,groups,variation_guide=None):
    header(page,title,subtitle)
    txt(M,H-108,'1 bar per chord | [P] within scale, * outside | Keys pp3-4 | Chords p5 | Tips p14',9)
    y=H-140
    for group,loops in groups:
        txt(M,y,group,14,'Bold');y-=29
        for label,seq,desc in loops:
            assert all(ch in CH for ch in seq),seq
            kind='H' if any(OUTSIDE[ch] for ch in seq) else 'P'
            if '[P]' in label:assert kind=='P',label
            if '[H]' in label:assert kind=='H',label
            assert pdfmetrics.stringWidth(desc,'Body',8.7)<=INNER,desc
            txt(M,y,label,10,'Bold');sequence(y-22,seq)
            txt(M,y-42,desc,8.7)
            y = draw_variation(y-58, label) - 18
        y-=23
    if variation_guide:
        txt(M, 60, variation_guide, 9)
    assert y>60;c.showPage()

style_page(6,'AMBIENT & ETHEREAL','E minor pentatonic loops | Let the harmony breathe.',[
 ('Ambient | 50-75 BPM',[
  ('06  [P] Quiet return',['Em7(add11)','D6sus4','Gadd9','Em7(add11)'],'Use soft attacks and leave gaps; let the E bass settle at the end.'),
  ('07  [H] Wide horizon',['Em9','Cmaj7','Am7','Em9'],'Spread the chords across octaves, with a gentle moving bass below.')]),
 ('Ethereal | 65-95 BPM',[
  ('08  [P] Floating light',['Em7','Gadd9','D6sus4','Em7'],'Play right-hand notes one at a time, with quiet delay and reverb.'),
  ('09  [H] Falling through',['Em7','Bm7','Am7','Cmaj7','Em7','Em7'],'Use a sparse high melody; let the final Em7 last two bars.'),
  ('10  [P] Glass motion',['Em7(add11)','G6','A7sus4','D6sus4','Em7','Em7'],'Let shared notes ring; keep the moving bass roots distinct.')])],
    variation_guide='Ambient variation: 05 on p5.')

style_page(7,'METAL & ROCK','E minor pentatonic loops | Make the rhythm carry the weight.',[
 ('Metal | 85-140 BPM',[
  ('11  [P] Short pressure',['E5','G5','A5','E5'],'Strike root-plus-fifth pairs briefly, then release. Tip 2, p14.'),
  ('12  [H] Climb and collapse',['E5','D5','C5','B5','E5','E5'],'Hit twice per beat, then stop early before returning to E5. Glossary: eighth-note hits.'),
  ('13  [P] Heavy descent',['E5','G5','D5','A5','E5','E5'],'Use a strong snare on beat 3 and low bass octaves. Glossary: half-time feel.')]),
 ('Rock | 95-140 BPM',[
  ('14  [H] Open drive',['Em','C','G','D','Em','Em'],'Play all three chord notes together, twice per beat. Tip 3, p14.'),
  ('15  [P] Angular lift',['Em','G','Asus2','Dsus4','Em','Em'],'Repeat a melody ending D-E when Dsus4 returns to Em. Tip 4, p14.'),
  ('16  [H] Dark release',['Em','Am','C','B7','Em','Em'],'Start with E3-G3; later spread Em as E2-B2-G3-E4. Tip 5, p14.')])])

style_page(8,'POP & CINEMATIC','E minor pentatonic loops | Compare open pentatonic and wider minor harmony.',[
 ('Pop / dark pop | 85-120 BPM',[
  ('17  [H] Dark chorus',['Em','G','D','C','Am','Em'],'Use a steady groove and a repeating melody that settles on E.'),
  ('18  [P] Bright surface',['Em','G','Dsus4','Asus2'],'Build a short E-G-B melody; let the loop resolve back to Em.'),
  ('19  [H] Stepwise shade',['Em','D','C','B7'],'Move bass E-D-C-B; hear the borrowed D# in B7 lead back to E.')]),
 ('Cinematic / tension | 55-90 BPM',[
  ('20  [P] Open shadow',['Em','D6sus4','A7sus4','Em'],'Use quiet, slowly changing chords with plenty of silence between phrases.'),
  ('21  [H] Long scene',['Em','Em','Am','C','G','Bm7','B7','Em'],'Build layers over eight bars, then return to a clear E bass.'),
  ('22  [P] Suspended scene',['Em7','G6','D6sus4','A7sus4','Em7(add11)','Em7(add11)'],'Use slow broken chords and sustain the final E-centred harmony.')])])

style_page(9,'ELECTRO & ELECTROPOP','E minor pentatonic loops | Suggested starting tempos, not genre rules.',[
 ('Electro | 110-135 BPM',[
  ('24  [P] Metallic circuit',['E5','G5','D5','E5'],'Sequence short bass bursts, leaving gaps around the snare hits.'),
  ('25  [H] Cold transmission',['Em7','Bm7','Cmaj7','Em9'],'Use a glassy pluck or vocal-like pad; play stabs between the main beats.')]),
 ('Electropop | 100-125 BPM',[
  ('26  [H] Neon refrain',['Em','C','D','G'],'Use a steady kick and bright chords; make E feel like home in the melody.'),
  ('27  [P] Glass chorus',['Em7','Gadd9','D6sus4','A7sus4'],'Repeat a clear melody over the open chords, then return to E.'),
  ('28  [H] Night drive',['Em','Am','D','B7'],'Try octave bass pulses and a wide pad behind a simple lead melody.')])],
    variation_guide='Electro variation: 23 on p5.')

style_page(10,'HYPERPOP & BLACK METAL','E minor pentatonic loops | Let texture and articulation define the contrast.',[
 ('Hyperpop | 140-180 BPM, or half-time feel',[
  ('29  [H] Sugar and static',['Em9','Cmaj7','Gmaj7','D'],'Use bright layered synths, sudden stops and a melody doubled an octave higher.'),
  ('30  [P] Pixel jump',['Em','G','Dsus4','Asus2','G','Em'],'Chop the chords into quick bursts; jump registers between phrases.'),
  ('31  [H] Digital bloom',['Em9','Bm7','Cmaj7','Am7','B7','Em9'],'Layer a pluck with a pad; strip back to bass before the final chord.')]),
 ('Black metal | 140-200 BPM, or slower atmospheric feel',[
  ('32  [P] Frost line',['Em','Esus4','G','Em'],'Rapidly repeat upper chord tones over a thin pad and relentless drums.'),
  ('33  [H] Ash descent',['Em','D','C','Bm7'],'Use fast repeated notes while the bass follows E-D-C-B.'),
  ('34  [H] Distant ruin',['Em','F','Em','C','B7','Em'],'F* adds a borrowed half-step colour; contrast fast notes with a long final Em.')])])

style_page(11,'DUB & DUBSTEP','E minor pentatonic loops | Leave space for bass, rhythm and effects.',[
 ('Dub | 65-85 BPM',[
  ('35  [P] Echo chamber',['Em7','A7sus4','G6','Em7'],'Play short offbeat chords, melodic bass and occasional echo repeats.'),
  ('36  [H] Moving skank',['Em','Am','Em','B7'],'Keep the chords brief; answer them with bass phrases rather than held roots.'),
  ('37  [P] Empty space',['Em7','D6sus4','A7sus4','G6'],'Omit some chord hits on later repeats; let bass and echoes fill the gaps.')]),
 ('Dubstep | around 140 BPM, half-time feel',[
  ('38  [P] Sub pressure',['E5','G5','A5','D5'],'Keep the deep sub simple; put rhythmic filter changes on a separate mid bass.'),
  ('39  [H] Broken signal',['Em','Bm7','C','Em'],'Use sparse half-time drums and syncopated bass replies between the chords.'),
  ('40  [H] Weightless drop',['Em9','Cmaj7','Gmaj7','B7'],'Begin with airy pads, then shorten the chords to open room for the bass drop.')])])

header(12,'BLUES | SCALE EXCEPTIONS','E minor pentatonic blues | Expanded chords and the blue note are clearly marked')
y=H-108
y=paragraph(y,'Only example 41 stays entirely inside E minor pentatonic. Examples 42-43 borrow notes.',9,16)
y=paragraph(y,'E minor blues melody: E G A Bb B D. Bb is outside the five-note scale.',9,16)
txt(M,H-184,'41  [P] Pentatonic blues-inspired loop | 65-95 BPM',11,'Bold')
sequence(H-209,['Em7','A7sus4','Em7','Dsus4','Em7','Em7'])
paragraph(H-231,'This is a six-bar modal sketch, not a traditional 12-bar blues. Try a long-short shuffle and short phrases that answer each other.',9)
borrow={'E7':'E G# B D','A7':'A C# E G','B7':'B D# F# A'}
assert pcs(borrow['E7'])-ALLOWED=={8}
assert pcs(borrow['A7'])-ALLOWED=={1}
assert pcs(borrow['B7'])-ALLOWED=={3,6}
minor=['Em7']*4+['Am7']*2+['Em7']*2+['B7','Am7','Em7','B7']
dominant=['E7','A7','E7','E7','A7','A7','E7','E7','B7','A7','E7','B7']
for yy,title,seq,desc in [
 (H-307,'42  [H] Minor 12-bar blues',minor,'Am7* adds C. B7* adds D# and F#. The melody can adapt at those chords.'),
 (H-466,'43  [H] Dominant 12-bar blues',dominant,'E7* adds G#; A7* adds C#; B7* adds D# and F#. These are blues colours.')]:
    assert len(seq)==12;txt(M,yy,title,11,'Bold')
    for row in range(3):
        ss=seq[row*4:row*4+4]
        display=['|']
        for ch in ss:
            outside=pcs((borrow if ch in borrow else CH)[ch])-ALLOWED
            display.extend([ch+('*' if outside else ''),'|'])
        txt(M,yy-25-row*22,' '.join(display),11,'Courier')
    paragraph(yy-99,desc,9)
txt(M,208,'ADDITIONAL BLUES CHORD SPELLINGS',11,'Bold')
table(187,['Chord','Complete notes','Outside the pentatonic scale'],[87,170,INNER-257],
      [('E7*','E G# B D','G#'),('A7*','A C# E G','C#'),('B7*','B D# F# A','D#, F#')],height=26,size=8.5)
paragraph(61,'Holding G against the G# in E7 creates a familiar blues clash. That can be intentional; it does not mean every pentatonic note will sound equally settled.',8.7,12)
c.showPage()

style_page(13,'MORE ELECTRONIC DIRECTIONS','E minor pentatonic loops | Techno, house, industrial and breakbeat arrangements.',[
 ('Techno / house / industrial',[
  ('44  [P] Techno | 125-140 BPM',['Em','Dsus4','Em','Asus2'],'Repeat short chord stabs over eight bars.'),
  ('45  [P] House | 118-128 BPM',['Em7','G6','A7sus4','Dsus4'],'Delay offbeat stabs slightly; move the bass on each beat. Glossary: swung offbeats. Bass: tip 1, p14.'),
  ('46  [P] Industrial | 100-135 BPM',['E5','D5','G5','E5'],'Play E+B as clipped stabs; add metallic percussion and repeating bass. Tip 2, p14.')]),
 ('Drum & bass / UK garage / trip-hop',[
  ('48  [P] UK garage | 128-138 BPM',['Em7','G6','A7sus4','D6sus4'],'Delay offbeat stabs; add syncopated kicks and snares on 2 and 4. Glossary: two-step groove.'),
  ('49  [H] Trip-hop | 65-95 BPM',['Em7','Cmaj7','Am7','Em7'],'Loosen drums; vary mellow keys over sparse bass. Glossary: loose drums and warm keys.')])],
    variation_guide='Drum & bass variation: 47 on p5.')

header(14,'PLAYING EXAMPLES','Bass, chords and melodic phrasing for E minor pentatonic')
tips = [

    ('1  Walking bass', 'Play one note per beat: E-G-A-B over Em7, landing on A for A7sus4.'),
    ('2  Clipped fifths', 'Strike E and B together and release immediately. B5 adds F# outside E minor pentatonic.'),


    ('3  Full triads', 'Sound all three chord tones together: E-G-B for Em. A power chord leaves out the third.'),
    ('4  Melodic hook', 'Repeat a short phrase ending D-E as Dsus4 returns to Em.'),
    ('5  Wider voicings', 'Begin with E3-G3, add B3, then spread Em across E2-B2-G3-E4.'),
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
