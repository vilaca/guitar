# Guitar tunings reference generator

Creates the six-page tuning reference as a printable PDF. It includes the standard, all-fourths, drop, Josh Homme and Stephen Carpenter tunings, interval tables, scale relationships and linked artist sources.

## Run

Use Python 3.9 or newer. In the extracted folder run:

```sh
python -m pip install -r requirements.txt
python generate_tunings_reference.py --output-dir generated
```

Use `python3` instead of `python` if that is the command on your system.

The generator writes `guitar_tunings_reference.pdf` in the output directory, replacing any previous copy.

## Edit

All text and tuning tables are defined in the Python file. Change that content and run it again. Assertions check tuning intervals and the Phrygian open-string rule. The generator runs offline with Python and the fonts bundled with ReportLab.
