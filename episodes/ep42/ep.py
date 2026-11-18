"""Ancient India, Simply Unearthed — Episode 42: Coins and Inscriptions.
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

EP = 42
CODE = 'Anc42'
TITLE = 'Coins_and_Inscriptions'
NAME = "Coins and Inscriptions"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_cointray(ctx, 960, 640, 2.4, a, t)

CFG = dict(
    ep=42, period=(-600, 1200), dig=_dig,
    question='What makes an object better evidence than a chronicle?',
    tags=(('A THOUSAND YEARS IN ONE TRAY', 150, 300),),
    sources=('coin', 'stone', 'trowel'),
    src_note='Nobody copied these, nobody edited them centuries later.',
    panels=[
        (P_ROW(['PUNCH-MARKED  ·  silver, several punches, no name',
                'INDO-GREEK  ·  the first portrait and name, often bilingual',
                'KUSHANA  ·  gold, in quantity',
                'WESTERN KSHATRAPA  ·  silver, and dated',
                'GUPTA  ·  gold, in many designs'], size=22), 'FOLLOW THE SEQUENCE'),
        (P_ROW(['A name and a title, so a ruler',
                'A date, if it carries one',
                'Find-spots, which map where a currency circulated',
                'Metal and purity, which can show a treasury under strain',
                'And imagery: how a ruler wanted to be seen'], size=22), 'WHAT A COIN GIVES YOU'),
        (P_ROW(['Rock and pillar edicts', 'Copper-plate grants',
                'Temple-wall inscriptions', 'Prashastis, the praise-poems',
                'Seals, and memorial stones'], size=23), 'INSCRIPTIONS, BY TYPE'),
        (P_ROW(['Prinsep worked out Brahmi in 1837',
                'Kharoshthi was read in the same period',
                'Before that, centuries were literally illegible',
                'The Shaka era from 78 CE; the Gupta era from 319 or 320 CE',
                'A dated stone fixes everything around it'], size=22), 'AND THE DECIPHERMENT'),
    ],
    plaque=dict(kind='names', title='OLD NAME, NEW NAME', left='NUMISMATICS', right='THE STUDY OF COINS'),
    tip=['COINS DATE IT', 'INSCRIPTIONS PLACE IT'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('coin'), 'PUNCH-MARKED COINS'), (Q_SHAPE('prashasti'), 'EPIGRAPHY'),
          (Q_SHAPE('letterforms'), 'PALAEOGRAPHY')],
    mains='Why are archaeological sources more reliable than literary ones?',
    mains_tags=('CONTEMPORARY AND UNEDITED', 'OFTEN DATED', 'BUT ALSO PARTIAL'),
    facts=('Punch-marked to Gupta gold', 'Brahmi deciphered in 1837',
           'Dated inscriptions anchor everything'),
    next='WOMEN IN ANCIENT INDIA',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
