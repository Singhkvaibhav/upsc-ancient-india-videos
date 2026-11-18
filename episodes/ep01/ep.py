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

EP = 1
CODE = 'Anc01'
TITLE = 'How_We_Know'
NAME = 'How We Know About Ancient India'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_seal(ctx, 700, 620, 1.9, a, t)
    Q = Q_SHAPE('coin'); Q(ctx, 1320, 620, a, t)

CFG = dict(
    ep=1, period=(-2600, 650), dig=_dig,
    question='How does anyone know what happened three thousand years ago?',
    tags=(('PUNCH-MARKED COIN', 150, 300), ('PALM LEAF', 150, 364)),
    sources=('trowel', 'leaf', 'stone', 'coin', 'staff'),
    src_note='Five kinds of evidence, and every one of them has a limit.',
    panels=[
        (P_STACK([('POTS AND TOOLS', 'sand'), ('HOUSES AND POST-HOLES', 'clay'),
                  ('BONES AND SEEDS', 'terra')]), 'WHAT THE GROUND KEEPS'),
        (P_ROW(['Vedas', 'Epics', 'Buddhist and Jain texts', 'Sanskrit and Tamil literature']), 'WHAT PEOPLE WROTE'),
        (P_OBJ(lambda c, x, y, s, a, t: Q_SHAPE('edict')(c, x, y, a, t), s=1.5,
               label='CARVED AT THE TIME, MEANT TO BE READ'), 'INSCRIPTIONS · PRINSEP, 1837'),
        (P_ROW(['Megasthenes', 'Fa-Hien', 'Hiuen Tsang'],
               obj=lambda c, x, y, s, a, t: Q_SHAPE('traveller')(c, x, y - 40, a, t)), 'TRAVELLERS FROM OUTSIDE'),
    ],
    plaque=dict(kind='names', left='PATALIPUTRA', right='PATNA'),
    tip=['DIG · READ · CARVE', 'COIN · VISIT'],
    prompt='PAUSE AND NAME THE SOURCE',
    quiz=[(Q_SHAPE('edict'), 'AN INSCRIPTION'), (Q_SHAPE('coin'), 'A PUNCH-MARKED COIN'),
          (Q_SHAPE('traveller'), "A TRAVELLER'S ACCOUNT")],
    mains='How far can literary sources be relied on for early Indian history?',
    mains_tags=('THE INSIGHT', 'THE DATING PROBLEM', 'READ WITH BOTH'),
    facts=('Five kinds of evidence', 'Prinsep read Brahmi in 1837', 'Every date here is a best reading'),
    next='STONE AGE INDIA',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
