"""Ancient India, Simply Unearthed — Episode 22: Shungas, Kanvas and Satavahanas.
Approved narration, word for word. No boundaries, no outline of India; no
kingdom is drawn as shaded territory.

The Buddha is never drawn as a face or a figure: the Sanchi and Bharhut
panels are shown through the empty seat, the tree and the footprints, which
is what those panels actually do.
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

EP = 22
CODE = 'Anc22'
TITLE = 'Shungas_Kanvas_and_Satavahanas'
NAME = "Shungas, Kanvas and Satavahanas"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_torana(ctx, 960, 640, 2.4, a, t)

CFG = dict(
    ep=22, period=(-185, 225), dig=_dig,
    question='What replaces an empire that could build across a subcontinent?',
    tags=(('A GATEWAY, NOT A WALL', 150, 300),),
    sources=('stone', 'coin', 'leaf'),
    src_note='The Puranas give dynastic lists, which are useful but not precise.',
    panels=[
        (P_ROW(['Pushyamitra Shunga takes power about 185 BCE',
                'A much smaller territory, from Pataliputra and Vidisha',
                'Then the Kanvas, briefly',
                'No single power holds the north for five hundred years'], size=24),
         'THE NORTH BREAKS UP'),
        (P_SITES([('PRATISHTHANA', -140, -60), ('AMARAVATI', 330, 110), ('NASHIK', -430, -170),
                  ('KARLE', -480, -40)]), 'THE DECCAN RISES'),
        (P_TWO(['Rulers took their mothers\u2019 names',
                'Gautamiputra: son of Gautami',
                'Vasishthiputra: son of Vasishthi',
                'Unusual, and much discussed'],
               ['Lead and other coinage',
                'Rock-cut monasteries funded',
                'Merchants of the ports paid too',
                'Trade routes across the Deccan'],
               'MATRONYMICS', 'COINS AND PATRONAGE'), 'TWO THINGS TO KNOW'),
        (P_ROW(['Stupas enlarged at Sanchi and Bharhut', 'Railings and gateways carved',
                'Later, Amaravati in the south-east',
                'At the centre of each story: an empty seat',
                'The Buddha is in every scene, and never shown'], size=22),
         'AND THEN THE ART'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='The Satavahanas rose soon after the Mauryas, in the late first century BCE.',
                right='Their effective power begins later, in the first century CE.'),
    tip=['NORTH SPLITS', 'DECCAN RISES'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('torana'), 'A TORANA'), (Q_SHAPE('matronymic'), 'A MATRONYMIC'),
          (Q_SHAPE('aniconic'), 'ANICONIC REPRESENTATION')],
    mains='Who paid for the early Buddhist monuments?',
    mains_tags=('MERCHANTS AND GUILDS', 'MONKS AND NUNS', 'HOUSEHOLDERS, MORE THAN KINGS'),
    facts=('Shungas from about 185 BCE', 'Satavahanas in the Deccan', 'Gateways at Sanchi and Bharhut'),
    next='INDO-GREEKS, SHAKAS AND PARTHIANS',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
