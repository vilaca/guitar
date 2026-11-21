#!/usr/bin/env python3
"""E minor pentatonic: guitar, piano and 49 progressions

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

parser = argparse.ArgumentParser(description='E minor pentatonic: guitar, piano and 49 progressions')
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
c.setTitle('E Minor Pentatonic - 7-string guitar, piano and 49 progressions')
W,H=A4; M=38; INNER=W-2*M; TOTAL=15
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



header(1,'E MINOR PENTATONIC','Five-note scale | Standard 7-string, drop A and piano / synth')
y=H-110
for text,size in [
 ('Scale: E G A B D',12),('Formula from E: 1  b3  4  5  b7',10),
 ('E is the tonal centre: the note or chord where a phrase feels settled. The first note you play does not have to be E.',9.5),
 ('All open strings fit: standard B E A D G B E and drop A A E A D G B E use only these five pitch classes.',9.5),
 ('Unlike a seven-note minor scale, this collection has neither C nor F#. Those notes can appear in an accompaniment, but they are outside E minor pentatonic.',9.5)]:
    y=paragraph(y,text,size)
txt(M,560,'STANDARD 7-STRING | FRETS 0-12',12,'Bold')
txt(M,542,'Dark cells = E roots. Other named cells = remaining scale notes.',9)
opens=[64,59,55,50,45,40,35];labels=['1 e','2 B','3 G','4 D','5 A','6 E','7 B']
x0=M+37;cw=(INNER-37)/13;rh=29;top=511
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
y=paragraph(y,'Thinnest string at the top. A dash marks a note outside the scale. The map repeats 12 frets higher. In drop A, string 7 has scale notes at frets 0, 2, 5, 7, 10 and 12; E is at fret 7.',9)-12
txt(M,y,'HOW TO READ THE PROGRESSION LABELS',11,'Bold');y-=20
for t in ['[P] = every chord note belongs to the five-note pentatonic collection.',
          '[H] = wider harmony. Chords marked * add outside notes, listed on page 5 or 12.',
          'Example: Em-C*-G-D* is common E minor harmony. C adds C natural; D adds F#. The melody can still begin with E-G-A-B-D, but listen to how each note meets the current chord.']:
    y=paragraph(y,t,9.3)-6
assert y>45
c.showPage()

header(2,'DIAGONAL GUITAR PATTERNS','Standard: B E A D G B E | Drop A: A E A D G B E')
standard=[[5,8,10,12],[10,12,15],[12,14,17],[14,17,19],[16,19,21],[20,22,24],[22,24]]
dropped=[[f+2 for f in standard[0]]]+standard[1:]
os=[35,40,45,50,55,59,64];od=[33]+os[1:]

def tab(top,title,frets,tuning,lab):
    txt(M,top,title,13,'Bold');xt=M+37;step=(INNER-52)/20;seq=[];idx=0
    for s,row in enumerate(frets):
        yy=top-42-(6-s)*20
        txt(M,yy-3,str(7-s)+' '+lab[s],8,'Bold')
        c.setLineWidth(.5);c.setStrokeColor(HexColor('#888888'));c.line(xt-5,yy,W-M,yy)
        for f in row:
            n=tuning[s]+f;seq.append(n);x=xt+idx*step;idx+=1
            c.setFillColor(white);c.rect(x-7,yy-6,14,12,fill=1,stroke=0)
            center(x,yy-3.2,str(f),9,'Bold' if n%12==4 else 'Body')
    assert all(n%12 in ALLOWED for n in seq)
    assert all(a<b for a,b in zip(seq,seq[1:]))
    assert all(a[0]<b[0] for a,b in zip(frets,frets[1:]))
    return seq

s1=tab(H-120,'STANDARD | start on E at string 7, fret 5',standard,os,['B','E','A','D','G','B','e'])
s2=tab(H-366,'DROP A | start on E at string 7, fret 7',dropped,od,['A','E','A','D','G','B','e'])
assert s1==s2
assert s1==[n for n in range(40,89) if n%12 in ALLOWED]
y=H-594
for p in ['Read from the bottom line upward, each group left to right. Both tabs play E2 through E6, four complete octaves, without missing any scale notes. Bold numbers mark E.',
          'Four notes on string 7, three on each middle string, two on string 1. Shift your hand along the neck instead of trying to hold the whole pattern in one position.',
          'Each next string begins at a higher fret. Standard starting frets: 5-10-12-14-16-20-22. Drop A starts: 7-10-12-14-16-20-22.',
          'The full run needs 24 frets. On a 22-fret guitar, stop at D6 (string 1, fret 22), or end earlier on E5 (string 3, fret 21).']:
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
txt(M,H-103,'The first six chords are [P]. C* and D* add outside notes, visibly shown below.',8.8)
for i,(ch,lh,rh) in enumerate(basic):
    verify(ch,lh,rh);top=H-128-i*80;star='*' if OUTSIDE[ch] else ''
    txt(M,top,ch+star,11,'Bold');txt(M+96,top,'LH: '+lh+'     RH: '+rh,9)
    piano(top-48,lh,rh)
txt(M,48,'C* adds C natural. D* adds F#. Suspended chords replace a third with another note.',8.5)
c.showPage()

full=[('Em7','E2 B2','D4 E4 G4 B4'),('G6','G2 D3','B3 D4 E4 G4'),
      ('Gadd9','G2 D3','A3 B3 D4 G4'),('A7sus4','A2 E3','G3 A3 D4 E4'),
      ('D6sus4','D3 A3','B3 D4 G4 A4'),('Em7(add11)','E2 B2','D4 E4 G4 A4')]
header(4,'PIANO KEYS | FULLER CHORDS','[P] Every played note belongs to E minor pentatonic')
txt(M,H-103,'L = root + fifth. R = upper chord notes. Em7(add11) uses all five scale notes.',8.8)
for i,(ch,lh,rh) in enumerate(full):
    verify(ch,lh,rh);assert ch in STRICT
    top=H-137-i*95;txt(M,top,ch,10.2,'Bold')
    txt(M+115,top,'LH: '+lh+'     RH: '+rh,8.8);piano(top-49,lh,rh)
paragraph(77,'For more weight, use a left-hand octave such as E2-E3. Keep dense chords above the low bass. C4 is middle C; octave names can vary between synth manufacturers.',9)
c.showPage()

def mark(ch):return ch+('*' if OUTSIDE.get(ch) else '')
def sequence(y,seq,size=10):
    s='| '+' | '.join(mark(ch) for ch in seq)+' |'
    while pdfmetrics.stringWidth(s,'Courier',size)>INNER:size-=.3
    txt(M,y,s,size,'Courier')

header(5,'START HERE | FOUR LOOPS','[P] = pentatonic-only chords | [H] = wider harmony | * = outside notes')
core=[('01  [P] Open pentatonic motion',['Em','Dsus4','Asus2','Em'],
       'Move bass E-D-A-E. Let the last Em feel settled.'),
      ('02  [P] Fuller colour',['Em7','G6','A7sus4','Em7'],
       'Use the fuller piano voicings on page 4. Keep the melody on E-G-A-B-D.'),
      ('03  [H] Familiar E minor harmony',['Em','C','G','D'],
       'C* adds C; D* adds F#. The lead melody can still start with E minor pentatonic.'),
      ('04  [H] Stronger return',['Em9','Cmaj7','Am7','B7'],
       'B7* adds D# and F#. Let D# rise to E when the loop returns to Em9*.')]
for i,(title,seq,desc) in enumerate(core):
    yy=H-116-i*66;txt(M,yy,title,10.8,'Bold');sequence(yy-21,seq)
    txt(M,yy-40,desc,8.6)
txt(M,414,'WIDER-HARMONY REFERENCE',11,'Bold')
extra=['C','D','Am','Am7','Bm7','B7','Cmaj7','Em9','Gmaj7','F','C5','B5']
table(394,['Chord','Complete notes','Outside E minor pentatonic'],[87,170,INNER-257],
      [(ch+'*',CH[ch],', '.join(n for n in CH[ch].split() if midi(n+'3')%12 not in ALLOWED)) for ch in extra],height=22,size=8.5)
paragraph(82,'An asterisk marks added notes, not an augmented chord. These harmonies expand the accompaniment; the pentatonic scale remains a useful starting palette for the melody. Match the current chord when a clash sounds unwanted.',8.5,12)
c.showPage()

def style_page(page,title,subtitle,groups):
    header(page,title,subtitle)
    txt(M,H-105,'[P] = all chord notes fit. [H] = expanded harmony; * marks outside notes.',8.7)
    txt(M,H-122,'One box = one bar in 4/4. Keys: pp3-4. Chord notes: p5. Playing tips: pp14-15.',8.7)
    y=H-160
    for group,loops in groups:
        txt(M,y,group,12,'Bold');y-=27
        for label,seq,desc in loops:
            assert all(ch in CH for ch in seq),seq
            kind='H' if any(OUTSIDE[ch] for ch in seq) else 'P'
            if '[P]' in label:assert kind=='P',label
            if '[H]' in label:assert kind=='H',label
            assert pdfmetrics.stringWidth(desc,'Body',8.7)<=INNER,desc
            txt(M,y,label,10,'Bold');sequence(y-22,seq)
            txt(M,y-42,desc,8.7);y-=83
        y-=23
    paragraph(83,'Tempos and moods are starting points, not genre rules. Give E a sense of rest through phrasing, bass and the final Em chord. Use E-G-A-B-D as the initial melody palette.',8.5,13)
    assert y>60;c.showPage()

style_page(6,'AMBIENT & ETHEREAL','Original E-centred sketches | Space, sustain and changing registers',[
 ('Ambient | 50-75 BPM',[
  ('05  [P] Slow drift',['Em7','G6','A7sus4','Em7'],'Sustain soft pads; give each chord two bars if you want slower harmony.'),
  ('06  [P] Quiet return',['Em7(add11)','D6sus4','Gadd9','Em7(add11)'],'Use soft attacks and leave gaps; let the E bass settle at the end.'),
  ('07  [H] Wide horizon',['Em9','Cmaj7','Am7','Em9'],'Spread the chords across octaves, with a gentle moving bass below.')]),
 ('Ethereal | 65-95 BPM',[
  ('08  [P] Floating light',['Em7','Gadd9','D6sus4','Em7'],'Play right-hand notes one at a time, with quiet delay and reverb.'),
  ('09  [H] Falling through',['Em7','Bm7','Am7','Cmaj7','Em7','Em7'],'Use a sparse high melody; let the final Em7 last two bars.'),
  ('10  [P] Glass motion',['Em7(add11)','G6','A7sus4','D6sus4','Em7','Em7'],'Let shared notes ring; keep the moving bass roots distinct.')])])

style_page(7,'METAL & ROCK','E-centred sketches | Fifths, full triads and clear rhythmic returns',[
 ('Metal | 85-140 BPM',[
  ('11  [P] Short pressure',['E5','G5','A5','E5'],'Strike root-plus-fifth pairs briefly, then release. Clipped fifths: tip 4, p14.'),
  ('12  [H] Climb and collapse',['E5','D5','C5','B5','E5','E5'],'Hit twice per beat, then stop early before returning to E5. Tip 7, p15.'),
  ('13  [P] Heavy descent',['E5','G5','D5','A5','E5','E5'],'Use a strong snare on beat 3 and low bass octaves. Half-time: tip 8, p15.')]),
 ('Rock | 95-140 BPM',[
  ('14  [H] Open drive',['Em','C','G','D','Em','Em'],'Play all three chord notes together, twice per beat. Full triads: tip 9, p15.'),
  ('15  [P] Angular lift',['Em','G','Asus2','Dsus4','Em','Em'],'Repeat a melody ending D-E when Dsus4 returns to Em. Hook: tip 10, p15.'),
  ('16  [H] Dark release',['Em','Am','C','B7','Em','Em'],'Start with E3-G3; later spread Em as E2-B2-G3-E4. Tip 11, p15.')])])

style_page(8,'POP & CINEMATIC','E-centred sketches | Compare open pentatonic and wider minor harmony',[
 ('Pop / dark pop | 85-120 BPM',[
  ('17  [H] Dark chorus',['Em','G','D','C','Am','Em'],'Use a steady groove and a repeating melody that settles on E.'),
  ('18  [P] Bright surface',['Em','G','Dsus4','Asus2'],'Build a short E-G-B melody; let the loop resolve back to Em.'),
  ('19  [H] Stepwise shade',['Em','D','C','B7'],'Move bass E-D-C-B; hear the borrowed D# in B7 lead back to E.')]),
 ('Cinematic / tension | 55-90 BPM',[
  ('20  [P] Open shadow',['Em','D6sus4','A7sus4','Em'],'Use quiet, slowly changing chords with plenty of silence between phrases.'),
  ('21  [H] Long scene',['Em','Em','Am','C','G','Bm7','B7','Em'],'Build layers over eight bars, then return to a clear E bass.'),
  ('22  [P] Suspended scene',['Em7','G6','D6sus4','A7sus4','Em7(add11)','Em7(add11)'],'Use slow broken chords and sustain the final E-centred harmony.')])])

style_page(9,'ELECTRO & ELECTROPOP','E-centred sketches | Short attacks, offbeats and moving bass lines',[
 ('Electro | 110-135 BPM',[
  ('23  [P] Machine steps',['Em','Dsus4','Asus2','Em'],'Use syncopated drum-machine kicks, short chord stabs and a dry octave bass.'),
  ('24  [P] Metallic circuit',['E5','G5','D5','E5'],'Sequence short bass bursts, leaving gaps around the snare hits.'),
  ('25  [H] Cold transmission',['Em7','Bm7','Cmaj7','Em9'],'Use a glassy pluck or vocal-like pad; play stabs between the main beats.')]),
 ('Electropop | 100-125 BPM',[
  ('26  [H] Neon refrain',['Em','C','D','G'],'Use a steady kick and bright chords; make E feel like home in the melody.'),
  ('27  [P] Glass chorus',['Em7','Gadd9','D6sus4','A7sus4'],'Repeat a clear melody over the open chords, then return to E.'),
  ('28  [H] Night drive',['Em','Am','D','B7'],'Try octave bass pulses and a wide pad behind a simple lead melody.')])])

style_page(10,'HYPERPOP & BLACK METAL','E-centred sketches | Texture and articulation create the contrast',[
 ('Hyperpop | 140-180 BPM, or half-time feel',[
  ('29  [H] Sugar and static',['Em9','Cmaj7','Gmaj7','D'],'Use bright layered synths, sudden stops and a melody doubled an octave higher.'),
  ('30  [P] Pixel jump',['Em','G','Dsus4','Asus2','G','Em'],'Chop the chords into quick bursts; jump registers between phrases.'),
  ('31  [H] Digital bloom',['Em9','Bm7','Cmaj7','Am7','B7','Em9'],'Layer a pluck with a pad; strip back to bass before the final chord.')]),
 ('Black metal | 140-200 BPM, or slower atmospheric feel',[
  ('32  [P] Frost line',['Em','Esus4','G','Em'],'Rapidly repeat upper chord tones over a thin pad and relentless drums.'),
  ('33  [H] Ash descent',['Em','D','C','Bm7'],'Use fast repeated notes while the bass follows E-D-C-B.'),
  ('34  [H] Distant ruin',['Em','F','Em','C','B7','Em'],'F* adds a borrowed half-step colour; contrast fast notes with a long final Em.')])])

style_page(11,'DUB & DUBSTEP','E-centred sketches | Give bass, rhythm and effects their own space',[
 ('Dub | 65-85 BPM',[
  ('35  [P] Echo chamber',['Em7','A7sus4','G6','Em7'],'Play short offbeat chords, melodic bass and occasional echo repeats.'),
  ('36  [H] Moving skank',['Em','Am','Em','B7'],'Keep the chords brief; answer them with bass phrases rather than held roots.'),
  ('37  [P] Empty space',['Em7','D6sus4','A7sus4','G6'],'Omit some chord hits on later repeats; let bass and echoes fill the gaps.')]),
 ('Dubstep | around 140 BPM, half-time feel',[
  ('38  [P] Sub pressure',['E5','G5','A5','D5'],'Keep the deep sub simple; put rhythmic filter changes on a separate mid bass.'),
  ('39  [H] Broken signal',['Em','Bm7','C','Em'],'Use sparse half-time drums and syncopated bass replies between the chords.'),
  ('40  [H] Weightless drop',['Em9','Cmaj7','Gmaj7','B7'],'Begin with airy pads, then shorten the chords to open room for the bass drop.')])])

header(12,'BLUES | SCALE EXCEPTIONS','E-centred blues | Expanded chords and the blue note are clearly marked')
y=H-108
y=paragraph(y,'E minor pentatonic is a common starting palette for E blues. Adding Bb gives E G A Bb B D, the E minor blues scale. Bb is outside the five-note pentatonic collection.',9.3)
y=paragraph(y,'Example 41 keeps every chord note pentatonic. Examples 42-43 use wider blues harmony; a melody note can rub against a chord tone, so listen to the current chord.',9.3)
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

style_page(13,'MORE ELECTRONIC DIRECTIONS','E-centred sketches | One loop for each additional production direction',[
 ('Techno / house / industrial',[
  ('44  [P] Techno | 125-140 BPM',['Em','Dsus4','Em','Asus2'],'Repeat a short chord; open the synth filter slowly over eight bars. Tip 1, p14.'),
  ('45  [P] House | 118-128 BPM',['Em7','G6','A7sus4','Dsus4'],'Delay offbeat stabs slightly; move the bass on each beat. Tips 2-3, p14.'),
  ('46  [P] Industrial | 100-135 BPM',['E5','D5','G5','E5'],'Play E+B as clipped stabs; add metallic percussion and repeating bass. Tip 4, p14.')]),
 ('Drum & bass / UK garage / trip-hop',[
  ('47  [H] Drum & bass | 165-175 BPM',['Em9','Cmaj7','Am7','B7'],'Let chords last a bar or two over fast breaks, with space for a clean sub bass.'),
  ('48  [P] UK garage | 128-138 BPM',['Em7','G6','A7sus4','D6sus4'],'Delay offbeat stabs; add syncopated kicks and snares on 2 and 4. Tip 5, p14.'),
  ('49  [H] Trip-hop | 65-95 BPM',['Em7','Cmaj7','Am7','Em7'],'Relax drums; use mellow keys, sparse bass and small sound changes. Tip 6, p14.')])])

def explain(y,title,texts):
    txt(M,y,title,11,'Bold');y-=19
    for p in texts:y=paragraph(y,p,9.3,14)-5
    return y-13

header(14,'PLAYING TIPS | SOUND & GROOVE','Terms 1-6 | Plain-language instructions with specific examples')
y=H-110
for title,texts in [
 ('1  Automate timbre slowly',['Timbre is the character of the sound. Automation changes a synth setting over time. Repeat the same notes while you gradually open a filter over eight bars, making the sound brighter without changing the chord.']),
 ('2  Swung offbeat chords',['Count "1 & 2 & 3 & 4 &". The numbers are the main beats; the & counts fall between them. Play short chords on the & counts. For swing, place those hits slightly later than the exact midpoint, giving a long-short bounce.']),
 ('3  Walking bass phrase',['Here this means a moving bass line rather than a held root. Play E-G-A-B, one note per beat over Em7, then land on A when A7sus4 arrives. Every note fits. Traditional jazz walking bass is a more specific technique.']),
 ('4  Clipped fifths',['Strike a root and fifth together, then stop quickly. For E5 use E+B; for A5 use A+E. Release after each short stab and leave silence. "Clipped" describes duration. B5 contains F#, so it needs an asterisk in this guide.']),
 ('5  Shuffled chord chops and a two-step beat',['Chops are short chord stabs. Shuffled timing has a long-short bounce with delayed offbeats. A UK garage starting point uses snares on beats 2 and 4, syncopated kicks, and gaps instead of a kick on every beat. Let bass phrases answer the chords.']),
 ('6  Loose drums, warm keys, sparse bass, evolving textures',['Loose drums have small timing and volume variations. Warm keys use a mellow sound with softer high frequencies. Sparse bass uses fewer notes and more silence.',
  'Let textures evolve by making small changes over several bars: fade in an echo, alter the filter, add a high note or introduce a background sound. Keep the main pulse recognizable.'])]:y=explain(y,title,texts)
assert y>45;c.showPage()

header(15,'PLAYING TIPS | NOTES & SPACE','Terms 7-11 | Count the rhythm, hear the return, spread the chord')
y=H-110
for title,texts in [
 ('7  Repeat eighth-note hits, then leave space',['Eighth notes give two hits per beat: "1 & 2 & 3 & 4 &". Repeat the current chord on those counts. In the last bar before E5 returns, play only "1 & 2 &", then rest for "3 & 4 &". Strike E5 on beat 1 of the next bar. Silence makes the return stand out.']),
 ('8  Half-time drum feel',['Keep the song tempo the same but make the drum accents feel slower. A common starting point replaces snares on beats 2 and 4 with one strong snare on beat 3. At 140 BPM, this can feel like a 70 BPM groove, even while other parts play fast notes.']),
 ('9  Full triads',['A triad has three different chord notes: Em = E-G-B; G = G-B-D. Both fit the pentatonic scale. E5 uses only E-B, leaving out G, the minor third that gives Em its minor character. The suspended chords shown earlier use another note in place of a third.']),
 ('10  Use the Dsus4-to-Em return as the hook',['A hook is a short idea repeated so listeners recognize and anticipate it. Each time Dsus4 changes to Em, repeat a melody ending D-E. Make it stand out with a stronger attack, a short pause beforehand or a distinctive repeating rhythm.']),
 ('11  Begin with fewer notes, then widen the voicing',['A voicing is the arrangement of chord notes across registers. Start with E3-G3. Add B3 to complete Em. Later spread it as E2-B2-G3-E4. C4 means middle C.',
  'Adding notes makes a chord fuller; spacing them farther apart makes it wider. Change these separately if you like. Try the widest version only on the final repeat while keeping the bass rhythm steady.'])]:y=explain(y,title,texts)
assert y>45;c.showPage();c.save()
print(OUT)
