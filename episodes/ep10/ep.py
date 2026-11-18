"""Ancient India, Simply Unearthed — Episode 1: How We Know About Ancient India (English + Hindi).
Approved narration, word for word. No boundaries, no outline of India.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 300.0
core.TOTAL = TOTAL
from engine.core import W, H
from engine.stone import S, carve, poly, rrect, drain_section, pot, brick, house, platform, coursed
from engine.auto import (build, fx_for, P_TEXT, P_SITES, P_ROW, P_TWO, P_STACK, P_VILLAGE,
                         P_OBJ, P_MON, Q_SHAPE, Q_OBJ, GY)
from engine import museum
from text import EN, HI as _HI

EP = 10
CODE = 'Anc10'
TITLE = 'Varna_and_Ashrama'
NAME = 'Varna, Ashrama and Vedic Society'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_altar(ctx, 960, 640, 3.0, a, t)

CFG = dict(
    ep=10, period=(-1500, -500), dig=_dig,
    question='Where did this order come from, and how fixed was it to begin with?',
    tags=(('A FIRE ALTAR', 150, 300),),
    sources=('leaf', 'trowel'),
    src_note='Mostly texts — written by the people doing the arranging.',
    panels=[
        (P_STACK([('BRAHMANA · priest and teacher', 'sand'), ('KSHATRIYA · ruler and warrior', 'clay'),
                  ('VAISHYA · farmer, herder, trader', 'terra'), ('SHUDRA · serves the other three', 'clay')]),
         'VARNA · THE FOURFOLD ORDER'),
        (P_TEXT('EARLY: OCCUPATIONAL AND LOOSE', 'LATER: INCREASINGLY BY BIRTH', size=46),
         'THE DIRECTION OF TRAVEL'),
        (P_ROW(['brahmacharya: student', 'grihastha: householder', 'vanaprastha: withdrawal',
                'sannyasa: renunciation']), 'ASHRAMA · FOUR STAGES OF A LIFE'),
        (P_ROW(['Gargi', 'Maitreyi', 'Lopamudra'],
               obj=lambda c, x, y, s, a, t: Q_SHAPE('dialogue')(c, x, y - 30, a, t)), 'WOMEN NAMED IN THE TEXTS'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Varna began as a flexible, largely occupational order and hardened later.',
                right='Hierarchy and birth are present early; the texts were written by those it favoured.'),
    tip=['FOUR STAGES', 'FOUR AIMS'],
    quiz=[(Q_SHAPE('hymn10'), 'THE PURUSHA SUKTA'), (Q_SHAPE('path4'), 'THE ASHRAMAS'),
          (Q_SHAPE('dialogue'), 'MAITREYI')],
    mains='Trace the development of the varna order.',
    mains_tags=('LOOSE, THEN BY BIRTH', 'IDEAL VS PRACTICE', 'JATI IS A LATER THING'),
    facts=('Four varnas, four ashramas, four aims', 'Purusha Sukta is in the latest book of the Rigveda',
           "Women's position narrows in the later Vedic period"),
    next='MEGALITHIC CULTURES OF THE SOUTH',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
