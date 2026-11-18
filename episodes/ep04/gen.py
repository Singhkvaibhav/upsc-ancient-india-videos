# -*- coding: utf-8 -*-
import re, io
t = open('../../scripts/sample_ep04.md', encoding='utf-8').read()
en_tbl = re.search(r'\| Time \| Segment \| Visual \| Narration \|(.*?)\n\n', t, re.S).group(1)
hi_tbl = re.search(r'#### Hindi narration \(हिंदी\)\s*\n\| Time \| Narration \|(.*?)\n\n', t, re.S).group(1)

def rows(tbl, col):
    out = []
    for r in tbl.split('\n'):
        if not r.strip().startswith('|'): continue
        c = [x.strip() for x in r.strip().strip('|').split('|')]
        if not c or c[0].startswith('---') or c[0] == 'Time': continue
        out.append(c[col])
    return out

EN_ROWS = rows(en_tbl, 3); HI_ROWS = rows(hi_tbl, 1)
assert len(EN_ROWS) == len(HI_ROWS) == 11, (len(EN_ROWS), len(HI_ROWS))

SPLIT = [['dig1', 'dig2'], ['src1'], ['frz1', 'frz2'], ['frz3'], ['frz4', 'frz5'],
         ['frz6', 'frz7'], ['frz8'], ['plq1', 'plq2'], ['ins1'],
         ['quiz1', 'quiz2', 'quiz3', 'quiz4'], ['gal1', 'gal2']]
assert len(SPLIT) == 11

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

EN, HI = [], []
for keys, e, h in zip(SPLIT, EN_ROWS, HI_ROWS):
    n = len(keys)
    if n == 1:
        EN.append((keys[0], e)); HI.append((keys[0], h)); continue
    ep_ = re.split(r'(?<=[.!?]) +', e); hp = re.split(r'(?<=[।!?]) +', h)
    for k, g in zip(keys, partition(ep_, n)): EN.append((k, ' '.join(g)))
    for k, g in zip(keys, partition(hp, n)): HI.append((k, ' '.join(g)))

assert ' '.join(x[1] for x in EN) == ' '.join(EN_ROWS), 'EN text changed'
assert ' '.join(x[1] for x in HI) == ' '.join(HI_ROWS), 'HI text changed'
assert [k for k, _ in EN] == [k for k, _ in HI]

with io.open('text.py', 'w', encoding='utf-8') as f:
    f.write('# -*- coding: utf-8 -*-\n# generated from scripts/sample_ep04.md - approved narration, word for word\n')
    f.write('EN = [\n')
    for k, v in EN: f.write(f' ({k!r}, {v!r}),\n')
    f.write(']\n\nHI = {\n')
    for k, v in HI: f.write(f' {k!r}: {v!r},\n')
    f.write('}\n')
print(len(EN), 'beats; longest EN', max(len(v.split()) for _, v in EN), 'words')
for k, v in EN: print(' ', k, len(v.split()))
