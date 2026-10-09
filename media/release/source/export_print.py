"""Export static publication pages as PDFs with embedded fonts."""
from pathlib import Path
from weasyprint import HTML,CSS
from weasyprint.text.fonts import FontConfiguration
ROOT=Path(__file__).resolve().parents[3]
SITE=ROOT/'site/launch'
config=FontConfiguration()
for lang in ['zh','en']:
    HTML(filename=SITE/f'manifesto-{lang}.html').write_pdf(SITE/f'downloads/AI-for-All-Manifesto-{lang.upper()}.pdf',font_config=config)
for page,file in [('qr-display','AI-for-All-Launch-QR-Display'),('panoramas','AI-for-All-Panoramas')]:
    HTML(filename=SITE/f'{page}.html').write_pdf(SITE/f'downloads/{file}.pdf',stylesheets=[CSS(string='@page { size:1600px 900px !important; margin:0 !important }')],font_config=config)
print('Exported four publication PDFs.')
