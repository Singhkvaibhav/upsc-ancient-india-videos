"""Ancient India, Simply Unearthed — Episode 41: Land Grants and the Feudalism Debate.
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

EP = 41
CODE = 'Anc41'
TITLE = 'Land_Grants_and_Feudalism'
NAME = "Land Grants and the Feudalism Debate"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_boundarystone(ctx, 960, 640, 2.5, a, t)

CFG = dict(
    ep=41, period=(200, 1200), dig=_dig,
    question='Who owns what is inside the boundary?',
    tags=(('A BOUNDARY, MADE PERMANENT', 150, 300),),
    sources=('stone', 'leaf'),
    src_note='An argument conducted almost entirely from one class of document.',
    panels=[
        (P_ROW(['The donor, usually a king',
                'The recipient: a Brahmin, temple, monastery or official',
                'The land, with its boundaries described',
                'The immunities: freedom from taxes, or the right to collect them',
                'And frequently a curse on anyone who revokes it'], size=22),
         'WHAT A GRANT ACTUALLY SAYS'),
        (P_ROW(['Grant the revenue away and the king\u2019s income falls',
                'Grant the right to administer and his authority falls',
                'Do it a thousand times over several centuries',
                'And a layer of intermediaries appears',
                'Between the king and the peasant'], size=22), 'THE ARGUMENT'),
        (P_ROW(['Long-distance trade declined after the Guptas',
                'Fewer coins were struck; towns shrank',
                'Villages became self-sufficient',
                'Cultivators were tied to the land',
                'A feudal order, comparable in structure to medieval Europe'], size=22),
         'THE FEUDALISM CASE'),
        (P_ROW(['Coin finds and port activity suggest trade continued',
                'Temple towns grew in the south in this very period',
                'Merchant guilds remained powerful',
                'The European template asks the wrong questions',
                'What the evidence shows is regional states forming'], size=22), 'THE CRITICS ANSWER'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='Indian feudalism: grants devolved revenue and authority, trade and towns declined.',
                right='Regional state formation: trade and towns persisted, and the analogy misleads.'),
    tip=['GRANT \u00b7 INTERMEDIARY', 'WEAKER STATE'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('immunity'), 'AN IMMUNITY'), (Q_SHAPE('divertedrevenue'), 'A BRAHMADEYA'),
          (Q_SHAPE('portcoins'), 'COIN FINDS AND PORT ACTIVITY')],
    mains='Was there an Indian feudalism?',
    mains_tags=('DESCRIBE THE GRANTS', 'BOTH CASES, WITH HISTORIANS', 'THEN COMMIT, WITH REASONS'),
    facts=('Agrahara and brahmadeya grants', 'Immunities written into the deed',
           'The debate is still open'),
    next='COINS AND INSCRIPTIONS',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
