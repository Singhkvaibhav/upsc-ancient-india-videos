"""Ancient India, Simply Unearthed — Episode 6: Harappan Sites and Decline (English + Hindi).
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

EP = 6
CODE = 'Anc06'
TITLE = 'Harappan_Sites_and_Decline'
NAME = 'Harappan Sites and Decline'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_figurine(ctx, 960, 600, 3.4, a, t)

CFG = dict(
    ep=6, period=(-2600, -1300), dig=_dig,
    question='Why did a world this capable empty out its own cities?',
    tags=(('BRONZE · LOST-WAX CASTING', 150, 300),),
    sources=('trowel',),
    src_note='No text tells us what happened. The evidence for the end is the ground itself.',
    panels=[
        (P_SITES([('HARAPPA', -620, -300), ('MOHENJO-DARO', -300, -140), ('DHOLAVIRA', 20, -330),
                  ('LOTHAL', 330, -120), ('RAKHIGARHI', 640, -260)]), 'A REGION LARGER THAN MANY EMPIRES'),
        (P_TEXT('THREE PARTS, NOT TWO', 'RESERVOIRS CUT INTO ROCK', 'A SIGNBOARD WE CANNOT READ', size=44),
         'DHOLAVIRA'),
        (P_ROW(['Lothal: a basin and channel', 'Kalibangan: rows of fire altars',
                'Rakhigarhi: still being excavated']), 'EACH SITE ADDS SOMETHING'),
        (P_STACK([('DRAINS UNREPAIRED', 'clay'), ('LARGE HOUSES DIVIDED', 'sand'),
                  ('REUSED RUBBLE FOR BRICK', 'terra'), ('SEALS AND WRITING FADE', 'clay')]),
         'FROM ABOUT 1900 BCE'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Environment: rivers shifted or dried and the monsoon weakened, so farming and trade could not support cities.',
                right='Economy and society: trade with Mesopotamia declined and the arrangements holding cities together came apart.'),
    tip=['WATER CAME', 'WATER WENT'],
    prompt='PAUSE AND NAME THE SITE',
    quiz=[(Q_SHAPE('threecity'), 'DHOLAVIRA'), (Q_SHAPE('basin'), 'LOTHAL'), (Q_SHAPE('mounds'), 'RAKHIGARHI')],
    mains='Assess the theories advanced for the decline of the Harappan cities.',
    mains_tags=('ENVIRONMENT', 'ECONOMY', 'NOT INVASION'),
    facts=('No single cause is agreed', 'Cities thinned; villages carried on', 'Late Harappan to about 1300 BCE'),
    next='THE EARLY VEDIC PERIOD',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
