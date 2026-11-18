"""Ancient India, Simply Unearthed — Episode 19: Ashoka and Dhamma.
Approved narration, word for word.

The State Emblem of India (the Sarnath lion capital) is NEVER drawn: this
episode's capital is the Rampurva bull. Ashoka is a generic carved figure with
a nameplate, never a likeness. The Kalinga war is shown through an edict tablet
and a map pin, never through battle or bodies.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 300.0
core.TOTAL = TOTAL
from engine.core import W, H
from engine.stone import S, carve, poly, rrect
from engine.auto import (build, fx_for, P_TEXT, P_SITES, P_ROW, P_TWO, P_STACK, P_VILLAGE,
                         P_OBJ, P_MON, Q_SHAPE, Q_OBJ, GY)
from engine import museum
from text import EN, HI as _HI

EP = 19
CODE = 'Anc19'
TITLE = 'Ashoka_and_Dhamma'
NAME = 'Ashoka and Dhamma'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_bullcapital(ctx, 960, 650, 2.4, a, t)

CFG = dict(
    ep=19, period=(-268, -232), dig=_dig,
    question='What did a king carve into rock, and why?',
    tags=(('RAMPURVA · A PILLAR CAPITAL', 150, 300),),
    sources=('stone', 'leaf', 'staff'),
    src_note='When the edicts and the tradition disagree, historians go with the edicts.',
    panels=[
        (P_ROW(['Came to the throne about 268 BCE', 'Grandson of Chandragupta',
                'Tradition says the succession was contested',
                'The edicts say nothing about it'], size=26), 'THE ACCESSION'),
        (P_ROW(['About 261 BCE  ·  Kalinga',
                'His own thirteenth rock edict gives the figures',
                'A hundred and fifty thousand deported',
                'A hundred thousand killed',
                'And then: remorse, carved into rock'], size=23), 'THE HINGE OF THE REIGN'),
        (P_ROW(['Obedience to parents, respect for teachers',
                'Generosity to Brahmins and ascetics alike',
                'Kindness to servants, truthfulness, restraint',
                'Non-injury to living beings',
                'Tolerance: disparaging another sect harms your own'], size=22),
         'WHAT HE MEANS BY DHAMMA'),
        (P_ROW(['Dhamma-mahamatras appointed', 'Dhamma-yatras replace hunting tours',
                'Trees planted, wells dug, rest houses built',
                'Medical treatment for people and animals',
                'Missions sent abroad'], size=22), 'AN ADMINISTRATION FOR IT'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Dhamma is his personal Buddhism, made public: he says he is a lay Buddhist, and the content overlaps.',
                right='Dhamma is a deliberately non-sectarian civic ethic; the public edicts never mention nirvana or the Eightfold Path.'),
    tip=['ONE WAR,', 'THEN NONE'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('kalinga'), 'KALINGA'), (Q_SHAPE('mahamatra'), 'THE DHAMMA-MAHAMATRAS'),
          (Q_SHAPE('roadworks'), 'DHAMMA-YATRAS')],
    mains='What was Ashoka’s dhamma?',
    mains_tags=('QUOTE THE EDICTS', 'GIVE BOTH READINGS', 'NOTE WHAT THEY LEAVE OUT'),
    facts=('Kalinga, about 261 BCE', 'Dhamma, in his own words', 'Dhamma-mahamatras appointed'),
    next='ASHOKA’S EDICTS',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
