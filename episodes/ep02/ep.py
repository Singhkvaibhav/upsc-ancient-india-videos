"""Ancient India, Simply Unearthed — Episode 2: Stone Age India (English + Hindi).
Approved narration, word for word. No boundaries, no outline of India.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 300.0
core.TOTAL = TOTAL
from engine.core import W, H
from engine.stone import S, carve, poly, rrect, drain_section, pot, brick, house, platform, coursed
from engine.auto import (build, fx_for, P_TEXT, P_SITES, P_ROW, P_TWO, P_STACK, P_VILLAGE,
                         P_OBJ, P_MON, Q_SHAPE, Q_OBJ, GY)
from engine import museum
from text import EN, HI as _HI

EP = 2
CODE = 'Anc02'
TITLE = 'Stone_Age_India'
NAME = 'Stone Age India'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_handaxe(ctx, 960, 620, 3.0, a, t)

CFG = dict(
    ep=2, period=(-3000, -2000), dig=_dig,
    question='Who were the first Indians, and how do we know anything at all about them?',
    tags=(('LOWER PALAEOLITHIC', 150, 300),),
    sources=('trowel',),
    src_note='No writing, no inscriptions. Everything here came out of the ground.',
    panels=[
        (P_ROW(['Hand axes', 'Cleavers', 'Choppers'],
               obj=lambda c, x, y, s, a, t: museum.ex_handaxe(c, x, y, .9, a, t)), 'PALAEOLITHIC · BIG TOOLS'),
        (P_TEXT('PAINTED ROCK SHELTERS', 'ANIMALS, HUNTS AND DANCES', 'BHIMBETKA · UNESCO', size=46), None),
        (P_OBJ(lambda c, x, y, s, a, t: Q_SHAPE('microlith')(c, x, y, a, t), s=1.6,
               label='TINY BLADES, SET IN A ROW'), 'MESOLITHIC · SMALL TOOLS'),
        (P_SITES([('MEHRGARH', -520, -210), ('BURZAHOM', -60, -330), ('KOLDIHWA', 430, -140)]),
         'NEOLITHIC · FARMING BEGINS'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Some Bhimbetka paintings may reach back into the Upper Palaeolithic.',
                right='Most of what survives is Mesolithic or later; the same walls were painted again and again.'),
    tip=['BIG STONE · SMALL STONE', 'SEED'],
    prompt='PAUSE AND NAME THE AGE',
    quiz=[(Q_SHAPE('handaxe'), 'PALAEOLITHIC'), (Q_SHAPE('microlith'), 'MESOLITHIC'),
          (Q_SHAPE('polished'), 'NEOLITHIC')],
    mains='Why did the shift to farming matter so much?',
    mains_tags=('SETTLEMENT', 'SURPLUS', 'STORAGE'),
    facts=('Palaeolithic, Mesolithic, Neolithic', "Bhimbetka's painted shelters", 'Farming begins at Mehrgarh'),
    next='CHALCOLITHIC CULTURES',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
