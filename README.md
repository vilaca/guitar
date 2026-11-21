# Guitar

Practice guides for 7-string guitar (standard B E A D G B E and drop A) with piano / synth voicings and 49 chord loops each.

## Layout

| Folder | Contents |
| --- | --- |
| `pdfs/` | The finished guides: B Phrygian, Bb dominant bebop (G-centred) and E minor pentatonic. |
| `generators/` | Python scripts that build the three PDFs. See `generators/README.md`. |
| `docs/` | Review notes: `fixes.md` lists corrections and suggested improvements. |

## Regenerate the PDFs

```sh
cd generators
python3 -m pip install -r requirements.txt
python3 generate_all.py --output-dir generated_pdfs
```

The output goes to `generators/generated_pdfs/`, which is git-ignored. To publish a new version, copy the PDFs you want into `pdfs/`.
