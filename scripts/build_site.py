#!/usr/bin/env python3
"""Build archived v1.1 resources, then the current v1.2 Chinese publication."""
from pathlib import Path
import subprocess,sys
HERE=Path(__file__).resolve().parent
for script in [HERE/'build_legacy_site.py',HERE/'publication/build.py']:
 subprocess.run([sys.executable,str(script)],check=True)
