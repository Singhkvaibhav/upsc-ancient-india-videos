"""Ancient India, Simply Unearthed — Episode 27: Trade with Rome and the World.
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

EP = 27
CODE = 'Anc27'
TITLE = 'Trade_with_Rome'
NAME = "Trade with Rome and the World"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_amphora(ctx, 960, 640, 2.4, a, t)

CFG = dict(
    ep=27, period=(-100, 300), dig=_dig,
    question='How did a Mediterranean jar end up buried in India?',
    tags=(('NOT MADE HERE', 150, 300),),
    sources=('staff', 'trowel', 'coin', 'leaf'),
    src_note='The Periplus of the Erythraean Sea was written by someone who clearly knew the route.',
    panels=[
        (P_ROW(['Along the coast: the better part of a year',
                'Across the open sea on the south-west monsoon: a season',
                'Back on the north-east monsoon',
                'Credited to Hippalus, but Arab and Indian sailors knew it'], size=23),
         'THE MONSOON MAKES IT POSSIBLE'),
        (P_SITES([('BARYGAZA', -470, -180), ('MUZIRIS', -300, 150), ('ARIKAMEDU', 90, 160),
                  ('PUHAR', 140, 60), ('TAMRALIPTI', 480, -150)]), 'SO THE PORTS GROW RICH'),
        (P_TWO(['Pepper, above all', 'Pearls and ivory', 'Fine cotton and silk',
                'Precious stones and spices'],
               ['Gold and silver coin', 'Wine and olive oil', 'Glass and fine pottery', 'Coral'],
               'OUT OF INDIA', 'INTO INDIA'), 'NOTICE THE ASYMMETRY'),
        (P_ROW(['Hoards of Roman coins across peninsular India',
                'Concentrated in the south, where the pepper came from',
                'Pliny complained the trade drained the empire',
                'Quoted in every textbook',
                'Worth asking how reliable it is'], size=22), 'THE MONEY IN THE GROUND'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='The drain was real: the hoards are large, and Roman writers noticed the outflow.',
                right='Pliny\u2019s figure is rhetoric, not accounting; the coins may be bullion by weight.'),
    tip=['PEPPER OUT', 'GOLD IN'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('handbook'), 'THE PERIPLUS'), (Q_SHAPE('monsoon'), 'THE MONSOON'),
          (Q_SHAPE('deltaport'), 'TAMRALIPTI')],
    mains='What does Indo-Roman trade tell us about the ancient Indian economy?',
    mains_tags=('PORTS AND GOODS', 'COIN HOARDS', 'CRAFT BEHIND THE EXPORTS'),
    facts=('The Periplus describes the ports', 'Hippalus and the monsoon winds',
           'Roman coin hoards in the south'),
    next='THE RISE OF THE GUPTAS',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
