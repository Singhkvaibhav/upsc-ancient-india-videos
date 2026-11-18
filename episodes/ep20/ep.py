"""Ancient India, Simply Unearthed — Episode 20: Ashoka's Edicts.
Approved narration, word for word. Edict sites are pins on a schematic physical
board: no boundaries, no outline of India. The State Emblem is never drawn.
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

EP = 20
CODE = 'Anc20'
TITLE = 'Ashokas_Edicts'
NAME = "Ashoka's Edicts"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_rockedict(ctx, 960, 640, 2.5, a, t)

CFG = dict(
    ep=20, period=(-260, -232), dig=_dig,
    question='Who carved this, and who was meant to read it?',
    tags=(('CARVED TO BE READ', 150, 300),),
    sources=('stone', 'staff'),
    src_note='The edicts are their own source, and the main one for this episode.',
    panels=[
        (P_ROW(['Fourteen major rock edicts', 'Minor rock edicts, shorter and more personal',
                'Major pillar edicts, on polished sandstone',
                'Minor pillar inscriptions',
                'Cave inscriptions at Barabar, given to the Ajivikas'], size=22),
         'THE GROUPS'),
        (P_ROW(['Prakrit in Brahmi  ·  most of them',
                'Prakrit in Kharoshthi  ·  the north-west',
                'Greek  ·  at Kandahar',
                'Aramaic  ·  at Kandahar'], size=26), 'FOUR SCRIPTS, SO THEY COULD BE READ'),
        (P_SITES([('GIRNAR', -420, -40), ('DHAULI', 360, 30), ('JAUGADA', 410, 160),
                  ('KALSI', -200, -360), ('SHAHBAZGARHI', -650, -400), ('MANSEHRA', -560, -440),
                  ('MASKI', -120, 260), ('SARNATH', 100, -190), ('TOPRA', -280, -300)]),
         'A HANDFUL OF SITES'),
        (P_ROW(['Nobody could read Brahmi for centuries',
                'Deciphered in 1837 by James Prinsep',
                'The edicts call their author Devanampiya Piyadasi',
                'Maski and others name Ashoka directly',
                'A forgotten king, read back from his own stones'], size=22),
         'A DETECTIVE STORY'),
    ],
    plaque=dict(kind='names', title='OLD NAME, NEW NAME', left='PIYADASI', right='ASHOKA',
                note='Brahmi deciphered 1837 · James Prinsep'),
    tip=['ROCKS AND PILLARS', 'BRAHMI AND KHAROSHTHI'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('kharoshthi'), 'KHAROSHTHI'), (Q_SHAPE('coastpin'), 'DHAULI'),
          (Q_SHAPE('caves'), 'BARABAR')],
    mains='What do the edicts tell us that other sources cannot?',
    mains_tags=('A RULER’S OWN VOICE', 'DATED AND PLACED', 'STILL HIS OWN ACCOUNT'),
    facts=('Major and minor rock edicts', 'Pillar edicts', 'Brahmi, Kharoshthi, Greek, Aramaic'),
    next='MAURYAN ADMINISTRATION AND DECLINE',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
