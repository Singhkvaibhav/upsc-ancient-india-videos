"""Ancient India, Simply Unearthed — Episode 37: The Rajput Kingdoms.
Approved narration, word for word. No boundaries, no outline of India; no
kingdom is drawn as shaded territory.\n\nRajput origins are given as a live dispute with each position attributed.\nNo community is described as naturally martial.
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

EP = 37
CODE = 'Anc37'
TITLE = 'The_Rajput_Kingdoms'
NAME = "The Rajput Kingdoms"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_hillfort(ctx, 960, 640, 2.5, a, t)

CFG = dict(
    ep=37, period=(750, 1200), dig=_dig,
    question='Why build where the rock already is?',
    tags=(('BUILT WHERE THE ROCK ALREADY WAS', 150, 300),),
    sources=('stone', 'leaf', 'trowel'),
    src_note='Bardic poems were composed long after the events, and must be handled carefully.',
    panels=[
        (P_ROW(['CHAHAMANAS  ·  Ajmer and Delhi',
                'PARAMARAS  ·  Dhar and Malwa',
                'CHANDELAS  ·  Bundelkhand, around Khajuraho',
                'SOLANKIS  ·  Gujarat'], size=25), 'FOUR CLANS TO KNOW'),
        (P_ROW(['Genealogies trace them to the sun, the moon, or a fire ritual',
                'Colonial-era writers proposed Central Asian descent',
                'A third view: Rajput as a status that emerged over time',
                'Acquired by families who gained land and power',
                'Who then commissioned genealogies to match'], size=22), 'THE ORIGINS QUESTION'),
        (P_TWO(['Nagara temples on high platforms',
                'Towers rising in clustered peaks'],
               ['Marble at Mount Abu',
                'Ceilings that look turned, not cut'],
               'KHAJURAHO', 'DILWARA'), 'WHAT YOU CAN STILL VISIT'),
        (P_ROW(['Hill forts, desert forts, water forts, forest forts',
                'Chittorgarh, Ranthambore, Jaisalmer, Kumbhalgarh',
                'And stepwells, reaching down to the water table',
                'In a dry region that is infrastructure, not decoration'], size=23), 'THE FORTS'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Descent from older ruling lineages, as the genealogies claim.',
                right='Rajput as a status acquired over time, with genealogies composed afterwards to fit.'),
    tip=['FOUR CLANS', 'FOUR CAPITALS'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('shikhara'), 'THE CHANDELAS'), (Q_SHAPE('stepwell'), 'A STEPWELL, OR BAOLI'),
          (Q_SHAPE('hillring'), 'A HILL FORT')],
    mains='How did regional kingdoms maintain themselves in this period?',
    mains_tags=('DEFENSIBLE PLACES', 'CONTROL OF WATER', 'WHAT MADE SMALL STATES DURABLE'),
    facts=('Chahamanas, Paramaras, Chandelas, Solankis', 'Khajuraho and Dilwara',
           'Forts on hills and in deserts'),
    next='ANCIENT INDIAN SCIENCE AND MATHEMATICS',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
