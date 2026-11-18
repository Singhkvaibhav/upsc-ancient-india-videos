"""Ancient India, Simply Unearthed — Episode 39: Ancient Universities.
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

EP = 39
CODE = 'Anc39'
TITLE = 'Ancient_Universities'
NAME = "Ancient Universities"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_nalandaseal(ctx, 960, 640, 2.5, a, t)

CFG = dict(
    ep=39, period=(-600, 1200), dig=_dig,
    question='What does it mean for an institution to have its own seal?',
    tags=(('AN INSTITUTION WITH ITS OWN SEAL', 150, 300),),
    sources=('staff', 'stone', 'trowel', 'leaf'),
    src_note='Two Chinese pilgrims lived and studied at Nalanda and described it from the inside.',
    panels=[
        (P_SITES([('TAXILA', -620, -360), ('NALANDA', 430, -90), ('VALLABHI', -430, 30),
                  ('VIKRAMASHILA', 500, -150)]), 'FOUR TO KNOW, IN ORDER'),
        (P_TWO(['A city where distinguished teachers each took students',
                'Medicine, archery, law, the Vedas',
                'Students attached to a teacher, not enrolled'],
               ['A single endowed complex',
                'Buildings, a curriculum, residence',
                'And a governing body'],
               'TAXILA', 'NALANDA'), 'NOT THE SAME KIND OF PLACE'),
        (P_ROW(['Monastery blocks in a row, temples facing them',
                'Each block around a courtyard, with cells',
                'Endowed by Gupta rulers, then the Palas',
                'One copper plate records a grant from a Sumatran king',
                'A library large enough to burn for a long time'], size=22), 'NALANDA\u2019S PLAN'),
        (P_ROW(['An entrance examination at the gate',
                'That turned away most applicants',
                'I-Tsing describes the daily routine and the rules',
                'Logic, grammar, medicine, mathematics',
                'Destroyed in the late twelfth or early thirteenth century'], size=22),
         'WHAT THE PILGRIMS RECORD'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Taxila was a university: a renowned centre drawing students from across the subcontinent.',
                right='Taxila was a city of individual teachers; the word imposes a later institutional idea.'),
    tip=['TAXILA \u00b7 NALANDA', 'VALLABHI \u00b7 VIKRAMASHILA'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('gatequestion'), 'HIUEN TSANG'), (Q_SHAPE('monastery'), 'VIKRAMASHILA'),
          (Q_SHAPE('anthologies'), 'VALLABHI')],
    mains='Describe the ancient Indian centres of learning.',
    mains_tags=('TAXILA\u2019S PATTERN', 'NALANDA\u2019S INSTITUTION', 'WHAT WAS ACTUALLY TAUGHT'),
    facts=('Nalanda, endowed by Guptas and Palas', 'Hiuen Tsang and I-Tsing studied there',
           'Libraries and an entrance examination'),
    next='FOREIGN TRAVELLERS',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
