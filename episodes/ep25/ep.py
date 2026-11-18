"""Ancient India, Simply Unearthed — Episode 25: The Sangam Kingdoms.
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

EP = 25
CODE = 'Anc25'
TITLE = 'The_Sangam_Kingdoms'
NAME = "The Sangam Kingdoms"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_herostone(ctx, 960, 640, 2.5, a, t)

CFG = dict(
    ep=25, period=(-300, 300), dig=_dig,
    question='Who was this stone set up for?',
    tags=(('A HERO STONE', 150, 300),),
    sources=('leaf', 'stone', 'trowel', 'staff'),
    src_note='Mediterranean accounts describe these ports in detail, because their merchants used them.',
    panels=[
        (P_ROW(['CHERA  ·  the bow  ·  west, on the Arabian Sea',
                'CHOLA  ·  the tiger  ·  Uraiyur, and the port of Puhar',
                'PANDYA  ·  the fish  ·  Madurai, and the pearl port Korkai'], size=25),
         'THE THREE CROWNED KINGS'),
        (P_ROW(['Pepper, pearls, ivory, fine cotton, stones go west',
                'Roman gold and wine come east',
                'Puhar and Muziris in poems and in Roman sources',
                'Arikamedu: Mediterranean pottery and glass in the ground'], size=23),
         'TRADING STATES'),
        (P_ROW(['KURINJI  ·  hills', 'MULLAI  ·  forest', 'MARUDAM  ·  farmland',
                'NEIDAL  ·  coast', 'PALAI  ·  wasteland'], size=24),
         'THE FIVE LANDSCAPES'),
        (P_ROW(['Kings and smaller chieftains', 'Bards travelling between patrons',
                'Cattle raids, and the stones that mark them', 'Markets and ports',
                'Poets name generous patrons, and mean ones'], size=22), 'THE SOCIETY'),
    ],
    plaque=dict(kind='names', title='OLD NAME, NEW NAME', left='MUZIRIS', right='NEAR KODUNGALLUR'),
    tip=['CHERA \u00b7 CHOLA \u00b7 PANDYA', 'BOW \u00b7 TIGER \u00b7 FISH'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('bow'), 'THE CHERAS'), (Q_SHAPE('fishpearl'), 'THE PANDYAS'),
          (Q_SHAPE('harbour'), 'ARIKAMEDU')],
    mains='What does Sangam literature tell us about early south Indian society?',
    mains_tags=('THE FIVE LANDSCAPES', 'PATRONAGE AND TRADE', 'POETRY IDEALISES'),
    facts=('Three crowned kings', 'Bow, tiger and fish', 'Ports trading with Rome'),
    next='SANGAM LITERATURE AND SOCIETY',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
