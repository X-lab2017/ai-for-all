"""Build the approved release only; superseded editions are not published."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
for name in ['build_current_release.py','build_film.py','package_current_release.py']:
 subprocess.run([sys.executable,str(root/name)],check=True)
