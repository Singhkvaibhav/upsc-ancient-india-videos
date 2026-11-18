"""Ancient India, Simply Unearthed — Episode 12: Mahajanapadas (English + Hindi).
Approved narration, word for word. No boundaries, no outline of India.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 300.0
core.TOTAL = TOTAL
from engine.core import W, H
from engine.stone import S, carve, poly, rrect, pot, brick, house, platform, coursed
from engine.auto import (build, fx_for, P_TEXT, P_SITES, P_ROW, P_TWO, P_STACK, P_VILLAGE,
                         P_OBJ, P_MON, Q_SHAPE, Q_OBJ, GY)
from engine import museum
from text import EN, HI as _HI

EP = 12
CODE = 'Anc12'
TITLE = 'Mahajanapadas'
NAME = 'The Mahajanapadas'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_punchcoin(ctx, 860, 660, 2.3, a, t)
    museum.ex_wallsection(ctx, 1200, 640, 1.5, a*.85, t)

CFG = dict(
    ep=12, period=(-600, -400), dig=_dig,
    question='Why do cities and coins come back at the same moment?',
    tags=(('COINS AND A CITY WALL', 150, 300),),
    sources=('leaf', 'trowel', 'coin'),
    src_note='Coins are new evidence from this period, and they are mostly evidence about trade.',
    panels=[
        (P_SITES([('MAGADHA', 420, -150), ('KOSALA', 90, -250), ('VATSA', -120, -140),
                  ('AVANTI', -400, -60), ('GANDHARA', -620, -380), ('KURU', -180, -340),
                  ('PANCHALA', 40, -380), ('ANGA', 620, -220)]), 'SIXTEEN STATES, FOUR THAT MATTER'),
        (P_TWO(['One hereditary king', 'A treasury', 'An army'],
               ['An assembly of family heads', 'They met and debated', 'They decided together'],
               'MONARCHY', 'GANASANGHA'), 'TWO KINDS OF STATE'),
        (P_VILLAGE(n=9, cit=True), 'THE SECOND URBANISATION'),
        (P_ROW(['Iron and the plough', 'Rice transplanting', 'Surplus feeds specialists',
                'Trade, then coins', 'Taxes, then armies'], size=23), 'THE CHAIN'),
    ],
    plaque=dict(kind='names', title='OLD NAME, NEW NAME', left='CHAMPA', right='BHAGALPUR',
                note='Kashi is Varanasi · Vaishali is in Bihar'),
    tip=['SIXTEEN STATES', 'TWO KINDS'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('assembly'), 'A GANASANGHA'), (Q_SHAPE('nbpw'), 'NORTHERN BLACK POLISHED WARE'),
          (Q_SHAPE('coin'), 'A PUNCH-MARKED COIN')],
    mains='What caused the second urbanisation of the Ganga plains?',
    mains_tags=('IRON AND SURPLUS', 'TRADE AND COINS', 'TAXATION AND ARMIES'),
    facts=('Sixteen mahajanapadas', 'Monarchies and ganasanghas', 'Cities return after a thousand years'),
    next='THE RISE OF MAGADHA',
)

BEATS = build(CFG, EN)
FX = fx_for(EN)
