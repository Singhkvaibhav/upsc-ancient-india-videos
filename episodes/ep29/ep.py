"""Ancient India, Simply Unearthed — Episode 29: Gupta Administration and Society.
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

EP = 29
CODE = 'Anc29'
TITLE = 'Gupta_Administration_and_Society'
NAME = "Gupta Administration and Society"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_copperplate(ctx, 960, 640, 2.4, a, t)

CFG = dict(
    ep=29, period=(320, 550), dig=_dig,
    question='What happens when a state gives its own revenue away?',
    tags=(('A DEED, IN METAL', 150, 300),),
    sources=('stone', 'leaf', 'staff'),
    src_note='Law books tell us what was supposed to happen, not what did.',
    panels=[
        (P_ROW(['BHUKTIS  ·  provinces, under uparikas',
                'VISHAYAS  ·  districts, under vishayapatis',
                'VILLAGES  ·  headmen and local assemblies',
                'Looser than the Mauryas: more left to local people'], size=24),
         'THE STRUCTURE'),
        (P_ROW(['Land granted to Brahmins, temples and monasteries',
                'And to officials, in place of salary',
                'The grant transferred a village\u2019s revenue',
                'Often the right to administer it too',
                'Sometimes in perpetuity, and free of tax'], size=22), 'THE CHANGE THAT MATTERS'),
        (P_TWO(['Travel was safe', 'Charitable rest houses and free hospitals',
                'Officials did not demand documents'],
               ['Chandalas lived outside the towns',
                'And struck wood to announce themselves',
                'So others could avoid them'],
               'WHAT FA-HIEN PRAISED', 'WHAT HE ALSO RECORDED'), 'BOTH ARE IN THE SAME ACCOUNT'),
        (P_ROW(['Guilds remained important in towns',
                'Villages ran much of their own affairs',
                'The law books set out a rigid social order',
                'Women and the lowest-ranked more restricted',
                'But law books are prescriptive, not descriptive'], size=22), 'WHAT ELSE THE SOURCES SHOW'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Land grants created an Indian feudalism: lords, dependent peasants and a weakened state.',
                right='The European parallel misleads: trade and towns did not simply collapse.'),
    tip=['LAND GRANTED', 'POWER DIVIDED'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('province'), 'THE BHUKTI'), (Q_SHAPE('plateandring'), 'A COPPER-PLATE GRANT'),
          (Q_SHAPE('pilgrim'), 'FA-HIEN')],
    mains='Did the Gupta period see the beginnings of Indian feudalism?',
    mains_tags=('THE LAND-GRANT EVIDENCE', 'BOTH POSITIONS', 'THEN COMMIT, WITH REASONS'),
    facts=('Provinces, districts, villages', 'Land grants in copper', 'Fa-Hien\u2019s account'),
    next='GUPTA SCIENCE AND LITERATURE',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
