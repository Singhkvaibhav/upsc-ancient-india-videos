"""Ancient India, Simply Unearthed — Episode 31: Harshavardhana.
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

EP = 31
CODE = 'Anc31'
TITLE = 'Harshavardhana'
NAME = "Harshavardhana"
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
HI = _HI
EXTRA = {'ins1': 2.2, 'gal2': 1.8}

def _dig(ctx, p, t, a):
    museum.ex_sealedplate(ctx, 960, 640, 2.4, a, t)

CFG = dict(
    ep=31, period=(606, 647), dig=_dig,
    question='What do you do when both your sources want to flatter?',
    tags=(('A GRANT, AND A SEAL', 150, 300),),
    sources=('leaf', 'staff', 'stone'),
    src_note='Two of the three sources had reasons to be generous; the third was a foreign visitor.',
    panels=[
        (P_ROW(['Came to the throne about 606 CE, at Thanesar',
                'Moved his capital to Kannauj',
                'Which becomes the prize for the next two centuries',
                'Campaigned, and brought much of the north under him'], size=24),
         'THE ACCESSION'),
        (P_ROW(['Checked at the Narmada by Pulakeshin the Second',
                'Recorded not by Harsha\u2019s writers but in the Aihole inscription',
                'Which is exactly why historians trust it',
                'The north and the Deccan were separate political worlds'], size=23),
         'AND THEN HE STOPPED'),
        (P_ROW(['An assembly at Kannauj', 'A great distribution at Prayag',
                'Patronised Buddhism, and supported other traditions',
                'Endowed the monastery at Nalanda',
                'Wrote three Sanskrit plays himself'], size=22), 'WHAT HIUEN TSANG DESCRIBES'),
        (P_ROW(['Officials paid with land, not salary',
                'Subordinate rulers held their own territories',
                'They acknowledged him rather than being governed',
                'He died without an heir, around 647 CE',
                'An empire held by one person does not survive them'], size=22),
         'WHY IT DISSOLVES'),
    ],
    plaque=dict(kind='disagree', title='SCHOLARS DISAGREE',
                left='A genuine north Indian empire, the last before the Turkish invasions.',
                right='A paramountcy over feudatories; its extent is inflated by his own biographer.'),
    tip=['TWO WRITERS,', 'ONE KING'],
    prompt='PAUSE AND NAME IT',
    quiz=[(Q_SHAPE('handbook'), 'THE HARSHACHARITA'), (Q_SHAPE('narmadastop'), 'THE NARMADA'),
          (Q_SHAPE('monastery'), 'NALANDA')],
    mains='What is Hiuen Tsang\u2019s account worth as a source?',
    mains_tags=('WHAT AN OUTSIDER SEES', 'WHAT AN INSIDER DOES NOT', 'A GUEST AT A FRIENDLY COURT'),
    facts=('Reigned from about 606 CE', 'Banabhatta and Hiuen Tsang', 'Stopped at the Narmada'),
    next='THE VAKATAKAS AND THE DECCAN',)

BEATS = build(CFG, EN)
FX = fx_for(EN)
