"""Ancient India, Simply Unearthed — Episode 16: Jainism (English + Hindi).
Approved narration, word for word.

Mahavira and the Tirthankaras are NEVER drawn as faces or figures. They are
shown through places, objects and symbols only: a votive tablet, a crossing,
the vows carved as tablets. See CLAUDE.md rule 3.
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

EP = 16
CODE = 'Anc16'
TITLE = 'Jainism'
NAME = 'Jainism'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_ayagapata(ctx, 960, 630, 2.5, a, t)

CFG = dict(
    ep=16, period=(-599, 500), dig=_dig,
    question='Who set this up, and what did they believe?',
    tags=(('AYAGAPATA · A VOTIVE TABLET', 150, 300),),
    sources=('leaf', 'stone', 'trowel'),
    src_note='Jain donor inscriptions are among the most useful evidence we have for this period.',
    panels=[
        (P_ROW(['FIRST  ·  Rishabhanatha, also Adinatha',
                'TWENTY-THIRD  ·  Parshvanatha, traditionally 9th century BCE',
                'TWENTY-FOURTH  ·  Mahavira',
                'MAHAVIRA DID NOT FOUND JAINISM  ·  he reformed it'], size=25),
         'TWENTY-FOUR TIRTHANKARAS'),
        (P_ROW(['Born Vardhamana, near Vaishali', 'Left home at about thirty',
                'About twelve years of austerity', 'Attained kevala, complete knowledge',
                'Taught thirty years; died at Pavapuri'], size=22), 'THE LIFE'),
        (P_TWO(['Right faith', 'Right knowledge', 'Right conduct'],
               ['Ahimsa  ·  non-violence', 'Satya  ·  truth', 'Asteya  ·  not taking',
                'Aparigraha  ·  non-possession', 'Brahmacharya  ·  chastity'],
               'THREE JEWELS', 'FIVE VOWS'), 'THE TEACHING'),
        (P_TEXT('ANEKANTAVADA', 'REALITY HAS MANY SIDES', 'NO SINGLE VIEW HOLDS ALL OF IT', size=42),
         'THE DISTINCTIVE IDEA'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='A famine and a migration south split the community, the dispute crystallising over clothing.',
                right='The division developed gradually over centuries; the famine account is later tradition.'),
    tip=['THREE JEWELS · FIVE VOWS', 'TWENTY-FOUR'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('crossing'), 'PARSHVANATHA'), (Q_SHAPE('vows5'), 'BRAHMACHARYA'),
          (Q_SHAPE('manysided'), 'ANEKANTAVADA')],
    mains='Compare the teachings of Buddhism and Jainism.',
    mains_tags=('BOTH REJECT SACRIFICE AND BIRTH', 'JAINISM IS STRICTER', 'MANY-SIDEDNESS HAS NO PARALLEL'),
    facts=('Twenty-four Tirthankaras', 'Three jewels, five vows', 'Two major sects'),
    next='OTHER SECTS AND FOREIGN INVASIONS',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
