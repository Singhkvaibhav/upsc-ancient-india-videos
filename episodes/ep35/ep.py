"""Ancient India, Simply Unearthed — Episode 35: The Cholas.
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

EP = 35
CODE = 'Anc35'
TITLE = 'The_Cholas'
NAME = "The Cholas"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_cholatower(ctx, 960, 640, 2.4, a, t)

CFG = dict(
    ep=35, period=(850, 1279), dig=_dig,
    question='What does it take to build sixty metres of stone?',
    tags=(('SIXTY METRES OF STONE', 150, 300),),
    sources=('stone', 'trowel', 'leaf', 'staff'),
    src_note='The Cholas wrote on walls, which is why they are the best-documented ancient Indian state.',
    panels=[
        (P_ROW(['Vijayalaya, from about 850 CE',
                'RAJARAJA I  ·  the Brihadisvara temple, and a land survey',
                'RAJENDRA I  ·  campaigned north to the Ganga',
                'And founded Gangaikonda Cholapuram'], size=24), 'THE DYNASTY'),
        (P_ROW(['They built a navy and used it',
                'A naval expedition against Srivijaya',
                'Trade and diplomacy with China',
                'Protecting merchant guilds\u2019 access to eastern trade'], size=24),
         'SOMETHING NO OTHER DYNASTY DID'),
        (P_ROW(['UR  ·  the general assembly of an ordinary village',
                'SABHA  ·  the assembly of a brahmadeya',
                'NAGARAM  ·  the assembly of a merchant town',
                'Their proceedings inscribed on temple walls'], size=24), 'THREE ASSEMBLIES'),
        (P_ROW(['The village divided into wards',
                'Candidates qualified by property, age, literacy and conduct',
                'Names on palm leaves, put in a pot, a ticket drawn',
                'Committees for gardens, tanks, gold and justice',
                'Anyone who had not submitted accounts was disqualified'], size=22),
         'THE UTTARAMERUR INSCRIPTION'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='A strong centralised empire with a real bureaucracy, revenue survey and standing army.',
                right='A segmentary state: ritual sovereignty at the centre, real power local.'),
    tip=['UR \u00b7 SABHA', 'NAGARAM'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('potlots'), 'THE KUDAVOLAI SYSTEM'), (Q_SHAPE('towerplan'), 'THE BRIHADISVARA TEMPLE'),
          (Q_SHAPE('harbour'), 'SRIVIJAYA')],
    mains='Describe Chola local self-government.',
    mains_tags=('THE THREE ASSEMBLIES', 'THE UTTARAMERUR PROCEDURE', 'ONE INSCRIPTION IS AN IDEAL'),
    facts=('Rajaraja and Rajendra', 'Village assemblies recorded in stone',
           'A navy that reached Southeast Asia'),
    next='CHALUKYAS, HOYSALAS, YADAVAS AND KAKATIYAS',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
