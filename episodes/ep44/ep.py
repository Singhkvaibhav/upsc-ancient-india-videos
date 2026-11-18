"""Ancient India, Simply Unearthed — Episode 44: Ancient India: a Walk Through the Gallery.
Approved narration, word for word. No boundaries, no outline of India; no
kingdom is drawn as shaded territory.\n\nThe series recap. Its four middle panels are the gallery walk itself:\nevery case from Episode 1 to Episode 43, panned slowly past.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 300.0
core.TOTAL = TOTAL
from engine.core import W, H, seg, ease
from engine.stone import S, carve, poly, rrect, engraved
from engine.auto import (build, fx_for, P_TEXT, P_SITES, P_ROW, P_TWO, P_STACK, P_VILLAGE,
                         P_OBJ, P_MON, P_WHEEL, Q_SHAPE, Q_OBJ, GY)
from engine import museum
from text import EN, HI as _HI

EP = 44
CODE = 'Anc44'
TITLE = 'A_Walk_Through_the_Gallery'
NAME = "Ancient India: a Walk Through the Gallery"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_cointray(ctx, 960, 640, 2.0, a, t)

def _walk(lo, hi):
    """one stretch of the hall: cases lo..hi, panned slowly past the camera"""
    def d(ctx, cx, gy, a, t):
        n = hi - lo + 1
        span = n*300.
        ox = cx - 760 - (t/6.2 % 1.)*max(0., span - 1520)
        ctx.save(); ctx.translate(ox, 0)
        for i in range(n):
            ep_ = lo + i
            x = i*300.
            q = ease(seg(t, .2 + i*.12, .8 + i*.12))
            if q <= 0: continue
            carve(ctx, lambda x=x: rrect(ctx, x, gy - 430, 262, 360, 8),
                  tuple(v*.9 for v in S['clay']), a*q, depth=4.4, seed=1200 + ep_)
            ent = museum.EXHIBITS.get(ep_)
            if ent:
                ent[0](ctx, x + 131, gy - 190, .62, a*q, t)
            engraved(ctx, f'EP {ep_}', x + 131, gy - 92, 22, a*q*.9, S['ochre'], 'c', serif=False)
        ctx.restore()
    return d


CFG = dict(
    ep=44, period=(-2500000, 1200), dig=_dig,
    question='How does anybody know any of this?',
    tags=(('THE LAST SWEEP', 150, 300),),
    sources=('trowel', 'leaf', 'stone', 'coin', 'staff'),
    src_note='All five, for the only time in the series.',
    panels=[
        (_walk(1, 11), 'THE FIRST ROOM'),
        (_walk(12, 21), 'CITIES, FAITH AND EMPIRE'),
        (_walk(22, 34), 'CROSSROADS AND GOLDEN AGE'),
        (_walk(35, 43), 'REGIONS, AND THE THEMES'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Ancient India ends around 1200 CE, with the establishment of the Delhi Sultanate.',
                right='The division is a convenience; nothing ended neatly in any year.'),
    tip=['STONE \u00b7 SEED \u00b7 CITY \u00b7 STATE', 'FAITH \u00b7 EMPIRE \u00b7 REGION'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('undeciphered'), 'THE HARAPPAN SCRIPT'), (Q_SHAPE('prashasti'), 'AN INSCRIPTION'),
          (Q_SHAPE('immunity'), 'LAND GRANTS')],
    mains='Name your source, and say what kind of source it is.',
    mains_tags=('"THE ARTHASHASTRA SAYS"', 'IS NOT', '"THE INSCRIPTION RECORDS"'),
    facts=('Forty-four episodes, seven rooms', 'Every claim rests on a source',
           'The arguments are part of the subject'),
    next='MEDIEVAL INDIA, SIMPLY PAINTED',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
