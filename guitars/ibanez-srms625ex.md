# Ibanez SRMS625EX (Black Flat)

5-string multi-scale bass (35.5" to 34"), Bartolini BH2 pickups, Ibanez 3-band EQ with bypass and a 3-way mid-frequency switch. Factory tuning B E A D G.

- **Source:** https://www.ibanez.com/usa/products/detail/srms625ex_1p_03.html (Ibanez USA), read on 2026-11-21.
- **Basis:** every spec below is from that page. Anything I calculated or added is labelled. See "Not on the page" for what is missing.

## Identity

| Field | Value |
| --- | --- |
| Model code | SRMS625EX |
| Series | SR, electric basses |
| Finish | BKF: Black Flat (the only colour listed) |
| Logo | "Iron Label" logo image beside the title (no text on the page) |
| Hardware colour | Black |
| Recommended case | MB300C |

The page doesn't state the number of strings as a field. Five follows from the factory tuning (1G, 2D, 3A, 4E, 5B) and the five gauges.

## Specifications

Labels are as on the page. The page runs the pickup labels together with "Passive"; they are separated here.

| Field | Value |
| --- | --- |
| Neck | SRMS5 for Multi Scale, 5pc maple/walnut |
| Body | Okoume |
| Fretboard | Ebonol |
| Frets | Medium, 24 |
| Bridge | MR5 |
| String space | 16.5 mm |
| Neck pickup | Bartolini BH2, passive |
| Bridge pickup | Bartolini BH2, passive |
| Equalizer | Ibanez Custom Electronics 3-band EQ with EQ bypass switch (passive tone control on treble pot) and 3-way mid frequency switch |
| Factory tuning | 1G, 2D, 3A, 4E, 5B |
| Strings | D'Addario EXL170-5SL |
| String gauges | .045 / .065 / .080 / .100 / .130 |
| Hardware | Black |

## Neck dimensions

| Dimension | Value |
| --- | --- |
| Scale | 901.7 mm (35.5") to 864.0 mm (34.0"), multi-scale |
| Width at nut | 45 mm |
| Width at 24th fret | 68 mm |
| Thickness at 1st fret | 19.5 mm |
| Thickness at 12th fret | 23 mm |
| Fingerboard radius | 305 mmR |

- The page gives the scale as a range, one end per outer string. It doesn't say which end is the low B. It also doesn't give the scale length of the three middle strings or the fan angle.
- 34" is exactly 863.6 mm. The page prints 864.0 mm.
- **Calculated:** the two ends differ by 1.5" (about 38 mm). 305 mm is a 12" radius.

## Strings and tuning

Factory tuning from the page is **B standard bass**, thickest to thinnest: B E A D G. Every gap is a perfect fourth (5-5-5-5 semitones).

| String | Note | Gauge |
| --- | --- | --- |
| 5 (thickest) | B0 | .130 |
| 4 | E1 | .100 |
| 3 | A1 | .080 |
| 2 | D2 | .065 |
| 1 (thinnest) | G2 | .045 |

- The page gives note names only. The octave numbers are my assumption from the usual 5-string bass register.
- **General note, not on the page:** in D'Addario's naming, "5SL" means a five-string set for super long scale. The page doesn't explain the code.
- **Calculated:** 4 gaps at 16.5 mm span 66 mm. The page doesn't say where the string spacing is measured.

## Electronics and controls

Described in the page's text. I did not view the control diagram.

- **Pickups:** two Bartolini BH2, passive. The page describes them as dual-coil with a long blade pole piece.
- **Knobs:** three small knobs on the lower body edge are bass, mid and treble boost/cut. Two larger knobs near the bridge are pickup balance and volume.
- **Switches:** a 3-way mid-frequency switch and an EQ bypass switch.

### Mid-frequency switch

| Position | Mid boost/cut peak |
| --- | --- |
| Neck side | 250 Hz |
| Centre | 450 Hz |
| Bridge side | 700 Hz |

### EQ bypass switch

| Position | Result |
| --- | --- |
| Neck side | EQ off |
| Bridge side | EQ on |

With the EQ off, the treble knob works as a passive tone control.

### EQ curves, per the page

- **Bass:** boost/cut peaks at 20 Hz. The variable range narrows toward the highs and reaches zero near 1,000 Hz.
- **Treble:** a mountain-shaped curve that peaks near 10,000 Hz, with zero variable range near 100 Hz.
- **Mid:** a bell-shaped curve with zero variable range near 20 Hz and near 10,000 Hz. The peak frequency switches between 700, 450 and 250 Hz.
- **Range:** about ±15 dB for each of the three bands. The page prints no other limits.

## Features, as the page describes them

Paraphrased from the page's feature blocks:

- **Neck:** five pieces of maple and walnut.
- **Fretboard:** Ebonol, a synthetic material made from layers of black paper and phenolic resin, described as giving a tight, bright sound.
- **Multi scale:** said to give equalised string tension and a more lively tone, and to suit the hand angle as you move up the neck.
- **Body:** okoume, described as bright and solid sounding.
- **Pickups:** Bartolini BH2, dual-coil with a long blade pole piece.
- **EQ:** the Ibanez Custom Electronics 3-band EQ with bypass and the 3-way mid switch.
- **Bridge:** MR5, described as a Mono-Rail V bridge with each saddle locked independently to the body.

The page doesn't use the word "fanned". "Multi scale" is its only term. **General note:** a multi-scale bass has a different scale length per string and angled (fanned) frets.

## How it relates to the other instruments in this repo (calculated)

- **Solar A1.7ROP-29+ (7-string, B standard):** its lowest five strings are B E A D G. The bass is tuned to the same five notes, exactly one octave lower. The bass pitches B0 to G2 are 31 to 98 Hz. The guitar's B1 to G3 are 62 to 196 Hz.
- **Ibanez XPTB720 (7-string, A or G standard):** its lowest five strings don't match the bass. They are A D G C F in A standard and G C F Bb Eb in G standard.
- **`tunings/` PDF:** `B E A D G` is the start of the all-fourths sequence `B E A D G C F` on page 2. The bass in B standard has no major third between any pair of strings, so no 4-semitone gap.
- **Scale guides in `scales/pdfs/`:** the bass's five strings match strings 7 to 3 of the guitar tabs in B standard, so those fret numbers give the same note names one octave lower. All five open strings (B E A D G) belong to B Phrygian and E minor pentatonic. In the Bb dominant bebop collection, B and E are outside the scale.

## Not on the page

- Price, availability, weight and country of origin.
- Number of strings as a field, nut material, tuner model and neck profile name.
- Scale lengths of the middle strings, the fan angle and which end of the scale range is the low B.
- Pickup output, resistance and wiring, pot values and battery or power details.
- Other colours (the page shows Black Flat only).
- Photos and diagrams (neck, control and EQ curve): I did not view them.
- Whether any content sits behind tabs on the live page, since I read a text conversion.

## Links on the page

- Manuals index: https://www.ibanez.com/world/support/manual/ (generic, not specific to this model).
- Parts lookup: https://cs.hoshinogakki.co.jp/pcw.nsf
- Support: https://www.ibanez.com/usa/support/
