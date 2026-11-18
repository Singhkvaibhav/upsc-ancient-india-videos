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

EP = 7
CODE = 'Anc07'
TITLE = 'Early_Vedic_Period'
NAME = 'The Early Vedic Period'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_leaf(ctx, 960, 620, 3.0, a, t)

CFG = dict(
    ep=7, period=(-1500, -1000), dig=_dig,
    question='How do we know so much about what these people thought, and so little about where they lived?',
    tags=(('ALMOST NOTHING SURVIVES', 150, 300),),
    sources=('leaf', 'trowel'),
    src_note='Texts do most of the work here, and archaeology only checks them.',
    panels=[
        (P_TEXT('MORE THAN A THOUSAND HYMNS', 'TEN BOOKS', 'CARRIED BY MEMORY FOR CENTURIES', size=46), 'THE RIGVEDA'),
        (P_SITES([('SINDHU', -560, -240), ('SARASWATI', -140, -330), ('GANGA: ONCE ONLY', 480, -130)]),
         'SAPTA SINDHU · THE LAND OF SEVEN RIVERS'),
        (P_TEXT('WEALTH MEASURED IN CATTLE', 'THE WORD FOR BATTLE MEANS', 'A SEARCH FOR COWS', size=44), 'A PASTORAL ECONOMY'),
        (P_ROW(['jana: the tribe', 'raja: a chief, not a king', 'sabha: the smaller assembly',
                'samiti: the larger assembly']), 'TRIBAL, NOT ROYAL'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Migration: language and texts point to Indo-Aryan speakers arriving from Central Asia.',
                right='Indigenous development: the material culture shows continuity, with no evidence of invasion.'),
    tip=['COWS, NOT CROPS', 'CHIEF, NOT KING'],
    quiz=[(Q_SHAPE('rigveda'), 'THE RIGVEDA'), (Q_SHAPE('assembly'), 'THE SABHA AND THE SAMITI'),
          (Q_SHAPE('rivers'), 'SAPTA SINDHU')],
    mains='Describe the polity of the Early Vedic period.',
    mains_tags=('NO TERRITORY', 'NO REGULAR TAX', 'ASSEMBLIES MATTERED'),
    facts=('The Rigveda is the oldest text in India', 'Wealth measured in cattle', 'Sabha and samiti'),
    next='THE LATER VEDIC PERIOD',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
