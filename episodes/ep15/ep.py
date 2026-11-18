"""Ancient India, Simply Unearthed — Episode 15: Buddhist Councils, Schools and Spread.
Approved narration, word for word. The Buddha is never drawn as a face or figure:
stupas, chaityas, viharas and the wheel stand in his place, as early art did.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 300.0
core.TOTAL = TOTAL
from engine.core import W, H
from engine.stone import S, carve, poly, rrect
from engine.auto import (build, fx_for, P_TEXT, P_SITES, P_ROW, P_TWO, P_STACK, P_VILLAGE,
                         P_OBJ, P_MON, Q_SHAPE, Q_OBJ, GY)
from engine import museum
from text import EN, HI as _HI

EP = 15
CODE = 'Anc15'
TITLE = 'Councils_Schools_and_Spread'
NAME = 'Buddhist Councils, Schools and Spread'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_stupamodel(ctx, 960, 630, 2.6, a, t)

CFG = dict(
    ep=15, period=(-483, 200), dig=_dig,
    question='How does a mound over relics become an architecture?',
    tags=(('A RELIQUARY, THEN A MONUMENT', 150, 300),),
    sources=('leaf', 'stone', 'trowel', 'staff'),
    src_note='Donor inscriptions carved on the monuments themselves name who paid for them.',
    panels=[
        (P_ROW(['FIRST  ·  Rajagriha  ·  what he taught',
                'SECOND  ·  Vaishali  ·  discipline, and a split',
                'THIRD  ·  Pataliputra  ·  under Ashoka',
                'FOURTH  ·  Kashmir  ·  under Kanishka'], size=25), 'FOUR COUNCILS'),
        (P_TWO(['Called Hinayana by the other side', 'Theravada by its own adherents',
                'The earlier texts, in Pali', 'The Buddha as a teacher'],
               ['Sanskrit', 'The bodhisattva ideal', 'Delays release to help others',
                'The Buddha as something greater'],
               'THE OLDER STREAM', 'MAHAYANA'), 'TWO VEHICLES'),
        (P_SITES([('SRI LANKA', -120, 150), ('CENTRAL ASIA', -560, -360), ('CHINA', 600, -330),
                  ('SOUTHEAST ASIA', 520, 60)]), 'IT TRAVELLED WITH MERCHANTS'),
        (P_MON('stupa', s=1.0, sky='dawn', label='SANCHI · BHARHUT · AMARAVATI · AJANTA · KARLE'),
         'AND IT BUILT'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='The councils are broadly historical, recording real disputes over doctrine and discipline.',
                right='The later accounts were written by the winning side and read later divisions backwards.'),
    tip=['FOUR COUNCILS', 'TWO VEHICLES'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('stupa'), 'A STUPA'), (Q_SHAPE('chaitya'), 'A CHAITYA'),
          (Q_SHAPE('vihara'), 'A VIHARA')],
    mains='Why did Buddhism spread beyond India?',
    mains_tags=('TRADE ROUTES', 'MERCHANT AND ROYAL PATRONAGE', 'MONASTERIES AS INFRASTRUCTURE'),
    facts=('Four councils', 'Hinayana and Mahayana', 'Carried along trade routes'),
    next='JAINISM',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
