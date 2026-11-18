"""Ancient India, Simply Unearthed — Episode 34: The Tripartite Struggle.
Approved narration, word for word. No boundaries, no outline of India; no
empire is drawn as shaded territory.\n\nKailasa is drawn as architecture only, with the sanctum left as a dark,\nempty opening.
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

EP = 34
CODE = 'Anc34'
TITLE = 'The_Tripartite_Struggle'
NAME = "The Tripartite Struggle"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_kailasa(ctx, 960, 640, 2.3, a, t)

CFG = dict(
    ep=34, period=(750, 1000), dig=_dig,
    question='How do you build a temple by taking a hillside away?',
    tags=(('CUT DOWNWARD, FROM THE TOP', 150, 300),),
    sources=('stone', 'staff', 'leaf'),
    src_note='Copper plates and temple inscriptions from all three powers are the backbone here.',
    panels=[
        (P_ROW(['PALAS  ·  the east, Bengal and Bihar',
                'GURJARA-PRATIHARAS  ·  the west',
                'RASHTRAKUTAS  ·  the Deccan',
                'All three tried to take Kannauj',
                'Hold the city and you were the pre-eminent power'], size=22),
         'THREE POWERS, ONE CITY'),
        (P_ROW(['PALAS  ·  endowed Nalanda, founded Vikramashila',
                'Buddhism\u2019s last great royal patrons in India',
                'PRATIHARAS  ·  held the west, resisted expansion beyond Sindh',
                'RASHTRAKUTAS  ·  most often successful in the north'], size=23),
         'EACH IS MORE THAN THE FIGHTING'),
        (P_ROW(['Cut downward out of the hillside in the eighth century',
                'Under Krishna the First',
                'Tower, hall, gateway, courtyard  ·  all excavated',
                'Ellora also holds Buddhist, Jain and Hindu caves',
                'Three traditions patronised at one site'], size=22), 'KAILASA AT ELLORA'),
        (P_ROW(['Nobody wins; Kannauj changes hands repeatedly',
                'All three weaken by the tenth century',
                'Their own feudatories become independent kingdoms',
                'Rajput houses, Chandelas, Paramaras, Chalukyas of Kalyani',
                'The outcome is a map of regional states'], size=22), 'HOW IT ENDS'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='The struggle exhausted all three and left the north fragmented and vulnerable.',
                right='Each declined for its own reasons; these were culturally rich states, not merely failing ones.'),
    tip=['PALA \u00b7 PRATIHARA \u00b7 RASHTRAKUTA', 'ALL FOR KANNAUJ'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('citypin'), 'KANNAUJ'), (Q_SHAPE('monastery'), 'VIKRAMASHILA'),
          (Q_SHAPE('cutpit'), 'KAILASA')],
    mains='What were the consequences of the tripartite struggle?',
    mains_tags=('THE CONVENTIONAL ANSWER', 'THEN COMPLICATE IT', 'REGIONAL STATES FORMED'),
    facts=('Three powers, one city', 'Palas endowed Nalanda and Vikramashila',
           'Kailasa cut from the rock at Ellora'),
    next='EARLY MEDIEVAL KINGDOMS',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
