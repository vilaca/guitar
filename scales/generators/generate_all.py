#!/usr/bin/env python3
"""Generate the scale guides and shared glossary into one directory."""
import argparse
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', default='generated_pdfs')
args = parser.parse_args()
destination = Path(args.output_dir).expanduser().resolve()
destination.mkdir(parents=True, exist_ok=True)
script_dir = Path(__file__).resolve().parent
jobs = [
    ('generate_playing_glossary.py', 'playing_glossary.pdf'),
    ('generate_phrygian.py', 'phrygian_7_string_standard.pdf'),
    ('generate_b_flat_dominant_bebop.py', 'b_flat_dominant_bebop_7_string_and_piano.pdf'),
    ('generate_e_minor_pentatonic.py', 'e_minor_pentatonic_7_string_and_piano.pdf'),
]
for script, filename in jobs:
    subprocess.run([sys.executable, str(script_dir / script),
                    '--output', str(destination / filename)], check=True)
