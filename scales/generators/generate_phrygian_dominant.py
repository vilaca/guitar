#!/usr/bin/env python3
"""7-string Phrygian dominant: guitar, piano and 43 progressions

Install: python -m pip install reportlab
Run: python generate_phrygian_dominant.py --output my_guide.pdf
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, HexColor, white
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reportlab
from pathlib import Path

import argparse

parser = argparse.ArgumentParser(description='7-string Phrygian dominant: guitar, piano and 43 progressions')
parser.add_argument('--output', default='phrygian_dominant_7_string_standard.pdf',
                    help='Output PDF path (default: %(default)s)')
args = parser.parse_args()
OUT = Path(args.output).expanduser().resolve()
OUT.parent.mkdir(parents=True, exist_ok=True)

c = canvas.Canvas(str(OUT), pagesize=A4)
c.setTitle('B Phrygian Dominant - 7-string guitar, piano and 43 progressions')
c.setAuthor('')
W,H = A4
M=38
TOTAL=14
font_dir = Path(reportlab.__file__).resolve().parent / 'fonts'
for family, filename in [('Body', 'Vera.ttf'), ('Bold', 'VeraBd.ttf')]:
    pdfmetrics.registerFont(TTFont(family, str(font_dir / filename)))

def txt(x,y,s,size=10,font='Body'):
    c.setFillColor(black); c.setFont(font,size); c.drawString(x,y,s)

note_names = {11: 'B', 0: 'C', 3: 'D#', 4: 'E', 6: 'F#', 7: 'G', 9: 'A'}
allowed = set(note_names)
opens = [35, 40, 45, 50, 55, 59, 64]
labels = ['7 B', '6 E', '5 A', '4 D', '3 G', '2 B', '1 e']
def route(per_string):
    notes = [n for n in range(35, 100) if n % 12 in allowed]
    rows, i = [], 0
    for open_pitch, count in zip(opens, per_string):
        rows.append([n - open_pitch for n in notes[i:i + count]])
        i += count
    return rows

diagonal = route([4] * 7)

def pattern(top, title, frets, gap=26):
    txt(M, top, title, 13, 'Bold')
    left = M + 38
    step = (W - M - 12 - left) / (sum(map(len, frets)) + 1)
    played = []

    def draw_row(y, label, open_pitch, row, start):
        txt(M, y - 3, label, 8, 'Bold')
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
            size = 9 if neighbor else 11
            font = 'Bold' if (open_pitch + fret) % 12 == 11 else 'Body'
            x = left + (start + 1 + i - first) * step
            width = c.stringWidth(label, font, size) + 1
            c.setFillColor(white)
            c.rect(x - width / 2, y - 6, width, 12, fill=1, stroke=0)
            c.setFillColor(black)
            c.setFont(font, size)
            c.drawCentredString(x, y - 3, label)

    for string, row in enumerate(frets):
        y = top - 42 - (6 - string) * gap
        draw_row(y, labels[string], opens[string], row, len(played))
        played.extend(opens[string] + f for f in row)
    return played

def header(title, subtitle, page):
    size = 20
    while pdfmetrics.stringWidth(title, 'Bold', size) > W - 2 * M:
        size -= .5
    txt(M,H-44,title,size,'Bold')
    txt(M,H-66,subtitle,9)
    c.setStrokeColor(HexColor('#aaaaaa')); c.setLineWidth(.6); c.line(M,H-80,W-M,H-80)
    txt(M,25,'7-STRING PHRYGIAN DOMINANT | guitar + piano / synth',7)
    txt(W-M-30,25,f'{page}/{TOTAL}',7)

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
            txt(xs[j]+6,yy-13,str(cell),font_size,'Bold' if i==0 else 'Body')
        c.setStrokeColor(HexColor('#cccccc'));c.setLineWidth(.4)
        c.line(M,yy-row_h+5,xs[-1],yy-row_h+5)
    return y-(len(rows)+1)*row_h


# Page 1: scale, formula and fretboard map.
header('7-STRING PHRYGIAN DOMINANT','Standard seven-string tuning | B E A D G B E',1)
lines(H-110,['B Phrygian dominant: B  C  D#  E  F#  G  A',
             'Formula from B: 1  b2  3  4  5  b6  b7'],11,18)
lines(H-150,['Phrygian dominant is Phrygian with a major third: D# turns the tonic into a B major chord.',
             'Keep the half-step pull from C to B; this is the fifth mode of E harmonic minor. B is home.'],9.5,15)
txt(M, H-210, 'STANDARD 7-STRING | FRETS 0-12', 12, 'Bold')
txt(M, H-228, 'Dark cells mark B roots. A dash marks a note outside the scale.', 9)
left = M + 38
cell_width = (W - M - left) / 13
row_height = 29
grid_top = H - 262
c.setFont('Bold', 8)
for fret in range(13):
    c.drawCentredString(left + (fret + 0.5) * cell_width, grid_top + 9, str(fret))
for row, (label, pitch) in enumerate(zip(reversed(labels), reversed(opens))):
    y = grid_top - (row + 1) * row_height
    txt(M, y + 10, label, 9, 'Bold')
    for fret in range(13):
        note = note_names.get((pitch + fret) % 12, '-')
        x = left + fret * cell_width
        root = note == 'B'
        c.setFillColor(HexColor('#333333') if root else white)
        c.setStrokeColor(HexColor('#cccccc'))
        c.rect(x, y, cell_width, row_height, fill=1, stroke=1)
        c.setFillColor(white if root else black)
        c.setFont('Bold' if root else 'Body', 9)
        c.drawCentredString(x + cell_width / 2, y + 10, note)
y = grid_top - 7 * row_height - 28
lines(y,['Thinnest string at the top. The map repeats 12 frets higher.'],9)
txt(M, y - 34, 'Root rule', 11, 'Bold')
lines(y - 54,['The open seventh string is the root. Open D is outside the scale; the other open strings fit.',
              'For a lower standard tuning, keep the fret numbers and use the new seventh-string root.'],9.5,15)
txt(M, y - 108, 'Using the half-step', 11, 'Bold')
lines(y - 128,['Land on B to rest. Move to C for tension, then fall back to B.',
               'You do not need every scale note in every chord.'],9.5,15)
c.showPage()

# Page 2: guitar patterns.
header('GUITAR PATTERNS','B Phrygian dominant | Standard B E A D G B E',2)
played = pattern(H-120, 'DIAGONAL | start on open B, string 7', diagonal)
assert played == [n for n in range(35, 82) if n % 12 in allowed]
assert all(a < b for a, b in zip([r[0] for r in diagonal], [r[0] for r in diagonal][1:]))
y = H-350
for instruction in [
    'Read left to right. Bold numbers mark B. Parentheses show the neighboring scale frets on the same string. Skip them when playing the run.',
    'Diagonal: start on open B1 (string 7), play four notes per string and shift up the neck. Finish on A5 (string 1, fret 17).',
]:
    for line in simpleSplit(instruction, 'Body', 9.3, W - 2 * M):
        txt(M, y, line, 9.3); y -= 14
    y -= 10
assert y > 45
c.showPage()

header('PIANO KEYS | BASIC CHORDS','L = left-hand bass | R = right-hand chord | C4 = middle C',3)
chords=[('I','B','B D# F#'),('bII','C','C E G'),('iii diminished','D#dim','D# F# A'),('iv','Em','E G B'),('v diminished','F#dim','F# A C'),('bVI augmented','G+','G B D#'),('bvii','Am','A C E')]
voicings=[('B','B2','B3 D#4 F#4'),('C','C3','C4 E4 G4'),
          ('D#dim','D#3','A3 D#4 F#4'),('Em','E3','B3 E4 G4'),
          ('F#dim','F#2','A3 C4 F#4'),('G+','G2','B3 D#4 G4'),
          ('Am','A2','C4 E4 A4')]
expected={'B':{11,3,6},'C':{0,4,7},'D#dim':{3,6,9},'Em':{4,7,11},
          'F#dim':{6,9,0},'G+':{7,11,3},'Am':{9,0,4}}
pitch_classes={'C':0,'D#':3,'E':4,'F#':6,'G':7,'A':9,'B':11}
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
        c.setFillColor(black);c.setFont('Body',7)
        c.drawCentredString(x+kw/2,y-9,names[n%12]+str(n//12-1))
        if n in targets:
            c.setFillColor(white);c.circle(x+kw/2,y+11,6.5,fill=1,stroke=1)
            c.setFillColor(black);c.setFont('Bold',8)
            c.drawCentredString(x+kw/2,y+8,targets[n])
    for j,n in enumerate(white_notes[:-1]):
        if n%12 not in {0,2,5,7,9}: continue
        sharp=n+1;x=x0+(j+1)*kw-bw/2
        c.setFillColor(black);c.rect(x,y+kh-bh,bw,bh,fill=1,stroke=1)
        if sharp in targets:
            c.setFillColor(white);c.circle(x+bw/2,y+kh-bh+9,6,fill=1,stroke=0)
            c.setFillColor(black);c.setFont('Bold',8)
            c.drawCentredString(x+bw/2,y+kh-bh+6,targets[sharp])
    # All selected notes must be represented by a key within this range.
    assert all(41<=n<=71 for n in targets)

txt(M,H-105,'Play each L and all three R keys together. Shading also marks the selected white keys.',9)
for i,((degree,_,notes),(name,lh,rh)) in enumerate(zip(chords,voicings)):
    top=H-133-i*94
    txt(M,top,name+' ('+degree+')',11,'Bold')
    txt(M+155,top,'LH: '+lh+'     RH: '+rh,10)
    piano(top-54,lh,rh)
txt(M,49,'All notes fit B Phrygian dominant. Play these voicings over the B-standard guitar patterns.',9)
c.showPage()

# New progressions and their complete pitch collections.
extensions={'B7':{11,3,6,9},'Cmaj7':{0,4,7,11},'Emadd9':{4,7,11,6},
            'F#m7b5':{6,9,0,4},'Am7':{9,0,4,7},'D#m7b5':{3,6,9,0}}
catalog={**expected,**extensions}
for name,root in [('B5',11),('C5',0),('E5',4),('A5',9)]:
    catalog[name]={root,(root+7)%12}
assert all(notes <= allowed for notes in catalog.values())

header('PIANO KEYS | FULLER CHORDS','L = left-hand root + fifth | R = right-hand chord | C4 = middle C',4)
lines(H-106,['Use these richer chords in loops 05-10 and wherever their symbols appear.',
              'The keyboard shows every played key. Move a voicing up an octave if the bass gets muddy.'],9,15)
full=[('B7','B2 F#3','A3 B3 D#4 F#4'),('Cmaj7','C3 G3','B3 C4 E4 G4'),
      ('Emadd9','E3 B3','E4 F#4 G4 B4'),('F#m7b5','F#2 C3','A3 C4 E4 F#4'),
      ('Am7','A2 E3','G3 C4 E4 A4'),('D#m7b5','D#3 A3','C4 D#4 F#4 A4')]
for i,(name,lh,rh) in enumerate(full):
    assert {pc(n) for n in (lh+' '+rh).split()} == catalog[name]
    top=H-155-i*94
    txt(M,top,name,11,'Bold')
    txt(M+105,top,'LH: '+lh+'     RH: '+rh,10)
    piano(top-54,lh,rh)
lines(75,['Power-chord spellings: B5 = B F#; C5 = C G; E5 = E B; A5 = A E.',
          'Optional bass octaves: replace a left-hand fifth with root + root an octave higher.',
          'Pages 1-11 and 13 stay in B Phrygian dominant. Page 12 marks the blues exceptions.'],9,16)
c.showPage()

header('START HERE | FOUR LOOPS','Each box is one bar in 4/4. Try 70-100 BPM and repeat each loop.',5)
txt(M, H-110,'One chord per bar in 4/4. Follow the roots in the bass and resolve to B or B7.',10)
variations = {
    '22': ('Variation 31 - Digital bloom / Hyperpop | 140-180 BPM, or half-time feel',
           'Layer a pluck with a wide pad; switch to sparse bass for the final return.'),
    '19': ('Variation 33 - Ash descent / Black metal | 140-200 BPM, or slower atmospheric feel',
           'Use tremolo-like repeated notes; sustain the low root while each chord lasts.'),
    '06': ('Variation 35 - Echo chamber / Dub | 65-85 BPM',
           'Use short offbeat chord chops, a melodic sub bass and occasional delay throws.'),
    '04': ('Variation 39 - Broken signal / Dubstep | around 140 BPM, half-time feel',
           'Use a sparse half-time groove and syncopated bass replies between chord hits.'),
    '32': ('Variation 44 - Techno | 125-140 BPM',
           'Repeat short chord stabs over eight bars.'),
    '37': ('Variation 48 - UK garage | 128-138 BPM',
           'Delay offbeat chord stabs; use syncopated kicks and snares on 2 and 4. Glossary: two-step groove.'),
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

progressions=[
 ('01  The Phrygian half-step','| B | C | B | B |','I - bII - I - I: hold B and hear C pull back down.'),
 ('02  Add a darker turn','| B | C | Am | B |','I - bII - bvii - I: A natural keeps the return to B major clear.'),
 ('03  Descending roots','| B | Am | G+ | C | B | B |','I - bvii - bVI+ - bII - I - I: give the final B extra time.'),
 ('04  Dark lift, close return','| B | D#dim | C | B |','I - iii dim - bII - I: return from C to B to reinforce B as home.')]
yy=H-143
for title,prog,caption in progressions:
    txt(M,yy,title,11,'Bold')
    txt(M,yy-23,prog,10,'Courier')
    txt(M,yy-43,caption,9)
    draw_variation(yy-56, title)
    yy-=77
txt(M,367,'Moving-bass loop: B - C - A - B',13,'Bold')
lines(346,['Both hands change each bar. The right-hand notes match the piano diagrams.',
           'Hear the bass climb a half-step from B to C, drop to A, then return to B.'],9,15)
moving=[('1','B','B2','B3 D#4 F#4'),('2','C','C3','C4 E4 G4'),
        ('3','Am','A2','C4 E4 A4'),('4','B','B2','B3 D#4 F#4')]
for _,chord,lh,rh in moving:
    assert all(pc(n) in allowed for n in [lh]+rh.split())
    assert {pc(n) for n in [lh]+rh.split()} == expected[chord]
table(301,['Bar','Chord','Left hand','Right hand'],[45,95,100,W-2*M-240],moving,row_h=27)
lines(145,['Start simply: play both hands on beat 1 and hold for the bar.',
           'Then try: bass on beat 1, right-hand notes from low to high on beats 2, 3 and 4.',
           'Let B settle; use C natural in the melody to highlight the Phrygian tension.',
           'If the scale root changes with a lower tuning, transpose every chord equally.'],9,18)
c.showPage()

def styles_page(page,title,subtitle,groups,variation_guide=None):
    header(title,subtitle,page)
    txt(M,H-108,'1 bar per chord | Keys pp3-4 | Chords p5 | Tips p14',9)
    y=H-140
    for group,loops in groups:
        txt(M,y,group,14,'Bold');y-=29
        for label,seq,feel in loops:
            assert all(chord in catalog for chord in seq)
            txt(M,y,label,10,'Bold')
            txt(M,y-23,'| '+' | '.join(seq)+' |',10,'Courier')
            txt(M,y-43,feel,9)
            y = draw_variation(y-58, label) - 18
        y-=24
    if variation_guide:
        txt(M, 60, variation_guide, 9)
    assert y>60
    c.showPage()

styles_page(6,'AMBIENT & ETHEREAL','B Phrygian dominant loops | Let the harmony breathe.',[
 ('Ambient | 50-75 BPM',[
  ('05  Slow drift',['B7','Cmaj7','Emadd9','B7'],'Sustain pads; give each chord two bars if you want a slower harmonic rhythm.'),
  ('06  Quiet return',['B7','Emadd9','Cmaj7','B7'],'Use soft attacks and sparse notes; let Cmaj7 settle back into B7.'),
  ('07  Wide horizon',['B7','F#m7b5','Cmaj7','B7'],'Spread notes across octaves; play the bass gently and leave gaps.')]),
 ('Ethereal | 65-95 BPM',[
  ('08  Floating light',['B7','Emadd9','Cmaj7','B7'],'Arpeggiate the right hand in eighth notes; add delay and light reverb.'),
  ('09  Falling through',['B7','Am7','Emadd9','Cmaj7','B7','B'],'Use a high, sparse melody; hold the final B7 for the last two bars.'),
  ('10  Glass motion',['B7','F#m7b5','Emadd9','Cmaj7','B7','B'],'Keep common tones ringing with a synth release; change bass notes cleanly.')])])

styles_page(7,'METAL & ROCK','B Phrygian dominant loops | Make the rhythm carry the weight.',[
 ('Metal | 85-140 BPM',[
  ('11  Half-step pressure',['B5','C5','B5','A5'],'Play B+F# briefly and release; leave silence after each hit. Tip 2, p14.'),
  ('12  Climb and collapse',['B5','C5','E5','C5','B5','B5'],'Strike twice per beat; stop early before the return to B5. Glossary: eighth-note hits.'),
  ('13  Heavy descent',['B5','E5','A5','C5','B5','B5'],'Use a strong snare on beat 3; sustain bass octaves below. Glossary: half-time feel.')]),
 ('Rock | 95-140 BPM',[
  ('14  Open drive',['B','Am','D#dim','C','B','B7'],'Play all 3 chord notes (B = B D# F#), twice per beat. Tip 3, p14.'),
  ('15  Angular lift',['B','D#dim','Am','C','B','B7'],'Repeat a melody ending C-B as C changes to B. Tip 4, p14.'),
  ('16  Dark release',['B','Em','Am','C','B','B7'],'Start with B3-D#4; later spread B as B2-F#3-D#4-B4. Tip 5, p14.')])])

styles_page(8,'POP & CINEMATIC','B Phrygian dominant loops | Familiar motion with a darker half-step.',[
 ('Pop / dark pop | 85-120 BPM',[
  ('17  Dark chorus',['B','Em','D#dim','Am','C','B'],'Use a regular drum groove and a repeating melody; save C for the final turn.'),
  ('18  Bright surface',['B','D#dim','Em','C'],'Keep a simple hook around B and D#; the loop returns from C to B.'),
  ('19  Stepwise bass',['B','Am','G+','C'],'Use bass B-A-G-C; try offbeat chord stabs and resolve the melody to B.')]),
 ('Cinematic / tension | 55-90 BPM',[
  ('20  Unstable shadow',['B','F#dim','C','B'],'Play F#dim quietly and briefly; hear its C natural lead into the C chord.'),
  ('21  Long scene',['B','B7','Em','C','G+','Am','C','B'],'Build over eight bars: start sparse, add layers, then return to a clear B bass.'),
  ('22  Suspended scene',['B7','Am7','Cmaj7','Emadd9','Cmaj7','B7'],'Use slow broken chords; let the final B7 ring before repeating.')])])

styles_page(9,'ELECTRO & ELECTROPOP','B Phrygian dominant loops | Suggested starting tempos, not genre rules.',[
 ('Electro | 110-135 BPM',[
  ('23  Machine steps',['B','C','Em','B'],'Use a syncopated drum-machine beat, short chord stabs and a dry octave bass.'),
  ('24  Metallic circuit',['B5','E5','C5','B5'],'Sequence sixteenth-note bass bursts; leave rests around snare hits.'),
  ('25  Cold transmission',['B7','Am7','Cmaj7','B7'],'Use an FM pluck or vocoder-like pad; put chords on unexpected offbeats.')]),
 ('Electropop | 100-125 BPM',[
  ('26  Neon refrain',['B','Em','Am','C'],'Use a steady kick, bright chord stabs and a short vocal-style melody on B.'),
  ('27  Glass chorus',['B7','Emadd9','Am7','Cmaj7'],'Build a repeating synth hook; use C natural before the return to B7.'),
  ('28  Night drive',['B','Em','D#dim','C'],'Try octave bass pulses and a wide pad; keep the lead melody simple.')])])

styles_page(10,'HYPERPOP & BLACK METAL','B Phrygian dominant loops | Let texture and articulation define the contrast.',[
 ('Hyperpop | 140-180 BPM, or half-time feel',[
  ('29  Sugar and static',['B7','F#m7b5','Emadd9','Cmaj7'],'Use bright supersaws and abrupt stops; double a simple hook an octave higher.'),
  ('30  Pixel jump',['B','C','D#dim','Am','C','B'],'Chop the chords into short bursts; jump registers between phrases.'),
  ]),
 ('Black metal | 140-200 BPM, or slower atmospheric feel',[
  ('32  Frost line',['B','C','B','Em'],'Rapidly repeat upper chord tones; use a thin pad under a relentless drum pulse.'),
  ('34  Distant ruin',['B','F#dim','Em','C','B','B7'],'Let the diminished chord add friction; contrast fast repetition with a long B.')])],
    variation_guide='Hyperpop and black metal variations: 31 and 33 on p8.')

styles_page(11,'DUB & DUBSTEP','B Phrygian dominant loops | Leave space for bass, rhythm and effects.',[
 ('Dub | 65-85 BPM',[
  ('36  Half-step skank',['B','C','B','Am'],'Keep the chord hits brief; answer them with bass phrases rather than held roots.'),
  ('37  Empty space',['B7','Am7','Emadd9','Cmaj7'],'Drop the chords out for a bar on later repeats; let bass and echoes carry it.')]),
 ('Dubstep | around 140 BPM, half-time feel',[
  ('38  Sub pressure',['B5','C5','B5','E5'],'Keep deep sub notes simple; put rhythmic filter movement on a separate mid bass.'),
  ('40  Weightless drop',['B7','F#m7b5','Emadd9','Cmaj7'],'Start with airy pads, then shorten the chords and open space for the bass drop.')])],
    variation_guide='Dub and dubstep variations: 35 on p6 and 39 on p5.')

header('BLUES | SCALE EXCEPTIONS','B Phrygian dominant blues | Blues harmony can deliberately leave the scale.',12)
lines(H-111,['Only example 41 stays entirely inside B Phrygian dominant. Examples 42-43 borrow notes.',
              'B blues melody: B D E F F# A. D and F are outside the scale; D# is its major third.'],9,16)
txt(M,H-169,'41  Phrygian dominant blues-inspired loop | 65-95 BPM',12,'Bold')
txt(M,H-194,'| B7 | Em | B7 | C | B7 | B7 |',10,'Courier')
lines(H-217,['This is a six-bar modal loop, not a traditional 12-bar blues.',
             'Try a shuffle feel and short answering phrases. Keep the melody in B Phrygian dominant.'],9,16)

minor_blues=['B7']*4+['Em']*2+['B7']*2+['F#7','Em','B7','F#7']
dominant_blues=['B7','E7','B7','B7','E7','E7','B7','B7','F#7','E7','B7','F#7']
borrowed={'F#7':{6,10,1,4},'E7':{4,8,11,2}}
assert borrowed['F#7']-allowed == {10,1}
assert borrowed['E7']-allowed == {8,2}
for yy,title,seq,description in [
 (H-300,'42  12-bar blues | B7 and Em, borrowed F#7',minor_blues,
  'F#7 adds A# and C#. B Phrygian dominant alone will clash with these chord tones.'),
 (H-470,'43  Dominant 12-bar blues | outside the scale',dominant_blues,
  'E7 adds G# and D; F#7 adds A# and C#. B7 stays inside the scale.')]:
    assert len(seq)==12 and all(ch in catalog or ch in borrowed for ch in seq)
    txt(M,yy,title,12,'Bold')
    for row in range(3):
        txt(M,yy-26-row*22,'| '+' | '.join(seq[row*4:row*4+4])+' |',10,'Courier')
    txt(M,yy-100,description,9)

txt(M,210,'Chord notes for the borrowed harmony',12,'Bold')
table(190,['Chord','Notes','Notes outside B Phrygian dominant'],[80,180,W-2*M-260],
      [('E7','E G# B D','G#, D'),('F#7','F# A# C# E','A#, C#')],row_h=26)
lines(58,['Choose the scale by the current harmony here; the scale-only rule is relaxed.'],9,16)
c.showPage()

styles_page(13,'MORE ELECTRONIC DIRECTIONS','B Phrygian dominant loops | Techno, house, industrial and breakbeat arrangements.',[
 ('Techno / house / industrial',[
  ('45  House | 118-128 BPM',['B7','Emadd9','Am7','Cmaj7'],'Delay offbeat stabs; move bass each beat. Glossary: swung offbeats. Bass: tip 1, p14.'),
  ('46  Industrial | 100-135 BPM',['B5','C5','E5','B5'],'Play B+F# as short stabs; add metallic percussion and repeating bass. Tip 2, p14.')]),
 ('Drum & bass / UK garage / trip-hop',[
  ('47  Drum & bass | 165-175 BPM',['B7','Emadd9','Em','Cmaj7'],'Let chords last a bar or two over fast breaks; leave room for a clean sub bass.'),
  ('49  Trip-hop | 65-95 BPM',['B7','Cmaj7','Am7','B7'],'Loosen the drums; vary mellow keys over sparse bass. Glossary: loose drums and warm keys.')])],
    variation_guide='Techno and UK garage variations: 44 on p10 and 48 on p11.')


header('PLAYING EXAMPLES','Bass, chords and melodic phrasing for B Phrygian dominant',14)
tips = [

    ('1  Walking bass', 'Play one note per beat: B-C-D#-F# over B7, landing on E for Em.'),
    ('2  Clipped fifths', 'Strike B and F# together and release immediately.'),


    ('3  Full triads', 'Sound all three chord tones together: B-D#-F# for B major. A power chord leaves out the third.'),
    ('4  Melodic hook', 'Repeat a short phrase ending C-B as C returns to B.'),
    ('5  Wider voicings', 'Begin with B3-D#4, add F#4, then spread B across B2-F#3-D#4-B4.'),
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
