"""Generate two directed, original AI voices for closing audio auditions.

Uses the Qwen team's public Gradio API; never imitate a named person.
Music and final mastering are handled separately by audio_ab_mix.py.
"""
import json, os, shutil
from pathlib import Path
from gradio_client import Client

OUT = Path(os.environ.get('FILM_OUTPUT', str(Path(__file__).resolve().parents[4] / 'audio-ab-build')))
OUT.mkdir(parents=True, exist_ok=True)
TEXT = '分享一个需要，贡献一个工具，开放一个场景。让技术，成为机会！让创造，惠及更多人！加入我们。现在——就一起行动！'
PROFILES = {
    'A': '标准普通话，成熟男性，四十岁左右，浑厚而通透的中低音，温暖的胸腔共鸣。正在国际大会上坚定地发表一份鼓舞人心的公益宣言。声音庄严、有力量、有信念，抑扬顿挫，气息充分。前半段稳健推进，重读分享、贡献、开放，句间有短暂停顿。后半段情绪逐层抬升，重读机会、更多人。最后一句怀着热切的希望向全场发出有力的行动邀请，重读一起行动，落点坚定。自然口语的连贯性，清晰饱满的吐字，不要新闻播报腔，不要压低嗓音，不要愤怒，不要吼叫。',
    'B': '标准普通话，成熟男性，三十五岁左右，中低音饱满有磁性，温暖明亮、有胸腔共鸣。充满信念和希望的大会演讲，像一位热忱的共创者邀请全场加入共同事业。语气昂扬而真诚，节奏鲜明，声音有向前的推动力，真实的情绪起伏，不要平铺直叙。三个行动短句逐步加强；让技术成为机会，重读机会；让创造惠及更多人，重读更多人；加入我们要亲近、有感染力；现在之后有一次有意的短停顿，最后就一起行动激情充沛、向上打开、坚定落下！保持自然、不喊叫，不要机械播报，不要故作深沉。',
}

if __name__ == '__main__':
    client = Client('https://qwen-qwen3-tts.hf.space',
                    ssl_verify='/etc/ssl/certs/ca-certificates.crt',
                    httpx_kwargs={'timeout': 90}, download_files=str(OUT / 'qwen'))
    (OUT / 'direction.json').write_text(json.dumps({'text':TEXT,'profiles':PROFILES}, ensure_ascii=False, indent=2))
    for key, direction in PROFILES.items():
        target = OUT / f'voice-{key}-raw.wav'
        if target.exists():
            print(key, 'already generated', flush=True)
            continue
        print(key, 'generating', flush=True)
        result = client.predict(text=TEXT, language='Chinese', voice_description=direction,
                                api_name='/generate_voice_design')
        print(key, 'result', result, flush=True)
        if not result[0]:
            raise RuntimeError(result[1])
        shutil.copyfile(result[0], target)
