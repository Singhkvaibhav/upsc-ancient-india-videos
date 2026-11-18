"""Ancient India, Simply Unearthed — Episode 38: Ancient Indian Science and Mathematics.
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

EP = 38
CODE = 'Anc38'
TITLE = 'Science_and_Mathematics'
NAME = "Ancient Indian Science and Mathematics"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_zerostone(ctx, 960, 640, 2.5, a, t)

CFG = dict(
    ep=38, period=(-800, 1200), dig=_dig,
    question='Who decided that nothing deserved a sign of its own?',
    tags=(('A CIRCLE THAT MEANS NOTHING', 150, 300),),
    sources=('leaf', 'stone'),
    src_note='A numeral on a dated stone proves the system was in ordinary use, not just in a manuscript.',
    panels=[
        (P_ROW(['Texts on the geometry of altar construction',
                'A square converted to a circle of equal area',
                'Doubling a square',
                'Relations between the sides of right-angled triangles',
                'Applied mathematics, because a ritual required exactness'], size=22),
         'THE SHULBA SUTRAS'),
        (P_ROW(['Nine digits whose meaning depends on their column',
                'And a symbol for an empty column',
                'Aryabhata works with it, born 476 CE',
                'Brahmagupta writes rules for zero and negative numbers',
                'The system travels to the Arab world, then to Europe'], size=22),
         'THE SYSTEM ITSELF'),
        (P_ROW(['ARYABHATA  ·  eclipses as shadows; the earth rotates',
                'VARAHAMIHIRA  ·  compiles earlier schools, Greek among them',
                'BHASKARA II  ·  the Siddhanta Shiromani, algebra, planetary motion'], size=25),
         'ASTRONOMY'),
        (P_ROW(['CHARAKA  ·  diagnosis, causes, treatment, prevention',
                'SUSHRUTA  ·  surgical procedures and many instruments',
                'Operations for cataract and nose reconstruction',
                'Both compiled over long periods, so hard to date'], size=23), 'MEDICINE'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='The ninth-century Gwalior inscription is the earliest firmly dated written zero in India.',
                right='Radiocarbon work on the Bakhshali manuscript may push it earlier, but its dating is contested.'),
    tip=['ZERO \u00b7 SURGERY', 'THE SPINNING EARTH'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('altarropes'), 'THE SHULBA SUTRAS'), (Q_SHAPE('zerorules'), 'BRAHMAGUPTA'),
          (Q_SHAPE('instruments'), 'THE SUSHRUTA SAMHITA')],
    mains='What did ancient India contribute to science?',
    mains_tags=('NAME THE TEXT', 'AND ROUGHLY WHEN', 'CLAIM NO MODERN DISCOVERIES'),
    facts=('Decimal place value with zero', 'Aryabhata and Brahmagupta', 'Sushruta on surgery'),
    next='THE ANCIENT UNIVERSITIES',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
