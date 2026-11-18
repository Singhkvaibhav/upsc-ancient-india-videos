#!/usr/bin/env python3
"""Build the YouTube upload text for finished Ancient India episodes.

Writes output/youtube/AncNN.txt with an English block (title, short
description, memory tip, chapters) and a Hindi block (title, description),
plus a sourcing note.

Chapter times come from the delivered output/AncNN.en.srt, so this works
after an episode's scratch has been cleared. Chapter labels come from the
beat ids in episodes/epNN/text.py and the panel headings in ep.py, so they
follow the episode's own structure rather than a fixed list.

usage: python3 tools/youtube_meta.py [NN ...]   (default: every delivered episode)
"""
import glob, importlib.util, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'output')
YT = os.path.join(OUT, 'youtube')
SERIES = 'Ancient India, Simply Unearthed'
SERIES_HI = 'प्राचीन भारत, सरल खोज'

SEG = {'dig': 'The dig', 'src': 'How do we know?', 'plq': 'The plaque',
       'ins': 'The inscription: the memory tip', 'quiz': 'Dig Quiz, and one Mains line',
       'gal': 'The gallery'}

# Hindi topic names, for the Hindi title. Written by hand; the Hindi
# narration itself is the approved script text and is quoted, not translated.
HI_NAME = {
 1: 'प्राचीन भारत को हम कैसे जानते हैं', 2: 'पाषाण काल', 3: 'ताम्रपाषाण संस्कृतियाँ',
 4: 'हड़प्पा के नगर', 5: 'हड़प्पाई जीवन', 6: 'हड़प्पाई स्थल और पतन',
 7: 'पूर्व वैदिक काल', 8: 'उत्तर वैदिक काल', 9: 'वैदिक साहित्य',
 10: 'वर्ण, आश्रम और वैदिक समाज', 11: 'दक्षिण की महापाषाण संस्कृतियाँ',
 12: 'महाजनपद', 13: 'मगध का उदय', 14: 'बौद्ध धर्म: जीवन और शिक्षाएँ',
 15: 'बौद्ध संगीतियाँ, सम्प्रदाय और प्रसार', 16: 'जैन धर्म',
 17: 'अन्य सम्प्रदाय और विदेशी आक्रमण', 18: 'चंद्रगुप्त मौर्य और अर्थशास्त्र',
 19: 'अशोक और धम्म', 20: 'अशोक के अभिलेख', 21: 'मौर्य प्रशासन और पतन',
 22: 'शुंग, कण्व और सातवाहन', 23: 'हिन्द-यवन, शक और पह्लव', 24: 'कुषाण',
 25: 'संगम राज्य', 26: 'संगम साहित्य और समाज', 27: 'रोम और विश्व से व्यापार',
 28: 'गुप्तों का उदय', 29: 'गुप्त प्रशासन और समाज', 30: 'गुप्तकालीन विज्ञान और साहित्य',
 31: 'हर्षवर्धन', 32: 'वाकाटक और दक्कन', 33: 'बादामी के चालुक्य और पल्लव',
 34: 'त्रिपक्षीय संघर्ष', 35: 'चोल', 36: 'परवर्ती चालुक्य, होयसल, यादव और काकतीय',
 37: 'राजपूत राज्य', 38: 'प्राचीन भारतीय विज्ञान और गणित', 39: 'प्राचीन विश्वविद्यालय',
 40: 'विदेशी यात्री', 41: 'भूमि अनुदान और सामंतवाद की बहस',
 42: 'सिक्के और अभिलेख', 43: 'प्राचीन भारत में महिलाएँ',
 44: 'प्राचीन भारत: पूरी दीर्घा की सैर',
}

DISPLAY = {20: "Ashoka's Edicts", 44: 'Ancient India: a Walk Through the Gallery'}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# Frieze chapter labels for episodes written before ep.py carried a CFG with
# panel headings. Episode 4's are the ones written by hand for its first upload.
FRZ = {4: ['A common plan, c. 2600-1900 BCE', 'Citadel west, lower town east',
           'Streets in a grid, and the 1:2:4 brick', 'Covered drains',
           'Courtyard houses, wells and side lanes', 'The Great Bath at Mohenjo-daro',
           'The structures called granaries', 'Sites you can visit today']}


def srt_starts(path):
    """First cue start time, in seconds, for each subtitle cue."""
    out = []
    for line in open(path, encoding='utf-8'):
        m = re.match(r'(\d\d):(\d\d):(\d\d),(\d\d\d) -->', line.strip())
        if m:
            h, mi, s, ms = (int(x) for x in m.groups())
            out.append(h*3600 + mi*60 + s + ms/1000.)
    return out


def cue_texts(path):
    """Cue text, one per cue, in order."""
    out, buf, seen_time = [], [], False
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if re.match(r'\d\d:\d\d:\d\d,\d\d\d -->', line.strip()):
            if buf:
                out.append(' '.join(buf)); buf = []
            seen_time = True
        elif seen_time and line.strip() and not line.strip().isdigit():
            buf.append(line.strip())
    if buf:
        out.append(' '.join(buf))
    return out


def norm(s):
    return re.sub(r'[^a-z0-9 ]', '', s.lower())


def beat_times(ep_dir, srt):
    """Start time of each beat, by matching its opening words to the subtitles."""
    text = load(os.path.join(ep_dir, 'text.py'), 'text')
    starts, texts = srt_starts(srt), cue_texts(srt)
    times, j = [], 0
    for bid, line in text.EN:
        head = ' '.join(norm(line).split()[:4])
        hit = None
        for k in range(j, len(texts)):
            if norm(texts[k]).startswith(head[:len(head)]) or head in norm(texts[k]):
                hit = k; break
        if hit is None:
            times.append(None)
        else:
            times.append(starts[hit]); j = hit + 1
    return [(b, t) for (b, _), t in zip(text.EN, times)], text


def chapters(ep_dir, bt, cfg, n=0):
    """One chapter per segment; the frieze is split by its panel headings."""
    headings = [h for _, h in cfg.get('panels', []) if h] or FRZ.get(n, [])
    frz = [(b, t) for b, t in bt if b.startswith('frz')]
    per = max(1, (len(frz) + len(headings) - 1)//max(1, len(headings))) if headings else 1
    rows, fi = [], 0
    for b, t in bt:
        if t is None:
            continue
        pre = re.sub(r'\d+$', '', b)
        if pre in ('frz', 'pan', 'part'):
            if fi % per == 0:
                if headings:
                    lab = headings[min(fi//per, len(headings) - 1)]
                    # CFG headings are set in capitals for the screen; hand-written
                    # chapter labels are already cased, so leave those alone.
                    if lab == lab.upper():
                        lab = lab.title()
                else:
                    lab = f'Part {fi//per + 1}'
                rows.append((t, lab))
            fi += 1
        else:
            lab = SEG.get(pre)
            if lab and (not rows or rows[-1][1] != lab):
                rows.append((t, lab))
    keep = [(0.0, rows[0][1] if rows else 'Intro')]
    for t, lab in rows[1:]:
        if t - keep[-1][0] >= 10:
            keep.append((t, lab))
    return keep


def stamp(s):
    return f"{int(s//60)}:{int(s%60):02d}"


def build(n):
    nn = f"{n:02d}"
    ep_dir = os.path.join(ROOT, 'episodes', f'ep{nn}')
    vids = glob.glob(os.path.join(OUT, f'Anc{nn}_*.mp4'))
    srt = os.path.join(OUT, f'Anc{nn}.en.srt')
    if not vids or not os.path.exists(srt) or not os.path.exists(os.path.join(ep_dir, 'ep.py')):
        return False
    sys.path.insert(0, ROOT); sys.path.insert(0, ep_dir)
    cwd = os.getcwd(); os.chdir(ep_dir)
    try:
        ep = load(os.path.join(ep_dir, 'ep.py'), f'ep{nn}mod')
    finally:
        os.chdir(cwd)
    name = DISPLAY.get(n, ep.NAME)
    bt, text = beat_times(ep_dir, srt)
    chs = chapters(ep_dir, bt, getattr(ep, 'CFG', {}), n)

    en = dict(text.EN)
    hi = dict(text.HI)
    HIL = [(k, hi[k]) for k, _ in text.EN if k in hi]
    hook = ' '.join(v for k, v in text.EN if k.startswith('dig'))
    tip = ' '.join(v for k, v in text.EN if k.startswith('ins'))
    tip = re.sub(r'^.*?carved in stone\.\s*', '', tip)
    hook_hi = ' '.join(v for k, v in HIL if k.startswith('dig'))
    tip_hi = ' '.join(v for k, v in HIL if k.startswith('ins'))
    if 'तरकीब' in tip_hi.split('।')[0] or 'याद' in tip_hi.split('।')[0]:
        tip_hi = '।'.join(tip_hi.split('।')[1:]).strip() or tip_hi
    q = getattr(ep, 'CFG', {}).get('question', '')

    L = []
    L += ['=== ENGLISH ===', 'TITLE', f'{name} | {SERIES} Ep {n}', '']
    if q and norm(q) in norm(hook):
        q = ''
    L += ['SHORT DESCRIPTION', f'{hook} {q}'.strip(), '',
          f'Episode {n} of {SERIES}: a calm, five-minute animated explainer for UPSC '
          f'aspirants, with a memory tip you can carry into the exam hall. '
          f'English and Hindi audio tracks; subtitles in both.', '']
    L += ['MEMORY TIP', tip, '']
    L += ['CHAPTERS'] + [f'{stamp(t)} {lab}' for t, lab in chs] + ['']
    L += ['=== हिंदी ===', 'TITLE', f'{HI_NAME.get(n, name)} | {SERIES_HI} एपिसोड {n}', '']
    L += ['DESCRIPTION', f'{hook_hi}', '',
          f'{SERIES_HI} का एपिसोड {n}: UPSC की तैयारी करने वालों के लिए पाँच मिनट का '
          f'शांत, एनिमेटेड एक्सप्लेनर, हर एपिसोड में एक याद रखने की तरकीब के साथ। '
          f'हिंदी ऑडियो ट्रैक चुनने के लिए YouTube के सेटिंग्स में Audio track पर जाएँ।', '']
    L += ['याद रखने की तरकीब', tip_hi, '']
    L += ['A NOTE ON SOURCING',
          'Narration follows the approved script word for word, in both languages. '
          'Dates are given as the standard textbook dates, with "about" where the '
          'sources are uncertain. Where historians genuinely disagree, both readings '
          'appear on equal tablets and neither is presented as settled.',
          '',
          'No national or state boundaries, no outline of India and no kingdom as '
          'shaded territory appear in this episode: sites are pins on a schematic '
          'physical board. Nothing revered is depicted as a face or a figure.', '']
    L += ['TAGS',
          'UPSC, UPSC history, ancient India, ancient Indian history, NCERT history, '
          f'UPSC prelims, UPSC mains, GS Paper 1, {name}, GyaanXstudios', '']
    L += [f'#UPSC #AncientIndia #History #GyaanXstudios']

    os.makedirs(YT, exist_ok=True)
    open(os.path.join(YT, f'Anc{nn}.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    for p in (ep_dir, ROOT):
        if p in sys.path:
            sys.path.remove(p)
    for k in list(sys.modules):
        if k in ('text', f'ep{nn}mod'):
            del sys.modules[k]
    return True


if __name__ == '__main__':
    eps = [int(a) for a in sys.argv[1:]] or list(range(1, 45))
    ok = [n for n in eps if build(n)]
    print(f'wrote {len(ok)} metadata files: {", ".join(f"{n:02d}" for n in ok)}')
    missing = [n for n in eps if n not in ok]
    if missing:
        print('skipped (no delivered video yet): ' + ', '.join(f'{n:02d}' for n in missing))
