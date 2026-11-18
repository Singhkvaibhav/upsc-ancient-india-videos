"""Ancient India, Simply Unearthed — Episode 14: Buddhism, Life and Teachings (English + Hindi).
Approved narration, word for word.

The Buddha is NEVER drawn as a face or a figure anywhere in this episode. He is
shown the way the earliest Indian art showed him: an empty throne, the Bodhi
tree, footprints, a wheel, a stupa. See CLAUDE.md rule 3.
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

EP = 14
CODE = 'Anc14'
TITLE = 'Buddhism_Life_and_Teachings'
NAME = 'Buddhism: Life and Teachings'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_bodhi(ctx, 960, 620, 2.5, a, t)

CFG = dict(
    ep=14, period=(-563, -483), dig=_dig,
    question='Why is the subject of this carving not in it?',
    tags=(('HE IS SHOWN BY ABSENCE', 150, 300),),
    sources=('leaf', 'trowel'),
    src_note='The canon was written down centuries later; historians separate the earliest layer from what grew around it.',
    panels=[
        (P_SITES([('LUMBINI', -340, -340), ('BODH GAYA', 150, -120), ('SARNATH', -120, -210),
                  ('KUSHINAGAR', -40, -380), ('RAJAGRIHA', 330, -150)]), 'THE LIFE, PLACE BY PLACE'),
        (P_ROW(['ONE  ·  there is suffering', 'TWO  ·  its cause is craving',
                'THREE  ·  so it can end', 'FOUR  ·  there is a path'], size=26),
         'THE FOUR NOBLE TRUTHS'),
        (P_OBJ(lambda c, x, y, s, a, t: museum.ex_bodhi(c, x, y, s*0.9, a, t), s=1.6,
               label='WISDOM · CONDUCT · DISCIPLINE'), 'THE EIGHTFOLD PATH'),
        (P_TWO(['Prakrit, the spoken language', 'Not Sanskrit, which few followed'],
               ['Open regardless of birth', 'An institution to carry the teaching'],
               'THE LANGUAGE', 'THE SANGHA'), 'WHY IT SPREAD'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='The traditional dating places his life at about 563 to 483 BCE, and textbooks use it.',
                right='Much recent scholarship argues for a later date, with his death closer to 400 BCE.'),
    tip=['FOUR TRUTHS · EIGHT STEPS', 'THE MIDDLE WAY'],
    prompt='PAUSE AND NAME THE PLACE',
    quiz=[(Q_SHAPE('bodhitree'), 'BODH GAYA'), (Q_SHAPE('wheelpark'), 'SARNATH'),
          (Q_SHAPE('stupa'), 'KUSHINAGAR')],
    mains='Why did Buddhism spread so widely in this period?',
    mains_tags=('A SPOKEN LANGUAGE', 'AN OPEN ORDER', 'MERCHANTS AND KINGS'),
    facts=('Four Noble Truths', 'The Eightfold Path', 'Taught in Prakrit, not Sanskrit'),
    next='COUNCILS, SCHOOLS AND SPREAD',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
