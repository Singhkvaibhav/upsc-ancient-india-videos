"""Ancient India, Simply Unearthed — Episode 32: The Vakatakas and the Deccan.
Approved narration, word for word. No boundaries, no outline of India; no
empire is drawn as shaded territory.\n\nThe Ajanta paintings are shown through ornament and borders only: no\ndeity or revered figure is drawn, and sanctum openings stay dark and empty.
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

EP = 32
CODE = 'Anc32'
TITLE = 'The_Vakatakas_and_the_Deccan'
NAME = "The Vakatakas and the Deccan"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_painted(ctx, 960, 640, 2.5, a, t)

CFG = dict(
    ep=32, period=(250, 550), dig=_dig,
    question='Why does almost all surviving ancient Indian painting sit inside caves?',
    tags=(('PIGMENT ON PLASTER', 150, 300),),
    sources=('stone', 'trowel', 'leaf'),
    src_note='The Vakatakas are known mostly from what they left, not from literature about them.',
    panels=[
        (P_SITES([('NANDIVARDHANA', -180, -130), ('VATSAGULMA', -330, 60), ('AJANTA', -420, -40),
                  ('ELLORA', -480, -150)]), 'THE VAKATAKAS IN THE DECCAN'),
        (P_ROW(['Chandragupta the Second married his daughter to a Vakataka ruler',
                'Prabhavatigupta governed as regent for some two decades',
                'Her own inscriptions cite her Gupta descent',
                'A friendly power on the Gupta southern flank'], size=23), 'THE LINK TO THE GUPTAS'),
        (P_ROW(['A horseshoe cliff above a river',
                'The earlier caves: Satavahana centuries',
                'The later, larger group: fifth century, Vakataka',
                'Chaitya halls and viharas',
                'Cut from the top down, so no corrections were possible'], size=22), 'AJANTA'),
        (P_ROW(['Pigment on a prepared plaster ground',
                'Related to fresco, but not identical',
                'Mostly Jataka stories, with court scenes and ceilings',
                'Shown here as ornament and borders',
                'The best surviving body of ancient Indian painting'], size=22), 'THE PAINTINGS'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='A short, intense phase of royal and ministerial patronage under one Vakataka ruler.',
                right='A longer process with many donors, as the inscriptions inside the caves suggest.'),
    tip=['PAINTED,', 'NOT CARVED'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('regent'), 'PRABHAVATIGUPTA'), (Q_SHAPE('cliffcaves'), 'AJANTA'),
          (Q_SHAPE('plasterlayers'), 'THE JATAKAS')],
    mains='What do the Deccan caves tell us about patronage?',
    mains_tags=('KINGS, YES', 'BUT ALSO MINISTERS AND MONKS', 'AND MERCHANTS'),
    facts=('Vakatakas in the Deccan', 'Prabhavatigupta\u2019s regency', 'Ajanta\u2019s later caves'),
    next='CHALUKYAS OF BADAMI AND PALLAVAS',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
