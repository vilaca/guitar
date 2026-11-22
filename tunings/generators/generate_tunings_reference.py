#!/usr/bin/env python3
"""Generate a PDF reference to guitar tunings.

Install: python -m pip install reportlab
Run: python generate_tunings_reference.py --output-dir generated
"""
from pathlib import Path
import argparse
import re
from xml.sax.saxutils import escape

def pc(note):
    m=re.fullmatch(r'([A-G])([#b]?)',note)
    assert m,note
    return ({'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}[m[1]]+
            {'':0,'#':1,'b':-1}[m[2]])%12

def intervals(notes):
    pitches=[pc(n) for n in notes.split()]
    return [(b-a)%12 for a,b in zip(pitches,pitches[1:])]

def tuning(name,notes,expected):
    assert intervals(notes)==expected,(name,intervals(notes),expected)
    return [name,notes,'-'.join(map(str,expected))]

PAGES=[]
def page(title):
    p={'title':title,'blocks':[]};PAGES.append(p);return p['blocks']
def para(p,s):p.append(('p',s))
def heading(p,s):p.append(('h',s))
def grid(p,heads,rows,weights):p.append(('t',heads,rows,weights))
def link(p,label,url):p.append(('link',label,url))

p=page('Guitar tunings reference')
para(p,'A reference to the standard, all-fourths, drop and repeated-note tunings, including the Josh Homme and Stephen Carpenter examples. The note order and interval pattern let you compare what changes physically and musically.')
heading(p,'Reading the tuning tables')
para(p,'Every tuning runs from thickest to thinnest string. Intervals are ascending semitones between adjacent open strings. 5 = perfect fourth; 4 = major third; 3 = minor third; 7 = perfect fifth; 0 = unison. The # symbol means sharp and b means flat. Octaves are shown only where the register matters; C4 is middle C.')
heading(p,'Building the eight-string tuning')
grid(p,['Version','Open notes','Semitones'],[
 tuning('Original sequence','G# B E A D G B E',[3,5,5,5,5,4,5]),
 tuning('First interval changed to 5','F# B E A D G B E',[5,5,5,5,5,4,5]),
 tuning('Same pattern starting on E','E A D G C F A D',[5,5,5,5,5,4,5])],[1.6,2.3,1.7])
para(p,'Changing G# to F# makes the first gap a perfect fourth. Moving the entire second tuning down a whole tone gives the E-starting version and preserves every interval.')
heading(p,'Standard reference tunings')
grid(p,['Instrument or layout','Open notes','Semitones'],[
 tuning('6-string standard','E A D G B E',[5,5,5,4,5]),
 tuning('Solar A1.7ROP-29+ (B standard)','B E A D G B E',[5,5,5,5,4,5]),
 tuning('Xiphos XPTB720 (A standard, factory)','A D G C F A D',[5,5,5,5,4,5]),
 tuning('Xiphos XPTB720 (G standard, owner setup)','G C F Bb Eb G C',[5,5,5,5,4,5]),
 tuning('8-string standard','F# B E A D G B E',[5,5,5,5,5,4,5])],[2.5,1.65,1.45])
para(p,'In B standard the 4-semitone gap is G to B. It helps familiar open chords and their movable barre forms. All-fourths tuning removes that exception, making shapes transfer consistently across string groups; many smaller chord voicings remain practical in either system.')

p=page('All-fourths tuning and C major')
para(p,'All-fourths tuning puts exactly 5 semitones between adjacent strings. A conventional drop modification lowers only the thickest string a whole tone, changing its first interval from 5 to 7 semitones.')
heading(p,'All-fourths examples')
grid(p,['Strings and layout','Open notes','Semitones'],[
 tuning('6 all-fourths','E A D G C F',[5,5,5,5,5]),
 tuning('7 all-fourths','B E A D G C F',[5,5,5,5,5,5]),
 tuning('7 all-fourths base for drop E','F# B E A D G C',[5,5,5,5,5,5]),
 tuning('7 custom drop E','E B E A D G C',[7,5,5,5,5,5]),
 tuning('7 custom drop A','A E A D G C F',[7,5,5,5,5,5])],[1.6,2.3,1.7])
heading(p,'Seven strings using only C major notes')
para(p,'With seven strings and every gap fixed at 5 semitones, B E A D G C F is the only pitch-class sequence entirely inside C major. Starting elsewhere reaches F to Bb before filling all seven strings. Choosing another octave changes the register, not that sequence.')
para(p,'Allowing a 7-semitone first gap and keeping the remaining gaps at 5 gives two C-major-only choices: E B E A D G C and A E A D G C F. Their three lowest strings form root-fifth-octave shapes.')
heading(p,'How the layouts feel')
grid(p,['Layout','What it makes convenient'],[
 ['All fourths','Scales, arpeggios and small voicings move consistently across strings.'],
 ['Drop plus all fourths','A low root-fifth-octave shape, with regular fourths above it.'],
 ['Standard with its major third','Conventional open and barre-chord shapes, plus the familiar fretboard layout.']],[1.65,3.95])
para(p,'For seven-string drop E, lower only the F# in the all-fourths base to E. The top string stays at C. The Deftones eight-string drop E on page 5 ends on E. The lowest note alone does not identify the whole tuning.')

p=page('Lower tunings and open-string scales')
para(p,'In standard tuning, start Phrygian on the open seventh string. In drop tuning, start at fret 2 on that string. All seven open strings belong to the resulting scale.')
grid(p,['Seven-string tuning','Open notes','Phrygian root'],[
 ['B standard (Solar)','B E A D G B E','B'],['A standard (Xiphos factory)','A D G C F A D','A'],
 ['G standard (Xiphos current)','G C F Bb Eb G C','G'],['Drop A','A E A D G B E','B'],
 ['Drop G','G D G C F A D','A'],['Drop F','F C F Bb Eb G C','G'],
 ['Drop Eb','Eb Bb Eb Ab Db F Bb','F']],[2.25,2.1,1.25])
for row in p[-1][2]:
    expected=[7,5,5,5,4,5] if row[0].startswith('Drop') else [5,5,5,5,4,5]
    assert intervals(row[1])==expected
    root=pc(row[2]);scale={(root+i)%12 for i in [0,1,3,5,7,8,10]}
    assert all(pc(n) in scale for n in row[1].split())
para(p,'Standard open-string degrees are 1-4-b7-b3-b6-1-4. In drop tuning they are b7-4-b7-b3-b6-1-4. Lowering the thickest string changes its scale degree from 1 to b7, still inside Phrygian. Drop Eb here means seven strings; a six-string tuning with the same name has a different full note sequence.')
heading(p,'Open pitches outside each scale')
scales = [
    ('B Phrygian', 'B C D E F# G A'),
    ('A Phrygian', 'A Bb C D E F G'),
    ('G Phrygian', 'G Ab Bb C D Eb F'),
    ('B minor pentatonic', 'B D E F# A'),
    ('E minor pentatonic', 'E G A B D'),
    ('Bb dominant bebop', 'Bb C D Eb F G Ab A'),
]
rows = []
for name, notes in scales:
    members = {pc(note) for note in notes.split()}
    row = [name, notes]
    for open_notes in ('B E A D G B E', 'A D G C F A D', 'G C F Bb Eb G C'):
        outside = [note for note in dict.fromkeys(open_notes.split()) if pc(note) not in members]
        row.append(', '.join(outside) or 'None')
    rows.append(row)
grid(p, ['Scale', 'Scale notes', 'B standard / drop A', 'A standard', 'G standard'],
     rows, [1.35, 1.55, 1, .85, .95])
para(p,'B standard and drop A share the same open pitch classes. For the Xiphos, keep the fret numbers in the B Phrygian guide. The pattern becomes A Phrygian in factory A standard and G Phrygian in the current G-standard setup.')

link(p,'B Phrygian guide for seven-string guitar','https://github.com/vilaca/guitar/blob/main/scales/pdfs/phrygian_7_string_standard.pdf')

p=page('Josh Homme and the G D tuning')
para(p,'A viewer transcribes GGDGDD at about 52 minutes in the Rick Beato interview [2]. This example reads those notes from thickest to thinnest. The octaves below are one playable interpretation. The video excerpt [1] provides listening context.')
heading(p,'One six-string octave mapping')
grid(p,['String','Standard reference','G D realization','Change'],[
 ['6','E2','G2','Up 3 semitones'],['5','A2','G2','Down 2 semitones'],
 ['4','D3','D3','Unchanged'],['3','G3','G3','Unchanged'],
 ['2','B3','D4','Up 3 semitones'],['1','E4','D4','Down 2 semitones']],[.55,1.55,1.65,1.85])
assert intervals('G G D G D D')==[0,7,5,7,0]
para(p,'Thickest to thinnest: G2 G2 D3 G3 D4 D4. The adjacent intervals are 0-7-5-7-0 semitones. Strings 6 and 5 are in unison; strings 2 and 1 are also in unison. These pairs are not octave doubles.')
heading(p,'Why this tuning works')
para(p,'Every open string is either G or D, so the whole guitar forms a G5 power chord. There is no third, leaving the major or minor character for a melody, another instrument or a fretted note. Repeated notes support ringing drones and a doubled texture; slight differences between matching pitches can create beating and a chorus-like shimmer.')
grid(p,['Shape','Result'],[
 ['All strings open','G5'],['Barre all strings at fret 3','Bb5'],['Barre all strings at fret 5','C5'],
 ['Open strings plus string 3 at fret 3','Adds Bb, producing G minor'],
 ['Open strings plus string 3 at fret 4','Adds B, producing G major']],[2.8,2.8])
para(p,'The tuning favours repeating notes, drones and large chord textures. It gives up the broad pitch coverage and consistent scale shapes of an all-fourths layout. The interval map above is for the exact unisons shown; different octave choices would change it.')

p=page('Stephen Carpenter and Deftones')
para(p,'The Deftones examples went beyond lowering a bass string. Stephen Carpenter also used seven-string instruments with a duplicated highest string. The 2013 rig rundown lists the open pitches for all three instruments [3]. In 2016 Carpenter identified the F# eight-string tuning as standard, described lowering its bass to E, and explained his extra high-E drone [4].')
grid(p,['Layout','Open notes','Semitones'],[
 tuning('7 strings with doubled high E','E A D G B E E',[5,5,5,4,5,0]),
 tuning('7 strings with doubled high D','C G C F A D D',[7,5,5,4,5,0]),
 tuning('8-string standard','F# B E A D G B E',[5,5,5,5,5,4,5]),
 tuning('8-string drop E','E B E A D G B E',[7,5,5,5,5,4,5])],[1.7,2.2,1.7])
heading(p,'Doubled high strings')
para(p,'The seven-string realizations are E2 A2 D3 G3 B3 E4 E4 and C2 G2 C3 F3 A3 D4 D4. The extra string repeats the top pitch instead of extending the bass range. Carpenter described an extra high string as a drone in a later interview [4].')
heading(p,'Standard eight-string tuning and drop E')
para(p,'For the eight-string examples, F#1 B1 E2 A2 D3 G3 B3 E4 becomes E1 B1 E2 A2 D3 G3 B3 E4 when only the thickest string drops a whole tone. Carpenter described that change in the 2016 interview [4]. The lowest three strings then form E-B-E, a root-fifth-octave shape.')
heading(p,'Relationship to the Homme example')
grid(p,['Feature','Homme G D example','Carpenter doubled top'],[
 ['Repeated pitches','Both outer pairs','Highest pair'],
 ['All open strings one power chord','Yes, G and D only','No, a wider collection'],
 ['Familiar standard shapes','Substantially altered','Retained across the original six-string layout']],[1.85,1.8,1.95])

p=page('Choosing a layout and checking sources')
heading(p,'Compare the musical priorities')
grid(p,['If you want','Relevant tuning family'],[
 ['Consistent shapes across strings','All fourths: E A D G C F, or B E A D G C F.'],
 ['A low power-chord shape','A drop tuning, with a 7-semitone first interval.'],
 ['All-fourths regularity above a dropped bass','The custom seven-string E B E A D G C or A E A D G C F.'],
 ['A whole guitar built from root and fifth','The G G D G D D example on page 4.'],
 ['An extra high drone without another bass string','The Deftones E A D G B E E or C G C F A D D examples.']],[2.35,3.25])
heading(p,'Three distinctions to keep clear')
para(p,'Pitch classes and octaves are different: G2 and G3 share a note name but are an octave apart. A unison is the same pitch, such as G2 and G2. The register matters whenever you compare actual semitone distances.')
para(p,'Lowering the whole tuning preserves every interval and transposes the fretboard shapes. Dropping only the thickest string changes the first interval. Neither operation decides the tonal centre of the music by itself.')
para(p,'A tuning lists available open notes; a scale defines a pitch collection; a tonal centre is the note that feels like home. The same tuning can support many scales and centres.')
heading(p,'Sources for the artist examples')
link(p,'1  Video excerpt: Why Josh Homme’s Guitar Is Purposely Out Of Tune','https://www.youtube.com/watch?v=NE81yc52qto')
link(p,'2  Viewer transcription pointing to G G D G D D around 52 minutes','https://www.guitarristas.info/foros/josh-homme-echopark-signature/349903')
link(p,'3  Premier Guitar Deftones rig rundown from November 2013','https://www.premierguitar.com/rig-rundown-deftones-stephen-carpenter-sergio-vega')
link(p,'4  Premier Guitar A Little Darkness interview from March 2016','https://www.premierguitar.com/artists/deftones-a-little-darkness')
para(p,'The interval patterns and scale-membership statements in this reference are calculated from the listed notes. Artist associations follow the sources above; the Homme octave realization is explicitly identified as a worked example.')

def make_pdf(path):
    import reportlab
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
    from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    font_dir=Path(reportlab.__file__).resolve().parent/'fonts'
    for name,filename in [('RefBody','Vera.ttf'),('RefBold','VeraBd.ttf')]:pdfmetrics.registerFont(TTFont(name,str(font_dir/filename)))
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle('RefP',fontName='RefBody',fontSize=10,leading=13.3,spaceAfter=8))
    styles.add(ParagraphStyle('RefH',fontName='RefBold',fontSize=12,leading=15,spaceBefore=8,spaceAfter=7,keepWithNext=True))
    styles.add(ParagraphStyle('RefTitle',fontName='RefBold',fontSize=21,leading=25,spaceAfter=15))
    styles.add(ParagraphStyle('RefCell',fontName='RefBody',fontSize=8.8,leading=11.4))
    styles.add(ParagraphStyle('RefTH',parent=styles['RefCell'],fontName='RefBold',textColor=colors.white))
    styles.add(ParagraphStyle('RefLink',parent=styles['RefP'],fontSize=9,leading=12,spaceAfter=6))
    story=[];inner=7.1*72
    for idx,page in enumerate(PAGES):
        if idx:story.append(PageBreak())
        story.append(Paragraph(escape(page['title']),styles['RefTitle']))
        for b in page['blocks']:
            if b[0]=='p':story.append(Paragraph(escape(b[1]),styles['RefP']))
            elif b[0]=='h':story.append(Paragraph(escape(b[1]),styles['RefH']))
            elif b[0] == 'link':
                url = escape(b[2], {'"': '&quot;'})
                label = f'<link href="{url}">{escape(b[1])}</link>'
                address = f'<link href="{url}">{escape(b[2])}</link>'
                story.append(Paragraph(f'{label}<br/>{address}', styles['RefLink']))
            else:
                _,heads,rows,weights=b
                data=[[Paragraph(escape(str(s)),styles['RefTH'] if i==0 else styles['RefCell']) for s in row] for i,row in enumerate([heads]+rows)]
                t=Table(data,colWidths=[inner*w/sum(weights) for w in weights],repeatRows=1,hAlign='LEFT')
                t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#404040')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f4f4f4')]),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#d9d9d9')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
                story.extend([t,Spacer(1,9)])
    def footer(c,doc):
        c.setFont('RefBody',8);c.drawRightString(8.5*72-.7*72,25,str(doc.page))
    SimpleDocTemplate(str(path),pagesize=(8.5*72,11*72),leftMargin=.7*72,rightMargin=.7*72,topMargin=.65*72,bottomMargin=.65*72,title='Guitar tunings reference',author='').build(story,onFirstPage=footer,onLaterPages=footer)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir',default='generated_tunings')
    ap.add_argument('--format', choices=['pdf'], help=argparse.SUPPRESS)
    args = ap.parse_args()
    dest = Path(args.output_dir).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / 'guitar_tunings_reference.pdf'
    make_pdf(out)
    print(out)
