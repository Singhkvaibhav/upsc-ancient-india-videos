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

EP = 11
CODE = 'Anc11'
TITLE = 'Megalithic_South'
NAME = 'Megalithic Cultures of the South'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_megalith(ctx, 960, 640, 2.4, a, t)

CFG = dict(
    ep=11, period=(-1200, -300), dig=_dig,
    question='Who built these, and what happened to them?',
    tags=(('A BURIAL, NOT A HOUSE', 150, 300),),
    sources=('trowel',),
    src_note='Only the ground, and mostly graves — a particular kind of evidence with a particular bias.',
    panels=[
        (P_SITES([('BRAHMAGIRI', -600, -260), ('MASKI', -280, -150), ('HALLUR', 40, -320),
                  ('ADICHANALLUR', 360, -140), ('NAGARJUNAKONDA', 650, -280)]), 'THOUSANDS OF SITES'),
        (P_ROW(['cist: a box of slabs, sunk', 'dolmen: slabs under a capstone',
                'menhir: one tall stone', 'cairn circle: a ring of stones', 'urn burial: remains in a pot'],
               size=22), 'FIVE KINDS OF BURIAL'),
        (P_ROW(['Iron blades and arrowheads', 'Horse fittings', 'Black and Red Ware']), 'WHAT WENT INTO THE GRAVES'),
        (P_TEXT('IRON APPEARS EARLY IN THE SOUTH', 'AS EARLY AS ANYWHERE', 'IN THE SUBCONTINENT', size=44),
         'WHY IT MATTERS'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Continuity: the megalith builders are the direct predecessors of Sangam-age society.',
                right='Caution: the gap in evidence is real, and the link is inferred rather than demonstrated.'),
    tip=['STONE OVER THE DEAD', 'IRON BESIDE THEM'],
    prompt='PAUSE AND NAME THE BURIAL',
    quiz=[(Q_SHAPE('dolmen'), 'A DOLMEN'), (Q_SHAPE('menhir'), 'A MENHIR'), (Q_SHAPE('urn'), 'AN URN BURIAL')],
    mains='What do megalithic burials tell us about society in the early south?',
    mains_tags=('IRON IN QUANTITY', 'DIFFERENCES IN STATUS', 'A SHARED PRACTICE'),
    facts=('Iron appears early in the south', 'Burials of several kinds', 'Black and Red Ware'),
    next='THE MAHAJANAPADAS',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
