"""Ancient India, Simply Unearthed — Episode 36: Later Chalukyas, Hoysalas, Yadavas and Kakatiyas.
Approved narration, word for word. No boundaries, no outline of India; no
kingdom is drawn as shaded territory.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 300.0
core.TOTAL = TOTAL
from engine.core import W, H
from engine.stone import S, carve, poly, rrect
from engine.auto import (build, fx_for, P_TEXT, P_SITES, P_ROW, P_TWO, P_STACK, P_VILLAGE,
                         P_OBJ, P_MON, P_WHEEL, Q_SHAPE, Q_OBJ, GY)
from engine import museum
from text import EN, HI as _HI

EP = 36
CODE = 'Anc36'
TITLE = 'Deccan_Kingdoms'
NAME = "Later Chalukyas, Hoysalas, Yadavas and Kakatiyas"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_starplan(ctx, 960, 640, 2.6, a, t)

CFG = dict(
    ep=36, period=(973, 1323), dig=_dig,
    question='Why would anyone build a temple on a star-shaped plan?',
    tags=(('A PLAN, NOT A PICTURE', 150, 300),),
    sources=('stone', 'trowel', 'leaf'),
    src_note='Inscriptions in Kannada, Telugu and Sanskrit, in large numbers.',
    panels=[
        (P_ROW(['KALYANI  ·  the Later Chalukyas, from about 973 CE',
                'DWARASAMUDRA  ·  the Hoysalas',
                'DEVAGIRI  ·  the Yadavas',
                'WARANGAL  ·  the Kakatiyas'], size=25), 'FOUR KINGDOMS, BY CAPITAL'),
        (P_ROW(['Star plans, on raised platforms',
                'Soapstone, soft enough to work almost like wood',
                'And it hardens with exposure',
                'Horizontal bands of carving right round the building',
                'Several sculptors signed their work'], size=22), 'THE HOYSALAS'),
        (P_ROW(['No great river crosses the Telangana plateau',
                'So they built tanks, in their thousands',
                'Bunded reservoirs catching the monsoon',
                'Released through sluices into the fields',
                'A state\u2019s power resting on an engineering decision'], size=22), 'THE KAKATIYAS'),
        (P_TWO(['A fortress on an isolated hill', 'Concentric defences',
                'Considered near-impregnable'],
               ['The Ayyavole guild across the Deccan',
                'Long-distance trade carried on',
                'Whoever held which capital'],
               'DEVAGIRI', 'THE MERCHANT GUILDS'), 'TWO MORE THINGS'),
    ],
    plaque=dict(kind='names', title='OLD NAME, NEW NAME', left='DWARASAMUDRA', right='HALEBIDU'),
    tip=['KALYANI \u00b7 DWARASAMUDRA', 'DEVAGIRI \u00b7 WARANGAL'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('towerplan'), 'THE HOYSALAS'), (Q_SHAPE('tanksluice'), 'TANKS, UNDER THE KAKATIYAS'),
          (Q_SHAPE('hillring'), 'DEVAGIRI')],
    mains='How did regional kingdoms shape Indian art and engineering?',
    mains_tags=('HOYSALA SOAPSTONE', 'KAKATIYA TANKS', 'DISPLAY, AND WHAT PAID FOR IT'),
    facts=('Four Deccan kingdoms', 'Soapstone carving at Belur and Halebidu',
           'Tank irrigation under the Kakatiyas'),
    next='THE RAJPUT KINGDOMS',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
