"""Ancient India, Simply Unearthed — Episode 30: Gupta Science and Literature.
Approved narration, word for word. No boundaries, no outline of India; no
empire is drawn as shaded territory.
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

EP = 30
CODE = 'Anc30'
TITLE = 'Gupta_Science_and_Literature'
NAME = "Gupta Science and Literature"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_ironpillar(ctx, 960, 640, 2.4, a, t)

CFG = dict(
    ep=30, period=(320, 550), dig=_dig,
    question='Why is sixteen-hundred-year-old iron not a heap of rust?',
    tags=(('IRON, AND ALMOST NO RUST', 150, 300),),
    sources=('leaf', 'stone'),
    src_note='Inscriptions show the numerals were in everyday use, not only in scholars\u2019 books.',
    panels=[
        (P_ROW(['Born 476 CE; wrote the Aryabhatiya at twenty-three',
                'A value for pi correct to four decimal places',
                'And described, correctly, as approximate',
                'Eclipses explained as shadows, not myth',
                'The earth rotates on its axis'], size=22), 'ARYABHATA'),
        (P_ROW(['The same nine digits mean different amounts by column',
                'An empty column needs a symbol of its own',
                'Developed in India over this period',
                'Passed to the Arab world, then to Europe',
                'Which is why Europeans called them Arabic numerals'], size=22),
         'DECIMAL PLACE VALUE, WITH ZERO'),
        (P_ROW(['VARAHAMIHIRA  ·  the Brihat Samhita',
                'BRAHMAGUPTA  ·  rules for zero and negative numbers',
                'CHARAKA AND SUSHRUTA  ·  diagnosis, treatment, surgery'], size=25),
         'OTHERS TO KNOW'),
        (P_ROW(['KALIDASA  ·  Abhijnanashakuntalam, Meghaduta, Raghuvamsha',
                'THE PANCHATANTRA  ·  fables that travelled further than most',
                'THE PURANAS  ·  compiled in their final form',
                'Sanskrit becomes the language of courts and learning'], size=23),
         'THE LITERATURE'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='A golden age: an extraordinary concentration of mathematics, astronomy, literature and art.',
                right='The label flatters a court elite; the same period\u2019s law books restrict women and lower castes further.'),
    tip=['ZERO \u00b7 PI', 'THE SPINNING EARTH'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('aryabhata'), 'ARYABHATA'), (Q_SHAPE('placevalue'), 'DECIMAL PLACE VALUE, WITH ZERO'),
          (Q_SHAPE('playtitle'), 'KALIDASA')],
    mains='Does the Gupta period deserve to be called a golden age?',
    mains_tags=('GIVE THE ACHIEVEMENTS', 'THEN ASK: GOLDEN FOR WHOM', 'WHOSE SOURCES SURVIVED'),
    facts=('Aryabhata, born 476 CE', 'Decimal place value and zero', 'Kalidasa\u2019s plays and poems'),
    next='HARSHAVARDHANA',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
