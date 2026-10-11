"""Validate the current approved publication."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
exec((ROOT/"scripts/publication/check.py").read_text())
