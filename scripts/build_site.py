#!/usr/bin/env python3
"""Build the approved v1.2 publication and 13-chapter presentation."""
from pathlib import Path
import subprocess,sys
HERE=Path(__file__).resolve().parent
for script in [HERE/'publication/build.py',HERE/'presentation/build.py']:
 subprocess.run([sys.executable,str(script)],check=True)
