"""Ancient India, Simply Unearthed — Episode 23: Indo-Greeks, Shakas and Parthians.
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

EP = 23
CODE = 'Anc23'
TITLE = 'Indo_Greeks_Shakas_and_Parthians'
NAME = "Indo-Greeks, Shakas and Parthians"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_bicoin(ctx, 960, 640, 2.5, a, t)

CFG = dict(
    ep=23, period=(-200, 100), dig=_dig,
    question='Who wanted to be understood by two populations at once?',
    tags=(('TWO SCRIPTS, ONE COIN', 150, 300),),
    sources=('coin', 'stone', 'leaf'),
    src_note='Some of these rulers appear in no text at all, and are known only from their coins.',
    panels=[
        (P_ROW(['INDO-GREEKS  ·  from Bactria', 'SHAKAS  ·  the Scythians',
                'PARTHIANS  ·  the Pahlavas', 'KUSHANAS  ·  their own episode'], size=25),
         'FOUR WAVES, IN ORDER'),
        (P_ROW(['First coins in India with a ruler\u2019s portrait and name',
                'Which is how we date things by them',
                'Menander, called Milinda in Indian sources',
                'Questions the monk Nagasena in the Milindapanha'], size=24),
         'THE INDO-GREEKS'),
        (P_ROW(['The Western Kshatrapas, based at Ujjain',
                'Rudradaman the First',
                'His Junagadh inscription is in polished Sanskrit',
                'It records repairing the Sudarshana lake',
                'The same Mauryan dam, four centuries on'], size=22), 'THE SHAKAS'),
        (P_TWO(['Begins in 78 CE',
                'India adopted it as the national calendar in 1957'],
               ['Gandhara, in the north-west',
                'Hellenistic drapery on Buddhist subjects',
                'Mathura develops its own idiom',
                'Shown here as drapery and ornament only'],
               'THE SHAKA ERA', 'A NEW SCULPTURE'), 'WHAT THEY LEAVE BEHIND'),
    ],
    plaque=dict(kind='names', title='OLD NAME, NEW NAME', left='SHAKARI', right='ENEMY OF THE SHAKAS'),
    tip=['GREEKS \u00b7 SHAKAS', 'PARTHIANS \u00b7 KUSHANAS'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('dialogue'), 'THE MILINDAPANHA'), (Q_SHAPE('junagadh'), 'THE JUNAGADH INSCRIPTION'),
          (Q_SHAPE('era'), 'THE SHAKA ERA')],
    mains='What did the contacts from the north-west change?',
    mains_tags=('COINAGE', 'SANSKRIT IN INSCRIPTIONS', 'GANDHARA AND THE ROUTES'),
    facts=('Coins in two scripts', 'The Shaka era, 78 CE', 'Gandhara art begins'),
    next='THE KUSHANAS',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
