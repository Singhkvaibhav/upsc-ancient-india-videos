"""Ancient India, Simply Unearthed — Episode 24: The Kushanas.
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

EP = 24
CODE = 'Anc24'
TITLE = 'The_Kushanas'
NAME = "The Kushanas"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_goldcoin(ctx, 960, 640, 2.5, a, t)

CFG = dict(
    ep=24, period=(30, 230), dig=_dig,
    question='Who was earning this much foreign gold, and how?',
    tags=(('GOLD, AND A LONG WAY FROM HOME', 150, 300),),
    sources=('coin', 'stone', 'staff', 'leaf'),
    src_note='The Kushanas sat on the route to China, so Chinese accounts describe them.',
    panels=[
        (P_SITES([('PURUSHAPURA', -430, -230), ('MATHURA', -40, -80), ('BACTRIA', -660, -400),
                  ('TAXILA', -530, -330)]), 'OUT OF CENTRAL ASIA'),
        (P_TWO(['Silk moving west from China',
                'Indian goods joining it',
                'Roman gold coming the other way'],
               ['Roman gold melted down, say some',
                'Which would explain the sudden abundance',
                'Either way the wealth is real'],
               'THE SILK ROAD', 'WHERE THE GOLD CAME FROM'), 'ASTRIDE THE ROUTE'),
        (P_ROW(['Kanishka the First', 'Convened the fourth Buddhist council, in Kashmir',
                'Texts compiled; Mahayana ideas gain ground',
                'Buddhism sent along the routes he controlled',
                'Coins carry Iranian, Greek and Indian deities'], size=22), 'KANISHKA'),
        (P_TWO(['Grey schist, Hellenistic drapery', 'In the north-west'],
               ['Red sandstone', 'A distinctly Indian idiom'],
               'GANDHARA', 'MATHURA'), 'TWO SCHOOLS'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Kanishka\u2019s reign begins in 78 CE, and the Shaka era is his.',
                right='A later start, around 127 CE, fits the inscriptions and the Chinese evidence better.'),
    tip=['KANISHKA \u00b7 FOURTH COUNCIL', 'SILK ROAD'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('mountaincapital'), 'PURUSHAPURA'), (Q_SHAPE('councilhall'), 'THE FOURTH'),
          (Q_SHAPE('silkroad'), 'THE SILK ROAD')],
    mains='Why did Buddhism spread into Central Asia and China?',
    mains_tags=('AN EMPIRE ON THE ROUTES', 'A PATRON RULER', 'MONASTERIES AND MERCHANTS'),
    facts=('Kanishka, probably from 78 CE', 'The fourth Buddhist council', 'Gold coinage and the Silk Road'),
    next='THE SANGAM KINGDOMS',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
