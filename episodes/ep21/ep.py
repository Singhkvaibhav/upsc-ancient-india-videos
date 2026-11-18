"""Ancient India, Simply Unearthed — Episode 21: Mauryan Administration and Decline.
Approved narration, word for word. No boundaries and no shaded empire.
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

EP = 21
CODE = 'Anc21'
TITLE = 'Mauryan_Administration_and_Decline'
NAME = 'Mauryan Administration and Decline'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_pillarsection(ctx, 960, 620, 2.4, a, t)

CFG = dict(
    ep=21, period=(-321, -185), dig=_dig,
    question='How do you actually run the first empire in the subcontinent?',
    tags=(('MAURYAN POLISH', 150, 300),),
    sources=('leaf', 'staff', 'stone', 'trowel'),
    src_note='The Indica survives only as fragments quoted by later Greek writers, which is a real limitation.',
    panels=[
        (P_ROW(['PATALIPUTRA  ·  the capital',
                'TAXILA  ·  the north-west', 'UJJAIN  ·  the west',
                'SUVARNAGIRI  ·  the south', 'TOSALI  ·  the east',
                'Below them: rajukas, pradeshikas, yuktas'], size=22), 'THE SHAPE OF IT'),
        (P_ROW(['A great city on the river', 'A timber palisade, towers and gates',
                'Excavation has found the palisade',
                'Committees for crafts, foreigners, trade, tax',
                'The structure is plausible; the detail is secondhand'], size=22),
         'MEGASTHENES ON PATALIPUTRA'),
        (P_ROW(['Land revenue, a share of the produce',
                'Collected by a salaried bureaucracy',
                'Mines, forests and workshops run by the state',
                'The Sudarshana lake, built under the Mauryas',
                'A standing army paid out of all this'], size=22), 'THE MONEY'),
        (P_ROW(['Ashoka dies about 232 BCE', 'The later Mauryas are barely known',
                'Brihadratha killed about 185 BCE',
                'By his commander-in-chief, Pushyamitra Shunga',
                'About a hundred and forty years in all'], size=22), 'THE END'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Fiscal and administrative: a huge salaried bureaucracy outran the revenue, and the provinces had no strength of their own.',
                right='Political: weak successors, revolts and pressure in the north-west. Pacifism is no longer accepted as the cause.'),
    tip=['FOUR PROVINCES', 'ONE CAPITAL'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('rajuka'), 'THE RAJUKAS'), (Q_SHAPE('lake'), 'THE SUDARSHANA LAKE'),
          (Q_SHAPE('fragments'), 'THE INDICA')],
    mains='Why did the Mauryan empire decline?',
    mains_tags=('ADMINISTRATIVE AND FISCAL', 'POLITICAL', 'WHY PACIFISM IS REJECTED'),
    facts=('Four provincial capitals', 'The Indica survives in fragments', 'Ended about 185 BCE'),
    next='AFTER THE MAURYAS',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
