"""Ancient India, Simply Unearthed — Episode 40: Foreign Travellers.
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

EP = 40
CODE = 'Anc40'
TITLE = 'Foreign_Travellers'
NAME = "Foreign Travellers"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_staffjournal(ctx, 960, 640, 2.4, a, t)

CFG = dict(
    ep=40, period=(-300, 1050), dig=_dig,
    question='What does an outsider notice that an insider never records?',
    tags=(('HE WROTE IT DOWN', 150, 300),),
    sources=('staff', 'leaf', 'stone'),
    src_note='Reading a traveller against the ground is the method throughout.',
    panels=[
        (P_ROW(['MEGASTHENES  ·  c. 300 BCE  ·  a Greek ambassador',
                'FA-HIEN  ·  early 5th century  ·  a Chinese monk seeking texts',
                'HIUEN TSANG  ·  7th century  ·  studied at Nalanda',
                'I-TSING  ·  travelled by sea, wrote on monastic practice',
                'AL-BIRUNI  ·  11th century  ·  a scholar who learned Sanskrit'], size=22),
         'FIVE, IN ORDER'),
        (P_ROW(['The Indica: his palisade is confirmed by excavation',
                'But the work does not survive',
                'Only passages quoted by later writers, who selected',
                'His seven classes match no Indian source',
                'An outsider fitting what he saw into a familiar frame'], size=22), 'MEGASTHENES'),
        (P_ROW(['Fa-Hien: safe roads, free hospitals, rest houses',
                'And the exclusion of chandalas from the towns',
                'Hiuen Tsang: Harsha\u2019s reign, Nalanda from the inside',
                'I-Tsing: monastic rules, and the voyage itself',
                'All three devout men describing a land they revered'], size=22), 'THE PILGRIMS'),
        (P_ROW(['He learned Sanskrit to read Indian texts directly',
                'Compared Indian astronomy with Greek work',
                'Wrote the Kitab-ul-Hind as a study, not a travelogue',
                'And is candid about language barriers',
                'And about the suspicion the campaigns created'], size=22), 'AL-BIRUNI'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Invaluable: outsiders record the everyday things insiders never write down.',
                right='Treacherous: each came with a purpose and a frame, and reported what fitted it.'),
    tip=['MEGASTHENES \u00b7 FA-HIEN \u00b7 HIUEN TSANG', 'I-TSING \u00b7 AL-BIRUNI'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('scrollfrag'), 'THE INDICA OF MEGASTHENES'), (Q_SHAPE('harbour'), 'I-TSING'),
          (Q_SHAPE('twoscripts'), 'AL-BIRUNI')],
    mains='How useful are foreign accounts for Indian history?',
    mains_tags=('BOTH SIDES', 'WHAT IS CORROBORATED', 'SAY WHAT HE CAME FOR'),
    facts=('Five travellers across thirteen centuries', 'Each came for a different reason',
           'Each saw what he came to see'),
    next='LAND GRANTS AND THE FEUDALISM DEBATE',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
