"""Ancient India, Simply Unearthed — Episode 43: Women in Ancient India.
Approved narration, word for word. No boundaries, no outline of India; no
kingdom is drawn as shaded territory.\n\nPrescriptive law books are kept separate from what inscriptions record,\nand the episode says plainly whose lives the sources actually show.
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

EP = 43
CODE = 'Anc43'
TITLE = 'Women_in_Ancient_India'
NAME = "Women in Ancient India"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_womentablet(ctx, 960, 640, 2.5, a, t)

CFG = dict(
    ep=43, period=(-1500, 1200), dig=_dig,
    question='Where do women appear in the record in their own right?',
    tags=(('NAMED, IN THEIR OWN RIGHT', 150, 300),),
    sources=('leaf', 'stone', 'staff'),
    src_note='Keeping literature and law books apart is the whole method here.',
    panels=[
        (P_ROW(['Hymns attributed to Lopamudra and Ghosha',
                'Gargi questioning a philosopher in public debate',
                'Maitreyi choosing instruction over property',
                'The Therigatha, verses by Buddhist nuns',
                'And donor inscriptions naming women who gave'], size=22), 'THE NAMED'),
        (P_TWO(['They tell you what their authors wanted',
                'Restrictions on inheritance and remarriage',
                'A falling age of marriage',
                'And that a woman should not be independent'],
               ['Women owning property',
                'Making donations',
                'Endowing temples',
                'Acting as patrons'],
               'LAW BOOKS PRESCRIBE', 'INSCRIPTIONS RECORD'), 'EVIDENCE OF DIFFERENT THINGS'),
        (P_ROW(['Participation in ritual and learning more visible early',
                'More restricted in the later Vedic material',
                'Stridhana recognised, but bounded',
                'Yet Buddhist and Jain orders admitted women',
                'And donor inscriptions continue throughout'], size=22), 'NOT ONE SMOOTH LINE'),
        (P_ROW(['Nearly all our evidence concerns women of property',
                'Or of religious orders',
                'Because those are the women whose names got carved',
                'Women who farmed, wove or carried water appear rarely',
                'A claim about "women" is a claim about a small minority'], size=22),
         'AND WHO IS INVISIBLE'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='A steady decline from the Vedic period, visible in texts, inheritance law and marriage age.',
                right='Not one curve: evidence varies by region, period and class, and leans on prescriptive texts.'),
    tip=['PRESCRIPTION IS', 'NOT DESCRIPTION'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('debatehall'), 'GARGI'), (Q_SHAPE('verses'), 'THE THERIGATHA'),
          (Q_SHAPE('womandonor'), 'STRIDHANA')],
    mains='What was the status of women in ancient India?',
    mains_tags=('THE BROAD TREND', 'SEPARATE THE SOURCE TYPES', 'SAY WHOSE LIVES THEY SHOW'),
    facts=('Named women in the Rigveda and the Therigatha', 'Donor inscriptions name women',
           'Law books prescribe, they do not describe'),
    next='A WALK THROUGH THE GALLERY',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
