"""Ancient India, Simply Unearthed — Episode 28: The Rise of the Guptas.
Approved narration, word for word. No boundaries, no outline of India; no
empire is drawn as shaded territory.
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

EP = 28
CODE = 'Anc28'
TITLE = 'The_Rise_of_the_Guptas'
NAME = "The Rise of the Guptas"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_guptacoin(ctx, 960, 640, 2.5, a, t)

CFG = dict(
    ep=28, period=(320, 415), dig=_dig,
    question='Why does a coin suddenly look like a statement about a king?',
    tags=(('STRUCK, NOT TRADED FOR', 150, 300),),
    sources=('stone', 'coin', 'staff'),
    src_note='One pillar inscription carries most of what we know about Samudragupta.',
    panels=[
        (P_ROW(['Shri Gupta and Ghatotkacha: little more than names',
                'Chandragupta the First, from about 319 or 320 CE',
                'Married Kumaradevi, a Lichchhavi princess',
                'The Gupta era counts from his accession'], size=24), 'THE DYNASTY BEGINS SMALL'),
        (P_ROW(['Kings of the north uprooted', 'Kings of the south defeated, then reinstated',
                'Frontier states made tributary', 'Distant powers sent envoys'], size=25),
         'THE ALLAHABAD PRASHASTI'),
        (P_TWO(['A coin type shows him playing the vina',
                'A ruler advertising himself as a musician'],
               ['He performed the ashvamedha',
                'An old claim to paramountcy', 'Fallen out of use, and revived'],
               'THE MUSICIAN', 'THE HORSE SACRIFICE'), 'TWO DETAILS ABOUT SAMUDRAGUPTA'),
        (P_ROW(['Took the title Vikramaditya',
                'Defeated the Western Kshatrapas',
                'Which gave the Guptas the western ports',
                'Silver coinage for the western provinces',
                'The navaratna tradition is later, not contemporary'], size=22),
         'CHANDRAGUPTA THE SECOND'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='The southern campaign was a real military progress: kings were defeated before being reinstated.',
                right='A prashasti exists to glorify; the southern claims may describe display, not lasting control.'),
    tip=['CHANDRA \u00b7 SAMUDRA', 'VIKRAMADITYA'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('prashasti'), 'THE ALLAHABAD PRASHASTI'), (Q_SHAPE('vina'), 'THE VINA'),
          (Q_SHAPE('title'), 'VIKRAMADITYA')],
    mains='How reliable are prashastis as historical sources?',
    mains_tags=('WHAT THEY ARE FOR', 'WHAT THEY GIVE YOU', 'WHAT THEY WILL NOT'),
    facts=('Gupta era from 319 or 320 CE', 'The Allahabad pillar inscription',
           'Gold coinage of unusual quality'),
    next='GUPTA ADMINISTRATION AND SOCIETY',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
