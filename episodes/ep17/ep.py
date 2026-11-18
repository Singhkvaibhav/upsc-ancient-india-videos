"""Ancient India, Simply Unearthed — Episode 17: Other Sects and Foreign Invasions.
Approved narration, word for word. No boundaries, no outline of India; the
north-west is a schematic board of rivers and ranges only.
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

EP = 17
CODE = 'Anc17'
TITLE = 'Other_Sects_and_Invasions'
NAME = 'Other Sects and Foreign Invasions'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_greekcoin(ctx, 960, 640, 2.6, a, t)

CFG = dict(
    ep=17, period=(-600, -300), dig=_dig,
    question='Why does this coin have a face on it?',
    tags=(('A COIN WITH A FACE ON IT', 150, 300),),
    sources=('leaf', 'stone', 'coin', 'staff'),
    src_note='The Greek accounts of Alexander were written by people who were not neutral.',
    panels=[
        (P_ROW(['Buddhism and Jainism lasted', 'But the field was crowded',
                'The Buddhist texts list rivals', 'And argue with them seriously'], size=26),
         'AN AGE OF ARGUMENT'),
        (P_TWO(['Associated with Makkhali Gosala', 'Niyati  ·  everything is determined',
                'Effort changes nothing', 'Lasted centuries, had patronage'],
               ['Also called Lokayata', 'Only what the senses verify',
                'No afterlife, no scriptural authority', 'Known mainly through opponents'],
               'THE AJIVIKAS', 'THE CHARVAKAS'), 'TWO SCHOOLS WORTH KNOWING'),
        (P_ROW(['Cyrus, then Darius the First', 'Parts of the north-west taken',
                'Trade with west Asia', 'The Aramaic script, and Kharoshthi from it',
                'Administrative ideas borrowed later'], size=22), 'THE PERSIANS CAME FIRST'),
        (P_ROW(['326 BCE  ·  defeated Porus at the Hydaspes',
                'Restored him, say the Greek sources',
                'Pushed east to the Beas',
                'His army refused to go further',
                'About two years in India'], size=23), 'ALEXANDER'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Limited: he held no territory long, Indian sources barely mention him, Magadha was untouched.',
                right='Significant: routes opened, Indo-Greek kingdoms followed, the north-west was left loose.'),
    tip=['PERSIANS FIRST · GREEKS SECOND', 'NEITHER STAYED'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('niyati'), 'THE AJIVIKAS'), (Q_SHAPE('senses'), 'THE CHARVAKAS'),
          (Q_SHAPE('riverhalt'), 'THE BEAS')],
    mains='What did the Persian and Greek contacts leave behind?',
    mains_tags=('SCRIPT AND TRADE', 'ADMINISTRATIVE BORROWING', 'THE INDO-GREEK KINGDOMS'),
    facts=('Ajivikas and Charvakas', 'Persian rule in the north-west', 'Alexander turned back at the Beas'),
    next='CHANDRAGUPTA MAURYA',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
