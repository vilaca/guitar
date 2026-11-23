# Music PDF generators

Standalone generators for the four scale guides and their shared playing glossary.

| Script | Guide | Pages |
| --- | --- | --- |
| `generate_phrygian.py` | 7-string B Phrygian, B standard, piano/synth, 43 progressions | 14 |
| `generate_phrygian_dominant.py` | 7-string B Phrygian dominant, B standard, piano/synth, 43 progressions | 14 |
| `generate_fretboard_maps.py` | B-standard fretboard maps, frets 0-24, with the diagonal route: B Phrygian dominant, B Phrygian, B minor pentatonic | 3 |
| `generate_b_flat_dominant_bebop.py` | Bb dominant bebop, G-centred riff, guitar/piano, 45 progressions | 14 |
| `generate_e_minor_pentatonic.py` | E minor pentatonic, guitar/piano, 46 progressions | 14 |
| `generate_playing_glossary.py` | Shared rhythm and production terms | 1 |

## Requirements

Python 3.9 or newer and ReportLab. No internet or API access is needed after installing the dependency. The scripts do not call an AI service.

## Generate the complete set

Extract this folder, open a terminal in it, then run:

```sh
python -m pip install -r requirements.txt
python generate_all.py --output-dir generated_pdfs
```

On systems where Python is named `python3`, use `python3` in both commands. The PDFs will be written to `generated_pdfs`.

## Generate one guide

```sh
python generate_playing_glossary.py --output playing_glossary.pdf
python generate_phrygian.py --output phrygian.pdf
python generate_phrygian_dominant.py --output phrygian_dominant.pdf
python generate_fretboard_maps.py --output fretboard_maps.pdf
python generate_b_flat_dominant_bebop.py --output bebop.pdf
python generate_e_minor_pentatonic.py --output pentatonic.pdf
```

Each script works independently; it does not need another generator or any original workspace files. Without `--output`, it writes its descriptive default PDF filename into the current directory. Running it again overwrites that output file.

## Customize

The scale patterns, chord spellings, piano voicings, progressions and explanatory text are ordinary Python lists and dictionaries in each script. Edit them and rerun the script. Assertions check note membership, guitar pitch sequences and chord voicings; if you change a scale, update its related data consistently.

All guides use the Vera fonts bundled with ReportLab, so they do not depend on system font paths. Minor font/layout differences from earlier PDF copies are possible.
