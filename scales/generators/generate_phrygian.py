#!/usr/bin/env python3
"""7-string Phrygian: guitar, piano and 49 progressions

Install: python -m pip install reportlab
Run: python generate_phrygian.py --output my_guide.pdf
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, HexColor, white
from pathlib import Path

import argparse

parser = argparse.ArgumentParser(description='7-string Phrygian: guitar, piano and 49 progressions')
parser.add_argument('--output', default='phrygian_7_string_standard.pdf',
                    help='Output PDF path (default: %(default)s)')
args = parser.parse_args()
OUT = Path(args.output).expanduser().resolve()
OUT.parent.mkdir(parents=True, exist_ok=True)

c = canvas.Canvas(str(OUT), pagesize=A4)
c.setTitle('7-string Phrygian - B Standard')
c.setAuthor('')
W,H = A4
M=40

def txt(x,y,s,size=10,font='Helvetica'):
    c.setFillColor(black); c.setFont(font,size); c.drawString(x,y,s)

txt(M, H-48, '7-STRING PHRYGIAN', 23, 'Helvetica-Bold')
txt(M, H-69, 'Three notes per string and a wide diagonal | B E A D G B E', 11)
txt(M, H-95, 'Formula: 1  b2  b3  4  5  b6  b7', 11, 'Helvetica-Bold')
txt(M, H-113, 'B Phrygian: B  C  D  E  F#  G  A', 10)

allowed = {11, 0, 2, 4, 6, 7, 9}
compact = [[0, 1, 3], [0, 2, 3], [0, 2, 3], [0, 2, 4], [0, 2, 4], [1, 3, 5], [2, 3, 5]]
wide = [[0, 1, 3, 5], [2, 3, 5, 7], [3, 5, 7, 9], [5, 7, 9, 10], [7, 9, 11, 12], [10, 12, 13, 15], [12, 14, 15, 17]]
assert all(len(row) == 3 for row in compact)

def pattern(top, title, frets):
    txt(M, top, title, 13, 'Helvetica-Bold')
    opens = [35, 40, 45, 50, 55, 59, 64]
    labels = ['7 B', '6 E', '5 A', '4 D', '3 G', '2 B', '1 e']
    left = M + 38
    step = (W - M - 12 - left) / (sum(map(len, frets)) + 1)
    played = []

    def draw_row(y, label, open_pitch, row, start):
        txt(M, y - 3, label, 8, 'Helvetica-Bold')
        c.setStrokeColor(HexColor('#888888'))
        c.setLineWidth(.5)
        c.line(left - 10, y, W - M, y)
        scale_frets = [f for f in range(25) if (open_pitch + f) % 12 in allowed]
        first = scale_frets.index(row[0])
        assert row == scale_frets[first:first + len(row)]
        for i in range(max(0, first - 1), min(len(scale_frets), first + len(row) + 1)):
            fret = scale_frets[i]
            neighbor = i < first or i >= first + len(row)
            label = f'({fret})' if neighbor else str(fret)
            size = 8 if neighbor else 9
            font = 'Helvetica-Bold' if (open_pitch + fret) % 12 == 11 else 'Helvetica'
            x = left + (start + 1 + i - first) * step
            width = c.stringWidth(label, font, size) + 1
            c.setFillColor(white)
            c.rect(x - width / 2, y - 6, width, 12, fill=1, stroke=0)
            c.setFillColor(black)
            c.setFont(font, size)
            c.drawCentredString(x, y - 3, label)

    for string, row in enumerate(frets):
        y = top - 32 - (6 - string) * 19
        draw_row(y, labels[string], opens[string], row, len(played))
        played.extend(opens[string] + f for f in row)
    return played

assert pattern(H-158, 'THREE NOTES PER STRING | B1 to A4', compact) == [n for n in range(35, 70) if n % 12 in allowed]
assert pattern(H-384, 'WIDE DIAGONAL | B1 to A5', wide) == [n for n in range(35, 82) if n % 12 in allowed]
txt(M, 247, 'Read left to right. Parentheses show the neighboring scale frets on the same string. Skip them in the run.', 9)

c.setStrokeColor(HexColor('#AAAAAA')); c.line(M,174,W-M,174)
txt(M,154,'Root rule',11,'Helvetica-Bold')
txt(M,136,'Standard: root = open thickest string.',10)
txt(M,80,'Bold fret numbers mark the root, B. All open strings fit the scale.',9)
txt(M,45,'Transpose to lower standard tunings: keep the fret numbers and apply the same root rule.',9)
txt(W-65,27,'1/14',8); c.showPage()




def header(title, subtitle, page):
    txt(M,H-48,title,21,'Helvetica-Bold')
    txt(M,H-70,subtitle,10)
    c.setStrokeColor(HexColor('#aaaaaa')); c.line(M,H-85,W-M,H-85)
    txt(M,27,'7-STRING PHRYGIAN | B standard',8)
    txt(W-65,27,str(page)+'/14',8)

def lines(y, rows, size=10, leading=16):
    for row in rows:
        txt(M,y,row,size); y-=leading
    return y

def table(y, columns, widths, rows, row_h=27, font_size=10):
    xs=[M]
    for w in widths: xs.append(xs[-1]+w)
    for i,row in enumerate([columns]+rows):
        yy=y-i*row_h
        if i==0:
            c.setFillColor(HexColor('#eeeeee'));c.rect(M,yy-row_h+5,sum(widths),row_h,fill=1,stroke=0)
        for j,cell in enumerate(row):
            txt(xs[j]+6,yy-13,str(cell),font_size,'Helvetica-Bold' if i==0 else 'Helvetica')
        c.setStrokeColor(HexColor('#cccccc'));c.setLineWidth(.4)
        c.line(M,yy-row_h+5,xs[-1],yy-row_h+5)
    return y-(len(rows)+1)*row_h

header('PIANO KEYS | B PHRYGIAN','L = left-hand bass | R = right-hand chord | C4 = middle C',2)
chords=[('i','Bm','B D F#'),('bII','C','C E G'),('bIII','D','D F# A'),('iv','Em','E G B'),('v diminished','F#dim','F# A C'),('bVI','G','G B D'),('bvii','Am','A C E')]
voicings=[('Bm','B2','B3 D4 F#4'),('C','C3','C4 E4 G4'),
          ('D','D3','A3 D4 F#4'),('Em','E3','B3 E4 G4'),
          ('F#dim','F#2','A3 C4 F#4'),('G','G2','B3 D4 G4'),
          ('Am','A2','C4 E4 A4')]
expected={'Bm':{11,2,6},'C':{0,4,7},'D':{2,6,9},'Em':{4,7,11},
          'F#dim':{6,9,0},'G':{7,11,2},'Am':{9,0,4}}
pitch_classes={'C':0,'D':2,'E':4,'F#':6,'G':7,'A':9,'B':11}
def pc(note): return pitch_classes[note[:-1]]
for name,lh,rh in voicings:
    assert {pc(n) for n in [lh]+rh.split()} == expected[name]
def midi(note): return (int(note[-1])+1)*12+pc(note)

def piano(y,lh,rh):
    # F2 through B4, identical range in every diagram.
    white_notes=[n for n in range(41,72) if n%12 in {0,2,4,5,7,9,11}]
    x0=M+5; kw=(W-2*M-10)/len(white_notes); kh=43; bh=27; bw=kw*.59
    targets={**{midi(n):'L' for n in lh.split()},**{midi(n):'R' for n in rh.split()}}
    assert len(targets)==len(lh.split())+len(rh.split())
    names={0:'C',2:'D',4:'E',5:'F',7:'G',9:'A',11:'B'}
    for j,n in enumerate(white_notes):
        x=x0+j*kw
        c.setFillColor(HexColor('#d9d9d9') if n in targets else white)
        c.setStrokeColor(black);c.setLineWidth(.5);c.rect(x,y,kw,kh,fill=1,stroke=1)
        c.setFillColor(black);c.setFont('Helvetica',7)
        c.drawCentredString(x+kw/2,y-9,names[n%12]+str(n//12-1))
        if n in targets:
            c.setFillColor(white);c.circle(x+kw/2,y+11,6.5,fill=1,stroke=1)
            c.setFillColor(black);c.setFont('Helvetica-Bold',8)
            c.drawCentredString(x+kw/2,y+8,targets[n])
    for j,n in enumerate(white_notes[:-1]):
        if n%12 not in {0,2,5,7,9}: continue
        sharp=n+1;x=x0+(j+1)*kw-bw/2
        c.setFillColor(black);c.rect(x,y+kh-bh,bw,bh,fill=1,stroke=1)
        if sharp in targets:
            c.setFillColor(white);c.circle(x+bw/2,y+kh-bh+9,6,fill=1,stroke=0)
            c.setFillColor(black);c.setFont('Helvetica-Bold',8)
            c.drawCentredString(x+bw/2,y+kh-bh+6,targets[sharp])
    # All selected notes must be represented by a key within this range.
    assert all(41<=n<=71 for n in targets)

txt(M,H-105,'Play each L and all three R keys together. Shading also marks the selected white keys.',9)
for i,((degree,_,notes),(name,lh,rh)) in enumerate(zip(chords,voicings)):
    top=H-133-i*94
    txt(M,top,name+' ('+degree+')',11,'Helvetica-Bold')
    txt(M+155,top,'LH: '+lh+'     RH: '+rh,10)
    piano(top-54,lh,rh)
txt(M,49,'All notes fit B Phrygian. These keyboard voicings work with either guitar tuning.',9)
c.showPage()

header('PROGRESSIONS & SYNTH IDEAS','Original practice loops | Suggested tempo: 70-100 BPM, in 4/4.',3)
txt(M, H-110,'Each box is one bar. Repeat each loop; finish on Bm.',10)
progressions=[
 ('01  The Phrygian half-step','| Bm | C | Bm | Bm |','i - bII - i - i: hold Bm and hear C pull back down.'),
 ('02  Add a darker turn','| Bm | C | Am | Bm |','i - bII - bvii - i: A natural keeps the return to B minor clear.'),
 ('03  Descending roots','| Bm | Am | G | C | Bm | Bm |','i - bvii - bVI - bII - i - i: give the final Bm extra time.'),
 ('04  Minor lift, close return','| Bm | D | C | Bm |','i - bIII - bII - i: return from C to Bm to reinforce B as home.')]
yy=H-143
for title,prog,caption in progressions:
    txt(M,yy,title,11,'Helvetica-Bold')
    txt(M,yy-23,prog,13,'Courier-Bold')
    txt(M,yy-43,caption,9)
    yy-=77
txt(M,367,'Moving-bass loop: B - C - A - B',13,'Helvetica-Bold')
lines(346,['Both hands change each bar. The right-hand notes match the piano diagrams.',
           'Hear the bass climb a half-step from B to C, drop to A, then return to B.'],9,15)
moving=[('1','Bm','B2','B3 D4 F#4'),('2','C','C3','C4 E4 G4'),
        ('3','Am','A2','C4 E4 A4'),('4','Bm','B2','B3 D4 F#4')]
for _,chord,lh,rh in moving:
    assert all(pc(n) in allowed for n in [lh]+rh.split())
    assert {pc(n) for n in [lh]+rh.split()} == expected[chord]
table(301,['Bar','Chord','Left hand','Right hand'],[45,95,100,W-2*M-240],moving,row_h=27)
lines(145,['Start simply: play both hands on beat 1 and hold for the bar.',
           'Then try: bass on beat 1, right-hand notes from low to high on beats 2, 3 and 4.',
           'Let Bm settle; use C natural in the melody to highlight the Phrygian tension.',
           'If the scale root changes with a lower tuning, transpose every chord equally.'],9,18)
c.showPage()

# New progressions and their complete pitch collections.
extensions={'Bm7':{11,2,6,9},'Cmaj7':{0,4,7,11},'Em7':{4,7,11,2},
            'Gmaj7':{7,11,2,6},'Am7':{9,0,4,7},'Dadd9':{2,6,9,4}}
catalog={**expected,**extensions}
for name,root in [('B5',11),('C5',0),('D5',2),('G5',7),('A5',9)]:
    catalog[name]={root,(root+7)%12}
assert all(notes <= allowed for notes in catalog.values())

def styles_page(page,title,subtitle,groups):
    header(title,subtitle,page)
    lines(H-108,['Each box = one bar in 4/4. Repeat the loop; end the piece on Bm or Bm7.',
                 'Piano keys: triads p2, extended chords p7. Tips: pp13-14. Bass follows chord roots.'],9,15)
    y=H-163
    for group,loops in groups:
        txt(M,y,group,14,'Helvetica-Bold');y-=29
        for label,seq,feel in loops:
            assert all(chord in catalog for chord in seq)
            txt(M,y,label,10,'Helvetica-Bold')
            txt(M,y-23,'| '+' | '.join(seq)+' |',11,'Courier-Bold')
            txt(M,y-43,feel,9)
            y-=83
        y-=24
    lines(84,['Keep B as the point of rest: emphasize B in the melody and let C resolve toward B.',
              'These are mood suggestions; rhythm, voicing and sound shape the result.'],9,16)
    assert y>60
    c.showPage()

styles_page(4,'AMBIENT & ETHEREAL','Original B Phrygian loops | Let the harmony breathe.',[
 ('Ambient | 50-75 BPM',[
  ('05  Slow drift',['Bm7','Cmaj7','Em7','Bm7'],'Sustain pads; give each chord two bars if you want a slower harmonic rhythm.'),
  ('06  Quiet return',['Bm7','Em7','Cmaj7','Bm7'],'Use soft attacks and sparse notes; let Cmaj7 settle back into Bm7.'),
  ('07  Wide horizon',['Bm7','Gmaj7','Cmaj7','Bm7'],'Spread notes across octaves; play the bass gently and leave gaps.')]),
 ('Ethereal | 65-95 BPM',[
  ('08  Floating light',['Bm7','Dadd9','Cmaj7','Bm7'],'Arpeggiate the right hand in eighth notes; add delay and light reverb.'),
  ('09  Falling through',['Bm7','Am7','Em7','Cmaj7','Bm7','Bm7'],'Use a high, sparse melody; hold the final Bm7 for the last two bars.'),
  ('10  Glass motion',['Bm7','Gmaj7','Em7','Cmaj7','Bm7','Bm7'],'Keep common tones ringing with a synth release; change bass notes cleanly.')])])

styles_page(5,'METAL & ROCK','Original B Phrygian loops | Make the rhythm carry the weight.',[
 ('Metal | 85-140 BPM',[
  ('11  Half-step pressure',['B5','C5','B5','A5'],'Play B+F# briefly and release; leave silence after each hit. See term 4, p13.'),
  ('12  Climb and collapse',['B5','C5','D5','C5','B5','B5'],'Strike twice per beat; stop early before the return to B5. See term 7, p14.'),
  ('13  Heavy descent',['B5','G5','A5','C5','B5','B5'],'Use a strong snare on beat 3; sustain bass octaves below. See term 8, p14.')]),
 ('Rock | 95-140 BPM',[
  ('14  Open drive',['Bm','G','D','C','Bm','Bm'],'Play all 3 chord notes (Bm = B D F#), twice per beat. See term 9, p14.'),
  ('15  Angular lift',['Bm','D','Am','C','Bm','Bm'],'Repeat a melody ending C-B as C changes to Bm. See term 10, p14.'),
  ('16  Dark release',['Bm','Em','G','C','Bm','Bm'],'Start with B3-D4; later spread Bm as B2-F#3-D4-B4. See term 11, p14.')])])

styles_page(6,'POP & CINEMATIC','Original B Phrygian loops | Familiar motion with a darker half-step.',[
 ('Pop / dark pop | 85-120 BPM',[
  ('17  Dark chorus',['Bm','G','D','Am','C','Bm'],'Use a regular drum groove and a repeating melody; save C for the final turn.'),
  ('18  Bright surface',['Bm','D','G','C'],'Keep a simple hook around B and D; the loop returns from C to Bm.'),
  ('19  Stepwise bass',['Bm','Am','G','C'],'Use bass B-A-G-C; try offbeat chord stabs and resolve the melody to B.')]),
 ('Cinematic / tension | 55-90 BPM',[
  ('20  Unstable shadow',['Bm','F#dim','C','Bm'],'Play F#dim quietly and briefly; hear its C natural lead into the C chord.'),
  ('21  Long scene',['Bm','Bm','Em','C','G','Am','C','Bm'],'Build over eight bars: start sparse, add layers, then return to a clear B bass.'),
  ('22  Suspended scene',['Bm7','Am7','Cmaj7','Em7','Cmaj7','Bm7'],'Use slow broken chords; let the final Bm7 ring before repeating.')])])

header('FULLER PIANO VOICINGS','L = left-hand root + fifth | R = right-hand chord | C4 = middle C',7)
lines(H-106,['Use these richer chords in loops 05-10 and wherever their symbols appear.',
              'The keyboard shows every played key. Move a voicing up an octave if the bass gets muddy.'],9,15)
full=[('Bm7','B2 F#3','A3 B3 D4 F#4'),('Cmaj7','C3 G3','B3 C4 E4 G4'),
      ('Em7','E3 B3','D4 E4 G4 B4'),('Gmaj7','G2 D3','F#3 B3 D4 G4'),
      ('Am7','A2 E3','G3 C4 E4 A4'),('Dadd9','D3 A3','D4 E4 F#4 A4')]
for i,(name,lh,rh) in enumerate(full):
    assert {pc(n) for n in (lh+' '+rh).split()} == catalog[name]
    top=H-155-i*94
    txt(M,top,name,11,'Helvetica-Bold')
    txt(M+105,top,'LH: '+lh+'     RH: '+rh,10)
    piano(top-54,lh,rh)
lines(75,['Power-chord spellings: B5 = B F#; C5 = C G; D5 = D A; G5 = G D; A5 = A E.',
          'Optional bass octaves: replace a left-hand fifth with root + root an octave higher.',
          'Pages 1-10 and 12 stay in B Phrygian. Page 11 marks the blues exceptions.'],9,16)
c.showPage()

styles_page(8,'ELECTRO & ELECTROPOP','B Phrygian sketches | Suggested starting tempos, not genre rules.',[
 ('Electro | 110-135 BPM',[
  ('23  Machine steps',['Bm','C','Em','Bm'],'Use a syncopated drum-machine beat, short chord stabs and a dry octave bass.'),
  ('24  Metallic circuit',['B5','D5','C5','B5'],'Sequence sixteenth-note bass bursts; leave rests around snare hits.'),
  ('25  Cold transmission',['Bm7','Am7','Cmaj7','Bm7'],'Use an FM pluck or vocoder-like pad; put chords on unexpected offbeats.')]),
 ('Electropop | 100-125 BPM',[
  ('26  Neon refrain',['Bm','G','Am','C'],'Use a steady kick, bright chord stabs and a short vocal-style melody on B.'),
  ('27  Glass chorus',['Bm7','Dadd9','Am7','Cmaj7'],'Build a repeating synth hook; use C natural before the return to Bm7.'),
  ('28  Night drive',['Bm','Em','D','C'],'Try octave bass pulses and a wide pad; keep the lead melody simple.')])])

styles_page(9,'HYPERPOP & BLACK METAL','B Phrygian sketches | Let texture and articulation define the contrast.',[
 ('Hyperpop | 140-180 BPM, or half-time feel',[
  ('29  Sugar and static',['Bm7','Gmaj7','Dadd9','Cmaj7'],'Use bright supersaws and abrupt stops; double a simple hook an octave higher.'),
  ('30  Pixel jump',['Bm','C','D','Am','C','Bm'],'Chop the chords into short bursts; jump registers between phrases.'),
  ('31  Digital bloom',['Bm7','Am7','Cmaj7','Em7','Cmaj7','Bm7'],'Layer a pluck with a wide pad; switch to sparse bass for the final return.')]),
 ('Black metal | 140-200 BPM, or slower atmospheric feel',[
  ('32  Frost line',['Bm','C','Bm','Em'],'Rapidly repeat upper chord tones; use a thin pad under a relentless drum pulse.'),
  ('33  Ash descent',['Bm','Am','G','C'],'Use tremolo-like repeated notes; sustain the low root while each chord lasts.'),
  ('34  Distant ruin',['Bm','F#dim','Em','C','Bm','Bm'],'Let the diminished chord add friction; contrast fast repetition with a long Bm.')])])

styles_page(10,'DUB & DUBSTEP','B Phrygian sketches | Leave space for bass, rhythm and effects.',[
 ('Dub | 65-85 BPM',[
  ('35  Echo chamber',['Bm7','Em7','Cmaj7','Bm7'],'Use short offbeat chord chops, a melodic sub bass and occasional delay throws.'),
  ('36  Half-step skank',['Bm','C','Bm','Am'],'Keep the chord hits brief; answer them with bass phrases rather than held roots.'),
  ('37  Empty space',['Bm7','Am7','Em7','Cmaj7'],'Drop the chords out for a bar on later repeats; let bass and echoes carry it.')]),
 ('Dubstep | around 140 BPM, half-time feel',[
  ('38  Sub pressure',['B5','C5','B5','G5'],'Keep deep sub notes simple; put rhythmic filter movement on a separate mid bass.'),
  ('39  Broken signal',['Bm','D','C','Bm'],'Use a sparse half-time groove and syncopated bass replies between chord hits.'),
  ('40  Weightless drop',['Bm7','Gmaj7','Em7','Cmaj7'],'Start with airy pads, then shorten the chords and open space for the bass drop.')])])

header('BLUES | SCALE EXCEPTIONS','B-centred examples | Blues harmony can deliberately leave B Phrygian.',11)
lines(H-111,['Only example 41 stays entirely inside B Phrygian. Examples 42-43 borrow notes.',
              'B minor blues melody: B D E F F# A. F natural is also outside B Phrygian.'],9,16)
txt(M,H-169,'41  Phrygian blues-inspired loop | 65-95 BPM',12,'Helvetica-Bold')
txt(M,H-194,'| Bm7 | Em7 | Bm7 | C | Bm7 | Bm7 |',11,'Courier-Bold')
lines(H-217,['This is a six-bar modal loop, not a traditional 12-bar blues.',
             'Try a shuffle feel and short answering phrases. Keep the melody in B Phrygian.'],9,16)

minor_blues=['Bm7']*4+['Em7']*2+['Bm7']*2+['F#7','Em7','Bm7','F#7']
dominant_blues=['B7','E7','B7','B7','E7','E7','B7','B7','F#7','E7','B7','F#7']
borrowed={'F#7':{6,10,1,4},'B7':{11,3,6,9},'E7':{4,8,11,2}}
assert borrowed['F#7']-allowed == {10,1}
assert borrowed['B7']-allowed == {3}
assert borrowed['E7']-allowed == {8}
for yy,title,seq,description in [
 (H-300,'42  Minor 12-bar blues | borrowed dominant',minor_blues,
  'F#7 adds A# and C#. B Phrygian alone will clash with these chord tones.'),
 (H-470,'43  Dominant 12-bar blues | outside Phrygian',dominant_blues,
  'B7 adds D#; E7 adds G#; F#7 adds A# and C#. This uses a different palette.')]:
    assert len(seq)==12 and all(ch in catalog or ch in borrowed for ch in seq)
    txt(M,yy,title,12,'Helvetica-Bold')
    for row in range(3):
        txt(M,yy-26-row*22,'| '+' | '.join(seq[row*4:row*4+4])+' |',12,'Courier-Bold')
    txt(M,yy-100,description,9)

txt(M,210,'Chord notes for the borrowed harmony',12,'Helvetica-Bold')
table(190,['Chord','Notes','Notes outside B Phrygian'],[80,180,W-2*M-260],
      [('B7','B D# F# A','D#'),('E7','E G# B D','G#'),('F#7','F# A# C# E','A#, C#')],row_h=26)
lines(58,['Choose the scale by the current harmony here; the Phrygian-only rule is relaxed.'],9,16)
c.showPage()

styles_page(12,'MORE ELECTRONIC DIRECTIONS','B Phrygian sketches | One starting loop for each production direction.',[
 ('Techno / house / industrial',[
  ('44  Techno | 125-140 BPM',['Bm','C','Bm','Em'],'Repeat a short chord; slowly open the synth filter over 8 bars. See term 1, p13.'),
  ('45  House | 118-128 BPM',['Bm7','Em7','Am7','Cmaj7'],'Delay offbeat chord hits slightly; move bass on each beat. See terms 2-3, p13.'),
  ('46  Industrial | 100-135 BPM',['B5','C5','G5','B5'],'Play B+F# as short stabs; add metallic percussion and repeating bass. See 4, p13.')]),
 ('Drum & bass / UK garage / trip-hop',[
  ('47  Drum & bass | 165-175 BPM',['Bm7','Dadd9','Em7','Cmaj7'],'Let chords last a bar or two over fast breaks; leave room for a clean sub bass.'),
  ('48  UK garage | 128-138 BPM',['Bm7','Am7','Em7','Cmaj7'],'Delay offbeat chord stabs; use syncopated kicks and snares on 2 and 4. See 5, p13.'),
  ('49  Trip-hop | 65-95 BPM',['Bm7','Cmaj7','Am7','Bm7'],'Relax drum timing; use mellow keys, fewer bass notes and small changes. See 6, p13.')])])

from reportlab.lib.utils import simpleSplit

def explain(y,title,paragraphs):
    txt(M,y,title,12,'Helvetica-Bold'); y-=19
    for paragraph in paragraphs:
        for line in simpleSplit(paragraph,'Helvetica',10,W-2*M):
            txt(M,y,line,10); y-=14
        y-=5
    return y-13

header('PLAYING TIPS | SOUND & GROOVE','Terms 1-6 | Practical examples for the progression notes.',13)
y=H-112
y=explain(y,'1  Automate timbre slowly',[
 'Timbre means the character of the sound. Automation changes a synth setting over time. Keep the notes repeating while you gradually open the filter over eight bars: the sound becomes brighter without changing the chord.'])
y=explain(y,'2  Swung offbeat chords',[
 'Count "1 & 2 & 3 & 4 &". The numbered beats are the main pulse; the & counts sit between them. Strike short chords on the & counts. For swing, place those hits slightly later than the exact midpoint, creating a long-short bounce.'])
y=explain(y,'3  Walking bass phrase',[
 'Here this means a moving bass line instead of a held root. Try one note per beat: B-C-D-F# over Bm7, then land on E when Em7 arrives. All these notes fit B Phrygian. Traditional jazz walking bass is a more specific technique.'])
y=explain(y,'4  Clipped fifths',[
 'Play a root and its fifth together, then stop them quickly. For B5, strike B+F# and release, leaving silence. For C5 use C+G. "Clipped" describes the short duration; it does not change the interval.'])
y=explain(y,'5  Shuffled chord chops and a two-step beat',[
 'Chord chops are short chord stabs. Shuffled means a long-short rhythmic bounce, with delayed offbeats. A simple UK garage starting point uses snares on beats 2 and 4, syncopated kicks, and gaps instead of a kick on every beat. Let the bass answer the chord stabs.'])
y=explain(y,'6  Loose drums, warm keys, sparse bass, evolving textures',[
 'Loose drums have small timing and volume variations. Warm keys use a mellow piano or synth sound with softer high frequencies. Sparse bass means fewer notes and more silence.',
 'Let textures evolve by making small changes over several bars: add a quiet echo, alter a filter, introduce one high note, or fade in a background sound. Keep the main rhythm recognizable.'])
assert y>45
c.showPage()

header('PLAYING TIPS | NOTES & SPACE','Terms 7-11 | Count the rhythm, hear the return, spread the chord.',14)
y=H-112
y=explain(y,'7  Repeat eighth-note hits, then leave space',[
 'An eighth-note pulse has two hits per beat: "1 & 2 & 3 & 4 &". Repeat the current chord on those counts. In the final bar before returning to B5, play only on "1 & 2 &", then rest for "3 & 4 &". Hit B5 on beat 1 of the next bar. The silence makes that return stand out.'])
y=explain(y,'8  Half-time drum feel',[
 'Keep the song tempo unchanged but make the drum accents feel slower. A common starting point replaces snares on beats 2 and 4 with one strong snare on beat 3. At 140 BPM, this can feel like a 70 BPM groove. The notes can still move quickly above it.'])
y=explain(y,'9  Full triads',[
 'A triad contains three different chord notes. Bm = B-D-F#; C = C-E-G; D = D-F#-A. Play all three together. A power chord such as B5 uses only B-F#, leaving out D, the minor third that gives Bm its minor character.'])
y=explain(y,'10  Use the C-to-Bm return as the hook',[
 'A hook is a short idea you repeat so listeners recognize and anticipate it. Whenever the chords change from C to Bm, repeat a melody ending C-B. Emphasize that half-step fall with a stronger attack, a pause before it, or a repeated rhythm.'])
y=explain(y,'11  Begin with fewer notes, then widen the voicing',[
 'A voicing is how you arrange chord notes across registers. Start sparsely with B3-D4. Later add F#4 to complete Bm. For a wider version, spread the same chord as B2-F#3-D4-B4. C4 means middle C.',
 'Adding notes makes a chord fuller; spacing them farther apart makes it wider. You can increase these separately. Try widening only on the final repeat, while keeping the bass rhythm steady.'])
assert y>45
c.showPage()
c.save()
print(OUT)
