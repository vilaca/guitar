# Fixes for the 7-string scale PDFs

Review of `b_flat_dominant_bebop_7_string_and_piano.pdf`, `e_minor_pentatonic_7_string_and_piano.pdf` and `phrygian_7_string_standard.pdf`.

All notes, frets, chord spellings, keyboard diagrams and `[P]`/`[H]` labels checked out. Only the items below need changing.

## 1. Phrygian: piano-key page reference is incomplete

- **Where:** `phrygian_7_string_standard.pdf`, loop pages 4-6 and 8-10, 12 (the "Piano keys: p7." line).
- **Problem:** The triad diagrams (Bm, C, D, Em, F#dim, G, Am) are on p2. Page 7 has only Bm7, Cmaj7, Em7, Gmaj7, Am7 and Dadd9. Loops 14-16, 17-19 and others use only triads, so p7 doesn't show their chords.
- **Fix:** Change "Piano keys: p7." to "Piano keys: pp2, 7." on every loop page.

## 2. Bb bebop slide (fixed)

Page 2 identifies string 7 as the string for the six-note slide.

## 3. Bb bebop: Gm9 voicing contradicts its caption

- **Where:** `b_flat_dominant_bebop_7_string_and_piano.pdf`, p4, Gm9 diagram.
- **Problem:** The caption says A natural is "an added colour above G minor", but the voicing (RH A3 Bb3 D4 F4) puts A3 below Bb3. That leaves a minor 2nd at the bottom of the right hand.
- **Fix:** Change the right hand to Bb3 D4 F4 A4. Update the "RH:" line and the R markers. Then the 9th is on top, matching the caption.

## 4. E minor 22-fret fingering (fixed)

On a 22-fret guitar, stop one note before the end of the seventh-string diagonal on page 2. Play B5 at fret 19 and D6 at fret 22.

## Optional polish

- Give the three PDFs matching fonts. Phrygian uses Helvetica and Courier, while Bb bebop and E minor use DejaVu.
- Add a 0-12 fretboard map and a chord-spelling table to the Phrygian PDF, as the other two have.
- Set a document title in each PDF's metadata. It is currently empty.

# Suggested improvements

Roughly in order of value. Effort: S = small, M = medium, L = large.

## A. Add guitar chord shapes (L)

The PDFs say "guitar + piano", but chords appear only as piano diagrams. Guitarists get scale tabs and chord names with no fingerings.

- Add a few triad and seventh shapes for B standard.

## B. Share one template across the generators (M)

The generator source is now in `scales/generators/` (done), so fixes can be made there and the PDFs regenerated into `scales/pdfs/`. The three scripts are still standalone copies.

- Move the shared layout code into one module used by all three scripts.
- This also fixes the font mismatch.
- It makes fix #1 above a one-line change.

## C. Share the tips pages (S)

The last two pages of each PDF (playing tips, terms 1-11) are almost word-for-word identical.

- Move them into one `playing-tips.pdf` and point to it from each PDF.
- This saves about 2 pages per PDF.
- Each future fix is then made once.

## E. Add fixed-position boxes next to the long diagonal (M)

One diagonal across four octaves needs big hand shifts, especially on the pentatonic.

- Add two or three 3-notes-per-string positions per scale.
- They are easier to practice and improvise from.

## F. Bb bebop title (fixed)

The title identifies the Bb dominant bebop collection and the G-centred riff. The riff uses both Ab and A. Loop 03 uses Bb7 as its tonal anchor.

## G. Make the loops consistent across PDFs (M)

The Phrygian PDF labels loops with roman numerals (i, bII, bvii). Bb bebop and E minor don't.

- Add roman numerals to the other two.
- Then `Gm | Ab` and `Em | Dsus4` read as the same idea.

## H. Mark the blue note on the E minor grid (S)

The blues page adds Bb (b5) to the scale.

- Show Bb as an optional marked cell on the fretboard grid.
- This links the grid to the blues page.

## I. Trim the loop pages (M)

Many of the 49 loops per PDF are one idea reused across genres (i-bII-i and its relatives).

- Use a smaller set of distinct loops.
- Add a "how to vary it" note to each.

## J. Tidy the print layout (S)

- Page 1 of Bb bebop and E minor has a large blank gap between the intro and the grid.
- Phrygian p1 has an empty band above "Root rule".
- Add a short legend under each tab ("bold = root, dash = gap").
