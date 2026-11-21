#!/usr/bin/env python3
"""Bb dominant bebop: guitar, piano and 49 progressions

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

parser = argparse.ArgumentParser(description='Bb dominant bebop: guitar, piano and 49 progressions')
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
c.setTitle('Bb Dominant Bebop - 7-string guitar, piano and 49 progressions')
W,H=A4; M=38; INNER=W-2*M; TOTAL=15
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
header(1,'Bb DOMINANT BEBOP','Eight-note scale | Your original riff, mapped onto a standard 7-string')
y=H-110
y=paragraph(y,'Scale: Bb C D Eb F G Ab A',11)
y=paragraph(y,'Formula from Bb: 1  2  3  4  5  6  b7  7',10)
y=paragraph(y,'Your riff: low E frets 3-4 = G-Ab; A frets 0-3-5-6 = A-C-D-Eb.',9.5)
y=paragraph(y,'G felt like home to you. Starting this same collection on G gives G Ab A Bb C D Eb F: G Phrygian with an added natural 2nd (A).',9.5)
y=paragraph(y,'The name Bb dominant bebop identifies the collection; it does not force your riff to resolve to Bb. Most progressions here keep G as the point of rest.',9.5)
txt(M,566,'STANDARD 7-STRING | FRETS 0-12',12,'Bold')
txt(M,548,'Dark cells = your exact fret positions. Bold G = your tonal centre.',9)
opens=[64,59,55,50,45,40,35]
labels=['1 e','2 B','3 G','4 D','5 A','6 E','7 B']
highlights={(5,0),(5,3),(5,5),(5,6),(6,3),(6,4)}
x0=M+37;cw=(INNER-37)/13;rh=29;top=517
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
y=paragraph(y,'Read the thinnest string at the top. A dash marks a note outside the scale. The map repeats 12 frets higher.',9)
y-=12
y=paragraph(y,'Using A natural intentionally',11)
y=paragraph(y,'Over a Bb7 vamp, A is often used briefly between Bb and Ab rather than held as a resting note. In G-centred music, A can also be the 9th of Gm9, or a chord tone in Dm and F.',9.5)
y=paragraph(y,'Ab and A are different colours: Ab is G\'s dark b2; A is its natural 2. You do not need every scale note in every chord.',9.5)
assert y>50
c.showPage()

# Page 2: strictly rising starting frets; exact same pitches in standard/drop.
header(2,'DIAGONAL GUITAR PATTERNS','Standard: B E A D G B E | Drop A: A E A D G B E')
standard=[[8,9,10,11,13,15],[11,13,15,16],[12,13,15,17],[13,15,17,18],[14,15,17,19],[16,18,20,21],[17,18,20,22]]
dropped=[[n+2 for n in standard[0]]]+standard[1:]
os=[35,40,45,50,55,59,64]; od=[33]+os[1:]

def tab(top,title,frets,tuning,lab):
    txt(M,top,title,13,'Bold')
    xt=M+35;step=(INNER-48)/29;seq=[];idx=0
    for s,row in enumerate(frets):
        yy=top-42-(6-s)*20
        txt(M,yy-3,str(7-s)+' '+lab[s],8,'Bold')
        c.setLineWidth(.5);c.setStrokeColor(HexColor('#888888'));c.line(xt-5,yy,W-M,yy)
        for f in row:
            n=tuning[s]+f;seq.append(n);x=xt+idx*step;idx+=1
            c.setFillColor(white);c.rect(x-7,yy-6,14,12,fill=1,stroke=0)
            center(x,yy-3.2,str(f),9,'Bold' if n%12==7 else 'Body')
    assert all(n%12 in ALLOWED for n in seq)
    assert all(a<b for a,b in zip(seq,seq[1:]))
    assert all(a[0]<b[0] for a,b in zip(frets,frets[1:]))
    return seq

s1=tab(H-120,'STANDARD | start on G at string 7, fret 8',standard,os,['B','E','A','D','G','B','e'])
s2=tab(H-366,'DROP A | start on G at string 7, fret 10',dropped,od,['A','E','A','D','G','B','e'])
assert s1==s2
expected_seq=[n for n in range(s1[0],s1[-1]+1) if n%12 in ALLOWED]
assert s1==expected_seq
y=H-594
for p in ['Play from the bottom line upward, each group left to right. Both tabs play G2 through D6 with no missing scale notes. Bold fret numbers are G.',
          'There are six notes on string 7, then four on each remaining string. Slide along the first string rather than stretching to hold all six frets at once.',
          'Every next string begins at a higher fret. The standard starting frets are 8-11-12-13-14-16-17; drop A starts 10-11-12-13-14-16-17.',
          'Maximum fret: 22. If you transpose the whole tuning down, the shape still works but the pitch collection and chord names transpose with it.']:
    y=paragraph(y,p,9.3)-10
assert y>45
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
txt(M,H-103,'Play all marked keys together. Fm uses Ab; F uses A natural. Both fit the scale.',8.8)
for i,(ch,lh,rh) in enumerate(triads):
    verify_voicing(ch,lh,rh);top=H-128-i*80
    txt(M,top,ch,11,'Bold');txt(M+92,top,'LH: '+lh+'     RH: '+rh,9)
    piano(top-48,lh,rh)
txt(M,48,'The chord symbol names the harmony, regardless of guitar tuning.',8.5)
c.showPage()

full=[('Gm7','G2 D3','Bb3 D4 F4 G4'),('Abmaj7','Ab2 Eb3','C4 Eb4 G4 Ab4'),
      ('Bb7','Bb2 F3','Ab3 Bb3 D4 F4'),('Cm7','C3 G3','Bb3 C4 Eb4 G4'),
      ('F7','F2 C3','A3 C4 Eb4 F4'),('Gm9','G2 D3','A3 Bb3 D4 F4')]
header(4,'PIANO KEYS | FULLER CHORDS','L = root + fifth | R = upper chord notes | All notes belong to the scale')
txt(M,H-103,'Gm9 makes A natural audible as an added colour above G minor.',9)
for i,(ch,lh,rh) in enumerate(full):
    verify_voicing(ch,lh,rh);top=H-137-i*95
    txt(M,top,ch,11,'Bold');txt(M+93,top,'LH: '+lh+'     RH: '+rh,9)
    piano(top-49,lh,rh)
paragraph(77,'For more weight, replace a left-hand fifth with a bass octave, such as G2-G3. If the low register becomes crowded, move the right-hand chord up an octave.',9)
c.showPage()

header(5,'START HERE | FOUR LOOPS','Each box is one bar in 4/4. Try 70-100 BPM and repeat each loop.')
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

for i,(title,seq,desc) in enumerate(core):
    assert all(ch in CH for ch in seq)
    yy=H-119-i*76;txt(M,yy,title,11,'Bold');sequence(yy-23,seq)
    txt(M,yy-43,desc,8.8)
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

def style_page(page,title,subtitle,groups):
    header(page,title,subtitle)
    txt(M,H-105,'One box = one bar in 4/4. Tempos are starting points, not genre rules.',8.8)
    txt(M,H-122,'Keys: pp3-4. Extra chord notes: p5. Plain-language playing tips: pp14-15.',8.8)
    y=H-160
    for group,loops in groups:
        txt(M,y,group,12,'Bold');y-=27
        for label,seq,desc in loops:
            assert all(ch in CH for ch in seq),seq
            assert pdfmetrics.stringWidth(desc,'Body',8.7)<=INNER,desc
            txt(M,y,label,10,'Bold');sequence(y-22,seq)
            txt(M,y-42,desc,8.7);y-=83
        y-=23
    paragraph(83,'These are production sketches, not fixed genre formulas. For the G-centred loops, end on Gm or Gm9 and make G feel settled; the first chord alone does not establish the centre.',8.5,13)
    assert y>60
    c.showPage()

style_page(6,'AMBIENT & ETHEREAL','G-centred loops using the Bb dominant bebop pitch collection',[
 ('Ambient | 50-75 BPM',[
  ('05  Slow drift',['Gm7','Abmaj7','Cm7','Gm7'],'Sustain soft pads; let each chord last two bars if you want a slower change.'),
  ('06  Quiet return',['Gm9','Cm7','Abmaj7','Gm9'],'Use soft attacks and leave gaps; hear A natural in Gm9.'),
  ('07  Wide horizon',['Gm7','Ebmaj7','Abmaj7','Gm7'],'Spread chord notes across octaves, with a gentle moving bass below.')]),
 ('Ethereal | 65-95 BPM',[
  ('08  Floating light',['Gm9','Bbadd9','Abmaj7','Gm9'],'Play right-hand notes one at a time; add quiet delay and reverb.'),
  ('09  Falling through',['Gm7','Dm7','Cm7','Abmaj7','Gm9','Gm9'],'Use a high, sparse melody; let the final Gm9 last two bars.'),
  ('10  Glass motion',['Gm9','Ebmaj7','F7','Abmaj7','Gm9','Gm9'],'Let shared notes ring; keep the bass changes distinct.')])])

style_page(7,'METAL & ROCK','G-centred loops | Short attacks, silence and clear chord returns',[
 ('Metal | 85-140 BPM',[
  ('11  Half-step pressure',['G5','Ab5','G5','F5'],'Strike root-plus-fifth pairs briefly, then release. Clipped fifths: tip 4, p14.'),
  ('12  Climb and collapse',['G5','Ab5','Bb5','Ab5','G5','G5'],'Hit twice per beat, then stop early before returning to G5. Tip 7, p15.'),
  ('13  Heavy descent',['G5','Eb5','F5','Ab5','G5','G5'],'Use a strong snare on beat 3; add low bass octaves. Half-time: tip 8, p15.')]),
 ('Rock | 95-140 BPM',[
  ('14  Open drive',['Gm','Eb','Bb','Ab','Gm','Gm'],'Play all three chord notes together, twice per beat. Full triads: tip 9, p15.'),
  ('15  Angular lift',['Gm','Dm','F','Ab','Gm','Gm'],'Repeat a melody ending Ab-G when Ab returns to Gm. Hook: tip 10, p15.'),
  ('16  Dark release',['Gm','Cm','Eb','Ab','Gm','Gm'],'Start with G3-Bb3; later spread Gm as G2-D3-Bb3-G4. Tip 11, p15.')])])

style_page(8,'POP & CINEMATIC','G-centred loops | Brighter A natural and darker Ab can coexist',[
 ('Pop / dark pop | 85-120 BPM',[
  ('17  Dark chorus',['Gm','Eb','Bb','F','Ab','Gm'],'Use a steady groove and repeating melody; save Ab-G for the closing turn.'),
  ('18  Bright surface',['Gm','Dm','Eb','Ab'],'Build a short hook around G-Bb-A; resolve the melody to G on the repeat.'),
  ('19  Stepwise shade',['Gm','Fm','Eb','Ab'],'Bass moves G-F-Eb-Ab. Try offbeat stabs; compare Fm with F on a later repeat.')]),
 ('Cinematic / tension | 55-90 BPM',[
  ('20  Unstable shadow',['Gm','Ddim','Ab','Gm'],'Use Ddim briefly. Its Ab links to the next chord before the return to Gm.'),
  ('21  Long scene',['Gm','Gm','Cm','Ab','Eb','Fm','Ab','Gm'],'Build layers over eight bars, then return to a clear G bass.'),
  ('22  Suspended scene',['Gm9','Dm7','Abmaj7','Cm7','Abmaj7','Gm9'],'Use slow broken chords and sustain the final Gm9 before repeating.')])])

style_page(9,'ELECTRO & ELECTROPOP','G-centred loops | Short synth attacks and moving bass lines',[
 ('Electro | 110-135 BPM',[
  ('23  Machine steps',['Gm','Ab','Cm','Gm'],'Use syncopated drum-machine kicks, short chord stabs and a dry octave bass.'),
  ('24  Metallic circuit',['G5','Bb5','Ab5','G5'],'Sequence short bass bursts, leaving gaps around the snare hits.'),
  ('25  Cold transmission',['Gm7','Dm7','Abmaj7','Gm9'],'Use a glassy pluck or vocal-like pad; put chord stabs between the main beats.')]),
 ('Electropop | 100-125 BPM',[
  ('26  Neon refrain',['Gm','Eb','F','Ab'],'Use a steady kick and bright stabs, with a short melody that returns to G.'),
  ('27  Glass chorus',['Gm9','Bbadd9','Dm7','Abmaj7'],'Repeat a clear melody; let A in Dm7 contrast with Ab before returning to Gm9.'),
  ('28  Night drive',['Gm','Cm','F','Ab'],'Try octave bass pulses and a wide pad behind a simple lead melody.')])])

style_page(10,'HYPERPOP & BLACK METAL','G-centred loops | Sound and articulation create the contrast',[
 ('Hyperpop | 140-180 BPM, or half-time feel',[
  ('29  Sugar and static',['Gm9','Ebmaj7','Bbadd9','Abmaj7'],'Use bright layered synths, sudden stops and a melody doubled an octave higher.'),
  ('30  Pixel jump',['Gm','Ab','Bb','F','Ab','Gm'],'Chop the chords into quick bursts; jump registers between phrases.'),
  ('31  Digital bloom',['Gm9','Dm7','Abmaj7','Cm7','Abmaj7','Gm9'],'Layer a pluck with a pad; strip back to bass before the final chord.')]),
 ('Black metal | 140-200 BPM, or slower atmospheric feel',[
  ('32  Frost line',['Gm','Ab','Gm','Cm'],'Rapidly repeat upper chord tones over a thin pad and relentless drums.'),
  ('33  Ash descent',['Gm','Fm','Eb','Ab'],'Use fast repeated notes; let each moving bass root sustain below them.'),
  ('34  Distant ruin',['Gm','Ddim','Cm','Ab','Gm','Gm'],'Use the diminished chord for friction; contrast fast notes with a long final Gm.')])])

style_page(11,'DUB & DUBSTEP','G-centred loops | Give bass, rhythm and effects their own space',[
 ('Dub | 65-85 BPM',[
  ('35  Echo chamber',['Gm7','Cm7','Abmaj7','Gm7'],'Play short offbeat chord chops, melodic bass and occasional echo repeats.'),
  ('36  Half-step skank',['Gm','Ab','Gm','F7'],'Keep the chords brief; answer them with bass phrases rather than held roots.'),
  ('37  Empty space',['Gm9','Fm7','Cm7','Abmaj7'],'Omit some chord hits on later repeats; let bass and echoes fill the gaps.')]),
 ('Dubstep | around 140 BPM, half-time feel',[
  ('38  Sub pressure',['G5','Ab5','G5','Eb5'],'Keep the deep sub simple; put rhythmic filter changes on a separate mid bass.'),
  ('39  Broken signal',['Gm','Dm','Ab','Gm'],'Use a sparse half-time groove and syncopated bass replies between chords.'),
  ('40  Weightless drop',['Gm9','Ebmaj7','F7','Abmaj7'],'Begin with airy pads, then shorten the chords to open room for the bass drop.')])])

header(12,'BLUES | SCALE EXCEPTIONS','G-centred blues | Outside notes are explicitly marked')
y=H-108
y=paragraph(y,'Only example 41 stays inside Bb dominant bebop. Examples 42-43 use borrowed dominant chords. The G minor blues melody G Bb C Db D F also adds Db, which is outside this collection.',9.3)
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

style_page(13,'MORE ELECTRONIC DIRECTIONS','G-centred sketches | One loop for each additional production direction',[
 ('Techno / house / industrial',[
  ('44  Techno | 125-140 BPM',['Gm','Ab','Gm','Cm'],'Repeat a short chord; open the synth filter gradually over eight bars. Tip 1, p14.'),
  ('45  House | 118-128 BPM',['Gm9','Cm7','F7','Abmaj7'],'Delay offbeat stabs slightly; move bass on each beat. Tips 2-3, p14.'),
  ('46  Industrial | 100-135 BPM',['G5','Ab5','Eb5','G5'],'Play G+D as clipped stabs; add metallic percussion and repeating bass. Tip 4, p14.')]),
 ('Drum & bass / UK garage / trip-hop',[
  ('47  Drum & bass | 165-175 BPM',['Gm9','Bbadd9','Cm7','Abmaj7'],'Let chords last a bar or two over fast breaks, with space for a clean sub bass.'),
  ('48  UK garage | 128-138 BPM',['Gm7','Dm7','Cm7','Abmaj7'],'Delay offbeat stabs; add syncopated kicks and snares on 2 and 4. Tip 5, p14.'),
  ('49  Trip-hop | 65-95 BPM',['Gm9','Abmaj7','Fm7','Gm9'],'Relax drums; use mellow keys, sparse bass and small sound changes. Tip 6, p14.')])])

def explain(y,title,texts):
    txt(M,y,title,11,'Bold');y-=19
    for p in texts:y=paragraph(y,p,9.3,14)-5
    return y-13

header(14,'PLAYING TIPS | SOUND & GROOVE','Terms 1-6 | Plain-language instructions with specific examples')
y=H-110
for title,texts in [
 ('1  Automate timbre slowly',['Timbre is the character of the sound. Automation changes a synth setting over time. Repeat the same notes while you gradually open a filter over eight bars, making the sound brighter without changing the chord.']),
 ('2  Swung offbeat chords',['Count "1 & 2 & 3 & 4 &". The numbers are the main beats; the & counts fall between them. Play short chords on the & counts. For swing, place those hits slightly later than the exact midpoint, giving a long-short bounce.']),
 ('3  Walking bass phrase',['Here this means a moving bass line rather than a held root. Play G-Ab-Bb-D, one note per beat over Gm7, then land on C when Cm7 arrives. These notes all fit. Traditional jazz walking bass is a more specific technique.']),
 ('4  Clipped fifths',['Strike a root and fifth together, then stop quickly. For G5 use G+D; for Ab5 use Ab+Eb. Release after each short stab and leave silence. "Clipped" describes the duration; it does not change the interval.']),
 ('5  Shuffled chord chops and a two-step beat',['Chops are short chord stabs. Shuffled timing has a long-short bounce with delayed offbeats. A UK garage starting point uses snares on beats 2 and 4, syncopated kicks, and gaps instead of a kick on every beat. Let bass phrases answer the chord hits.']),
 ('6  Loose drums, warm keys, sparse bass, evolving textures',['Loose drums have small timing and volume variations. Warm keys use a mellow sound with softer high frequencies. Sparse bass uses fewer notes and more silence.',
  'Let textures evolve by making small changes over several bars: fade in an echo, alter the filter, add a high note or introduce a background sound. Keep the main pulse recognizable.'])]:
    y=explain(y,title,texts)
assert y>45
c.showPage()

header(15,'PLAYING TIPS | NOTES & SPACE','Terms 7-11 | Count the rhythm, hear the return, spread the chord')
y=H-110
for title,texts in [
 ('7  Repeat eighth-note hits, then leave space',['Eighth notes give two hits per beat: "1 & 2 & 3 & 4 &". Repeat the current chord on those counts. In the last bar before G5 returns, play only "1 & 2 &", then rest for "3 & 4 &". Strike G5 on beat 1 of the next bar. The silence makes the return stand out.']),
 ('8  Half-time drum feel',['Keep the song tempo the same but make the drum accents feel slower. A common starting point replaces snares on beats 2 and 4 with one strong snare on beat 3. At 140 BPM, this can feel like a 70 BPM groove, even while other parts play fast notes.']),
 ('9  Full triads',['A triad has three different chord notes: Gm = G-Bb-D; Ab = Ab-C-Eb; Bb = Bb-D-F. Play all three together. G5 uses only G-D, leaving out Bb, the minor third that gives Gm its minor character.']),
 ('10  Use the Ab-to-Gm return as the hook',['A hook is a short idea repeated so listeners recognize and anticipate it. Each time Ab changes to Gm, repeat a melody ending Ab-G. Make it stand out with a stronger attack, a short pause beforehand or a distinctive repeating rhythm.']),
 ('11  Begin with fewer notes, then widen the voicing',['A voicing is the arrangement of chord notes across registers. Start with G3-Bb3. Add D4 to complete Gm. Later spread the chord as G2-D3-Bb3-G4. C4 means middle C.',
  'Adding notes makes a chord fuller; spacing them farther apart makes it wider. Change these separately if you like. Try the widest version only on the last repeat while keeping the bass rhythm steady.'])]:
    y=explain(y,title,texts)
assert y>45
c.showPage();c.save()
print(OUT)
