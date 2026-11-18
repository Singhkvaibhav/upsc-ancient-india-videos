"""Ancient India, Simply Unearthed — Episode 5: Harappan Life (English + Hindi).
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

EP = 5
CODE = 'Anc05'
TITLE = 'Harappan_Life'
NAME = 'Harappan Life'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_seal(ctx, 960, 620, 2.6, a, t)

CFG = dict(
    ep=5, period=(-2600, -1900), dig=_dig,
    question='We can see every one of these seals clearly. Why can we not read a single one?',
    tags=(('STEATITE SEAL', 150, 300),),
    sources=('trowel',),
    src_note='One source we can use, and one we cannot: the script has never been deciphered.',
    panels=[
        (P_OBJ(lambda c, x, y, s, a, t: Q_SHAPE('field')(c, x, y, a, t), s=1.5,
               label='FURROWS CROSSING AT RIGHT ANGLES'), 'THE PLOUGHED FIELD AT KALIBANGAN'),
        (P_ROW(['Carnelian beads', 'Shell bangles', 'Copper and bronze', 'Wheel-thrown pottery']), 'CRAFTS'),
        (P_OBJ(lambda c, x, y, s, a, t: Q_SHAPE('weight')(c, x, y, a, t), s=1.5,
               label='1 · 2 · 4 · 8 · 16, AND ON UPWARDS'), 'WEIGHTS MEAN STANDARDS'),
        (P_TEXT('OVER FOUR HUNDRED SIGNS', 'MOSTLY RIGHT TO LEFT', 'NO BILINGUAL TEXT, EVER', size=44),
         'THE SCRIPT'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='The seals show figures and symbols that later Indian religion also uses.',
                right='Without readable text, identifying any figure is interpretation, not evidence.'),
    tip=['SEAL · SCALE · SAIL'],
    quiz=[(Q_SHAPE('field'), 'THE PLOUGHED FIELD AT KALIBANGAN'), (Q_SHAPE('weight'), 'A HARAPPAN WEIGHT'),
          (Q_SHAPE('bead'), 'A CHANHUDARO BEAD')],
    mains='What do Harappan weights and seals tell us about the economy?',
    mains_tags=('STANDARDISATION', 'SUPERVISION', 'LONG-DISTANCE TRADE'),
    facts=('Weights in a doubling series', 'Trade reached Mesopotamia', 'The script is still unread'),
    next='HARAPPAN SITES AND DECLINE',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
