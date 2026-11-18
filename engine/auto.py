"""Build a whole episode from a short config.

Writing bespoke scene code for 44 episodes is not realistic, so an episode is
declared as data: which sources light, what the frieze panels show, what the
plaque says, the inscription lines, the quiz, and the exhibit. This module turns
that into BEATS, obeying the same seven-segment format and the same motion rules.

Beat keys follow the sample: dig*, src*, frz*, plq*, ins*, quiz*, gal*. A segment
may span any number of beats; the config does not care how the narration was split.
"""
import cairo, math, random
from engine.core import W, H, cl, seg, ease, eoc, eob, lerp, rgba, rrect, wrap, font
from engine.stone import (S, carve, incise, coursed, poly, lamp, rake, lit, dust, vignette,
                          camera, bg_stone, bg_museum, bg_trench, unearth, brush, engraved,
                          kinetic, ribbon, tag, corner, filmgrain, house, platform,
                          drain_section, case, brick, pot, grain)
from engine.monument import (crowd, haze, horizon, godrays, scalebar, bg_sky, silhouette,
                             birds, moulding, pillar, colonnade, stupa, temple, chaitya, fort)
from engine.anc import frame, DIG, SOURCES, PLAQUE, INSCRIPTION, QUIZ, GALLERY, SUBSCRIBE
from engine import museum

GY = 820


# ================= generic frieze panels =================
def P_TEXT(*lines, size=40):
    """large engraved lines — for a panel that is an idea rather than a thing"""
    def d(ctx, cx, gy, a, t):
        for j, l in enumerate(lines):
            q = ease(seg(t, .2 + j*.35, .9 + j*.35))
            engraved(ctx, l, cx, gy - 300 + j*(size + 22), size, a*q, S['lime'])
    return d


def P_SITES(sites, note=True):
    """labelled pins on a schematic physical board. Never a boundary, never an outline."""
    def d(ctx, cx, gy, a, t):
        for k in range(6):
            ctx.new_path()
            for x in range(int(cx - 780), int(cx + 780), 24):
                y = gy - 140 + k*22 + 15*math.sin(x*.005 + k)
                (ctx.move_to if x < cx - 760 else ctx.line_to)(x, y)
            rgba(ctx, S['lime'], .15*a); ctx.set_line_width(3); ctx.stroke()
        for i, (nm, dx, dy) in enumerate(sites):
            q = ease(seg(t, .3 + i*.38, .9 + i*.38))
            if q <= 0: continue
            # keep every pin and its label on the board, clear of the note line
            dy = max(-430., min(170., float(dy)))
            dx = max(-830., min(830., float(dx)))
            x, y = cx + dx, gy + dy + (1 - eob(q, 1.4))*-150
            rgba(ctx, S['ochre'], a*q); ctx.set_line_width(3)
            ctx.move_to(x, y); ctx.line_to(x, y - 54); ctx.stroke()
            ctx.arc(x, y - 62, 11, 0, 2*math.pi); ctx.fill()
            for r_ in range(2):
                rp = seg(q, .5 + r_*.2, 1.)
                if rp > 0:
                    ctx.new_path(); rgba(ctx, S['ochre'], (1 - rp)*a); ctx.set_line_width(3)
                    ctx.arc(x, y, 10 + 56*rp, 0, 2*math.pi); ctx.stroke()
            engraved(ctx, nm, x, y - 88, 27, a*q, S['lime'])
        if note:
            engraved(ctx, 'SCHEMATIC · NOT TO SCALE · BOUNDARIES NOT SHOWN', cx, gy + 230, 19, a*.62, S['lime'], serif=False)
    return d


def P_ROW(items, obj=None, size=28):
    """a row of carved cards, each a short label, appearing one at a time.
    The type shrinks until the longest label fits its card in both directions,
    and the same size is used on every card so the row reads as a set."""
    def _fit(ctx, lab, sz, inner):
        """wrap at sz, measuring with the serif face engraved() actually draws"""
        font(ctx, sz, True, True)
        words, lines, cur = lab.split(), [], ''
        for w_ in words:
            cand = (cur + ' ' + w_).strip()
            if ctx.text_extents(cand).x_advance > inner and cur:
                lines.append(cur); cur = w_
            else:
                cur = cand
        if cur: lines.append(cur)
        over = any(ctx.text_extents(l).x_advance > inner for l in lines)
        return lines, over

    def d(ctx, cx, gy, a, t):
        n = len(items)
        wdt = min(360, 1560/n)
        inner = wdt - 40
        body_h = 150 if obj else 230          # room left under an object, if any
        sz = size
        while sz > 14:
            lines = [_fit(ctx, lab, sz, inner) for lab in items]
            if (not any(o for _, o in lines)
                    and max(len(ls) for ls, _ in lines)*(sz + 7) <= body_h):
                break
            sz -= 2
        lead = sz + 7
        for i, lab in enumerate(items):
            q = ease(seg(t, .25 + i*.3, .9 + i*.3))
            if q <= 0: continue
            x = cx - (n*wdt + (n - 1)*24)/2 + i*(wdt + 24)
            s_ = eob(q, 1.5)
            ctx.save(); ctx.translate(x + wdt/2, gy - 190); ctx.scale(s_, s_); ctx.translate(-(x + wdt/2), -(gy - 190))
            carve(ctx, lambda x=x: rrect(ctx, x, gy - 320, wdt, 260, 10), S['clay'], a*q, depth=5.)
            if obj: obj(ctx, x + wdt/2, gy - 215, .65, a*q, t)
            ls, _ = _fit(ctx, lab, sz, inner)
            base = (gy - 118) if obj else (gy - 190)
            y0 = base - (len(ls) - 1)*lead/2
            for j, l in enumerate(ls):
                engraved(ctx, l, x + wdt/2, y0 + j*lead, sz, a*q, S['lime'])
            ctx.restore()
    return d


def P_TWO(left, right, lhead=None, rhead=None):
    """two carved blocks of equal size, side by side. `left` and `right` are
    either one string or a list of short lines; the type size and line spacing
    shrink to fit whichever side has more, so the two cards stay equal."""
    def _lines(ctx, body, size, width):
        if isinstance(body, (list, tuple)):
            out = []
            for item in body:
                out.extend(wrap(ctx, item, size, width, True))
            return out
        return wrap(ctx, body, size, width, True)

    def d(ctx, cx, gy, a, t):
        # one size for both cards, chosen so the fuller side fits inside it
        size, lead = 30, 44
        for _ in range(6):
            n = max(len(_lines(ctx, b, size, 700)) for b in (left, right))
            if n*lead <= 250 or size <= 18: break
            size -= 2; lead = size + 12
        for i, (head, body) in enumerate(((lhead, left), (rhead, right))):
            q = ease(seg(t, .3 + i*.45, 1.0 + i*.45))
            if q <= 0: continue
            x = cx - 820 + i*840
            carve(ctx, lambda x=x: rrect(ctx, x, gy - 430, 800, 400, 12), S['clay'], a*q, depth=5.5)
            if head: engraved(ctx, head, x + 400, gy - 360, 32, a*q, S['ochre'])
            ls = _lines(ctx, body, size, 700)
            # the body sits in the band below the heading, never over it
            top, bot = gy - 310, gy - 60
            y0 = top + ((bot - top) - len(ls)*lead)/2 + lead*.78
            for j, l in enumerate(ls):
                engraved(ctx, l, x + 400, y0 + j*lead, size, a*q, S['lime'])
    return d


def P_STACK(bands):
    """stacked strata or layers, deepest last, each labelled on the right"""
    def d(ctx, cx, gy, a, t):
        n = len(bands)
        for i, (lab, col) in enumerate(bands):
            q = ease(seg(t, .25 + i*.35, .95 + i*.35))
            if q <= 0: continue
            y = gy - 440 + i*(400/n)
            carve(ctx, lambda y=y: ctx.rectangle(cx - 620, y, 1000, 400/n - 8),
                  S[col] if isinstance(col, str) else col, a*q, depth=4.5, seed=30 + i)
            engraved(ctx, lab, cx + 420, y + (400/n)/2 + 8, 28, a*q, S['ochre'], 'l')
    return d


def P_VILLAGE(n=7, cit=False):
    def d(ctx, cx, gy, a, t):
        if cit:
            platform(ctx, cx - 760, gy, 420, 180, a)
            for i, (hh, w_) in enumerate(((120, 90), (152, 78), (104, 84))):
                house(ctx, cx - 720 + i*124, gy - 180, w_, hh, a, seed=6 + i)
        for i in range(n):
            q = ease(seg(t, .2 + i*.12, .8 + i*.12))
            x = cx - (n*134)/2 + i*134 + (300 if cit else 0)
            house(ctx, x, gy, 110, 86 + (i % 3)*22, a*q, seed=20 + i)
        crowd(ctx, gy + 6, [cx - 560, cx - 516, cx + 540], .7*a, 1.0, t=t)
    return d


def P_OBJ(fn, s=2.6, label=None):
    """one object, large and lit"""
    def d(ctx, cx, gy, a, t):
        q = ease(seg(t, .2, 1.0))
        lamp(ctx, cx, gy - 260, 520, .26*a*q)
        ctx.save(); ctx.translate(cx, gy - 240); ctx.scale(s, s); ctx.translate(-cx, -(gy - 240))
        fn(ctx, cx, gy - 240, 1., a*q, t)
        ctx.restore()
        if label: engraved(ctx, label, cx, gy + 40, 30, a*q, S['ochre'])
    return d


def P_MON(kind, s=1.0, sky='dawn', label=None):
    """a monument hero shot inside the frieze"""
    def d(ctx, cx, gy, a, t):
        fn = {'stupa': stupa, 'temple': temple, 'chaitya': chaitya}[kind]
        fn(ctx, cx, gy + 120, s=s, a=a, t=t)
        if label: engraved(ctx, label, cx, 300, 32, a, S['ochre'])
    return d


def P_WHEEL(labels=(), hub=None):
    """an eight-spoked wheel, the dharmachakra, with short words on its spokes.
    Used instead of any figure: the wheel is how early Indian art carried this."""
    def d(ctx, cx, gy, a, t):
        cy = gy - 268
        q = ease(seg(t, .25, 1.0))
        if q <= 0: return
        R = 158
        carve(ctx, lambda: ctx.arc(cx, cy, R, 0, 2*math.pi), S['sand'], a*q, depth=5.5)
        carve(ctx, lambda: ctx.arc(cx, cy, R - 34, 0, 2*math.pi), tuple(v*.9 for v in S['sand']),
              a*q, depth=3., seed=311)
        carve(ctx, lambda: ctx.arc(cx, cy, 40, 0, 2*math.pi), S['lime'], a*q, depth=3.4, seed=312)
        for k in range(8):
            qq = ease(seg(t, .5 + k*.12, .9 + k*.12))
            if qq <= 0: continue
            ang = -math.pi/2 + k*math.pi/4
            rgba(ctx, S['ochre'], .5*a*qq); ctx.set_line_width(13)
            ctx.move_to(cx + 40*math.cos(ang), cy + 40*math.sin(ang))
            ctx.line_to(cx + (R - 36)*math.cos(ang), cy + (R - 36)*math.sin(ang)); ctx.stroke()
            if k < len(labels):
                lx, ly = cx + (R + 104)*math.cos(ang), cy + (R + 56)*math.sin(ang)
                al = 'c' if abs(math.cos(ang)) < .35 else ('l' if math.cos(ang) > 0 else 'r')
                engraved(ctx, labels[k], lx, ly + 8, 24, a*qq, S['lime'], al, serif=False)
        if hub:
            engraved(ctx, hub, cx, gy + 26, 30, a*q, S['ochre'], 'c', serif=False)
    return d


# ================= generic quiz card art =================
def Q_OBJ(fn, s=1.6):
    def d(ctx, cx, cy, a, t):
        ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s); ctx.translate(-cx, -cy)
        fn(ctx, cx, cy, 1., a, t); ctx.restore()
    return d


def Q_SHAPE(kind):
    def d(ctx, cx, cy, a, t):
        if kind == 'tank':
            carve(ctx, lambda: ctx.rectangle(cx - 250, cy - 90, 500, 150), S['sand'], a, depth=5.)
            for k in range(3):
                carve(ctx, lambda k=k: ctx.rectangle(cx - 215 + k*32, cy - 66 + k*34, 38, 36), S['lime'], a, depth=2.6, seed=10 + k)
                carve(ctx, lambda k=k: ctx.rectangle(cx + 177 - k*32, cy - 66 + k*34, 38, 36), S['lime'], a, depth=2.6, seed=20 + k)
            ctx.new_path(); ctx.rectangle(cx - 120, cy + 10, 240, 50)
            ctx.set_source_rgba(.26, .44, .48, .75*a); ctx.fill()
        elif kind == 'basin':
            carve(ctx, lambda: ctx.rectangle(cx - 240, cy - 80, 420, 170), S['sand'], a, depth=5.)
            ctx.new_path(); ctx.rectangle(cx - 200, cy - 42, 340, 96)
            ctx.set_source_rgba(.26, .44, .48, .72*a); ctx.fill()
            carve(ctx, lambda: ctx.rectangle(cx + 140, cy - 18, 180, 36), S['sand'], a, depth=4.)
        elif kind == 'threecity':
            for i, (dx, w_, h_) in enumerate(((-250, 150, 120), (-70, 170, 90), (130, 190, 140))):
                carve(ctx, lambda dx=dx, w_=w_, h_=h_: ctx.rectangle(cx + dx, cy + 40 - h_, w_, h_),
                      S['sand'], a, depth=4.5, seed=30 + i)
                coursed(ctx, cx + dx, cy + 40 - h_, w_, h_, a*.8, seed=40 + i)
        elif kind == 'edict':
            carve(ctx, lambda: (ctx.move_to(cx - 150, cy + 150), ctx.line_to(cx - 150, cy - 60),
                                ctx.curve_to(cx - 150, cy - 170, cx + 150, cy - 170, cx + 150, cy - 60),
                                ctx.line_to(cx + 150, cy + 150), ctx.close_path()), S['clay'], a, depth=6.)
            for k in range(6):
                rgba(ctx, S['soot'], .5*a); ctx.rectangle(cx - 100, cy - 80 + k*38, 200, 9); ctx.fill()
        elif kind == 'coin':
            carve(ctx, lambda: ctx.arc(cx, cy, 130, 0, 2*math.pi), S['lime'], a, depth=6.)
            rr = random.Random(5)
            for k in range(6):
                rgba(ctx, S['soot'], .5*a)
                ctx.arc(cx + rr.uniform(-70, 70), cy + rr.uniform(-70, 70), 17, 0, 2*math.pi); ctx.fill()
        elif kind == 'traveller':
            crowd(ctx, cy + 120, [cx], .95*a, 3.4, t=t)
            carve(ctx, lambda: rrect(ctx, cx + 90, cy - 120, 16, 250, 8), S['clay'], a, depth=3.)
        elif kind == 'handaxe':
            museum.ex_handaxe(ctx, cx, cy, 1.9, a, t)
        elif kind == 'microlith':
            carve(ctx, lambda: rrect(ctx, cx - 250, cy + 10, 500, 26, 12), S['clay'], a, depth=4.)
            for k in range(7):
                carve(ctx, lambda k=k: poly(ctx, [(cx - 220 + k*70, cy + 10), (cx - 196 + k*70, cy - 56),
                                                  (cx - 172 + k*70, cy + 10)]), S['lime'], a, depth=3., seed=50 + k)
        elif kind == 'polished':
            carve(ctx, lambda: poly(ctx, [(cx - 120, cy + 60), (cx - 60, cy - 90), (cx + 40, cy - 70),
                                          (cx + 20, cy + 76)]), tuple(v*1.2 for v in S['basalt']), a, depth=6.)
            for k in range(5):
                rgba(ctx, S['sand'], .55*a); ctx.arc(cx + 150 + (k % 3)*44, cy + 30 + (k//3)*40, 13, 0, 2*math.pi); ctx.fill()
        elif kind == 'copperstone':
            carve(ctx, lambda: poly(ctx, [(cx - 250, cy - 20), (cx - 110, cy - 60), (cx - 90, cy + 20),
                                          (cx - 230, cy + 50)]), tuple(v*1.4 for v in S['terra']), a, depth=5.)
            carve(ctx, lambda: poly(ctx, [(cx + 90, cy + 40), (cx + 150, cy - 60), (cx + 230, cy - 10),
                                          (cx + 190, cy + 60)]), tuple(v*1.2 for v in S['basalt']), a, depth=5.)
        elif kind == 'pot':
            pot(ctx, cx, cy + 90, 2.1, a)
        elif kind == 'channel':
            carve(ctx, lambda: ctx.rectangle(cx - 300, cy + 20, 600, 60), S['clay'], a, depth=5.)
            ctx.new_path(); ctx.rectangle(cx - 270, cy + 34, 540, 30)
            ctx.set_source_rgba(.26, .44, .48, .72*a); ctx.fill()
            carve(ctx, lambda: poly(ctx, [(cx - 320, cy + 20), (cx + 320, cy + 20), (cx + 260, cy - 60), (cx - 260, cy - 60)]),
                  S['sand'], a, depth=4.)
        elif kind == 'field':
            carve(ctx, lambda: ctx.rectangle(cx - 300, cy - 100, 600, 220), S['clay'], a, depth=4.5)
            for k in range(7):
                rgba(ctx, S['soot'], .35*a); ctx.rectangle(cx - 290 + k*84, cy - 96, 10, 212); ctx.fill()
            for k in range(4):
                rgba(ctx, S['soot'], .35*a); ctx.rectangle(cx - 296, cy - 90 + k*56, 592, 10); ctx.fill()
        elif kind == 'weight':
            carve(ctx, lambda: ctx.rectangle(cx - 70, cy - 70, 140, 140), S['lime'], a, depth=6.)
            carve(ctx, lambda: ctx.rectangle(cx + 120, cy - 20, 90, 90), S['lime'], a, depth=5.)
            carve(ctx, lambda: ctx.rectangle(cx - 220, cy - 110, 110, 180), S['lime'], a, depth=5.)
        elif kind == 'bead':
            carve(ctx, lambda: rrect(ctx, cx - 230, cy - 30, 460, 60, 30), tuple(v*1.5 for v in S['terra']), a, depth=5.)
            ctx.new_path(); ctx.rectangle(cx - 230, cy - 7, 460, 14)
            ctx.set_source_rgba(0, 0, 0, .7*a); ctx.fill()
        elif kind == 'seal':
            museum.ex_seal(ctx, cx, cy, 1.7, a, t)
        elif kind == 'rigveda':
            for k in range(10):
                carve(ctx, lambda k=k: rrect(ctx, cx - 230, cy - 150 + k*31, 460, 24, 6), S['sand'], a, depth=2.8, seed=70 + k)
        elif kind == 'assembly':
            for i in range(9):
                th = math.pi + i*math.pi/8
                crowd(ctx, cy + 60 + 70*math.sin(th), [cx + 230*math.cos(th)], .9*a, 1.5, t=t, seed=i)
        elif kind == 'rivers':
            for k in range(7):
                ctx.new_path()
                for x in range(int(cx - 300), int(cx + 300), 20):
                    ctx.line_to(x, cy - 90 + k*28 + 9*math.sin(x*.02 + k))
                rgba(ctx, S['lime'], .30*a); ctx.set_line_width(4); ctx.stroke()
        elif kind == 'ironplough':
            carve(ctx, lambda: poly(ctx, [(cx - 250, cy + 40), (cx - 60, cy - 10), (cx - 20, cy + 60),
                                          (cx - 210, cy + 96)]), tuple(v*1.1 for v in S['basalt']), a, depth=5.)
            carve(ctx, lambda: rrect(ctx, cx + 40, cy - 70, 30, 170, 10), S['clay'], a, depth=4.)
            carve(ctx, lambda: poly(ctx, [(cx + 30, cy + 94), (cx + 200, cy + 60), (cx + 215, cy + 110),
                                          (cx + 40, cy + 140)]), tuple(v*1.1 for v in S['basalt']), a, depth=5.)
        elif kind == 'pgw':
            museum.ex_pgw(ctx, cx, cy, 2.4, a, t)
        elif kind == 'horse':
            carve(ctx, lambda: poly(ctx, [(cx - 170, cy + 60), (cx - 150, cy - 20), (cx - 90, cy - 54),
                                          (cx + 60, cy - 50), (cx + 150, cy - 10), (cx + 170, cy + 60),
                                          (cx + 120, cy + 60), (cx + 100, cy + 10), (cx - 100, cy + 10),
                                          (cx - 120, cy + 60)]), S['clay'], a, depth=5.)
            rgba(ctx, S['ochre'], .5*a); ctx.set_line_width(4)
            ctx.move_to(cx - 230, cy + 96); ctx.line_to(cx + 230, cy + 96); ctx.stroke()
        elif kind == 'melody':
            for k in range(5):
                ctx.new_path()
                for x in range(int(cx - 240), int(cx + 240), 12):
                    ctx.line_to(x, cy - 80 + k*40 + 16*math.sin(x*.035 + k*1.2))
                rgba(ctx, S['ochre'], .55*a); ctx.set_line_width(4); ctx.stroke()
        elif kind == 'ritualbook':
            carve(ctx, lambda: rrect(ctx, cx - 220, cy - 130, 440, 260, 10), S['sand'], a, depth=5.)
            for k in range(7):
                rgba(ctx, S['soot'], .45*a); ctx.rectangle(cx - 180, cy - 100 + k*32, 360 - (k % 3)*70, 11); ctx.fill()
        elif kind == 'limbs':
            carve(ctx, lambda: ctx.arc(cx, cy, 84, 0, 2*math.pi), S['clay'], a, depth=5.)
            for k in range(6):
                th = k*math.pi/3
                carve(ctx, lambda th=th: ctx.arc(cx + 185*math.cos(th), cy + 115*math.sin(th), 40, 0, 2*math.pi),
                      S['sand'], a, depth=3.6, seed=80 + k)
        elif kind == 'hymn10':
            carve(ctx, lambda: rrect(ctx, cx - 230, cy - 140, 460, 280, 10), S['sand'], a, depth=5.)
            for k in range(9):
                rgba(ctx, S['soot'], .3*a); ctx.rectangle(cx - 190, cy - 110 + k*27, 380, 9); ctx.fill()
            rgba(ctx, S['ochre'], .85*a); ctx.rectangle(cx - 190, cy + 106, 380, 11); ctx.fill()
        elif kind == 'path4':
            rgba(ctx, S['dim'] if 'dim' in S else S['lime'], .3*a)
            ctx.set_line_width(6); ctx.move_to(cx - 290, cy + 60); ctx.line_to(cx + 290, cy + 60); ctx.stroke()
            for k in range(4):
                x = cx - 240 + k*160
                carve(ctx, lambda x=x: ctx.arc(x, cy + 60, 34, 0, 2*math.pi), S['clay'], a, depth=4., seed=90 + k)
                crowd(ctx, cy + 10, [x], .85*a, 1.0, t=t, seed=k)
        elif kind == 'dialogue':
            crowd(ctx, cy + 80, [cx - 90, cx + 90], .95*a, 2.0, t=t)
        elif kind == 'dolmen':
            museum.ex_megalith(ctx, cx, cy, 2.0, a, t)
        elif kind == 'menhir':
            carve(ctx, lambda: poly(ctx, [(cx - 44, cy + 120), (cx - 30, cy - 130), (cx + 26, cy - 140),
                                          (cx + 46, cy + 120)]), tuple(v*1.15 for v in S['basalt']), a, depth=5.5)
            crowd(ctx, cy + 124, [cx + 150], .8*a, 1.1, t=t)
        elif kind == 'urn':
            pot(ctx, cx, cy + 110, 2.2, a)
            carve(ctx, lambda: ctx.rectangle(cx - 240, cy + 110, 480, 26), tuple(v*.8 for v in S['clay']), a, depth=3.)
        elif kind == 'nbpw':
            def bowl():
                ctx.move_to(cx - 280, cy - 130); ctx.curve_to(cx - 260, cy + 115, cx + 260, cy + 115, cx + 280, cy - 130)
                ctx.close_path()
            carve(ctx, bowl, tuple(v*.5 for v in S['lime']), a, depth=5.)
            ctx.save(); ctx.new_path(); bowl(); ctx.clip()
            for k in range(4):
                rgba(ctx, S['lime'], .22*a); ctx.rectangle(cx - 300, cy - 100 + k*48, 600, 12); ctx.fill()
            ctx.restore()
        elif kind == 'hillring':
            for i, (dx, w_, h_) in enumerate(((-330, 230, 120), (-140, 200, 95), (150, 240, 130), (360, 190, 100))):
                carve(ctx, lambda dx=dx, w_=w_, h_=h_: poly(ctx, [(cx + dx - w_/2, cy + 110), (cx + dx, cy + 110 - h_),
                                                                  (cx + dx + w_/2, cy + 110)]),
                      tuple(v*1.1 for v in S['basalt']), a, depth=4.5, seed=160 + i)
            for i, dx in enumerate((-90, 10, 110)):
                carve(ctx, lambda dx=dx: ctx.rectangle(cx + dx - 36, cy + 34, 72, 76), S['sand'], a, depth=3.6, seed=170 + i)
        elif kind == 'treasury':
            carve(ctx, lambda: ctx.rectangle(cx - 300, cy - 30, 230, 150), S['sand'], a, depth=5.)
            for k in range(9):
                carve(ctx, lambda k=k: ctx.arc(cx - 270 + (k % 3)*58, cy + 10 + (k//3)*42, 20, 0, 2*math.pi),
                      S['ochre'], a, depth=3., seed=180 + k)
            crowd(ctx, cy + 120, [cx + 10 + i*62 for i in range(6)], .85*a, 1.5, t=t)
        elif kind == 'confederacy':
            for i, dx in enumerate((-290, -150, -10, 130, 270)):
                off = (0 if i < 2 else (i - 1)*22)
                carve(ctx, lambda dx=dx, off=off: ctx.rectangle(cx + dx + off, cy - 10 + off*.7, 108, 94),
                      S['sand'], a, depth=4., seed=190 + i)
                crowd(ctx, cy + 84 + off*.7, [cx + dx + off + 54], .8*a, 1.1, t=t, seed=i)
        elif kind == 'bodhitree':
            museum.ex_bodhi(ctx, cx, cy, 1.9, a, t)
        elif kind == 'wheelpark':
            carve(ctx, lambda: ctx.arc(cx, cy, 120, 0, 2*math.pi), S['sand'], a, depth=5.)
            carve(ctx, lambda: ctx.arc(cx, cy, 26, 0, 2*math.pi), tuple(v*.88 for v in S['sand']), a, depth=3.)
            for k in range(8):
                ang = k*math.pi/4
                rgba(ctx, S['soot'], .44*a); ctx.set_line_width(11)
                ctx.move_to(cx + 26*math.cos(ang), cy + 26*math.sin(ang))
                ctx.line_to(cx + 112*math.cos(ang), cy + 112*math.sin(ang)); ctx.stroke()
            for dx in (-270, 250):
                carve(ctx, lambda dx=dx: poly(ctx, [(cx + dx - 44, cy + 110), (cx + dx - 24, cy + 20),
                                                    (cx + dx + 24, cy + 20), (cx + dx + 44, cy + 110)]),
                      tuple(v*.9 for v in S['clay']), a, depth=3., seed=200)
        elif kind == 'stupa':
            museum.ex_stupamodel(ctx, cx, cy, 1.7, a, t)
        elif kind == 'chaitya':
            carve(ctx, lambda: ctx.rectangle(cx - 220, cy - 150, 440, 300), tuple(v*1.1 for v in S['basalt']), a, depth=6.)
            ctx.new_path()
            ctx.move_to(cx - 92, cy + 150); ctx.line_to(cx - 92, cy - 30)
            ctx.curve_to(cx - 92, cy - 136, cx + 92, cy - 136, cx + 92, cy - 30)
            ctx.line_to(cx + 92, cy + 150); ctx.close_path()
            ctx.set_source_rgba(0, 0, 0, .8*a); ctx.fill()
            for k in range(5):
                rgba(ctx, S['sand'], .4*a); ctx.set_line_width(5)
                ctx.arc(cx, cy - 30, 30 + k*14, math.pi, 2*math.pi); ctx.stroke()
        elif kind == 'vihara':
            carve(ctx, lambda: ctx.rectangle(cx - 280, cy - 130, 560, 260), S['sand'], a, depth=5.5)
            for k in range(8):
                ctx.new_path()
                ctx.rectangle(cx - 250 + (k % 4)*134, cy - 100 + (k//4)*124, 86, 88)
                ctx.set_source_rgba(0, 0, 0, .74*a); ctx.fill()
        elif kind == 'crossing':
            ctx.new_path(); ctx.rectangle(cx - 330, cy + 30, 660, 90)
            ctx.set_source_rgba(.26, .44, .48, .62*a); ctx.fill()
            for k in range(6):
                carve(ctx, lambda k=k: ctx.rectangle(cx - 280 + k*110, cy - 10, 58, 46),
                      S['sand'], a, depth=3.4, seed=210 + k)
            carve(ctx, lambda: poly(ctx, [(cx - 36, cy - 30), (cx - 22, cy - 150), (cx + 22, cy - 150),
                                          (cx + 36, cy - 30)]), tuple(v*1.1 for v in S['lime']), a, depth=4.5)
        elif kind == 'vows5':
            for k in range(5):
                carve(ctx, lambda k=k: rrect(ctx, cx - 350 + k*145, cy - 80, 120, 160, 8),
                      S['sand'], a, depth=4., seed=220 + k)
                for j in range(3):
                    rgba(ctx, S['soot'], .4*a)
                    ctx.rectangle(cx - 330 + k*145, cy - 40 + j*30, 80, 7); ctx.fill()
        elif kind == 'manysided':
            carve(ctx, lambda: poly(ctx, [(cx - 90, cy + 70), (cx - 110, cy - 40), (cx, cy - 100),
                                          (cx + 110, cy - 40), (cx + 90, cy + 70)]),
                  tuple(v*1.1 for v in S['lime']), a, depth=5.)
            for k in range(6):
                ang = math.pi + k*math.pi/5
                ex_, ey = cx + 300*math.cos(ang), cy + 190*math.sin(ang)
                rgba(ctx, S['ochre'], .42*a); ctx.set_line_width(5)
                ctx.move_to(ex_, ey); ctx.line_to(cx + 150*math.cos(ang), cy + 95*math.sin(ang)); ctx.stroke()
                rgba(ctx, S['ochre'], .5*a); ctx.arc(ex_, ey, 12, 0, 2*math.pi); ctx.fill()
        elif kind == 'niyati':
            carve(ctx, lambda: rrect(ctx, cx - 210, cy - 130, 420, 260, 10), S['sand'], a, depth=5.)
            for k in range(5):
                rgba(ctx, S['soot'], .42*a); ctx.rectangle(cx - 160, cy - 86 + k*42, 320, 10); ctx.fill()
            rgba(ctx, S['soot'], .3*a); ctx.set_line_width(7)
            ctx.move_to(cx - 160, cy - 86); ctx.line_to(cx + 160, cy + 128); ctx.stroke()
        elif kind == 'senses':
            carve(ctx, lambda: rrect(ctx, cx - 230, cy - 120, 460, 240, 10), S['sand'], a, depth=5.)
            for k in range(5):
                px = cx - 170 + k*85
                carve(ctx, lambda px=px: ctx.arc(px, cy, 30, 0, 2*math.pi),
                      tuple(v*.9 for v in S['lime']), a, depth=3., seed=230 + k)
        elif kind == 'riverhalt':
            ctx.new_path(); ctx.move_to(cx + 60, cy - 170)
            ctx.curve_to(cx + 140, cy - 40, cx - 20, cy + 50, cx + 90, cy + 170)
            ctx.set_source_rgba(.26, .44, .48, .72*a); ctx.set_line_width(58); ctx.stroke()
            crowd(ctx, cy + 90, [cx - 300 + i*60 for i in range(5)], .85*a, 1.5, t=t)
        elif kind == 'saptanga':
            labs = ['KING', 'MINISTERS', 'TERRITORY', 'FORT', 'TREASURY', 'ARMY', 'ALLY']
            for k in range(7):
                ang = -math.pi/2 + k*2*math.pi/7
                px, py = cx + 215*math.cos(ang), cy + 140*math.sin(ang)
                carve(ctx, lambda px=px, py=py: ctx.arc(px, py, 46, 0, 2*math.pi),
                      S['sand'], a, depth=3.4, seed=240 + k)
                engraved(ctx, labs[k], px, py + 8, 19, a*.95, S['soot'], 'c', serif=False)
            rgba(ctx, S['ochre'], .34*a); ctx.set_line_width(4)
            for k in range(7):
                a1 = -math.pi/2 + k*2*math.pi/7; a2 = -math.pi/2 + (k + 1)*2*math.pi/7
                ctx.move_to(cx + 215*math.cos(a1), cy + 140*math.sin(a1))
                ctx.line_to(cx + 215*math.cos(a2), cy + 140*math.sin(a2))
            ctx.stroke()
        elif kind == 'mandala':
            # rings of neighbours around you. The card is narrow, so it carries
            # the diagram alone; the narration names what the rings mean.
            for k, r in enumerate((58, 112, 166)):
                rgba(ctx, S['ochre'] if k % 2 == 0 else S['lime'], (.52 - k*.1)*a)
                ctx.set_line_width(9); ctx.arc(cx, cy, r, 0, 2*math.pi); ctx.stroke()
            carve(ctx, lambda: ctx.arc(cx, cy, 38, 0, 2*math.pi), S['sand'], a, depth=4.)
            engraved(ctx, 'YOU', cx, cy + 8, 21, a*.95, S['soot'], 'c', serif=False)
            for k, r in enumerate((112, 166)):
                carve(ctx, lambda r=r: ctx.arc(cx + r, cy, 17, 0, 2*math.pi),
                      S['lime'] if k else S['terra'], a, depth=2.8, seed=320 + k)
                carve(ctx, lambda r=r: ctx.arc(cx - r, cy, 17, 0, 2*math.pi),
                      S['lime'] if k else S['terra'], a, depth=2.8, seed=330 + k)
        elif kind == 'kalinga':
            carve(ctx, lambda: poly(ctx, [(cx - 170, cy + 120), (cx - 186, cy - 20), (cx - 80, cy - 110),
                                          (cx + 90, cy - 116), (cx + 184, cy - 10), (cx + 168, cy + 120)]),
                  tuple(v*1.12 for v in S['basalt']), a, depth=6.)
            for k in range(6):
                rgba(ctx, S['lime'], .34*a); ctx.rectangle(cx - 120, cy - 64 + k*26, 240, 7); ctx.fill()
            rgba(ctx, S['terra'], .6*a); ctx.arc(cx + 260, cy - 40, 15, 0, 2*math.pi); ctx.fill()
        elif kind == 'mahamatra':
            crowd(ctx, cy + 110, [cx - 180, cx, cx + 180], .9*a, 2.1, t=t)
            for i, dx in enumerate((-180, 0, 180)):
                carve(ctx, lambda dx=dx: rrect(ctx, cx + dx - 86, cy - 150, 172, 60, 8),
                      S['sand'], a, depth=3.6, seed=250 + i)
                for j in range(2):
                    rgba(ctx, S['soot'], .42*a)
                    ctx.rectangle(cx + dx - 62 + j*8, cy - 132 + j*22, 124 - j*16, 7); ctx.fill()
        elif kind == 'roadworks':
            carve(ctx, lambda: ctx.rectangle(cx - 400, cy + 70, 800, 36), tuple(v*.84 for v in S['clay']), a, depth=4.)
            for k, dx in enumerate((-300, -120, 80, 280)):
                carve(ctx, lambda dx=dx: ctx.rectangle(cx + dx - 9, cy - 40, 18, 110),
                      tuple(v*.8 for v in S['clay']), a, depth=3., seed=260 + k)
                carve(ctx, lambda dx=dx: ctx.arc(cx + dx, cy - 64, 44, 0, 2*math.pi),
                      S['lime'], a, depth=3., tex=.25, seed=270 + k)
            carve(ctx, lambda: ctx.arc(cx + 360, cy + 120, 40, math.pi, 2*math.pi), S['sand'], a, depth=3.4)
        elif kind == 'kharoshthi':
            carve(ctx, lambda: rrect(ctx, cx - 300, cy - 120, 600, 240, 10),
                  tuple(v*1.1 for v in S['basalt']), a, depth=5.5)
            rr = random.Random(23)
            for row in range(4):
                x = cx + 250
                while x > cx - 250:
                    w_ = rr.uniform(14, 40)
                    rgba(ctx, S['lime'], .36*a)
                    ctx.rectangle(x - w_, cy - 78 + row*44, w_, 7); ctx.fill()
                    x -= w_ + 12
        elif kind == 'coastpin':
            # a coastline down the left of the card, with a carved pin on it
            ctx.new_path(); ctx.move_to(cx - 150, cy - 150)
            ctx.curve_to(cx - 60, cy - 60, cx - 96, cy + 30, cx - 40, cy + 150)
            ctx.set_source_rgba(.26, .44, .48, .46*a); ctx.set_line_width(52); ctx.stroke()
            rgba(ctx, S['ochre'], a); ctx.set_line_width(4)
            ctx.move_to(cx + 70, cy + 70); ctx.line_to(cx + 70, cy - 10); ctx.stroke()
            carve(ctx, lambda: ctx.arc(cx + 70, cy - 28, 20, 0, 2*math.pi), S['ochre'], a, depth=3.)
            for r_ in (36, 60):
                rgba(ctx, S['ochre'], .26*a); ctx.set_line_width(3)
                ctx.new_path(); ctx.arc(cx + 70, cy + 70, r_, 0, 2*math.pi); ctx.stroke()
        elif kind == 'caves':
            carve(ctx, lambda: poly(ctx, [(cx - 330, cy + 150), (cx - 250, cy - 90), (cx - 40, cy - 160),
                                          (cx + 220, cy - 100), (cx + 330, cy + 150)]),
                  tuple(v*1.15 for v in S['basalt']), a, depth=6.)
            for dx in (-110, 110):
                ctx.new_path()
                ctx.move_to(cx + dx - 48, cy + 150); ctx.line_to(cx + dx - 48, cy + 20)
                ctx.curve_to(cx + dx - 48, cy - 44, cx + dx + 48, cy - 44, cx + dx + 48, cy + 20)
                ctx.line_to(cx + dx + 48, cy + 150); ctx.close_path()
                ctx.set_source_rgba(0, 0, 0, .82*a); ctx.fill()
        elif kind == 'rajuka':
            carve(ctx, lambda: rrect(ctx, cx - 260, cy - 120, 520, 150, 10), S['sand'], a, depth=4.5)
            engraved(ctx, 'RURAL AUTHORITY', cx, cy - 36, 34, a*.92, S['soot'], 'c', serif=False)
            for i, dx in enumerate((-300, -100, 100, 300)):
                carve(ctx, lambda dx=dx: ctx.rectangle(cx + dx - 46, cy + 70, 92, 66),
                      tuple(v*.88 for v in S['clay']), a, depth=3.2, seed=280 + i)
        elif kind == 'lake':
            ctx.new_path(); ctx.save(); ctx.translate(cx - 40, cy + 20); ctx.scale(1.5, 1.)
            ctx.arc(0, 0, 160, 0, 2*math.pi); ctx.restore()
            ctx.set_source_rgba(.26, .44, .48, .68*a); ctx.fill()
            carve(ctx, lambda: ctx.rectangle(cx + 210, cy - 110, 54, 260), S['sand'], a, depth=5.)
            for i in range(3):
                carve(ctx, lambda i=i: poly(ctx, [(cx - 330 + i*90, cy - 110), (cx - 290 + i*90, cy - 190),
                                                  (cx - 250 + i*90, cy - 110)]),
                      tuple(v*1.08 for v in S['basalt']), a, depth=4., seed=290 + i)
        elif kind == 'fragments':
            rr = random.Random(29)
            for k in range(5):
                px, py = cx - 240 + k*120, cy + rr.uniform(-50, 50)
                carve(ctx, lambda px=px, py=py, k=k: poly(ctx, [(px - 52, py + 70), (px - 60, py - 46),
                                                                (px + 8, py - 74), (px + 58, py - 20),
                                                                (px + 44, py + 64)]),
                      S['sand'], a, depth=3.6, seed=300 + k)
                for j in range(3):
                    rgba(ctx, S['soot'], .36*a)
                    ctx.rectangle(px - 36, py - 28 + j*24, rr.uniform(40, 72), 5); ctx.fill()
        elif kind == 'torana':
            museum.ex_torana(ctx, cx, cy, 1.7, a, t)
        elif kind == 'matronymic':
            carve(ctx, lambda: rrect(ctx, cx - 250, cy - 70, 500, 140, 10), S['sand'], a, depth=4.6)
            engraved(ctx, 'SON OF', cx, cy - 16, 30, a*.9, S['soot'], 'c', serif=False)
            engraved(ctx, 'GAUTAMI', cx, cy + 34, 44, a*.95, S['soot'], 'c')
        elif kind == 'aniconic':
            carve(ctx, lambda: rrect(ctx, cx - 250, cy - 170, 500, 340, 10), S['sand'], a, depth=5.)
            museum.ex_bodhi(ctx, cx, cy + 36, 1.18, a, t)
        elif kind == 'junagadh':
            carve(ctx, lambda: poly(ctx, [(cx - 230, cy + 110), (cx - 246, cy - 30), (cx - 150, cy - 108),
                                          (cx - 30, cy - 112), (cx + 18, cy - 24), (cx - 6, cy + 110)]),
                  tuple(v*1.12 for v in S['basalt']), a, depth=6.)
            for k in range(5):
                rgba(ctx, S['lime'], .32*a)
                ctx.rectangle(cx - 206, cy - 66 + k*30, 180 - (k % 2)*36, 7); ctx.fill()
            ctx.new_path(); ctx.save(); ctx.translate(cx + 140, cy + 20); ctx.scale(1.35, 1.)
            ctx.arc(0, 0, 72, 0, 2*math.pi); ctx.restore()
            ctx.set_source_rgba(.26, .44, .48, .64*a); ctx.fill()
            carve(ctx, lambda: ctx.rectangle(cx + 232, cy - 56, 30, 152), S['sand'], a, depth=4.5)
        elif kind == 'era':
            carve(ctx, lambda: ctx.rectangle(cx - 400, cy - 8, 800, 16), S['sand'], a, depth=4.)
            for k in range(7):
                x = cx - 360 + k*120
                carve(ctx, lambda x=x: ctx.rectangle(x - 4, cy - 30, 8, 22),
                      tuple(v*.9 for v in S['sand']), a, depth=2.4, seed=360 + k)
            carve(ctx, lambda: ctx.arc(cx - 120, cy, 34, 0, 2*math.pi), S['ochre'], a, depth=4.)
            engraved(ctx, '78 CE', cx - 120, cy - 70, 32, a*.95, S['ochre'], 'c', serif=False)
        elif kind == 'mountaincapital':
            for i, (dx, w_, h_) in enumerate(((-350, 300, 190), (-80, 250, 140), (230, 330, 220))):
                carve(ctx, lambda dx=dx, w_=w_, h_=h_: poly(ctx, [(cx + dx - w_/2, cy + 150),
                                                                  (cx + dx, cy + 150 - h_),
                                                                  (cx + dx + w_/2, cy + 150)]),
                      tuple(v*1.08 for v in S['basalt']), a, depth=4.5, seed=370 + i)
            carve(ctx, lambda: ctx.rectangle(cx - 70, cy + 50, 140, 100), S['sand'], a, depth=4.)
            carve(ctx, lambda: poly(ctx, [(cx - 86, cy + 50), (cx, cy + 6), (cx + 86, cy + 50)]),
                  S['sand'], a, depth=3.4, seed=375)
            rgba(ctx, S['ochre'], .42*a); ctx.set_line_width(6)
            ctx.move_to(cx - 420, cy + 120); ctx.curve_to(cx - 150, cy + 60, cx + 150, cy + 190, cx + 430, cy + 110)
            ctx.stroke()
        elif kind == 'councilhall':
            for i, (dx, w_, h_) in enumerate(((-210, 230, 150), (215, 250, 172))):
                carve(ctx, lambda dx=dx, w_=w_, h_=h_: poly(ctx, [(cx + dx - w_/2, cy + 150),
                                                                  (cx + dx, cy + 150 - h_),
                                                                  (cx + dx + w_/2, cy + 150)]),
                      tuple(v*1.06 for v in S['clay']), a, depth=4., seed=380 + i)
            carve(ctx, lambda: rrect(ctx, cx - 180, cy - 50, 360, 200, 10), S['sand'], a, depth=5.)
            for k in range(8):
                carve(ctx, lambda k=k: ctx.rectangle(cx - 152 + (k % 4)*82, cy - 14 + (k//4)*80, 56, 50),
                      tuple(v*.88 for v in S['sand']), a, depth=2.6, seed=390 + k)
        elif kind == 'silkroad':
            # a route winding between ranges, with bales moving along it
            for i, (dx, w_, h_) in enumerate(((-250, 240, 120), (40, 200, 90), (270, 230, 130))):
                carve(ctx, lambda dx=dx, w_=w_, h_=h_: poly(ctx, [(cx + dx - w_/2, cy - 40),
                                                                  (cx + dx, cy - 40 - h_),
                                                                  (cx + dx + w_/2, cy - 40)]),
                      tuple(v*1.0 for v in S['clay']), a, depth=4., seed=480 + i)
            rgba(ctx, S['ochre'], .5*a); ctx.set_line_width(9)
            ctx.new_path(); ctx.move_to(cx - 300, cy + 130)
            ctx.curve_to(cx - 100, cy + 40, cx + 100, cy + 170, cx + 300, cy + 70)
            ctx.stroke()
            for i, (bx, by) in enumerate(((-190, 92), (0, 108), (190, 92))):
                carve(ctx, lambda bx=bx, by=by: rrect(ctx, cx + bx - 26, cy + by - 22, 52, 40, 7),
                      S['sand'], a, depth=3., seed=490 + i)
        elif kind == 'bow':
            rgba(ctx, S['ochre'], .9*a); ctx.set_line_width(16)
            ctx.new_path(); ctx.arc(cx + 120, cy, 170, math.pi*.62, math.pi*1.38); ctx.stroke()
            rgba(ctx, S['lime'], .8*a); ctx.set_line_width(5)
            ctx.move_to(cx + 20, cy - 157); ctx.line_to(cx + 20, cy + 157); ctx.stroke()
            rgba(ctx, S['lime'], .9*a); ctx.set_line_width(7)
            ctx.move_to(cx - 150, cy); ctx.line_to(cx + 60, cy); ctx.stroke()
            carve(ctx, lambda: poly(ctx, [(cx - 150, cy), (cx - 112, cy - 20), (cx - 112, cy + 20)]),
                  S['lime'], a, depth=3.)
        elif kind == 'fishpearl':
            def fish():
                ctx.move_to(cx - 170, cy)
                ctx.curve_to(cx - 90, cy - 86, cx + 70, cy - 86, cx + 140, cy)
                ctx.curve_to(cx + 70, cy + 86, cx - 90, cy + 86, cx - 170, cy)
                ctx.close_path()
            carve(ctx, fish, S['lime'], a, depth=4.6)
            carve(ctx, lambda: poly(ctx, [(cx + 140, cy), (cx + 210, cy - 54), (cx + 196, cy),
                                          (cx + 210, cy + 54)]), S['lime'], a, depth=3.4, seed=400)
            for k in range(4):
                carve(ctx, lambda k=k: ctx.arc(cx - 240 + (k % 2)*58, cy - 30 + (k//2)*60, 24, 0, 2*math.pi),
                      tuple(v*1.04 for v in S['lime']), a, depth=3., tex=.15, seed=410 + k)
        elif kind == 'harbour':
            ctx.new_path(); ctx.rectangle(cx - 240, cy + 40, 480, 110)
            ctx.set_source_rgba(.26, .44, .48, .58*a); ctx.fill()
            for i, dx in enumerate((-120, 60)):
                carve(ctx, lambda dx=dx: poly(ctx, [(cx + dx - 86, cy + 44), (cx + dx + 86, cy + 44),
                                                    (cx + dx + 54, cy + 94), (cx + dx - 54, cy + 94)]),
                      tuple(v*.92 for v in S['clay']), a, depth=4., seed=420 + i)
                carve(ctx, lambda dx=dx: ctx.rectangle(cx + dx - 5, cy - 86, 10, 130),
                      tuple(v*.82 for v in S['clay']), a, depth=3., seed=430 + i)
            for i, dx in enumerate((168, 218)):
                carve(ctx, lambda dx=dx: poly(ctx, [(cx + dx - 20, cy - 16), (cx + dx + 20, cy - 16),
                                                    (cx + dx + 11, cy + 34), (cx + dx - 11, cy + 34)]),
                      tuple(v*1.18 for v in S['terra']), a, depth=3.2, seed=440 + i)
        elif kind == 'grammar':
            carve(ctx, lambda: poly(ctx, [(cx - 180, cy + 150), (cx - 40, cy + 40), (cx + 40, cy + 40),
                                          (cx + 180, cy + 150)]), tuple(v*.8 for v in S['clay']), a, depth=4.5)
            museum.ex_tamilleaf(ctx, cx, cy - 40, 1.1, a, t)
        elif kind == 'anthologies':
            for k in range(8):
                y = cy + 120 - k*32
                carve(ctx, lambda y=y, k=k: rrect(ctx, cx - 180 + (k % 2)*14, y - 24, 360, 26, 6),
                      S['sand'], a, depth=3., tex=.26, seed=450 + k)
        elif kind == 'unnamed':
            carve(ctx, lambda: rrect(ctx, cx - 250, cy - 150, 500, 300, 10), S['sand'], a, depth=5.)
            crowd(ctx, cy + 86, [cx - 70, cx + 70], .9*a, 1.5, t=t)
            for dx in (-70, 70):
                carve(ctx, lambda dx=dx: rrect(ctx, cx + dx - 60, cy - 122, 120, 40, 8),
                      tuple(v*.88 for v in S['sand']), a, depth=2.6, seed=460)
        elif kind == 'handbook':
            carve(ctx, lambda: rrect(ctx, cx - 210, cy - 140, 420, 280, 10), S['sand'], a, depth=5.)
            for k in range(8):
                rgba(ctx, S['soot'], .34*a)
                ctx.rectangle(cx - 170, cy - 104 + k*30, 340 - (k % 3)*70, 7); ctx.fill()
            rgba(ctx, S['ochre'], .5*a); ctx.set_line_width(4)
            ctx.move_to(cx - 170, cy + 128); ctx.line_to(cx + 170, cy + 128); ctx.stroke()
        elif kind == 'monsoon':
            for k in range(3):
                rgba(ctx, S['ochre'], (.5 - k*.12)*a); ctx.set_line_width(11 - k*2)
                ctx.new_path()
                ctx.move_to(cx - 360, cy - 60 + k*62)
                ctx.curve_to(cx - 120, cy - 130 + k*62, cx + 120, cy + 10 + k*62, cx + 300, cy - 50 + k*62)
                ctx.stroke()
                carve(ctx, lambda k=k: poly(ctx, [(cx + 300, cy - 50 + k*62), (cx + 250, cy - 76 + k*62),
                                                  (cx + 256, cy - 24 + k*62)]),
                      S['ochre'], a*(1 - k*.2), depth=2.6, seed=470 + k)
        elif kind == 'deltaport':
            ctx.new_path(); ctx.move_to(cx - 60, cy - 170)
            ctx.curve_to(cx - 20, cy - 60, cx - 140, cy - 20, cx - 180, cy + 90)
            ctx.set_source_rgba(.26, .44, .48, .6*a); ctx.set_line_width(44); ctx.stroke()
            ctx.new_path(); ctx.move_to(cx - 60, cy - 170)
            ctx.curve_to(cx + 30, cy - 50, cx + 60, cy - 10, cx + 40, cy + 110)
            ctx.set_source_rgba(.26, .44, .48, .6*a); ctx.set_line_width(36); ctx.stroke()
            ctx.new_path(); ctx.rectangle(cx - 420, cy + 110, 840, 120)
            ctx.set_source_rgba(.26, .44, .48, .52*a); ctx.fill()
            carve(ctx, lambda: poly(ctx, [(cx + 150, cy + 60), (cx + 270, cy + 60), (cx + 240, cy + 112),
                                          (cx + 180, cy + 112)]), tuple(v*.9 for v in S['clay']), a, depth=3.6)
        elif kind == 'prashasti':
            carve(ctx, lambda: ctx.rectangle(cx - 46, cy - 170, 92, 320), S['sand'], a, depth=5.4)
            carve(ctx, lambda: rrect(ctx, cx - 40, cy - 130, 80, 200, 6),
                  tuple(v*.9 for v in S['sand']), a, depth=2.6, seed=620)
            for k in range(9):
                rgba(ctx, S['soot'], .36*a)
                ctx.rectangle(cx - 30, cy - 116 + k*20, 60 - (k % 3)*14, 5); ctx.fill()
            for k in range(3):
                w_ = 56 - k*12
                carve(ctx, lambda k=k, w_=w_: ctx.rectangle(cx - w_, cy - 192 + k*12, w_*2, 11),
                      S['sand'], a, depth=2.4, tex=.2, seed=630 + k)
        elif kind == 'vina':
            carve(ctx, lambda: rrect(ctx, cx - 250, cy - 140, 500, 280, 10), S['sand'], a, depth=5.)
            # two gourd resonators, a long fretted neck between them
            carve(ctx, lambda: ctx.arc(cx - 128, cy + 48, 74, 0, 2*math.pi),
                  tuple(v*.82 for v in S['clay']), a, depth=4.4, seed=640)
            carve(ctx, lambda: ctx.arc(cx + 150, cy - 56, 46, 0, 2*math.pi),
                  tuple(v*.82 for v in S['clay']), a, depth=3.6, seed=641)
            ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.36); ctx.translate(-cx, -cy)
            carve(ctx, lambda: rrect(ctx, cx - 150, cy - 18, 310, 36, 12),
                  tuple(v*.9 for v in S['clay']), a, depth=3.6, seed=642)
            for k in range(9):                      # frets
                rgba(ctx, S['ochre'], .4*a)
                ctx.rectangle(cx - 126 + k*32, cy - 15, 5, 30); ctx.fill()
            for k in range(4):                      # strings
                rgba(ctx, S['lime'], .6*a); ctx.set_line_width(2.6)
                ctx.move_to(cx - 150, cy - 10 + k*7); ctx.line_to(cx + 160, cy - 10 + k*7); ctx.stroke()
            ctx.restore()
        elif kind == 'title':
            carve(ctx, lambda: rrect(ctx, cx - 250, cy - 150, 500, 300, 10), S['sand'], a, depth=4.8)
            # a seated ruler on a dais, with a title plate being conferred above
            carve(ctx, lambda: ctx.rectangle(cx - 86, cy + 64, 172, 40),
                  tuple(v*.88 for v in S['clay']), a, depth=3.6, seed=650)
            crowd(ctx, cy + 64, [cx], .95*a, 1.7, t=t)
            carve(ctx, lambda: rrect(ctx, cx - 160, cy - 118, 320, 86, 8),
                  tuple(v*.94 for v in S['sand']), a, depth=3.2, seed=651)
            for k in range(2):
                rgba(ctx, S['ochre'], .55*a)
                ctx.rectangle(cx - 128, cy - 96 + k*30, 256 - k*96, 12); ctx.fill()
            for k in range(5):                      # a small emblem band under the plate
                rgba(ctx, S['ochre'], .34*a)
                ctx.arc(cx - 64 + k*32, cy - 18, 8, 0, 2*math.pi); ctx.fill()
        elif kind == 'province':
            carve(ctx, lambda: rrect(ctx, cx - 230, cy - 150, 460, 110, 8), S['sand'], a, depth=4.4)
            crowd(ctx, cy - 48, [cx], .9*a, 1.5, t=t)
            for i, dx in enumerate((-180, -60, 60, 180)):
                carve(ctx, lambda dx=dx: ctx.rectangle(cx + dx - 44, cy + 50, 88, 80),
                      tuple(v*.9 for v in S['clay']), a, depth=3.2, seed=660 + i)
                rgba(ctx, S['ochre'], .34*a); ctx.set_line_width(3)
                ctx.move_to(cx, cy - 10); ctx.line_to(cx + dx, cy + 44); ctx.stroke()
        elif kind == 'plateandring':
            museum.ex_copperplate(ctx, cx, cy, 1.5, a, t)
        elif kind == 'pilgrim':
            crowd(ctx, cy + 110, [cx - 40], 1.1*a, 2.4, t=t)
            carve(ctx, lambda: ctx.rectangle(cx + 54, cy - 130, 9, 240),
                  tuple(v*.8 for v in S['clay']), a, depth=3.)
            carve(ctx, lambda: rrect(ctx, cx + 96, cy - 70, 150, 190, 8), S['sand'], a, depth=4., seed=670)
            for k in range(6):
                rgba(ctx, S['soot'], .34*a)
                ctx.rectangle(cx + 118, cy - 44 + k*26, 106 - (k % 2)*30, 6); ctx.fill()
        elif kind == 'aryabhata':
            carve(ctx, lambda: rrect(ctx, cx - 230, cy - 140, 460, 280, 10), S['sand'], a, depth=5.)
            rgba(ctx, S['ochre'], .5*a); ctx.set_line_width(5)
            ctx.new_path(); ctx.arc(cx, cy - 20, 92, 0, 2*math.pi); ctx.stroke()
            carve(ctx, lambda: ctx.arc(cx, cy - 20, 40, 0, 2*math.pi),
                  tuple(v*.9 for v in S['sand']), a, depth=3., seed=680)
            rgba(ctx, S['ochre'], .42*a); ctx.set_line_width(4)
            for k in range(8):
                ang = k*math.pi/4
                ctx.move_to(cx + 44*math.cos(ang), cy - 20 + 44*math.sin(ang))
                ctx.line_to(cx + 88*math.cos(ang), cy - 20 + 88*math.sin(ang))
            ctx.stroke()
            engraved(ctx, '476 CE', cx, cy + 112, 30, a*.92, S['ochre'], 'c', serif=False)
        elif kind == 'placevalue':
            for k in range(4):
                x = cx - 240 + k*160
                carve(ctx, lambda x=x, k=k: rrect(ctx, x - 64, cy - 90, 128, 180, 8),
                      S['sand'], a, depth=4., seed=690 + k)
                if k == 2:
                    rgba(ctx, S['ochre'], .85*a); ctx.set_line_width(13)
                    ctx.new_path(); ctx.save(); ctx.translate(x, cy); ctx.scale(.72, 1.)
                    ctx.arc(0, 0, 44, 0, 2*math.pi); ctx.restore(); ctx.stroke()
                else:
                    for j in range(3):
                        rgba(ctx, S['soot'], .4*a)
                        ctx.rectangle(x - 36, cy - 44 + j*34, 72 - j*18, 10); ctx.fill()
        elif kind == 'playtitle':
            carve(ctx, lambda: rrect(ctx, cx - 250, cy - 140, 500, 280, 10), S['sand'], a, depth=5.)
            rgba(ctx, S['clay'], .8*a)
            ctx.rectangle(cx - 210, cy - 108, 420, 22); ctx.fill()
            for k in range(9):               # a hanging curtain, so it reads as theatre
                rgba(ctx, S['clay'], (.5 - (k % 2)*.12)*a)
                ctx.rectangle(cx - 206 + k*46, cy - 86, 38, 96); ctx.fill()
            for k in range(2):
                rgba(ctx, S['ochre'], .5*a)
                ctx.rectangle(cx - 150, cy + 42 + k*34, 300 - k*120, 11); ctx.fill()
        elif kind == 'narmadastop':
            ctx.new_path(); ctx.move_to(cx - 330, cy + 40)
            ctx.curve_to(cx - 100, cy - 20, cx + 100, cy + 100, cx + 330, cy + 30)
            ctx.set_source_rgba(.26, .44, .48, .66*a); ctx.set_line_width(46); ctx.stroke()
            crowd(ctx, cy - 70, [cx - 150, cx - 90, cx - 30], .85*a, 1.5, t=t)
            crowd(ctx, cy + 150, [cx + 40, cx + 100, cx + 160], .85*a, 1.5, t=t)
        elif kind == 'monastery':
            carve(ctx, lambda: ctx.rectangle(cx - 280, cy - 140, 560, 280), S['sand'], a, depth=5.4)
            for k in range(12):
                ctx.new_path()
                ctx.rectangle(cx - 250 + (k % 6)*86, cy - 104 + (k//6)*128, 60, 96)
                ctx.set_source_rgba(0, 0, 0, .74*a); ctx.fill()
        elif kind == 'regent':
            carve(ctx, lambda: rrect(ctx, cx - 190, cy - 150, 380, 108, 8), S['sand'], a, depth=4.4)
            crowd(ctx, cy + 10, [cx], 1.0*a, 2.0, t=t)
            crowd(ctx, cy + 140, [cx - 110, cx + 110], .75*a, 1.3, t=t)
        elif kind == 'cliffcaves':
            def cliff():
                ctx.move_to(cx - 400, cy + 160)
                ctx.curve_to(cx - 330, cy - 120, cx + 330, cy - 120, cx + 400, cy + 160)
                ctx.close_path()
            carve(ctx, cliff, tuple(v*1.08 for v in S['basalt']), a, depth=6., seed=700)
            ctx.save(); ctx.new_path(); cliff(); ctx.clip()
            for k in range(7):
                x = cx - 300 + k*100
                y = cy + 60 - int(abs(3 - k) * -18)
                ctx.new_path()
                ctx.move_to(x - 28, cy + 160); ctx.line_to(x - 28, y)
                ctx.curve_to(x - 28, y - 46, x + 28, y - 46, x + 28, y)
                ctx.line_to(x + 28, cy + 160); ctx.close_path()
                ctx.set_source_rgba(0, 0, 0, .8*a); ctx.fill()
            ctx.restore()
            ctx.new_path(); ctx.rectangle(cx - 420, cy + 150, 840, 40)
            ctx.set_source_rgba(.26, .44, .48, .52*a); ctx.fill()
        elif kind == 'plasterlayers':
            carve(ctx, lambda: rrect(ctx, cx - 240, cy - 130, 480, 260, 8),
                  tuple(v*1.06 for v in S['basalt']), a, depth=5.)
            for k, col in enumerate((S['clay'], S['sand'], S['lime'])):
                carve(ctx, lambda k=k: ctx.rectangle(cx - 210, cy - 96 + k*42, 420, 38),
                      col, a, depth=2.8, tex=.24, seed=710 + k)
            for k in range(5):
                rgba(ctx, (S['terra'], S['ochre'], S['clay'])[k % 3], .55*a)
                ctx.arc(cx - 150 + k*76, cy + 76, 20, 0, 2*math.pi); ctx.fill()
        elif kind == 'shikhara':
            def tower():
                ctx.move_to(cx - 96, cy + 150)
                ctx.curve_to(cx - 86, cy - 20, cx - 44, cy - 130, cx, cy - 168)
                ctx.curve_to(cx + 44, cy - 130, cx + 86, cy - 20, cx + 96, cy + 150)
                ctx.close_path()
            carve(ctx, tower, S['sand'], a, depth=5., seed=720)
            ctx.save(); ctx.new_path(); tower(); ctx.clip()
            for k in range(9):
                rgba(ctx, S['soot'], .16*a); ctx.set_line_width(4)
                ctx.move_to(cx - 110 + k*28, cy + 150); ctx.line_to(cx - 46 + k*12, cy - 150); ctx.stroke()
            ctx.restore()
            carve(ctx, lambda: ctx.arc(cx, cy - 180, 22, 0, 2*math.pi), S['sand'], a, depth=3., seed=721)
            ctx.new_path(); ctx.rectangle(cx - 20, cy + 96, 40, 54)
            ctx.set_source_rgba(0, 0, 0, .82*a); ctx.fill()
        elif kind == 'vimana':
            for k in range(6):
                w_ = 120 - k*18
                carve(ctx, lambda k=k, w_=w_: ctx.rectangle(cx - w_, cy + 126 - k*46, w_*2, 42),
                      S['sand'], a, depth=3.6, tex=.24, seed=730 + k)
                for j in range(max(1, 5 - k)):
                    rgba(ctx, S['soot'], .2*a)
                    ctx.rectangle(cx - w_ + 12 + j*(w_*2 - 24)/max(1, 5 - k), cy + 132 - k*46, 11, 18)
                    ctx.fill()
            carve(ctx, lambda: ctx.arc(cx, cy - 148, 26, math.pi, 2*math.pi), S['sand'], a, depth=3., seed=740)
            ctx.new_path(); ctx.rectangle(cx - 21, cy + 118, 42, 50)
            ctx.set_source_rgba(0, 0, 0, .82*a); ctx.fill()
        elif kind == 'citypin':
            rgba(ctx, S['ochre'], .9*a)
            ctx.arc(cx, cy, 34, 0, 2*math.pi); ctx.fill()
            for k, r in enumerate((70, 108)):
                rgba(ctx, S['ochre'], (.34 - k*.1)*a); ctx.set_line_width(4)
                ctx.new_path(); ctx.arc(cx, cy, r, 0, 2*math.pi); ctx.stroke()
            for ang in (math.pi, math.pi/3, -math.pi/3):
                rgba(ctx, S['terra'], .66*a); ctx.set_line_width(9)
                ctx.move_to(cx + 300*math.cos(ang), cy + 190*math.sin(ang))
                ctx.line_to(cx + 130*math.cos(ang), cy + 82*math.sin(ang)); ctx.stroke()
                carve(ctx, lambda ang=ang: poly(ctx, [(cx + 120*math.cos(ang), cy + 76*math.sin(ang)),
                                                      (cx + 168*math.cos(ang) - 16, cy + 106*math.sin(ang) - 16),
                                                      (cx + 168*math.cos(ang) + 16, cy + 106*math.sin(ang) + 16)]),
                      S['terra'], a, depth=2.6, seed=750)
        elif kind == 'cutpit':
            museum.ex_kailasa(ctx, cx, cy, 1.45, a, t)
        elif kind == 'potlots':
            carve(ctx, lambda: (ctx.save(), ctx.translate(cx, cy + 20), ctx.scale(1, .9),
                                ctx.arc(0, 0, 96, math.pi*.88, math.pi*2.12), ctx.restore(),
                                ctx.close_path()), tuple(v*.86 for v in S['clay']), a, depth=5.)
            for k in range(6):
                lx = cx - 70 + k*28
                carve(ctx, lambda lx=lx, k=k: rrect(ctx, lx - 9, cy - 120 + (k % 3)*14, 18, 86, 5),
                      S['sand'], a, depth=2.4, tex=.26, seed=950 + k)
        elif kind == 'tanksluice':
            carve(ctx, lambda: poly(ctx, [(cx - 340, cy - 10), (cx + 340, cy - 10),
                                          (cx + 300, cy + 54), (cx - 300, cy + 54)]),
                  tuple(v*.84 for v in S['clay']), a, depth=5.)
            ctx.new_path(); ctx.rectangle(cx - 330, cy - 130, 660, 120)
            ctx.set_source_rgba(.26, .44, .48, .62*a); ctx.fill()
            carve(ctx, lambda: ctx.rectangle(cx - 26, cy - 14, 52, 72), S['sand'], a, depth=3.4, seed=960)
            for k in range(4):
                rgba(ctx, S['moss'] if 'moss' in S else S['clay'], .38*a)
                ctx.rectangle(cx - 240 + k*130, cy + 86, 100, 46); ctx.fill()
        elif kind == 'towerplan':
            museum.ex_starplan(ctx, cx, cy, 1.7, a, t)
        elif kind == 'stepwell':
            carve(ctx, lambda: ctx.rectangle(cx - 300, cy - 150, 600, 300),
                  tuple(v*.82 for v in S['clay']), a, depth=5.)
            for k in range(7):
                w_ = 250 - k*34
                ctx.new_path(); ctx.rectangle(cx - w_, cy - 128 + k*34, w_*2, 34)
                ctx.set_source_rgba(0, 0, 0, (.2 + k*.07)*a); ctx.fill()
                carve(ctx, lambda k=k, w_=w_: ctx.rectangle(cx - w_, cy - 128 + k*34, w_*2, 9),
                      S['sand'], a, depth=1.8, tex=.2, seed=970 + k)
            ctx.new_path(); ctx.rectangle(cx - 42, cy + 110, 84, 40)
            ctx.set_source_rgba(.26, .44, .48, .74*a); ctx.fill()
        elif kind == 'altarropes':
            carve(ctx, lambda: ctx.rectangle(cx - 150, cy - 110, 300, 220), S['sand'], a, depth=4.4, seed=980)
            rgba(ctx, S['ochre'], .6*a); ctx.set_line_width(4)
            ctx.new_path(); ctx.arc(cx, cy, 124, 0, 2*math.pi); ctx.stroke()
            for dx, dy in ((-150, -110), (150, -110), (-150, 110), (150, 110)):
                carve(ctx, lambda dx=dx, dy=dy: ctx.arc(cx + dx, cy + dy, 11, 0, 2*math.pi),
                      tuple(v*.8 for v in S['clay']), a, depth=2.4, seed=990)
            rgba(ctx, S['ochre'], .42*a); ctx.set_line_width(3)
            ctx.move_to(cx - 150, cy - 110); ctx.line_to(cx + 150, cy + 110); ctx.stroke()
        elif kind == 'zerorules':
            carve(ctx, lambda: rrect(ctx, cx - 230, cy - 140, 460, 280, 10), S['sand'], a, depth=5.)
            rgba(ctx, S['verd'], .85*a); ctx.set_line_width(11)
            ctx.new_path(); ctx.arc(cx, cy - 36, 42, 0, 2*math.pi); ctx.stroke()
            for k in range(3):
                rgba(ctx, S['soot'], .36*a)
                ctx.rectangle(cx - 160, cy + 44 + k*28, 320 - k*90, 9); ctx.fill()
        elif kind == 'instruments':
            carve(ctx, lambda: rrect(ctx, cx - 270, cy - 110, 540, 220, 8),
                  tuple(v*.82 for v in S['clay']), a, depth=4.6, seed=1000)
            for k in range(6):
                px = cx - 210 + k*84
                carve(ctx, lambda px=px, k=k: rrect(ctx, px - 8, cy - 70, 16, 120 - (k % 3)*20, 6),
                      S['lime'], a, depth=2.6, tex=.18, seed=1010 + k)
                if k % 2:
                    carve(ctx, lambda px=px: ctx.arc(px, cy - 80, 15, 0, 2*math.pi),
                          S['lime'], a, depth=2.2, tex=.18, seed=1020 + k)
        elif kind == 'gatequestion':
            carve(ctx, lambda: ctx.rectangle(cx - 250, cy - 150, 500, 300), S['sand'], a, depth=5.4, seed=1030)
            ctx.new_path()
            ctx.move_to(cx - 72, cy + 150); ctx.line_to(cx - 72, cy - 10)
            ctx.curve_to(cx - 72, cy - 80, cx + 72, cy - 80, cx + 72, cy - 10)
            ctx.line_to(cx + 72, cy + 150); ctx.close_path()
            ctx.set_source_rgba(0, 0, 0, .82*a); ctx.fill()
            crowd(ctx, cy + 150, [cx - 180, cx + 180], .9*a, 1.7, t=t)
        elif kind == 'scrollfrag':
            museum.ex_staffjournal(ctx, cx, cy, 1.5, a, t)
        elif kind == 'twoscripts':
            carve(ctx, lambda: rrect(ctx, cx - 260, cy - 130, 520, 260, 8),
                  tuple(v*.8 for v in S['clay']), a, depth=4.6, seed=1040)
            for side in (-1, 1):
                carve(ctx, lambda side=side: rrect(ctx, cx + side*130 - 100, cy - 96, 200, 192, 6),
                      S['sand'], a, depth=3., seed=1050 + side)
                for k in range(6):
                    rgba(ctx, S['soot'], .34*a)
                    if side < 0:
                        ctx.rectangle(cx - 212 + 0, cy - 68 + k*28, 150 - (k % 3)*40, 6)
                    else:
                        ctx.save(); ctx.translate(cx + 62, cy - 68 + k*28); ctx.rotate(.12)
                        ctx.rectangle(0, 0, 148 - (k % 3)*38, 6); ctx.restore()
                    ctx.fill()
        elif kind == 'immunity':
            museum.ex_copperplate(ctx, cx, cy - 20, 1.45, a, t)
            for k in range(3):
                rgba(ctx, S['ochre'], .5*a)
                ctx.rectangle(cx - 120 + k*96, cy + 110, 72, 12); ctx.fill()
        elif kind == 'divertedrevenue':
            # a village, with a grant plate sealed over it: the revenue now goes elsewhere
            for i, dx in enumerate((-210, -90, 30)):
                carve(ctx, lambda dx=dx: ctx.rectangle(cx + dx - 44, cy + 46, 88, 76),
                      tuple(v*.9 for v in S['clay']), a, depth=3.4, seed=1060 + i)
                carve(ctx, lambda dx=dx: poly(ctx, [(cx + dx - 54, cy + 46), (cx + dx, cy + 8),
                                                    (cx + dx + 54, cy + 46)]),
                      tuple(v*.82 for v in S['clay']), a, depth=2.8, seed=1070 + i)
            for k in range(6):                 # the fields beyond
                rgba(ctx, S['ochre'], .22*a)
                ctx.rectangle(cx - 250 + k*86, cy + 134, 64, 20); ctx.fill()
            carve(ctx, lambda: rrect(ctx, cx + 70, cy - 120, 220, 150, 8), S['sand'], a, depth=4.4, seed=1080)
            for k in range(4):
                rgba(ctx, S['soot'], .36*a)
                ctx.rectangle(cx + 96, cy - 94 + k*30, 170 - (k % 2)*48, 7); ctx.fill()
            rgba(ctx, S['ochre'], .55*a); ctx.set_line_width(7)
            ctx.move_to(cx - 60, cy + 10); ctx.line_to(cx + 66, cy - 44); ctx.stroke()
            carve(ctx, lambda: poly(ctx, [(cx + 76, cy - 48), (cx + 36, cy - 64), (cx + 42, cy - 24)]),
                  S['ochre'], a, depth=2.4, seed=1090)
        elif kind == 'portcoins':
            ctx.new_path(); ctx.rectangle(cx - 300, cy + 30, 600, 110)
            ctx.set_source_rgba(.26, .44, .48, .58*a); ctx.fill()
            for i, dx in enumerate((-150, 60)):
                carve(ctx, lambda dx=dx: poly(ctx, [(cx + dx - 80, cy + 34), (cx + dx + 80, cy + 34),
                                                    (cx + dx + 52, cy + 86), (cx + dx - 52, cy + 86)]),
                      tuple(v*.9 for v in S['clay']), a, depth=3.6, seed=1070 + i)
                carve(ctx, lambda dx=dx: ctx.rectangle(cx + dx - 5, cy - 86, 10, 120),
                      tuple(v*.8 for v in S['clay']), a, depth=3., seed=1080 + i)
            for k in range(5):
                carve(ctx, lambda k=k: ctx.arc(cx + 150 + (k % 3)*44, cy - 100 + (k//3)*44, 20, 0, 2*math.pi),
                      S['ochre'], a, depth=2.6, tex=.18, seed=1090 + k)
        elif kind == 'letterforms':
            carve(ctx, lambda: rrect(ctx, cx - 270, cy - 130, 540, 260, 8), S['sand'], a, depth=4.8)
            for row in range(3):
                for k in range(6):
                    px = cx - 210 + k*84
                    py = cy - 80 + row*78
                    rgba(ctx, S['soot'], (.42 - row*.08)*a); ctx.set_line_width(5 - row)
                    ctx.new_path()
                    ctx.move_to(px - 16, py + 16); ctx.line_to(px - 16 + row*4, py - 16)
                    ctx.line_to(px + 16, py - 16 + (k % 2)*8); ctx.stroke()
        elif kind == 'debatehall':
            carve(ctx, lambda: ctx.rectangle(cx - 300, cy - 150, 600, 70), S['sand'], a, depth=4., seed=1100)
            crowd(ctx, cy + 120, [cx - 200, cx - 120, cx + 120, cx + 200], .8*a, 1.4, t=t)
            crowd(ctx, cy + 120, [cx], 1.0*a, 2.0, t=t)
            carve(ctx, lambda: rrect(ctx, cx - 86, cy - 70, 172, 44, 7),
                  tuple(v*.9 for v in S['sand']), a, depth=2.6, seed=1101)
        elif kind == 'verses':
            for k in range(6):
                carve(ctx, lambda k=k: rrect(ctx, cx - 210 + (k % 2)*10, cy + 110 - k*38, 420, 32, 6),
                      S['sand'], a, depth=2.8, tex=.24, seed=1110 + k)
                for j in range(4):
                    rgba(ctx, S['soot'], .3*a)
                    ctx.rectangle(cx - 180 + j*104, cy + 120 - k*38, 70 - (j % 2)*22, 6); ctx.fill()
        elif kind == 'womandonor':
            museum.ex_womentablet(ctx, cx, cy, 1.6, a, t)
        elif kind == 'undeciphered':
            carve(ctx, lambda: rrect(ctx, cx - 160, cy - 160, 320, 320, 10), S['sand'], a, depth=5.4)
            for k in range(7):
                rgba(ctx, S['soot'], .46*a)
                ctx.rectangle(cx - 120 + k*36, cy - 120, 20, 44 - (k % 3)*12); ctx.fill()
            for k in range(5):
                rgba(ctx, S['soot'], .3*a)
                ctx.rectangle(cx - 100 + k*44, cy - 40, 16, 30); ctx.fill()
            engraved(ctx, '?', cx, cy + 96, 92, a*.5, S['soot'], 'c')
        elif kind == 'mounds':
            for i, (dx, w_, h_) in enumerate(((-260, 240, 90), (20, 300, 130), (300, 200, 70))):
                carve(ctx, lambda dx=dx, w_=w_, h_=h_: (ctx.save(), ctx.translate(cx + dx, cy + 70), ctx.scale(1, h_/w_*1.6),
                                                        ctx.arc(0, 0, w_/2, math.pi, 2*math.pi), ctx.restore(), ctx.close_path()),
                      S['clay'], a, depth=5., seed=60 + i)
    return d


# ================= the builder =================
def build(cfg, EN):
    """turn a config dict into BEATS; keys are grouped by their prefix"""
    keys = [k for k, _ in EN]
    def group(pfx): return [k for k in keys if k.startswith(pfx)]
    PERIOD = cfg['period']
    EPN = cfg['ep']
    SC = {}

    # ---- dig
    digk = group('dig')
    def mk_dig(i):
        def f(ctx, t, D):
            def body(ctx, t, D, a):
                DIG(ctx, t, D, a, cfg['dig'],
                    question=cfg.get('question') if i == len(digk) - 1 else None,
                    tags=cfg.get('tags', ()) if i == 0 else (),
                    sweep=(0.4, 4.2) if i == 0 else (-9, -8),
                    t_q=D*.45)
            frame(ctx, t, D, EPN, PERIOD, body, lambda c, tt: bg_trench(c, tt))
        f.bg = 'trench'; return f
    for i, k in enumerate(digk): SC[k] = mk_dig(i)

    # ---- sources
    for i, k in enumerate(group('src')):
        def mk_src(i=i):
            def f(ctx, t, D):
                def body(ctx, t, D, a):
                    SOURCES(ctx, t, D, a, on=cfg.get('sources', ('trowel',)), note=cfg.get('src_note'))
                frame(ctx, t, D, EPN, PERIOD, body, lambda c, tt: bg_stone(c, tt, lampx=W*.5, lampy=340))
            f.bg = 'stone'; return f
        SC[k] = mk_src()

    # ---- frieze
    frzk = group('frz'); panels = cfg['panels']
    assert len(panels) >= 1
    for i, k in enumerate(frzk):
        pi = min(int(i*len(panels)/max(len(frzk), 1)), len(panels) - 1)
        nxt = min(pi + 1, len(panels) - 1)
        def mk_frz(pi=pi, nxt=nxt, last=(i == len(frzk) - 1)):
            def f(ctx, t, D):
                def body(ctx, t, D, a):
                    prog = pi + (0 if pi == nxt else ease(cl((t - (D - .8))/.8)))*(nxt - pi)
                    ox = -prog*W
                    ctx.save(); ctx.translate(ox*.32, 0)
                    rgba(ctx, S['soot'], .5*a); ctx.rectangle(-W*12, 150, W*26, H); ctx.fill()
                    ctx.restore()
                    ctx.save(); ctx.translate(ox, 0)
                    camera(ctx, t, D, (1.0, 1.03), cx=prog*W + W/2, cy=560, depth=.55)
                    for yy in (208, GY + 168):
                        for kk in range(int(len(panels)*W//58) + 6):
                            x = -60 + kk*58
                            carve(ctx, lambda x=x, yy=yy: ctx.arc(x, yy, 12, 0, 2*math.pi), S['clay'], .55*a, depth=2.6, tex=.2)
                    for j, ent in enumerate(panels):
                        draw, label = (ent if isinstance(ent, tuple) else (ent, None))
                        d_ = abs(j - prog)
                        if d_ >= .92: continue
                        near = max(0., 1 - d_*1.9)
                        if near <= 0: continue
                        draw(ctx, j*W + W/2, GY, a*near, t)
                        if label: engraved(ctx, label, j*W + W/2, 300, 30, a*near*.9, S['ochre'])
                    ctx.restore()
                frame(ctx, t, D, EPN, PERIOD, body, lambda c, tt: bg_stone(c, tt, lampx=W*.52, lampy=300, beam=False))
            f.bg = 'stone'; return f
        SC[k] = mk_frz()

    # ---- plaque
    pq = cfg['plaque']
    for i, k in enumerate(group('plq')):
        def mk_plq(i=i):
            def f(ctx, t, D):
                def body(ctx, t, D, a):
                    PLAQUE(ctx, t, D, a, kind=pq['kind'], title=pq.get('title'),
                           left=pq['left'], right=pq['right'], t0=.3 if i == 0 else -3.)
                frame(ctx, t, D, EPN, PERIOD, body, lambda c, tt: bg_stone(c, tt, lampx=W*.5, lampy=320))
            f.bg = 'stone'; return f
        SC[k] = mk_plq()

    # ---- inscription
    for k in group('ins'):
        def mk_ins():
            def f(ctx, t, D):
                def body(ctx, t, D, a):
                    lines = cfg['tip']
                    INSCRIPTION(ctx, t, D, a, lines, t0=1.4, per=max(2.4, (D - 5.5)/max(len(lines), 1)))
                frame(ctx, t, D, EPN, PERIOD, body, lambda c, tt: bg_stone(c, tt, lampx=W*.5, lampy=360, beam=False))
            f.bg = 'stone'; return f
        SC[k] = mk_ins()

    # ---- quiz
    qk = group('quiz'); cards = cfg['quiz']; mains = cfg.get('mains')
    nq = len(cards)
    for i, k in enumerate(qk):
        is_mains = (i >= nq)
        ci = min(i, nq - 1)
        def mk_q(ci=ci, is_mains=is_mains):
            def f(ctx, t, D):
                def body(ctx, t, D, a):
                    if not is_mains:
                        QUIZ(ctx, t, D, a, [cards[ci]], mains=None, t0=.35, per=D - .9,
                             prompt=cfg.get('prompt', 'PAUSE AND NAME IT'))
                    else:
                        q = ease(seg(t, .2, .9))
                        rgba(ctx, (0, 0, 0), .55*a*q); ctx.rectangle(0, 150, W, H - 150); ctx.fill()
                        engraved(ctx, 'IN MAINS', W/2, 330, 34, a*q, S['ochre'], serif=False)
                        for j, l in enumerate(wrap(ctx, mains or '', 42, 1500, True)):
                            engraved(ctx, l, W/2, 430 + j*58, 42, a*q, S['lime'])
                        mt = list(cfg.get('mains_tags', ()))
                        if mt:
                            tsz = 26
                            while tsz > 15:
                                font(ctx, tsz, True, False)
                                widths = [ctx.text_extents(l).x_advance + 46 for l in mt]
                                if sum(widths) + 40*(len(mt) - 1) <= 1720: break
                                tsz -= 2
                            gap = 40
                            total = sum(widths) + gap*(len(mt) - 1)
                            xx = W/2 - total/2
                            for j, l in enumerate(mt):
                                qq = ease(seg(t, 1.2 + j*.5, 1.7 + j*.5))
                                if qq > 0:
                                    tag(ctx, l, xx + widths[j]/2, 740, a*qq, align='c', size=tsz)
                                xx += widths[j] + gap
                frame(ctx, t, D, EPN, PERIOD, body, lambda c, tt: bg_stone(c, tt, lampx=W*.5, lampy=330, beam=False))
            f.bg = 'stone'; return f
        SC[k] = mk_q()

    # ---- gallery
    galk = group('gal')
    for i, k in enumerate(galk):
        last = (i == len(galk) - 1)
        def mk_gal(i=i, last=last):
            def f(ctx, t, D):
                def body(ctx, t, D, a):
                    GALLERY(ctx, t, D, a,
                            lambda c, tt, aa, place: museum.hall(c, tt, aa, place, upto=EPN,
                                                                 cols=min(6, max(5, EPN))),
                            facts=cfg.get('facts', ()) if i == 0 else (),
                            nxt=cfg.get('next') if last else None, t0=.4)
                    if last: SUBSCRIBE(ctx, t, D, a, D - 4.4)
                frame(ctx, t, D, EPN, False, body, lambda c, tt: bg_museum(c, tt))
            f.bg = 'museum'; return f
        SC[k] = mk_gal()

    missing = [k for k in keys if k not in SC]
    assert not missing, f'no scene for beats: {missing}'
    return [(k, n, SC[k]) for k, n in EN]


def fx_for(EN):
    keys = [k for k, _ in EN]
    out = []
    dig = [k for k in keys if k.startswith('dig')]
    ins = [k for k in keys if k.startswith('ins')]
    gal = [k for k in keys if k.startswith('gal')]
    if dig: out += [('sweep', dig[0], .3, .5), ('thud', dig[0], 2.2, .4)]
    if ins: out += [('chisel', ins[0], 1.2, .6), ('chisel', ins[0], 4.2, .6)]
    if gal: out += [('thud', gal[0], 1.1, .5)]
    return out
