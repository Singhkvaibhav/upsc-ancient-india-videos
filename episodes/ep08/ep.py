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

EP = 8
CODE = 'Anc08'
TITLE = 'Later_Vedic_Period'
NAME = 'The Later Vedic Period'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_pgw(ctx, 960, 640, 3.0, a, t)

CFG = dict(
    ep=8, period=(-1000, -600), dig=_dig,
    question='How does a chief become a king?',
    tags=(('PAINTED GREY WARE', 150, 300),),
    sources=('leaf', 'trowel'),
    src_note='Two sources that talk to each other: the texts, and the pots and iron.',
    panels=[
        (P_OBJ(lambda c, x, y, s, a, t: Q_SHAPE('ironplough')(c, x, y, a, t), s=1.5,
               label='AXES CLEAR FOREST · PLOUGHS BREAK HEAVY SOIL'), 'IRON · THE DARK METAL'),
        (P_SITES([('THE DOAB', -260, -250), ('GANGA', 240, -120), ('YAMUNA', 540, -300)]), 'THE MOVE EAST'),
        (P_ROW(['rajasuya: consecration', 'ashvamedha: the horse sacrifice', 'vajapeya: the chariot race']),
         'BIG SACRIFICES MAKE BIG KINGS'),
        (P_STACK([('SAMITI MENTIONED LESS', 'clay'), ('SABHA NARROWS TO NOTABLES', 'sand'),
                  ('JANA HARDENS INTO JANAPADA', 'terra')]), 'THE ASSEMBLIES FADE'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Painted Grey Ware marks Later Vedic settlement: the spread matches the texts closely.',
                right='A pottery style is not a people: the fit is approximate and should not be pressed.'),
    tip=['IRON EAST', 'PLOUGH AND SACRIFICE'],
    quiz=[(Q_SHAPE('pgw'), 'PAINTED GREY WARE'), (Q_SHAPE('horse'), 'THE ASHVAMEDHA'),
          (Q_SHAPE('ironplough'), 'IRON')],
    mains='How did iron change early Indian society?',
    mains_tags=('FOREST CLEARED', 'SURPLUS AND TERRITORY', 'TAX AND KINGSHIP'),
    facts=('Iron and the move east', 'Big sacrifices make big kings', 'Assemblies fade'),
    next='VEDIC LITERATURE',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
