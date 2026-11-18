"""Ancient India, Simply Unearthed — Episode 26: Sangam Literature and Society.
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

EP = 26
CODE = 'Anc26'
TITLE = 'Sangam_Literature_and_Society'
NAME = "Sangam Literature and Society"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_tamilleaf(ctx, 960, 640, 2.3, a, t)

CFG = dict(
    ep=26, period=(-300, 300), dig=_dig,
    question='How does anything written on a palm leaf survive two thousand years?',
    tags=(('COPIED, AND COPIED AGAIN', 150, 300),),
    sources=('leaf', 'stone'),
    src_note='Early Tamil-Brahmi inscriptions corroborate names, places, and that writing was in use.',
    panels=[
        (P_ROW(['Three Sangams, academies at Madurai',
                'The first two: impossibly ancient, works lost',
                'The third produced the poetry we have',
                'Historians treat the three as later tradition'], size=24),
         'THE THREE ACADEMIES'),
        (P_ROW(['ETTUTHOKAI  ·  eight anthologies', 'PATTUPPATTU  ·  ten long poems',
                'Eighteen minor works', 'TOLKAPPIYAM  ·  the oldest Tamil grammar',
                'And the rules of the five landscapes'], size=22), 'THE CORPUS'),
        (P_TWO(['The inside', 'Love and private feeling',
                'The people are left unnamed', 'So the situation stands for anyone\u2019s'],
               ['The outside', 'War, kings, death, generosity',
                'People are named', 'Praised, and mourned'],
               'AKAM', 'PURAM'), 'HOW TAMIL POETICS DIVIDES EXPERIENCE'),
        (P_ROW(['Kings and many smaller chieftains', 'Patronage as public duty and reputation',
                'Trade and towns mattered', 'Women composed, and are named poets',
                'But these are poems, written for patrons'], size=22), 'WHAT IT TELLS US'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='The three Sangams preserve a real memory of organised literary patronage at Madurai.',
                right='The three-academy account is a later framing; only the surviving corpus can be dated.'),
    tip=['AKAM INSIDE', 'PURAM OUTSIDE'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('grammar'), 'THE TOLKAPPIYAM'), (Q_SHAPE('anthologies'), 'THE ETTUTHOKAI'),
          (Q_SHAPE('unnamed'), 'AKAM')],
    mains='Assess Sangam literature as a historical source.',
    mains_tags=('GOOD FOR SOCIETY AND TRADE', 'WRITTEN FOR PATRONS', 'HARD TO DATE'),
    facts=('Tolkappiyam, the earliest Tamil grammar', 'Akam and puram', 'Over four hundred named poets'),
    next='TRADE WITH ROME AND THE WORLD',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
