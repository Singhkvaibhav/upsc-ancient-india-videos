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

EP = 9
CODE = 'Anc09'
TITLE = 'Vedic_Literature'
NAME = 'Vedic Literature'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_leaf(ctx, 960, 620, 3.2, a, t)

CFG = dict(
    ep=9, period=(-1500, -500), dig=_dig,
    question='Nothing original survives. So how did any of it reach us?',
    tags=(('A COPY, NOT AN ORIGINAL', 150, 300),),
    sources=('leaf',),
    src_note='One source: the texts themselves, and how they are arranged.',
    panels=[
        (P_ROW(['Rigveda: hymns of praise', 'Samaveda: those hymns set to melody',
                'Yajurveda: formulas for the sacrifice', 'Atharvaveda: charms, remedies, daily life']),
         'FOUR VEDAS'),
        (P_STACK([('SAMHITA · the core hymns', 'sand'), ('BRAHMANA · the rituals explained', 'clay'),
                  ('ARANYAKA · the forest books', 'terra'), ('UPANISHAD · philosophy', 'clay')]),
         'FOUR LAYERS IN EACH'),
        (P_TEXT('WHAT IS THE SELF?', 'WHAT IS REALITY?', 'ARE THEY THE SAME?', size=50), 'THE UPANISHADS'),
        (P_ROW(['Shiksha: pronunciation', 'Kalpa: ritual', 'Vyakarana: grammar',
                'Nirukta: word meaning', 'Chhanda: metre', 'Jyotisha: astronomy'], size=22),
         'SIX VEDANGAS · THE LIMBS OF THE VEDA'),
    ],
    plaque=dict(kind='names', left='SHRUTI · HEARD', right='SMRITI · REMEMBERED'),
    tip=['FOUR VEDAS · FOUR LAYERS', 'SIX LIMBS'],
    quiz=[(Q_SHAPE('melody'), 'THE SAMAVEDA'), (Q_SHAPE('ritualbook'), 'THE BRAHMANAS'),
          (Q_SHAPE('limbs'), 'THE VEDANGAS')],
    mains='What did the Upanishads contribute to Indian thought?',
    mains_tags=('RITUAL TO ENQUIRY', 'THE SELF', 'TAKEN UP BY LATER SCHOOLS'),
    facts=('Four Vedas', 'Each in four layers', 'Six Vedangas'),
    next='VARNA, ASHRAMA AND VEDIC SOCIETY',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
