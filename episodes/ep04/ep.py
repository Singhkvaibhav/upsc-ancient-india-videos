"""Ancient India, Simply Unearthed — Episode 4: Harappan cities (English + Hindi).

No boundaries, no outline of India: the sites are pins on a schematic physical
board. Nothing revered is drawn. Approved narration, word for word.
"""
import os, sys, math, random, cairo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import core
TOTAL = 300.0
core.TOTAL = TOTAL
from engine.core import W, H, seg, ease, eoc, eob, lerp, rgba, rrect, wrap, font
from engine.stone import (S, carve, incise, coursed, poly, lamp, rake, lit, dust, vignette,
                          camera, bg_stone, bg_museum, bg_trench, unearth, brush, engraved,
                          kinetic, ribbon, tag, corner, filmgrain, house, platform,
                          drain_section, case, brick, pot, grain)
from engine.monument import (crowd, haze, horizon, godrays, scalebar, bg_sky, silhouette,
                             birds, moulding, fort)
from engine.anc import (frame, DIG, SOURCES, FRIEZE, PLAQUE, INSCRIPTION, QUIZ, GALLERY,
                        SUBSCRIBE, title_in, panel_text)
from engine import museum
from text import EN, HI as _HI

EP = 4
CODE = 'Anc04'
TITLE = 'Harappan_Cities'
NAME = 'Harappan Cities'
POST = None
BED = 'drone'
VOICE_EN = {'length': 1.10, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
VOICE_HI = {'length': 0.94, 'noise': (0.60, 0.75), 'gaps': (0.50, 0.32)}
CRF, PRESET = 18, 'medium'
EXTRA = {'dig2': .6, 'ins1': 2.4, 'gal2': 2.0}
HI = _HI
PERIOD = (-2600, -1900)
GY = 820          # the ground line of the carved city


def sc(fn, bgname='stone'):
    fn.bg = bgname
    return fn


# ================= 0:00 the dig =================
def _drain_artefact(ctx, p, t, a):
    drain_section(ctx, 300, 620, 1200, a, slabs=10, depth=6.)


def s_dig(first):
    def f(ctx, t, D):
        def body(ctx, t, D, a):
            DIG(ctx, t, D, a, _drain_artefact,
                question='How did people so long ago build cities this well planned?' if first else None,
                tags=(('HARAPPA · 1921', 150, 300), ('MOHENJO-DARO · 1922', 150, 364)) if first else (),
                sweep=(0.4, 4.2) if not first else (-9, -8),
                t_q=2.6)
        frame(ctx, t, D, EP, PERIOD, body, lambda c, tt: bg_trench(c, tt))
    return sc(f, 'trench')


# ================= 0:20 how do we know =================
def s_src(ctx, t, D):
    def body(ctx, t, D, a):
        SOURCES(ctx, t, D, a, on=('trowel',),
                note='The Harappans did write, on seals — but the script is\nnot yet deciphered.')
        q = seg(t, 3.0, 3.6)
        if q > 0:
            qa = a*ease(q)
            museum.ex_seal(ctx, 1600, 760, 1.05, qa, t)
            tag(ctx, 'SCRIPT NOT YET DECIPHERED', 1600, 912, qa, align='c')
    frame(ctx, t, D, EP, PERIOD, body, lambda c, tt: bg_stone(c, tt, lampx=W*.5, lampy=340))
sc(s_src)


# ================= 0:35–2:20 the frieze =================
def _p_region(ctx, cx, gy, a, t):
    """the river and its neighbours, as a schematic physical board — no boundaries"""
    for k in range(7):
        ctx.new_path()
        for x in range(int(cx - 820), int(cx + 820), 24):
            y = gy - 180 + k*17 + 13*math.sin(x*.006 + k*.8)
            (ctx.move_to if x < cx - 800 else ctx.line_to)(x, y)
        rgba(ctx, S['lime'], .20*a); ctx.set_line_width(3.4); ctx.stroke()
    for i, dx in enumerate((-470, -150, 190, 520)):
        q = ease(seg(t, .3 + i*.25, .9 + i*.25))
        rgba(ctx, S['ochre'], a*q); ctx.arc(cx + dx, gy - 40, 11, 0, 2*math.pi); ctx.fill()
        rgba(ctx, S['ochre'], .5*a*q); ctx.set_line_width(2)
        ctx.move_to(cx + dx, gy - 50); ctx.line_to(cx + dx, gy - 96); ctx.stroke()
    engraved(ctx, 'A VAST REGION ALONG THE RIVERS', cx, gy - 290, 34, a, S['lime'])
    engraved(ctx, 'SCHEMATIC · NOT TO SCALE · BOUNDARIES NOT SHOWN', cx, gy + 190, 19, a*.7, S['dim'] if 'dim' in S else S['lime'], serif=False)


def _p_twoparts(ctx, cx, gy, a, t):
    platform(ctx, cx - 740, gy, 420, 180, a)
    for i, (hh, w_) in enumerate(((120, 90), (152, 78), (104, 84))):
        house(ctx, cx - 700 + i*124, gy - 180, w_, hh, a, seed=6 + i)
    for i in range(7):
        house(ctx, cx - 180 + i*124, gy, 104, 84 + (i % 3)*20, a, seed=20 + i)
    rgba(ctx, S['soot'], .5*a); ctx.rectangle(cx - 250, gy - 180, 46, 182); ctx.fill()
    engraved(ctx, 'CITADEL · WEST · HIGHER', cx - 540, gy - 400, 28, a, S['ochre'])
    engraved(ctx, 'LOWER TOWN · EAST · WIDER', cx + 250, gy - 250, 28, a, S['ochre'])


def _p_grid(ctx, cx, gy, a, t):
    """streets crossing at right angles, then the brick and its 1:2:4"""
    for i in range(7):
        x = cx - 620 + i*206
        q = ease(seg(t, .2 + i*.08, .7 + i*.08))
        rgba(ctx, S['sand'], .30*a*q); ctx.rectangle(x, gy - 430, 26, 440); ctx.fill()
    for j in range(4):
        y = gy - 390 + j*120
        q = ease(seg(t, .5 + j*.1, 1.0 + j*.1))
        rgba(ctx, S['sand'], .30*a*q); ctx.rectangle(cx - 640, y, 1300*q, 22); ctx.fill()
    bq = ease(seg(t, 1.6, 2.2))
    if bq > 0:
        brick(ctx, cx - 120, gy - 150, 2.0, a*bq)
        engraved(ctx, '1 : 2 : 4', cx + 260, gy - 180, 64, a*bq, S['ochre'])
        engraved(ctx, 'THICK : WIDE : LONG', cx + 260, gy - 130, 24, a*bq, S['lime'], serif=False)


def _p_drains(ctx, cx, gy, a, t):
    drain_section(ctx, cx - 560, gy - 150, 1120, a, slabs=9, depth=5.)
    for i, dx in enumerate((-340, -40, 260)):
        q = ease(seg(t, .5 + i*.3, 1.1 + i*.3))
        rgba(ctx, S['sand'], .55*a*q); ctx.rectangle(cx + dx, gy - 330, 16, 180*q); ctx.fill()
        house(ctx, cx + dx - 70, gy - 330, 150, 118, a*q, seed=40 + i)
    engraved(ctx, 'HOUSE DRAINS JOIN THE STREET DRAIN', cx, gy + 80, 30, a, S['ochre'])


def _p_house(ctx, cx, gy, a, t):
    """a courtyard house in plan: rooms round an open court, a well, a side door"""
    carve(ctx, lambda: ctx.rectangle(cx - 330, gy - 440, 660, 440), S['sand'], a, depth=5.)
    ctx.new_path(); ctx.rectangle(cx - 150, gy - 310, 300, 190)
    ctx.set_source_rgba(0, 0, 0, .55*a); ctx.fill()
    engraved(ctx, 'COURTYARD', cx, gy - 205, 24, a*.9, S['lime'], serif=False)
    for (rx, ry, rw, rh) in ((-310, -420, 180, 100), (130, -420, 180, 100), (-310, -100, 180, 80), (130, -100, 180, 80)):
        carve(ctx, lambda rx=rx, ry=ry, rw=rw, rh=rh: ctx.rectangle(cx + rx, gy + ry, rw, rh),
              tuple(v*.92 for v in S['sand']), a, depth=3., tex=.3, seed=50)
    q = ease(seg(t, .6, 1.2))
    carve(ctx, lambda: ctx.arc(cx + 215, gy - 230, 34, 0, 2*math.pi), S['clay'], a*q, depth=4.)
    engraved(ctx, 'WELL', cx + 215, gy - 170, 21, a*q, S['ochre'], serif=False)
    q2 = ease(seg(t, 1.0, 1.6))
    rgba(ctx, S['ochre'], a*q2); ctx.rectangle(cx - 338, gy - 150, 14, 70); ctx.fill()
    engraved(ctx, 'DOOR ONTO THE SIDE LANE', cx - 430, gy - 110, 22, a*q2, S['ochre'], 'r', serif=False)


def _p_bath(ctx, cx, gy, a, t):
    """the Great Bath: a stepped watertight tank, in section"""
    carve(ctx, lambda: ctx.rectangle(cx - 480, gy - 230, 960, 230), S['sand'], a, depth=5.5)
    coursed(ctx, cx - 480, gy - 230, 960, 230, a*.85, seed=70)
    for k in range(4):
        carve(ctx, lambda k=k: ctx.rectangle(cx - 420 + k*42, gy - 200 + k*44, 48, 46), S['lime'], a, depth=3., seed=71 + k)
        carve(ctx, lambda k=k: ctx.rectangle(cx + 372 - k*42, gy - 200 + k*44, 48, 46), S['lime'], a, depth=3., seed=81 + k)
    ctx.new_path(); ctx.rectangle(cx - 252, gy - 60, 504, 60)
    g = cairo.LinearGradient(0, gy - 60, 0, gy)
    g.add_color_stop_rgba(0, .36, .58, .62, .62*a); g.add_color_stop_rgba(1, .18, .32, .36, .78*a)
    ctx.set_source(g); ctx.fill()
    for k in range(4):
        rgba(ctx, S['lime'], .14*a)
        ctx.rectangle(cx - 240, gy - 52 + k*13 + 3*math.sin(t*1.4 + k), 480, 2.4); ctx.fill()
    scalebar(ctx, cx - 520, gy, 230, 'ABOUT 12 M LONG', a*.9)
    engraved(ctx, 'THE GREAT BATH · MOHENJO-DARO', cx, gy - 290, 32, a, S['ochre'])


def _p_granary(ctx, cx, gy, a, t):
    for i in range(6):
        x = cx - 460 + (i % 3)*320; y = gy - (0 if i < 3 else 190)
        carve(ctx, lambda x=x, y=y: ctx.rectangle(x, y - 170, 250, 170), S['sand'], a, depth=5., seed=90 + i)
        coursed(ctx, x, y - 170, 250, 170, a*.8, seed=95 + i)
    engraved(ctx, 'LARGE STRUCTURES — CALLED "GRANARIES"', cx, gy + 90, 32, a, S['ochre'])


def _p_sites(ctx, cx, gy, a, t):
    """four sites as labelled pins on a schematic board. No boundaries, no outline."""
    for k in range(6):
        ctx.new_path()
        for x in range(int(cx - 760), int(cx + 760), 24):
            y = gy - 120 + k*22 + 15*math.sin(x*.005 + k)
            (ctx.move_to if x < cx - 740 else ctx.line_to)(x, y)
        rgba(ctx, S['lime'], .16*a); ctx.set_line_width(3); ctx.stroke()
    sites = (('DHOLAVIRA', -560, -230), ('LOTHAL', -200, -40), ('KALIBANGAN', 180, -300), ('RAKHIGARHI', 560, -150))
    for i, (nm, dx, dy) in enumerate(sites):
        q = ease(seg(t, .3 + i*.45, .9 + i*.45))
        if q <= 0: continue
        drop = (1 - eob(q, 1.4))*-150
        x, y = cx + dx, gy + dy + drop
        rgba(ctx, S['ochre'], a*q); ctx.set_line_width(3)
        ctx.move_to(x, y); ctx.line_to(x, y - 58); ctx.stroke()
        ctx.arc(x, y - 66, 12, 0, 2*math.pi); ctx.fill()
        for r_ in range(2):
            rp = seg(q, .5 + r_*.2, 1.)
            if rp > 0:
                ctx.new_path(); rgba(ctx, S['ochre'], (1 - rp)*a); ctx.set_line_width(3)
                ctx.arc(x, y, 10 + 60*rp, 0, 2*math.pi); ctx.stroke()
        engraved(ctx, nm, x, y - 92, 28, a*q, S['lime'])
    uq = ease(seg(t, 2.4, 3.0))
    if uq > 0: tag(ctx, 'DHOLAVIRA · UNESCO WORLD HERITAGE SITE', cx, gy + 190, a*uq, align='c')
    engraved(ctx, 'SCHEMATIC · NOT TO SCALE · BOUNDARIES NOT SHOWN', cx, gy + 250, 19, a*.65, S['lime'], serif=False)


PANELS = [(0, _p_region, None), (1, _p_twoparts, None), (2, _p_grid, 'STREETS AND BRICKS'),
          (3, _p_drains, None), (4, _p_house, 'A COURTYARD HOUSE'), (5, _p_bath, None),
          (6, _p_granary, None), (7, _p_sites, None)]
FRZ_KEYS = ['frz1', 'frz2', 'frz3', 'frz4', 'frz5', 'frz6', 'frz7', 'frz8']


def s_frz(i):
    def f(ctx, t, D):
        def body(ctx, t, D, a):
            # the camera sits on this beat's panel and eases on to the next
            # sit on this beat's panel, then pan to the next only in its last moment,
            # so two panels are never both on screen for long
            prog = i + ease(cl01((t - (D - .8))/.8))*(1 if i < len(PANELS) - 1 else 0)
            ox = -prog*W          # a panel at px lands centred when prog == px
            ctx.save(); ctx.translate(ox*.32, 0)
            rgba(ctx, S['soot'], .5*a); ctx.rectangle(-W*9, 150, W*20, H); ctx.fill()
            ctx.restore()
            ctx.save(); ctx.translate(ox, 0)
            camera(ctx, t, D, (1.0, 1.03), cx=prog*W + W/2, cy=560, depth=.55)
            for yy in (208, GY + 168):
                for k in range(int(9*W//58) + 4):
                    x = -60 + k*58
                    carve(ctx, lambda x=x, yy=yy: ctx.arc(x, yy, 12, 0, 2*math.pi), S['clay'], .6*a, depth=2.6, tex=.2)
            for px, draw, label in PANELS:
                d_ = abs(px - prog)
                if d_ >= .92: continue
                near = max(0., 1 - d_*1.9)
                if near <= 0: continue
                draw(ctx, px*W + W/2, GY, a*near, t)
                if label:
                    engraved(ctx, label, px*W + W/2, 300, 30, a*near*.9, S['ochre'])
            ctx.restore()
        frame(ctx, t, D, EP, PERIOD, body, lambda c, tt: bg_stone(c, tt, lampx=W*.52, lampy=300, beam=False))
    return sc(f)


def cl01(x): return max(0., min(1., x))


# ================= 2:20 the plaque =================
def s_plq(first):
    def f(ctx, t, D):
        def body(ctx, t, D, a):
            PLAQUE(ctx, t, D, a, kind='disagree',
                   title='SCHOLARS DISAGREE',
                   left='Granaries: stores for grain, collected as tax or through trade.',
                   right='Halls or warehouses: the evidence for stored grain is thin.',
                   t0=.3 if first == 0 else -3.)
        frame(ctx, t, D, EP, PERIOD, body, lambda c, tt: bg_stone(c, tt, lampx=W*.5, lampy=320))
    return sc(f)


# ================= 2:50 the inscription =================
def s_ins(ctx, t, D):
    def body(ctx, t, D, a):
        INSCRIPTION(ctx, t, D, a, ['WEST IS HIGH · EAST IS WIDE', 'BRICKS 1 : 2 : 4'], t0=1.6, per=3.2)
    frame(ctx, t, D, EP, PERIOD, body, lambda c, tt: bg_stone(c, tt, lampx=W*.5, lampy=360, beam=False))
sc(s_ins)


# ================= 3:20 the dig quiz =================
def _q_bath(ctx, cx, cy, a, t):
    carve(ctx, lambda: ctx.rectangle(cx - 250, cy - 90, 500, 150), S['sand'], a, depth=5.)
    for k in range(3):
        carve(ctx, lambda k=k: ctx.rectangle(cx - 215 + k*32, cy - 66 + k*34, 38, 36), S['lime'], a, depth=2.6, seed=10 + k)
        carve(ctx, lambda k=k: ctx.rectangle(cx + 177 - k*32, cy - 66 + k*34, 38, 36), S['lime'], a, depth=2.6, seed=20 + k)
    ctx.new_path(); ctx.rectangle(cx - 120, cy + 10, 240, 50)
    ctx.set_source_rgba(.26, .44, .48, .75*a); ctx.fill()


def _q_dock(ctx, cx, cy, a, t):
    carve(ctx, lambda: ctx.rectangle(cx - 240, cy - 80, 420, 170), S['sand'], a, depth=5.)
    ctx.new_path(); ctx.rectangle(cx - 200, cy - 42, 340, 96)
    ctx.set_source_rgba(.26, .44, .48, .72*a); ctx.fill()
    carve(ctx, lambda: ctx.rectangle(cx + 140, cy - 18, 180, 36), S['sand'], a, depth=4.)
    ctx.new_path(); ctx.rectangle(cx + 150, cy - 8, 170, 18)
    ctx.set_source_rgba(.26, .44, .48, .72*a); ctx.fill()
    for k in range(4):
        rgba(ctx, S['lime'], .14*a)
        ctx.rectangle(cx - 190, cy - 30 + k*20 + 3*math.sin(t*1.5 + k), 320, 2.4); ctx.fill()


def _q_three(ctx, cx, cy, a, t):
    for i, (dx, w_, h_) in enumerate(((-250, 150, 120), (-70, 170, 90), (130, 190, 140))):
        carve(ctx, lambda dx=dx, w_=w_, h_=h_: ctx.rectangle(cx + dx, cy + 40 - h_, w_, h_),
              S['sand'], a, depth=4.5, seed=30 + i)
        coursed(ctx, cx + dx, cy + 40 - h_, w_, h_, a*.8, seed=40 + i)
    for dx in (-200, 60):
        ctx.new_path(); ctx.rectangle(cx + dx, cy + 54, 120, 36)
        ctx.set_source_rgba(.26, .44, .48, .72*a); ctx.fill()


def s_quiz(i):
    def f(ctx, t, D):
        def body(ctx, t, D, a):
            cards = [(_q_bath, 'THE GREAT BATH · MOHENJO-DARO'), (_q_dock, 'THE DOCKYARD AT LOTHAL'), (_q_three, 'DHOLAVIRA')]
            if i < 3:
                QUIZ(ctx, t, D, a, [cards[i]], mains=None, t0=.35, per=D - .9,
                     prompt='PAUSE AND NAME THE SITE')
            else:
                q = ease(seg(t, .2, .9))
                rgba(ctx, (0, 0, 0), .55*a*q); ctx.rectangle(0, 150, W, H - 150); ctx.fill()
                engraved(ctx, 'IN MAINS', W/2, 330, 34, a*q, S['ochre'], serif=False)
                for j, l in enumerate(wrap(ctx, 'What does Harappan town planning tell us about how the cities were run?', 42, 1500, True)):
                    engraved(ctx, l, W/2, 430 + j*58, 42, a*q, S['lime'])
                for j, (l, cue) in enumerate((('THE GRID', 1.2), ('THE STANDARD BRICKS', 1.7), ('THE DRAINS', 2.2))):
                    qq = ease(seg(t, cue, cue + .5))
                    if qq > 0:
                        tag(ctx, l, 420 + j*430, 700, a*qq, align='c', size=26)
                qq = ease(seg(t, 3.0, 3.6))
                if qq > 0:
                    engraved(ctx, 'EVIDENCE OF PLANNING ON A LARGE SCALE', W/2, 830, 32, a*qq, S['ochre'])
        frame(ctx, t, D, EP, PERIOD, body, lambda c, tt: bg_stone(c, tt, lampx=W*.5, lampy=330, beam=False))
    return sc(f)


# ================= 4:30 the gallery =================
def s_gal(first):
    def f(ctx, t, D):
        def body(ctx, t, D, a):
            GALLERY(ctx, t, D, a,
                    lambda c, tt, aa, place: museum.hall(c, tt, aa, place, upto=4, cols=5),
                    facts=('c. 2600–1900 BCE', 'Citadel west, lower town east', 'Standard bricks, covered drains') if first == 0 else (),
                    nxt='HARAPPAN LIFE' if first else None,
                    t0=.4)
            if first:
                SUBSCRIBE(ctx, t, D, a, D - 4.4)
        frame(ctx, t, D, EP, False, body, lambda c, tt: bg_museum(c, tt))
    return sc(f, 'museum')


# ================= beats =================
SC = {}
for i, k in enumerate(['dig1', 'dig2']): SC[k] = s_dig(i)
SC['src1'] = s_src
for i, k in enumerate(FRZ_KEYS): SC[k] = s_frz(i)
for i, k in enumerate(['plq1', 'plq2']): SC[k] = s_plq(i)
SC['ins1'] = s_ins
for i, k in enumerate(['quiz1', 'quiz2', 'quiz3', 'quiz4']): SC[k] = s_quiz(i)
for i, k in enumerate(['gal1', 'gal2']): SC[k] = s_gal(i)

BEATS = [(k, n, SC[k]) for k, n in EN]

FX = [('sweep', 'dig1', .3, .5), ('thud', 'dig1', 2.2, .4),
      ('chisel', 'ins1', 1.4, .6), ('chisel', 'ins1', 4.6, .6),
      ('thud', 'gal1', 1.1, .5)]
