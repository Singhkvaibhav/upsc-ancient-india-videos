"""Ancient India, Simply Unearthed — Episode 18: Chandragupta Maurya and the Arthashastra.
Approved narration, word for word. No boundaries, no outline of India; the empire
is never drawn as shaded territory.
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

EP = 18
CODE = 'Anc18'
TITLE = 'Chandragupta_and_the_Arthashastra'
NAME = 'Chandragupta Maurya and the Arthashastra'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_arthashastra(ctx, 960, 640, 2.4, a, t)

CFG = dict(
    ep=18, period=(-321, -297), dig=_dig,
    question='Who sat down and wrote a manual for running a state?',
    tags=(('A MANUAL FOR RUNNING A STATE', 150, 300),),
    sources=('leaf', 'staff', 'stone'),
    src_note='These sources disagree with each other more than you might expect.',
    panels=[
        (P_ROW(['About 321 BCE  ·  the Nandas overthrown',
                'Kautilya, also Chanakya or Vishnugupta',
                'A Brahmin teacher from Taxila, then minister',
                'How much is history is debated  ·  the empire is not'], size=25),
         'THE FOUNDING'),
        (P_SITES([('PATALIPUTRA', 420, -170), ('TAXILA', -600, -360), ('UJJAIN', -230, -60),
                  ('THE DECCAN', -60, 190), ('THE NORTH-WEST', -520, -250)]), 'IT EXPANDED FAST'),
        (P_ROW(['About 305 BCE  ·  a settlement with Seleucus Nicator',
                'Territory ceded in the north-west',
                'Five hundred war elephants given',
                'Megasthenes sent as ambassador to Pataliputra'], size=25),
         'THE SETTLEMENT WITH SELEUCUS'),
        (P_ROW(['KING', 'MINISTERS', 'TERRITORY AND PEOPLE', 'FORT', 'TREASURY', 'ARMY', 'ALLY'],
               size=22), 'SAPTANGA  ·  THE SEVEN LIMBS'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Largely Kautilya’s own work, from the Mauryan period, and usable as evidence for it.',
                right='A compilation that reached its present form several centuries later.'),
    tip=['SEVEN LIMBS', 'OF THE STATE'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('saptanga'), 'THE SAPTANGA'), (Q_SHAPE('mandala'), 'THE MANDALA THEORY'),
          (Q_SHAPE('traveller'), 'MEGASTHENES')],
    mains='How far can the Arthashastra be used as evidence for Mauryan administration?',
    mains_tags=('A QUESTION OF DATING', 'AND OF GENRE', 'THEORY BEFORE PRACTICE'),
    facts=('Founded about 321 BCE', 'Kautilya’s Arthashastra', 'A treaty with Seleucus'),
    next='ASHOKA AND DHAMMA',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
