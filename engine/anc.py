"""Scene templates for Ancient India, Simply Unearthed.

The seven segments of the format: DIG, SOURCES, FRIEZE, PLAQUE, INSCRIPTION, QUIZ
and GALLERY, plus the timeline ribbon that runs along the top of every scene.

Every template obeys the motion rules: a camera move on each shot, layers at
different depths, entrances that stagger, and nothing left unchanged for long.
"""
import cairo, math, random
from engine.core import W, H, cl, seg, ease, eoc, eob, lerp, rgba, rrect, font, wrap
from engine.stone import (S, carve, incise, coursed, poly, lamp, rake, lit, dust, grain,
                          vignette, camera, bg_stone, bg_museum, bg_trench, unearth, brush,
                          engraved, kinetic, ribbon, tag, corner, filmgrain, blit, cached)
from engine.monument import (crowd, haze, horizon, godrays, scalebar, moulding, pillar,
                             colonnade, stupa, temple, chaitya, fort, bg_sky, silhouette, birds)


# ---------- the frame every scene shares ----------
def frame(ctx, t, D, ep, period, body, bgfn=None, fade=.35, grainy=.05):
    """draw a scene: background, body, then ribbon, corner tag and grain on top"""
    a = ease(seg(t, 0, fade))*ease(seg(D - t, 0, fade)) if D else 1.
    if bgfn: bgfn(ctx, t)
    body(ctx, t, D, a)
    if period is not False:
        ribbon(ctx, period, a=a, t=t)
    corner(ctx, ep, a)
    filmgrain(ctx, t, grainy)


def title_in(ctx, s, y, t, t0, a=1., size=56, col=None, serif=True):
    q = seg(t, t0, t0 + .5)
    if q <= 0: return 0.
    engraved(ctx, s, W/2, y + (1 - eob(q, 1.7))*22, size, a*ease(min(q*2, 1)), col or S['lime'], 'c', serif)
    return q


# ================= DIG =================
def DIG(ctx, t, D, a, artefact, question=None, tags=(), sweep=(0.4, 3.4), t_q=None, ep_t=0.):
    """A lamp-lit trench. A brush sweeps across in a few strokes and the episode's
    artefact emerges from the soil."""
    p = eoc(seg(t, sweep[0], sweep[1]))
    ctx.save(); camera(ctx, t, D, (1.0, 1.07), cy=620, depth=1.)
    artefact(ctx, p, t, a)
    # the soil still covering it, swept away left to right
    if p < 1:
        rr = random.Random(3)
        ctx.save(); ctx.rectangle(0, 380, W, 560); ctx.clip()
        for i in range(700):
            x, y = rr.uniform(0, W), rr.uniform(380, 940)
            f = cl((x/W - p + .18)/.26)
            if f <= 0: continue
            rgba(ctx, S['clay'], a*rr.uniform(.2, .9)*f)
            ctx.arc(x, y, rr.uniform(1.2, 4.6), 0, 2*math.pi); ctx.fill()
        ctx.restore()
    # the brush, riding the edge of what is still buried
    if p < 1:
        bx = lerp(120, W - 120, p)
        ang = 1.0 + .35*math.sin(t*5.5)
        brush(ctx, bx, 470 + 26*math.sin(t*5.5), ang, a, 1.6)
        rr = random.Random(9)
        for i in range(120):
            th = rr.uniform(-2.9, -1.3); d = rr.uniform(26, 230)
            rgba(ctx, S['clay'], a*rr.uniform(.08, .40))
            ctx.arc(bx + d*math.cos(th), 540 + d*math.sin(th)*.55, rr.uniform(1, 3.2), 0, 2*math.pi); ctx.fill()
    ctx.restore()
    for i, (s_, x, y) in enumerate(tags):
        q = seg(t, 1.1 + i*.4, 1.6 + i*.4)
        if q > 0: tag(ctx, s_, x, y, a*ease(q))
    if question:
        tq = t_q if t_q is not None else D*.62
        q = seg(t, tq, tq + .6)
        if q > 0:
            rgba(ctx, (0, 0, 0), .42*a*ease(q)); ctx.rectangle(0, 880, W, 200); ctx.fill()
            for j, l in enumerate(wrap(ctx, question, 44, 1600, True)):
                engraved(ctx, l, W/2, 950 + j*54, 44, a*ease(q), S['lime'])


# ================= SOURCES =================
SRC = [('trowel', 'DUG UP'), ('leaf', 'TEXTS'), ('stone', 'INSCRIPTIONS'), ('coin', 'COINS'), ('staff', "TRAVELLERS' ACCOUNTS")]

def _src_icon(ctx, kind, x, y, s, a, col):
    if kind == 'trowel':
        carve(ctx, lambda: poly(ctx, [(x - 6*s, y - 54*s), (x + 6*s, y - 54*s), (x + 6*s, y - 8*s), (x - 6*s, y - 8*s)]), col, a, depth=2.6*s, tex=.2)
        carve(ctx, lambda: poly(ctx, [(x - 26*s, y - 8*s), (x + 26*s, y - 8*s), (x, y + 56*s)]), col, a, depth=3.2*s, tex=.25)
    elif kind == 'leaf':
        for k in range(3):
            carve(ctx, lambda k=k: rrect(ctx, x - 52*s, y - 30*s + k*22*s, 104*s, 16*s, 7*s), col, a, depth=2.4*s, tex=.2)
        rgba(ctx, S['soot'], .5*a); ctx.arc(x, y + 4*s, 4*s, 0, 2*math.pi); ctx.fill()
    elif kind == 'stone':
        carve(ctx, lambda: (ctx.move_to(x - 42*s, y + 48*s), ctx.line_to(x - 42*s, y - 26*s),
                            ctx.curve_to(x - 42*s, y - 60*s, x + 42*s, y - 60*s, x + 42*s, y - 26*s),
                            ctx.line_to(x + 42*s, y + 48*s), ctx.close_path()), col, a, depth=3.4*s)
        for k in range(4):
            rgba(ctx, S['soot'], .45*a); ctx.rectangle(x - 28*s, y - 18*s + k*17*s, 56*s, 5*s); ctx.fill()
    elif kind == 'coin':
        carve(ctx, lambda: ctx.arc(x, y + 6*s, 44*s, 0, 2*math.pi), col, a, depth=3.2*s)
        rr = random.Random(5)
        for k in range(5):
            cx_, cy_ = x + rr.uniform(-22, 22)*s, y + 6*s + rr.uniform(-22, 22)*s
            rgba(ctx, S['soot'], .45*a); ctx.arc(cx_, cy_, 6*s, 0, 2*math.pi); ctx.fill()
    elif kind == 'staff':
        carve(ctx, lambda: rrect(ctx, x - 5*s, y - 58*s, 10*s, 116*s, 5*s), col, a, depth=2.6*s, tex=.2)
        carve(ctx, lambda: ctx.arc(x, y - 62*s, 14*s, 0, 2*math.pi), col, a, depth=2.4*s, tex=.2)


def SOURCES(ctx, t, D, a, on=(), note=None, t0=.4):
    """five carved source icons; the ones this episode rests on light up"""
    ctx.save(); camera(ctx, t, D, (1.0, 1.05), cy=520)
    for i, (kind, name) in enumerate(SRC):
        x = 250 + i*355; y = 480
        q = seg(t, t0 + i*.16, t0 + i*.16 + .5)
        if q <= 0: continue
        hot = kind in on
        al = a*ease(q)*(1. if hot else .30)
        if hot: lamp(ctx, x, y + 6, 190 + 10*math.sin(t*2 + i), .34*a*ease(q))
        _src_icon(ctx, kind, x, y, 1.15, al, S['sand'] if hot else S['basalt'])
        engraved(ctx, name, x, y + 128, 23, al, S['ochre'] if hot else S['lime'], 'c', serif=False)
    ctx.restore()
    if note:
        q = seg(t, D*.45, D*.45 + .6)
        if q > 0:
            ls = [x for ln in note.split('\n') for x in wrap(ctx, ln, 34, 1180, True)]
            for j, l in enumerate(ls):
                engraved(ctx, l, 760, 740 + j*48, 34, a*ease(q), S['lime'])


# ================= FRIEZE =================
def FRIEZE(ctx, t, D, a, panels, span=5.0, t0=.0, ep_t=0., ground=760):
    """One long carved relief panel, several screen-widths wide, that the camera
    pans across. `panels` is a list of (centre_x_in_panel_widths, draw_fn, label).
    The panel is centred on whichever scene the narration has reached."""
    n = max(len(panels), 1)
    # which panel we are on, with an ease between them
    prog = cl((t - t0)/max(D - t0, .001))*(n - 1)
    i = int(prog); f = prog - i
    centre = lerp(i, min(i + 1, n - 1), ease(cl(f*1.6 - .3)))
    ox = -centre*W + W/2
    # back wall of the panel, with its carved border top and bottom
    for depth_, yoff in ((0.45, 0), (1.0, 0)):
        pass
    ctx.save()
    ctx.translate(ox*0.35, 0)              # far plane: the wall behind, parallax
    rgba(ctx, S['soot'], .55*a); ctx.rectangle(-W*n, 150, W*n*3, H); ctx.fill()
    ctx.restore()
    ctx.save()
    ctx.translate(ox, 0)
    camera(ctx, t, D, (1.0, 1.035), cx=centre*W + W/2, cy=560, depth=.6)
    # the border motif, repeating the full length of the panel
    for yy in (214, ground + 150):
        for k in range(int(n*W//58) + 4):
            x = -60 + k*58
            carve(ctx, lambda x=x, yy=yy: ctx.arc(x, yy, 13, 0, 2*math.pi), S['clay'], .75*a, depth=2.8, tex=.2)
            carve(ctx, lambda x=x, yy=yy: ctx.arc(x + 29, yy, 6, 0, 2*math.pi), S['sand'], .6*a, depth=2., tex=0)
    for j, (px, draw, label) in enumerate(panels):
        near = cl(1.25 - abs(px - centre))
        if near <= 0: continue
        draw(ctx, px*W + W/2, ground, a*near, t)
        if label:
            engraved(ctx, label, px*W + W/2, ground + 108, 27, a*near*.95, S['ochre'], 'c')
    ctx.restore()


def panel_text(lines, size=34, dy=0):
    def d(ctx, cx, gy, a, t):
        for j, l in enumerate(lines):
            engraved(ctx, l, cx, gy - 240 + dy + j*48, size, a, S['lime'])
    return d


# ================= PLAQUE =================
def PLAQUE(ctx, t, D, a, kind='names', left=None, right=None, title=None, t0=.3):
    """either one plaque with two names joined by an arrow, or two tablets of equal
    size under 'Scholars disagree'"""
    ctx.save(); camera(ctx, t, D, (1.0, 1.045), cy=520)
    if kind == 'names':
        q = seg(t, t0, t0 + .6)
        if q > 0:
            carve(ctx, lambda: rrect(ctx, 260, 380, 1400, 300, 14), S['clay'], a*ease(q), depth=6.)
            engraved(ctx, left, 560, 545, 58, a*ease(q), S['lime'])
            engraved(ctx, right, 1360, 545, 58, a*ease(seg(t, t0 + .7, t0 + 1.2)), S['ochre'])
            aq = eoc(seg(t, t0 + .5, t0 + 1.1))
            if aq > 0:
                rgba(ctx, S['ochre'], a*.9); ctx.set_line_width(7)
                ctx.move_to(880, 530); ctx.line_to(880 + 180*aq, 530); ctx.stroke()
                if aq > .85:
                    poly(ctx, [(1060, 530), (1030, 514), (1030, 546)]); ctx.fill()
    else:
        title_in(ctx, title or 'SCHOLARS DISAGREE', 290, t, t0, a, 54, S['ochre'])
        for i, body in enumerate((left, right)):
            q = seg(t, t0 + .5 + i*.45, t0 + 1.1 + i*.45)
            if q <= 0: continue
            x = 110 + i*880; qa = a*ease(q)
            carve(ctx, lambda x=x: rrect(ctx, x, 370, 800, 420, 12), S['clay'], qa, depth=5.5)
            for j, l in enumerate(wrap(ctx, body, 34, 700, True)):
                engraved(ctx, l, x + 400, 460 + j*52, 34, qa, S['lime'])
        q = seg(t, D - 2.2, D - 1.6)
        if q > 0:
            engraved(ctx, 'THE EVIDENCE ALLOWS BOTH READINGS', W/2, 870, 30, a*ease(q), S['ochre'], serif=False)
    ctx.restore()


# ================= INSCRIPTION =================
def INSCRIPTION(ctx, t, D, a, lines, t0=.5, per=1.5):
    """a stone tablet; a chisel cuts the tip in, then the grooves fill with verdigris"""
    ctx.save(); camera(ctx, t, D, (1.0, 1.05), cy=500)
    carve(ctx, lambda: rrect(ctx, 250, 250, 1420, 500, 16), S['clay'], a, depth=8.)
    moulding(ctx, 250, 250, 1420, 46, a, S['clay'], 2, depth=3.)
    n = len(lines)
    y0 = 500 - (n - 1)*78/2
    done = t0 + n*per
    for i, l in enumerate(lines):
        ts = t0 + i*per
        q = cl((t - ts)/per)
        if q <= 0: continue
        font(ctx, 54, True, True)
        full = ctx.text_extents(l).x_advance
        cut = max(1, int(len(l)*q))
        engraved(ctx, l[:cut], W/2 - full/2, y0 + i*78, 54, a, S['lime'], 'l')
        if q < 1:
            # the chisel, working along the line
            cx = W/2 - full/2 + ctx.text_extents(l[:cut]).x_advance
            jitter = 5*math.sin(t*34)
            ctx.save(); ctx.translate(cx + 26, y0 + i*78 - 58 + jitter); ctx.rotate(.55)
            carve(ctx, lambda: poly(ctx, [(-9, -84), (9, -84), (9, -6), (0, 10), (-9, -6)]), S['basalt'], a, depth=2.6, tex=.2)
            ctx.restore()
            rr = random.Random(int(t*20))
            for k in range(7):
                rgba(ctx, S['dust'], a*rr.uniform(.2, .8))
                ctx.arc(cx + rr.uniform(-16, 16), y0 + i*78 + rr.uniform(-14, 10), rr.uniform(1, 3), 0, 2*math.pi); ctx.fill()
    # the grooves fill with verdigris and glow
    gq = ease(seg(t, done, done + 1.3))
    if gq > 0:
        for i, l in enumerate(lines):
            font(ctx, 54, True, True)
            e = ctx.text_extents(l)
            ctx.save()
            ctx.move_to(W/2 - e.x_advance/2, y0 + i*78); ctx.text_path(l)
            rgba(ctx, S['verd'], .92*gq*a); ctx.fill(); ctx.restore()
        lamp(ctx, W/2, 500, 560 + 24*math.sin(t*1.8), .20*gq*a, S['verd'], core=.26)
    ctx.restore()


# ================= QUIZ =================
def QUIZ(ctx, t, D, a, cards, mains=None, t0=.3, per=None, prompt='PAUSE AND NAME IT'):
    """three carved artefact cards, each with a 3-2-1 ring, then the answer carved
    in beneath; then one Mains line"""
    per = per or (D - 2.5 - (3.0 if mains else 0))/max(len(cards), 1)
    ctx.save(); camera(ctx, t, D, (1.0, 1.04), cy=520)
    for i, (draw, answer) in enumerate(cards):
        ts = t0 + i*per
        q = seg(t, ts, ts + per)
        if q <= 0 or t > ts + per + .4: continue
        local = t - ts
        qa = a*ease(seg(local, 0, .45))*ease(seg(per + .4 - local, 0, .4))
        rise = (1 - eob(cl(local/.6), 1.5))*120
        ctx.save(); ctx.translate(0, rise)
        carve(ctx, lambda: rrect(ctx, 430, 210, 1060, 540, 16), S['clay'], qa, depth=6.5)
        ctx.save(); ctx.translate(960, 500); ctx.scale(1.35, 1.35); ctx.translate(-960, -500)
        draw(ctx, 960, 500, qa, t); ctx.restore()
        ctx.restore()
        # the 3-2-1 ring
        cd = per*.52
        if local < cd:
            left = cd - local
            num = int(left) + 1
            frac = left - int(left)
            cx_, cy_ = 1640, 350
            ctx.new_path(); rgba(ctx, S['basalt'], .9*qa); ctx.arc(cx_, cy_, 78, 0, 2*math.pi); ctx.fill()
            ctx.new_path(); rgba(ctx, S['ochre'], qa); ctx.set_line_width(9)
            ctx.arc(cx_, cy_, 78, -math.pi/2, -math.pi/2 + 2*math.pi*frac); ctx.stroke()
            engraved(ctx, str(min(num, 3)), cx_, cy_ + 26, 68, qa, S['lime'])
            engraved(ctx, prompt, 960, 828, 34, qa, S['ochre'], serif=False)
        else:
            aq = ease(cl((local - cd)/.5))
            carve(ctx, lambda: rrect(ctx, 430, 782, 1060, 112, 10), S['basalt'], qa*aq, depth=4.)
            engraved(ctx, answer, 960, 856, 46, qa*aq, S['lime'])
    ctx.restore()
    if mains:
        mt = t0 + len(cards)*per + .3
        q = seg(t, mt, mt + .6)
        if q > 0:
            qa = a*ease(q)
            rgba(ctx, (0, 0, 0), .7*qa); ctx.rectangle(0, 150, W, H - 150); ctx.fill()
            engraved(ctx, 'IN MAINS', W/2, 400, 34, qa, S['ochre'], serif=False)
            for j, l in enumerate(wrap(ctx, mains, 40, 1500, True)):
                engraved(ctx, l, W/2, 490 + j*58, 40, qa*ease(seg(t, mt + .3 + j*.25, mt + .7 + j*.25)), S['lime'])


# ================= GALLERY =================
def GALLERY(ctx, t, D, a, hall, facts=(), nxt=None, t0=.4):
    """the museum hall; this episode's exhibit is placed in its case with a thud,
    then the label, then the next gallery"""
    ctx.save(); camera(ctx, t, D, (1.0, 1.05), cx=W*.42, cy=560, pan=(-40, 0))
    hall(ctx, t, a, eoc(seg(t, t0, t0 + 1.0)))
    ctx.restore()
    if facts:
        q = seg(t, t0 + 1.1, t0 + 1.7)
        if q > 0:
            qa = a*ease(q)
            carve(ctx, lambda: rrect(ctx, 1300, 170, 560, 300, 12), S['lime'], qa, depth=5.)
            engraved(ctx, 'MUSEUM LABEL', 1580, 226, 24, qa, S['soot'], serif=False)
            rgba(ctx, S['soot'], .35*qa); ctx.rectangle(1340, 246, 480, 2); ctx.fill()
            for j, f in enumerate(facts):
                fq = ease(seg(t, t0 + 1.5 + j*.3, t0 + 1.9 + j*.3))
                for k, l in enumerate(wrap(ctx, f, 26, 470, False)):
                    engraved(ctx, l, 1340, 300 + j*56 + k*31, 26, qa*fq, S['soot'], 'l', lit_=.0)
    if nxt:
        q = seg(t, D - 3.2, D - 2.6)
        if q > 0:
            qa = a*ease(q)
            rgba(ctx, (0, 0, 0), .78*qa); ctx.rectangle(0, 840, W*eoc(seg(t, D - 3.2, D - 2.4)), 110); ctx.fill()
            rgba(ctx, S['ochre'], qa); ctx.rectangle(0, 840, W*eoc(seg(t, D - 3.2, D - 2.4)), 3); ctx.fill()
            engraved(ctx, f'NEXT GALLERY  ·  {nxt}', 80, 910, 36, qa, S['lime'], 'l', serif=False)


def SUBSCRIBE(ctx, t, D, a, t0):
    """the one neutral subscribe card, at the very end and nowhere else"""
    q = seg(t, t0, t0 + .6)
    if q <= 0: return
    qa = a*ease(q)
    carve(ctx, lambda: rrect(ctx, 700, 920, 520, 104, 10), S['basalt'], qa, depth=4.)
    engraved(ctx, 'SUBSCRIBE  ·  GyaanXstudios', 960, 984, 28, qa, S['lime'], 'c', serif=False)
