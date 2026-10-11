"""Stage the approved site only. Old public editions are deliberately excluded."""
from pathlib import Path
import shutil,re
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'site';OUT=ROOT/'.publish-site'
if OUT.exists():shutil.rmtree(OUT)
# Legacy content remains discoverable through Git history, never this publication.
excluded={'v1.1.html','en-v1.1.html','presentation-v1.1','diagrams','diagrams.css','diagrams.js','narrative.md'}
shutil.copytree(SOURCE,OUT,ignore=lambda directory,names:[n for n in names if n in excluded])
for p in OUT.rglob('*.html'):
 s=p.read_text();assert not re.search(r'(?:href|src)=["\'][^"\']*(?:v1\.1|90s-|Conference-|archive-)',s),p
for p in (OUT/'launch').rglob('*'):
 assert not any(x in p.name for x in ['90s-','Conference-','archive-','Handbook','Draft']),p
print('Public site staged: four approved editions and current visuals only')
