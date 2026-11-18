"""Scaffold one episode from a unit script file.

usage: python3 tools/new_ep.py <EP> <script.md> "seg1,seg2,..."

The segment spec says how many beats each of the seven segments gets, e.g.
"2,1,2,1,2,2,1,2,1,4,2" — one number per row of the script's table, in order.
It writes episodes/epNN/text.py with both languages asserted word for word
against the script, and leaves ep.py to carry the config.
"""
import sys, os, re, io
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PREFIX_FOR = {'The Dig': 'dig', 'How do we know?': 'src', 'The Frieze': 'frz',
              'The Plaque': 'plq', 'Inscription': 'ins', 'Dig Quiz': 'quiz',
              'The Gallery': 'gal'}


def tables(md, ep):
    """pull the English and Hindi tables for one episode out of a unit script"""
    blocks = re.split(r'\n## Episode ', md)
    for b in blocks[1:]:
        if not b.startswith(f'{ep} '): continue
        en = re.search(r'\| Time \| Segment \| Visual \| Narration \|(.*?)\n\n', b, re.S).group(1)
        hi = re.search(r'#### Hindi narration \(हिंदी\)\s*\n\| Time \| Narration \|(.*?)\n\n', b, re.S).group(1)
        return en, hi
    raise SystemExit(f'episode {ep} not found')


def rows(tbl, cols):
    out = []
    for r in tbl.split('\n'):
        if not r.strip().startswith('|'): continue
        c = [x.strip() for x in r.strip().strip('|').split('|')]
        if not c or c[0].startswith('---') or c[0] == 'Time': continue
        out.append([c[i] for i in cols])
    return out


def partition(parts, n):
    assert len(parts) >= n, (len(parts), n)
    cum = []; a = 0
    for p in parts: a += len(p); cum.append(a)
    total = a; cuts = []
    for i in range(1, n):
        target = total*i/n
        lo = max(i - 1, (cuts[-1] + 1) if cuts else 0)
        hi = len(parts) - (n - i) - 1
        cuts.append(min(range(lo, hi + 1), key=lambda j: abs(cum[j] - target)))
    groups = []; start = 0
    for c in cuts + [len(parts) - 1]:
        groups.append(parts[start:c + 1]); start = c + 1
    assert len(groups) == n and all(groups)
    return groups


def main():
    ep = int(sys.argv[1]); path = sys.argv[2]
    spec = [int(x) for x in sys.argv[3].split(',')]
    md = open(path, encoding='utf-8').read()
    en_t, hi_t = tables(md, ep)
    en = rows(en_t, [1, 3])          # segment, narration
    hi = rows(hi_t, [1])             # narration
    assert len(en) == len(hi) == len(spec), (len(en), len(hi), len(spec))

    counts = {}
    EN, HI = [], []
    for (segment, e), (h,), n in zip(en, hi, spec):
        pfx = PREFIX_FOR.get(segment)
        if pfx is None:
            raise SystemExit(f'unknown segment name: {segment!r}')
        ks = []
        for _ in range(n):
            counts[pfx] = counts.get(pfx, 0) + 1
            ks.append(f'{pfx}{counts[pfx]}')
        if n == 1:
            EN.append((ks[0], e)); HI.append((ks[0], h)); continue
        ep_ = re.split(r'(?<=[.!?]) +', e); hp = re.split(r'(?<=[।!?]) +', h)
        for k, g in zip(ks, partition(ep_, n)): EN.append((k, ' '.join(g)))
        for k, g in zip(ks, partition(hp, n)): HI.append((k, ' '.join(g)))

    assert ' '.join(x[1] for x in EN) == ' '.join(r[1] for r in en), 'EN text changed'
    assert ' '.join(x[1] for x in HI) == ' '.join(r[0] for r in hi), 'HI text changed'
    assert [k for k, _ in EN] == [k for k, _ in HI]

    d = os.path.join(ROOT, 'episodes', f'ep{ep:02d}')
    os.makedirs(d, exist_ok=True)
    with io.open(os.path.join(d, 'text.py'), 'w', encoding='utf-8') as f:
        f.write('# -*- coding: utf-8 -*-\n')
        f.write(f'# generated from {os.path.basename(path)} - approved narration, word for word\n')
        f.write('EN = [\n')
        for k, v in EN: f.write(f' ({k!r}, {v!r}),\n')
        f.write(']\n\nHI = {\n')
        for k, v in HI: f.write(f' {k!r}: {v!r},\n')
        f.write('}\n')
    print(f'ep{ep:02d}: {len(EN)} beats, longest EN {max(len(v.split()) for _, v in EN)} words')
    for k, v in EN: print('  ', k, len(v.split()))


if __name__ == '__main__':
    main()
