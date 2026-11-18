"""Ancient India, Simply Unearthed — Episode 33: Chalukyas of Badami and Pallavas.
Approved narration, word for word. No boundaries, no outline of India; no
empire is drawn as shaded territory.\n\nTemples are drawn as architecture only; every sanctum is a dark, empty\nopening, and no deity or revered figure appears.
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

EP = 33
CODE = 'Anc33'
TITLE = 'Chalukyas_and_Pallavas'
NAME = "Chalukyas of Badami and Pallavas"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_ratha(ctx, 960, 640, 2.5, a, t)

CFG = dict(
    ep=33, period=(543, 757), dig=_dig,
    question='How do you carve a building downward out of one boulder?',
    tags=(('CUT FROM ONE STONE', 150, 300),),
    sources=('stone', 'trowel', 'leaf'),
    src_note='The standing monuments are the main evidence here; the texts are thinner than the stone.',
    panels=[
        (P_SITES([('BADAMI', -430, -40), ('AIHOLE', -360, -140), ('PATTADAKAL', -400, -90),
                  ('KANCHIPURAM', 180, 160), ('MAHABALIPURAM', 280, 210)]),
         'TWO DYNASTIES, FACING EACH OTHER'),
        (P_ROW(['Pulakeshin the Second, the Chalukya ruler',
                'The Aihole inscription, composed by Ravikirti',
                'It records checking Harsha at the Narmada',
                'Which is how we date Harsha',
                'Later defeated by Narasimhavarman the First'], size=22), 'THE INSCRIPTION'),
        (P_ROW(['FIRST  ·  shrines cut into cave faces',
                'THEN  ·  monoliths, whole temples from one boulder',
                'THEN  ·  structural temples, built from cut blocks',
                'Two centuries: from a hole in a cliff to a free-standing building'], size=23),
         'WATCH THE SEQUENCE'),
        (P_TWO(['The curving tower, the shikhara', 'Northern'],
               ['The stepped pyramidal vimana', 'Inside a walled enclosure', 'Southern'],
               'NAGARA', 'DRAVIDA'), 'BOTH STAND TOGETHER AT PATTADAKAL'),
    ],
    plaque=dict(kind='names', title='OLD NAME, NEW NAME', left='MAHABALIPURAM', right='MAMALLAPURAM'),
    tip=['AIHOLE \u00b7 BADAMI \u00b7 PATTADAKAL', 'MAHABALIPURAM'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('prashasti'), 'THE AIHOLE INSCRIPTION'), (Q_SHAPE('shikhara'), 'NAGARA'),
          (Q_SHAPE('vimana'), 'DRAVIDA')],
    mains='How did Indian temple architecture develop?',
    mains_tags=('CAVE, MONOLITH, STRUCTURAL', 'THEN THE TWO STYLES', 'PATTADAKAL HAS BOTH'),
    facts=('Pulakeshin II checked Harsha', 'Rathas at Mahabalipuram', 'Temple styles take shape'),
    next='THE TRIPARTITE STRUGGLE',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
