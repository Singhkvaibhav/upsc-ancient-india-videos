"""Ancient India, Simply Unearthed — Episode 3: Chalcolithic Cultures (English + Hindi).
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

EP = 3
CODE = 'Anc03'
TITLE = 'Chalcolithic_Cultures'
NAME = 'Chalcolithic Cultures'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    pot(ctx, 960, 740, 3.4, a)

CFG = dict(
    ep=3, period=(-2500, -700), dig=_dig,
    question='Why did these villages, so good at farming, never build a city?',
    tags=(('BLACK-ON-RED WARE', 150, 300),),
    sources=('trowel',),
    src_note='No writing again. Their pots, their copper, their houses and their graves.',
    panels=[
        (P_OBJ(lambda c, x, y, s, a, t: Q_SHAPE('copperstone')(c, x, y, a, t), s=1.5,
               label='COPPER FOR SOME JOBS, STONE FOR THE REST'), 'CHALCOLITHIC · COPPER-STONE'),
        (P_SITES([('AHAR', -560, -210), ('KAYATHA', -180, -310), ('MALWA', 160, -150), ('JORWE', 540, -260)]),
         'MANY CULTURES, NOT ONE'),
        (P_VILLAGE(8), 'FARMING VILLAGES, WELL ORGANISED'),
        (P_ROW(['Chariot with oxen', 'Buffalo', 'Elephant', 'Rhinoceros']), 'THE DAIMABAD BRONZES'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Late Harappan: the bronzes belong with the earlier phase at Daimabad.',
                right='Later: the casting technique suggests a date after the Chalcolithic levels.'),
    tip=['COPPER AND STONE', 'VILLAGE, NOT CITY'],
    quiz=[(Q_SHAPE('copperstone'), 'THE CHALCOLITHIC'), (Q_SHAPE('pot'), 'BLACK-ON-RED WARE'),
          (Q_SHAPE('channel'), 'INAMGAON')],
    mains='Why did Chalcolithic India produce no cities?',
    mains_tags=('SCALE', 'RAINFALL AND SOIL', 'NO SURPLUS, NO TRADE'),
    facts=('Copper used alongside stone', 'Ahar, Kayatha, Malwa, Jorwe', 'Villages, not cities'),
    next='HARAPPAN CITIES',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
