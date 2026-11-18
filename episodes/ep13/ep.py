"""Ancient India, Simply Unearthed — Episode 13: The Rise of Magadha (English + Hindi).
Approved narration, word for word. No boundaries, no outline of India.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 300.0
core.TOTAL = TOTAL
from engine.core import W, H
from engine.stone import S, carve, poly, rrect, coursed
from engine.auto import (build, fx_for, P_TEXT, P_SITES, P_ROW, P_TWO, P_STACK, P_VILLAGE,
                         P_OBJ, P_MON, Q_SHAPE, Q_OBJ, GY)
from engine import museum
from text import EN, HI as _HI

EP = 13
CODE = 'Anc13'
TITLE = 'The_Rise_of_Magadha'
NAME = 'The Rise of Magadha'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_wallsection(ctx, 960, 650, 2.6, a, t)

CFG = dict(
    ep=13, period=(-544, -321), dig=_dig,
    question='Who had this much money, and what were they afraid of?',
    tags=(('RAMPART AND PALISADE', 150, 300),),
    sources=('leaf', 'trowel'),
    src_note='The dynastic details differ between sources, so the sequence matters more than the years.',
    panels=[
        (P_ROW(['Rivers meeting: trade and defence', 'Hills round the first capital',
                'Iron ore nearby', 'Forests: timber and elephants', 'The most fertile Ganga soil'],
               size=22), 'WHY MAGADHA'),
        (P_ROW(['BIMBISARA  ·  marriage alliances, annexed Anga',
                'AJATASHATRU  ·  fought Kosala, broke the Vajjis',
                'UDAYIN  ·  a fort at Pataliputra'], size=26), 'THE HARYANKA DYNASTY'),
        (P_TWO(['Destroyed the power of Avanti', 'Magadha’s last rival gone'],
               ['An enormous army', 'A famously large treasury', 'Disliked for the taxes'],
               'SHISHUNAGA', 'NANDA'), 'THE DYNASTIES THAT FOLLOW'),
        (P_TWO(['Inside a ring of hills', 'Defensive', 'Right for a vulnerable state'],
               ['Where the rivers meet', 'Commercial and offensive', 'Controls the traffic'],
               'RAJAGRIHA', 'PATALIPUTRA'), 'THE CAPITAL MOVES'),
    ],
    plaque=dict(kind='names', title='OLD NAME, NEW NAME', left='PATALIPUTRA', right='PATNA',
                note='Rajagriha is Rajgir · both in Bihar'),
    tip=['IRON · RIVERS · ELEPHANTS', 'TWO CAPITALS'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('hillring'), 'RAJAGRIHA'), (Q_SHAPE('treasury'), 'THE NANDAS'),
          (Q_SHAPE('confederacy'), 'THE VAJJIS')],
    mains='Why did Magadha rise above the other mahajanapadas?',
    mains_tags=('GEOGRAPHY FIRST', 'THEN THE RULERS', 'THE SOURCES ARE PARTISAN'),
    facts=('Haryanka, Shishunaga, Nanda', 'Rajagriha, then Pataliputra', 'Geography did much of the work'),
    next='BUDDHISM: LIFE AND TEACHINGS',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
