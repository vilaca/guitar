# Guitar

Guitar reference material, grouped by topic. Each topic has its finished PDFs in `pdfs/` and the Python scripts that build them in `generators/`.

| Topic | What it covers |
| --- | --- |
| [`scales/`](scales/) | 7-string scale guides (standard B E A D G B E and drop A) with piano / synth voicings and 49 chord loops each: B Phrygian, Bb dominant bebop (G-centred) and E minor pentatonic. Review notes are in `scales/fixes.md`. |
| [`tunings/`](tunings/) | Six-page tunings reference: standard, all-fourths, drop, Josh Homme and Stephen Carpenter tunings, interval tables, scale relationships and linked artist sources. |

## Layout

```
guitar/
├── scales/
│   ├── pdfs/
│   ├── generators/
│   └── fixes.md
└── tunings/
    ├── pdfs/
    └── generators/
```

## Regenerate

Each `generators/` folder has its own `README.md` and `requirements.txt`.

```sh
# scales
cd scales/generators
python3 -m pip install -r requirements.txt
python3 generate_all.py --output-dir generated_pdfs

# tunings
cd tunings/generators
python3 -m pip install -r requirements.txt
python3 generate_tunings_reference.py --output-dir generated
```

Output goes to git-ignored folders. To publish a new version, copy the PDFs you want into the matching `pdfs/` folder.
