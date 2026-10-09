"""Create the bilingual conference handoff from the release's approved copy."""
from pathlib import Path
import json
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'site/launch/downloads'
COPY = json.loads((Path(__file__).parent / 'launch-copy.json').read_text())
URL = 'https://www.x-lab.info/ai-for-all/launch/'
doc = Document()
s = doc.sections[0]
s.page_width, s.page_height = Inches(8.27), Inches(11.69)
s.top_margin = s.bottom_margin = Inches(.60)
s.left_margin = s.right_margin = Inches(.78)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2']:
    st=doc.styles[name]
    st.font.name='Source Han Sans SC'
    st._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Source Han Sans SC')
    for key in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:
        st._element.rPr.rFonts.attrib.pop(qn('w:'+key),None)
    for border in st._element.xpath('./w:pPr/w:pBdr'):
        border.getparent().remove(border)
    st.font.color.rgb=RGBColor(0,0,0)
doc.styles['Normal'].font.size=Pt(10.5)
doc.styles['Normal'].paragraph_format.line_spacing=1.16
doc.styles['Normal'].paragraph_format.space_after=Pt(6)
doc.styles['Title'].font.size=Pt(25)
doc.styles['Heading 1'].font.size=Pt(19)
doc.styles['Heading 1'].paragraph_format.space_before=Pt(14)
doc.styles['Heading 2'].font.size=Pt(13)
doc.styles['Heading 2'].paragraph_format.space_before=Pt(10)
doc.core_properties.title='AI for All Conference Handbook'
doc.core_properties.author='X-lab AI'
doc.core_properties.subject='Bilingual host introduction, launch remarks and playback guide'

def p(t,style=None):return doc.add_paragraph(t,style)
def h(t):doc.add_heading(t,1)
def sub(t):doc.add_heading(t,2)
def page():doc.add_page_break()
def table(headers, rows, widths):
    t=doc.add_table(rows=1,cols=len(headers))
    t.autofit=False
    for i,w in enumerate(widths):t.columns[i].width=Inches(w)
    for i,x in enumerate(headers):t.rows[0].cells[i].text=x
    for row in rows:
        cells=t.add_row().cells
        for c,x in zip(cells,row):c.text=x
    for ri,row in enumerate(t.rows):
        for ci,c in enumerate(row.cells):
            c.width=Inches(widths[ci])
            pr=c._tc.get_or_add_tcPr()
            sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'273C35' if ri==0 else ('F3F5F3' if ri%2==0 else 'FFFFFF'));pr.append(sh)
            borders=OxmlElement('w:tcBorders')
            for edge in ['top','left','bottom','right']:
                el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');borders.append(el)
            pr.append(borders)
            margins=OxmlElement('w:tcMar')
            for edge in ['top','left','bottom','right']:
                el=OxmlElement('w:'+edge);el.set(qn('w:w'),'100');el.set(qn('w:type'),'dxa');margins.append(el)
            pr.append(margins)
            for par in c.paragraphs:
                par.paragraph_format.space_after=Pt(3)
                for r in par.runs:
                    r.font.size=Pt(9)
                    if ri==0:r.bold=True;r.font.color.rgb=RGBColor(255,255,255)
    t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
    return t

p('AI 普惠宣言正式发布包','Title')
p('AI for All Conference Handbook','Subtitle')
p('X-lab AI  ·  Release 1  ·  9 October 2026')
p('本手册供主持人、发布人及会务播放团队使用，包含中英文台词、发布环节顺序、材料入口与播放参数。中文影片以已定稿的 conference-v5 为基准，英文影片和双语字幕影片保持相同的 90 秒结构。')
p('This handbook brings together the speaking scripts, running order and playback information for the AI for All launch. Choose one language for each speaking segment and one film version for the screening.')
sub('建议发布顺序  Suggested running order')
table(['环节 Segment','建议时长 Duration','现场动作 Cue'],[
    ['主持人引入\nHost introduction','30–40 秒 / seconds','灯光渐暗，准备所选影片。\nDim the lights and cue the selected film.'],
    ['宣言影片\nManifesto film','90 秒 / seconds','全屏播放，保留片尾音乐。\nPlay full screen through the final music.'],
    ['发布致辞\nLaunch remarks','约 2 分钟 / about 2 min','切换到全景图，发布人发言。\nShow the panorama during the remarks.'],
    ['共建邀请\nInvitation','20–30 秒 / seconds','显示二维码，引导阅读与参与。\nShow the code and invite participation.'],
], [1.72,1.37,3.60])
sub('统一入口  One launch link')
p(URL)
p('视频、PPT、宣言、全景图和参与入口均在此汇合。会场可下载离线包，播放时无需依赖网络。\nFilms, slides, the manifesto, the framework and contribution routes are available here. Download the package before the event for local playback.')

page();h('中文现场台词')
sub('主持人引入词  约 30 秒');p(COPY['host_zh'])
sub('发布致辞  约 2 分钟')
for x in COPY['speech_zh'].split('\n\n'):p(x)
sub('片后扫码邀请  约 15 秒');p(COPY['closing_zh'])

page();h('English speaking scripts')
sub('Host introduction  About 35 seconds');p(COPY['host_en'])
sub('Launch remarks  About 2 minutes')
for x in COPY['speech_en'].split('\n\n'):p(x)
sub('Closing invitation  About 15 seconds');p(COPY['closing_en'])

page();h('版本选择与术语')
table(['文件 File','使用场景 Intended use'],[
    ['AI-for-All-90s-ZH.mp4','中文配音及中文字幕；已定稿的 conference-v5。\nApproved Chinese film with Chinese captions.'],
    ['AI-for-All-90s-Bilingual.mp4','原定稿中文音轨；画面保留中文，底部中英字幕。\nChinese narration and visuals, with Chinese and English captions.'],
    ['AI-for-All-90s-EN.mp4','英文 AI 配音、英文画面和英文字幕。\nEnglish AI narration, English visuals and captions.'],
], [2.80,3.89])
sub('核心术语  Shared terminology')
table(['中文','English'],COPY['term_pairs'],[2.36,4.33])
p('中文宣言为权威版本。英文视频为配合 90 秒时长的口语化表达；完整定义与承诺见中英文宣言。\nThe Chinese manifesto is authoritative. The English film adapts the narration to a ninety-second format. Consult the full manifesto for definitions and commitments.')

page();h('播放与交接')
sub('播放规格  Playback specification')
p('三版均为 1920 × 1080、16:9、30 fps、90 秒，H.264 视频与 AAC 48 kHz 立体声音频。字幕已嵌入画面；随包附 SRT 与 VTT，便于后续适配。建议按原始比例播放，勿裁切字幕或拉伸画面。')
p('All three versions are 1920 × 1080, 16:9, 30 fps and 90 seconds, with H.264 video and AAC 48 kHz stereo audio. Captions are burned in. SRT and VTT files are also included. Preserve the original aspect ratio and subtitle area.')
p('提前将文件复制至会场电脑，在实际屏幕和音响上完整播放一次。播放结束后切到全景图或二维码页，并在观众扫码时保持画面。\nCopy files to the venue computer and run the complete film on its screen and sound system. After the film, show the panorama or QR display and leave it visible while the audience scans.')
sub('材料与入口  Materials and access')
p('中英文 PPT 各 10 页，附逐页讲述备注。PDF 全景图适合现场备用，PNG 适合插入会务系统。二维码指向固定发布页，不会自动提交报名或个人信息。\nBoth slide decks contain ten slides with speaker notes. Panorama PDFs provide a portable fallback, while PNGs fit event systems. The QR code opens the launch page and does not submit a registration.')
sub('音乐与素材署名  Credits')
p('“Heroic Age” — Kevin MacLeod (incompetech.com). Licensed under Creative Commons Attribution 4.0: https://creativecommons.org/licenses/by/4.0/ . Excerpt, equalization, ducking and mix. Attribution remains in the films and the included CREDITS.txt.')
p('人声为 AI 合成。中文使用已定稿音轨；英文由 Qwen3-TTS 生成。第三方图像及标识保留原来源。内容、品牌及复用说明见 NOTICE.md。\nNarration is synthetic. The Chinese versions retain the approved audio; English narration was generated with Qwen3-TTS. Third-party images and marks retain their sources. See NOTICE.md for content and brand reuse terms.')
p('https://github.com/X-lab2017/ai-for-all/blob/main/NOTICE.md')

footer=s.footer.paragraphs[0]
footer.alignment=2
r=footer.add_run('X-lab AI  ·  ');r.font.size=Pt(8);r.font.color.rgb=RGBColor.from_string('65746D')
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
OUT.mkdir(parents=True,exist_ok=True)
doc.save(OUT/'AI-for-All-Conference-Handbook.docx')
print(OUT/'AI-for-All-Conference-Handbook.docx')
