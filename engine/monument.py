"""Monumental architecture for Ancient India, Simply Unearthed.

Scale is the whole trick. A tower is only grand next to something small, so almost
every form here takes a `figures` flag that sets generic human silhouettes at its
base. Light does the rest: shafts with volume, haze between planes, and a low
horizon so structures rise out of the top of the frame.

Nothing revered is ever drawn: no deity, no founder, no face. A sanctum doorway is
a dark opening and stays empty. The Sarnath lion capital is never drawn (its use is
restricted by law); pillar capitals here are lotus, bull or wheel.
"""
import cairo, math, random
from engine.core import W, H, cl, seg, ease, eoc, eob, lerp, rgba, rrect, font
from engine.stone import S, carve, incise, coursed, poly, lamp, grain, engraved, tag


# ---------- atmosphere ----------
def haze(ctx, y0, y1, a=.30, col=None):
    """atmospheric perspective: a band of haze that pushes a plane backwards"""
    col = col or S['sand']
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgba(0, col[0], col[1]*.9, col[2]*.74, a)
    g.add_color_stop_rgba(1, col[0], col[1]*.9, col[2]*.74, 0)
    ctx.set_source(g); ctx.rectangle(0, y0, W, y1 - y0); ctx.fill()


def godrays(ctx, x, y, t, a=.3, n=7, spread=1.05, length=1250, warm=None):
    """shafts of light with volume, fanning down from a high source"""
    if a <= 0: return
    warm = warm or S['lampw']
    ctx.save(); ctx.set_operator(cairo.OPERATOR_ADD)
    rr = random.Random(4)
    for i in range(n):
        base = -math.pi/2 + (i - (n - 1)/2)*(spread/n)
        ang = base + .035*math.sin(t*.3 + i*1.7)
        wdt = rr.uniform(34, 110)*(1 + .12*math.sin(t*.45 + i))
        x2, y2 = x - length*math.cos(ang), y - length*math.sin(ang)
        ctx.save()
        ctx.translate(x, y); ctx.rotate(math.atan2(y2 - y, x2 - x) + math.pi/2); ctx.translate(-x, -y)
        g = cairo.LinearGradient(0, y, 0, y + length)
        al = a*rr.uniform(.5, 1.)
        g.add_color_stop_rgba(0, warm[0], warm[1], warm[2], al)
        g.add_color_stop_rgba(1, warm[0], warm[1], warm[2], 0)
        ctx.set_source(g)
        poly(ctx, [(x - wdt*.35, y), (x + wdt*.35, y), (x + wdt*1.7, y + length), (x - wdt*1.7, y + length)])
        ctx.fill(); ctx.restore()
    ctx.restore()


def horizon(ctx, y, t, a=1., far=3):
    """receding ridges behind a monument, each hazier than the last"""
    for k in range(far):
        f = (k + 1)/far
        col = tuple(lerp(v, S['sand'][i]*.8, f*.55) for i, v in enumerate(S['basalt']))
        ctx.new_path(); ctx.move_to(-20, H)
        for x in range(-20, W + 61, 60):
            yy = y - 70*(1 - f) - 30*f*math.sin(x*.0016 + k*2.1) - 46*(1 - f)*math.sin(x*.0029 + k)
            ctx.line_to(x, yy)
        ctx.line_to(W + 40, H); ctx.close_path()
        rgba(ctx, col, a*(.9 - .18*k)); ctx.fill()


# ---------- scale ----------
def crowd(ctx, y, xs, a=.9, s=1., col=None, t=0., seed=2):
    """generic human silhouettes, for scale only. No faces, no identity."""
    col = col or S['soot']
    rr = random.Random(seed)
    for i, x in enumerate(xs):
        sc = s*rr.uniform(.9, 1.12)
        sway = .7*math.sin(t*.8 + i*1.3)
        ctx.save(); ctx.translate(x + sway, y); ctx.scale(sc, sc)
        rgba(ctx, col, a)
        ctx.arc(0, -46, 6.5, 0, 2*math.pi); ctx.fill()
        poly(ctx, [(-8, -38), (8, -38), (11, -6), (5, 0), (-5, 0), (-11, -6)]); ctx.fill()
        ctx.set_line_width(4.2); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(-4, 0); ctx.line_to(-5, 20); ctx.stroke()
        ctx.move_to(4, 0); ctx.line_to(6, 20); ctx.stroke()
        ctx.restore()


def scalebar(ctx, x, y, h, label, a=1.):
    """a measured height marker — grandeur you can check"""
    rgba(ctx, S['ochre'], .8*a); ctx.set_line_width(2)
    ctx.move_to(x, y); ctx.line_to(x, y - h); ctx.stroke()
    for yy in (y, y - h):
        ctx.move_to(x - 11, yy); ctx.line_to(x + 11, yy); ctx.stroke()
    ctx.save(); ctx.translate(x - 16, y - h/2); ctx.rotate(-math.pi/2)
    engraved(ctx, label, 0, 0, 22, a, S['ochre'], 'c', serif=False)
    ctx.restore()


# ---------- building blocks ----------
def moulding(ctx, x, y, w, h, a=1., col=None, n=3, depth=3.):
    """a horizontal band of stepped mouldings — the thing that makes stone look built"""
    col = col or S['sand']
    for i in range(n):
        f = i/max(n - 1, 1)
        inset = w*.035*i
        hh = h/n
        carve(ctx, lambda inset=inset, i=i, hh=hh: ctx.rectangle(x + inset, y + i*hh, w - inset*2, hh + 1),
              tuple(min(1, v*(1 + f*.10)) for v in col), a, depth=depth, seed=50 + i, tex=.35)


def pillar(ctx, x, y, h, a=1., s=1., col=None, capital='lotus', depth=4.):
    """a free-standing polished pillar. Capitals: lotus, bull or wheel — never the
    Sarnath lion capital."""
    col = col or S['sand']
    w = 26*s
    carve(ctx, lambda: poly(ctx, [(x - w*1.5, y), (x + w*1.5, y), (x + w*1.15, y - 26*s), (x - w*1.15, y - 26*s)]),
          col, a, depth=depth, seed=61)
    # a gently tapering shaft
    carve(ctx, lambda: poly(ctx, [(x - w, y - 26*s), (x + w, y - 26*s), (x + w*.74, y - h), (x - w*.74, y - h)]),
          col, a, depth=depth, seed=62)
    ty = y - h
    if capital == 'lotus':
        # inverted lotus bell
        carve(ctx, lambda: (ctx.move_to(x - w*.74, ty),
                            ctx.curve_to(x - w*1.9, ty - 16*s, x - w*1.75, ty - 40*s, x - w*1.1, ty - 46*s),
                            ctx.line_to(x + w*1.1, ty - 46*s),
                            ctx.curve_to(x + w*1.75, ty - 40*s, x + w*1.9, ty - 16*s, x + w*.74, ty),
                            ctx.close_path()), col, a, depth=depth, seed=63)
        for k in range(7):
            f = (k - 3)/3.
            rgba(ctx, S['soot'], .26*a); ctx.set_line_width(2.4*s)
            ctx.move_to(x + f*w*.7, ty - 2*s); ctx.line_to(x + f*w*1.6, ty - 42*s); ctx.stroke()
        carve(ctx, lambda: ctx.rectangle(x - w*1.35, ty - 64*s, w*2.7, 20*s), col, a, depth=depth*.8, seed=64)
        carve(ctx, lambda: ctx.rectangle(x - w*1.6, ty - 78*s, w*3.2, 16*s),
              tuple(min(1, v*1.08) for v in col), a, depth=depth*.7, tex=.25, seed=69)
    elif capital == 'wheel':
        carve(ctx, lambda: ctx.rectangle(x - w*1.3, ty - 22*s, w*2.6, 22*s), col, a, depth=depth*.8, seed=65)
        carve(ctx, lambda: ctx.arc(x, ty - 66*s, 44*s, 0, 2*math.pi), col, a, depth=depth, seed=66)
        for k in range(12):
            th = k*math.pi/6
            rgba(ctx, S['soot'], .45*a); ctx.set_line_width(3*s)
            ctx.move_to(x, ty - 66*s); ctx.line_to(x + 40*s*math.cos(th), ty - 66*s + 40*s*math.sin(th)); ctx.stroke()
    elif capital == 'bull':
        carve(ctx, lambda: ctx.rectangle(x - w*1.3, ty - 22*s, w*2.6, 22*s), col, a, depth=depth*.8, seed=67)
        carve(ctx, lambda: (poly(ctx, [(x - 52*s, ty - 30*s), (x + 44*s, ty - 30*s), (x + 50*s, ty - 54*s),
                                       (x + 30*s, ty - 70*s), (x - 40*s, ty - 70*s), (x - 56*s, ty - 50*s)])),
              col, a, depth=depth, seed=68)
        for sgn in (-1, 1):
            carve(ctx, lambda sgn=sgn: ctx.arc(x + sgn*30*s, ty - 78*s, 9*s, 0, 2*math.pi), col, a, depth=2.4, tex=.2)


def colonnade(ctx, x0, y, n, gap, h, a=1., recede=.72, s=1., col=None):
    """a row of pillars receding into the dark — the cheapest grandeur there is"""
    col = col or S['sand']
    for i in range(n - 1, -1, -1):
        f = i/max(n - 1, 1)
        sc = s*lerp(1., recede, f)
        xx = x0 + gap*sum(lerp(1., recede, k/max(n - 1, 1)) for k in range(i))
        yy = y - 40*f*(1 - recede)*s
        pillar(ctx, xx, yy, h*sc, a*lerp(1., .34, f), sc, col, 'lotus', depth=4.*sc)


def stupa(ctx, cx, y, s=1., a=1., col=None, torana=True, figures=True, t=0.):
    """A stupa: drum, dome, harmika and tiered umbrellas, inside a railing with a
    gateway. Drawn as architecture; nothing revered is depicted."""
    col = col or S['lime']
    R = 250*s
    # jagati: the raised circular terrace
    carve(ctx, lambda: ctx.rectangle(cx - R*1.5, y - 30*s, R*3, 34*s), tuple(v*.92 for v in col), a, depth=5*s, seed=70)
    # medhi: the drum
    carve(ctx, lambda: ctx.rectangle(cx - R*1.08, y - 118*s, R*2.16, 92*s), col, a, depth=5.5*s, seed=71)
    coursed(ctx, cx - R*1.08, y - 118*s, R*2.16, 92*s, a*.8, seed=72, course=26*s)
    # anda: the dome
    carve(ctx, lambda: (ctx.save(), ctx.translate(cx, y - 118*s), ctx.scale(1, .84),
                        ctx.arc(0, 0, R, math.pi, 2*math.pi), ctx.restore(), ctx.close_path()),
          col, a, depth=6*s, seed=73)
    # harmika: the square railing on the summit
    hy = y - 118*s - R*.84
    carve(ctx, lambda: ctx.rectangle(cx - 52*s, hy - 44*s, 104*s, 46*s), tuple(v*.95 for v in col), a, depth=4*s, seed=74)
    for k in range(3):
        rgba(ctx, S['soot'], .35*a); ctx.rectangle(cx - 52*s, hy - 36*s + k*13*s, 104*s, 3.5*s); ctx.fill()
    # yashti and chhatravali: the mast and its three umbrellas
    for k, rw in enumerate((78, 60, 42)):
        yy = hy - 60*s - k*42*s
        carve(ctx, lambda yy=yy, rw=rw: (ctx.save(), ctx.translate(cx, yy), ctx.scale(1, .26),
                                         ctx.arc(0, 0, rw*s, 0, 2*math.pi), ctx.restore(), ctx.close_path()),
              col, a, depth=3.4*s, tex=.2, seed=76 + k)
        carve(ctx, lambda yy=yy: ctx.rectangle(cx - 6*s, yy, 12*s, 44*s), tuple(v*.9 for v in col), a,
              depth=2.6*s, tex=.2, seed=79 + k)
    # vedika: the railing in front, with its uprights and three cross-bars
    for i in range(int(R*3.4//(46*s))):
        px = cx - R*1.7 + i*46*s
        carve(ctx, lambda px=px: ctx.rectangle(px, y - 2*s, 13*s, 88*s), tuple(v*.88 for v in col), a, depth=3.2*s, tex=.3, seed=80 + i)
    for k in range(3):
        rgba(ctx, col, .55*a)
        ctx.rectangle(cx - R*1.7, y + 14*s + k*26*s, R*3.4, 11*s); ctx.fill()
        rgba(ctx, S['soot'], .32*a)
        ctx.rectangle(cx - R*1.7, y + 14*s + k*26*s + 11*s, R*3.4, 3*s); ctx.fill()
    if torana:
        # the gateway: two posts and three curved architraves
        for sgn in (-1, 1):
            px = cx + sgn*R*.46
            carve(ctx, lambda px=px: ctx.rectangle(px - 15*s, y - 330*s, 30*s, 330*s), col, a, depth=4*s, seed=90)
        for k in range(3):
            yy = y - 258*s - k*52*s
            carve(ctx, lambda yy=yy: (ctx.move_to(cx - R*.78, yy),
                                      ctx.curve_to(cx - R*.3, yy - 22*s, cx + R*.3, yy - 22*s, cx + R*.78, yy),
                                      ctx.line_to(cx + R*.78, yy + 22*s),
                                      ctx.curve_to(cx + R*.3, yy, cx - R*.3, yy, cx - R*.78, yy + 22*s),
                                      ctx.close_path()), col, a, depth=3.6*s, seed=91 + k)
    if figures:
        crowd(ctx, y + 92*s, [cx - R*1.9, cx - R*1.62, cx + R*1.72, cx + R*1.95, cx + R*2.2], .85*a, s*1.05, t=t)


def temple(ctx, cx, y, s=1., a=1., col=None, style='nagara', figures=True, t=0., tiers=5):
    """An early temple in elevation: plinth, hall, and the tower over the sanctum.
    The sanctum doorway is a dark opening and stays empty."""
    col = col or S['sand']
    # jagati: the plinth everything stands on
    moulding(ctx, cx - 430*s, y - 70*s, 860*s, 70*s, a, col, 3, depth=4.4*s)
    # steps up to it
    for k in range(4):
        carve(ctx, lambda k=k: ctx.rectangle(cx - (120 - k*16)*s, y - (16 + k*17)*s, (240 - k*32)*s, 19*s),
              tuple(v*.94 for v in col), a, depth=2.8*s, seed=100 + k)
    bx, by = cx - 430*s, y - 70*s
    # mandapa: the pillared hall in front, with a low pyramidal roof
    carve(ctx, lambda: ctx.rectangle(bx + 30*s, by - 190*s, 340*s, 190*s), col, a, depth=5*s, seed=110)
    for k in range(4):
        px = bx + 60*s + k*86*s
        carve(ctx, lambda px=px: ctx.rectangle(px, by - 182*s, 26*s, 182*s), tuple(min(1, v*1.07) for v in col), a, depth=3.4*s, seed=111 + k)
    for k in range(4):
        iw = 360 - k*70
        carve(ctx, lambda k=k, iw=iw: ctx.rectangle(bx + 30*s + (360 - iw)*s/2, by - (190 + 34 + k*30)*s, iw*s, 34*s),
              tuple(v*(1 - .03*k) for v in col), a, depth=3.6*s, seed=120 + k)
    if style == 'nagara':
        # shikhara: a curvilinear tower, narrowing as it rises
        TH = 560*s; bw = 300*s
        def curve(side):
            pts = []
            for i in range(31):
                f = i/30
                w_ = bw*(1 - .62*f*f)*.5
                pts.append((cx + 170*s + side*w_, by - TH*f))
            return pts
        left = curve(-1); right = curve(1)[::-1]
        carve(ctx, lambda: poly(ctx, left + right), col, a, depth=6*s, seed=130)
        # the vertical bands (lata) that give a shikhara its ribbed look
        for b in (-.62, -.21, .21, .62):
            ctx.save(); ctx.new_path(); poly(ctx, left + right); ctx.clip()
            ctx.new_path()
            for i, (px, py) in enumerate(curve(1)):
                xx = cx + 170*s + b*(px - cx - 170*s)*1.0
                (ctx.move_to if i == 0 else ctx.line_to)(xx, py)
            rgba(ctx, S['soot'], .30*a); ctx.set_line_width(7*s); ctx.stroke()
            ctx.restore()
        # amalaka: the ribbed disc, and the kalasha above it
        ay = by - TH
        carve(ctx, lambda: (ctx.save(), ctx.translate(cx + 170*s, ay), ctx.scale(1, .52),
                            ctx.arc(0, 0, 62*s, 0, 2*math.pi), ctx.restore(), ctx.close_path()),
              tuple(min(1, v*1.06) for v in col), a, depth=4.4*s, seed=131)
        for k in range(9):
            th = -math.pi + k*math.pi/8
            rgba(ctx, S['soot'], .30*a); ctx.set_line_width(2.6*s)
            ctx.move_to(cx + 170*s + 58*s*math.cos(th), ay + 30*s*math.sin(th))
            ctx.line_to(cx + 170*s + 58*s*math.cos(th), ay - 30*s*math.sin(th)); ctx.stroke()
        carve(ctx, lambda: poly(ctx, [(cx + 152*s, ay - 30*s), (cx + 188*s, ay - 30*s),
                                      (cx + 180*s, ay - 72*s), (cx + 160*s, ay - 72*s)]), col, a, depth=3*s, seed=132)
        sanc_x = cx + 170*s
    else:
        # dravida vimana: diminishing storeys topped by a small domed finial
        yy = by; wdt = 330*s
        for k in range(tiers):
            hh = 84*s*(1 - k*.06)
            carve(ctx, lambda yy=yy, wdt=wdt, hh=hh: ctx.rectangle(cx + 170*s - wdt/2, yy - hh, wdt, hh),
                  tuple(v*(1 - .018*k) for v in col), a, depth=5*s, seed=140 + k)
            # the row of small shrine cells along each cornice
            nc = max(3, int(wdt//(52*s)))
            for j in range(nc):
                px = cx + 170*s - wdt/2 + 8*s + j*(wdt - 16*s)/nc
                carve(ctx, lambda px=px, yy=yy, wdt=wdt, nc=nc: ctx.rectangle(px, yy - 18*s, (wdt - 16*s)/nc - 7*s, 18*s),
                      tuple(min(1, v*1.1) for v in col), a, depth=2.4*s, tex=.2, seed=150 + j)
            yy -= hh; wdt *= .855
        carve(ctx, lambda yy=yy: (ctx.save(), ctx.translate(cx + 170*s, yy), ctx.scale(1, .72),
                                  ctx.arc(0, 0, 64*s, math.pi, 2*math.pi), ctx.restore(), ctx.close_path()),
              col, a, depth=4.4*s, seed=160)
        sanc_x = cx + 170*s
    # the sanctum doorway: a dark opening, deliberately empty
    dw, dh = 74*s, 150*s
    ctx.new_path(); ctx.rectangle(sanc_x - dw/2, by - dh, dw, dh)
    ctx.set_source_rgba(0, 0, 0, .88*a); ctx.fill()
    ctx.new_path(); ctx.rectangle(sanc_x - dw/2 - 9*s, by - dh - 11*s, dw + 18*s, 12*s)
    rgba(ctx, tuple(min(1, v*1.1) for v in col), a); ctx.fill()
    for sgn in (-1, 1):
        carve(ctx, lambda sgn=sgn: ctx.rectangle(sanc_x + sgn*(dw/2) - 5*s, by - dh, 10*s, dh),
              tuple(min(1, v*1.08) for v in col), a, depth=2.4*s, tex=.2, seed=170)
    if figures:
        crowd(ctx, y + 6*s, [cx - 560*s, cx - 516*s, cx + 500*s, cx + 548*s, cx + 596*s], .85*a, s*1.1, t=t)


def chaitya(ctx, cx, y, s=1., a=1., col=None, figures=True, t=0.):
    """a rock-cut hall facade: the great horseshoe window over a pillared verandah"""
    col = col or S['clay']
    Wd, Ht = 560*s, 620*s
    # the cliff face the hall is cut into
    carve(ctx, lambda: ctx.rectangle(cx - Wd, y - Ht, Wd*2, Ht), tuple(v*.78 for v in col), a, depth=7*s, tex=.6, seed=180)
    # the horseshoe window
    def arch():
        ctx.move_to(cx - 150*s, y - Ht*.52)
        ctx.curve_to(cx - 168*s, y - Ht*.86, cx + 168*s, y - Ht*.86, cx + 150*s, y - Ht*.52)
        ctx.curve_to(cx + 120*s, y - Ht*.44, cx - 120*s, y - Ht*.44, cx - 150*s, y - Ht*.52)
        ctx.close_path()
    ctx.new_path(); arch(); ctx.set_source_rgba(0, 0, 0, .9*a); ctx.fill()
    ctx.save(); ctx.new_path(); arch(); ctx.set_line_width(13*s)
    rgba(ctx, tuple(min(1, v*1.22) for v in col), a); ctx.stroke(); ctx.restore()
    for k in range(7):
        th = math.pi + k*math.pi/6
        rgba(ctx, col, .5*a); ctx.set_line_width(6*s)
        ctx.move_to(cx, y - Ht*.56); ctx.line_to(cx + 150*s*math.cos(th), y - Ht*.56 + 150*s*math.sin(th)); ctx.stroke()
    # the verandah below it
    carve(ctx, lambda: ctx.rectangle(cx - 260*s, y - Ht*.40, 520*s, 22*s), tuple(min(1, v*1.1) for v in col), a, depth=4*s, seed=181)
    for k in range(5):
        px = cx - 220*s + k*110*s
        pillar(ctx, px, y, Ht*.38, a, s*.85, tuple(min(1, v*1.06) for v in col), 'lotus', depth=3.6*s)
    ctx.new_path(); ctx.rectangle(cx - 88*s, y - Ht*.33, 176*s, Ht*.33)
    ctx.set_source_rgba(0, 0, 0, .86*a); ctx.fill()
    if figures:
        crowd(ctx, y + 4*s, [cx - 360*s, cx - 318*s, cx + 330*s, cx + 372*s], .85*a, s, t=t)


def fort(ctx, y, s=1., a=1., col=None, t=0., gate=True):
    """a fortified city wall running across the frame, with bastions and a gateway"""
    col = col or S['clay']
    Ht = 300*s
    carve(ctx, lambda: ctx.rectangle(-20, y - Ht, W + 40, Ht), col, a, depth=6*s, seed=190)
    coursed(ctx, -20, y - Ht, W + 40, Ht, a*.85, seed=191, course=30*s)
    for i in range(int((W + 120)//(66*s))):
        bx = -40 + i*66*s
        carve(ctx, lambda bx=bx: ctx.rectangle(bx, y - Ht - 36*s, 40*s, 40*s), col, a, depth=3.4*s, tex=.3, seed=200 + i)
    for bx in (250*s, W - 250*s):
        carve(ctx, lambda bx=bx: ctx.rectangle(bx - 86*s, y - Ht - 60*s, 172*s, Ht + 60*s),
              tuple(min(1, v*1.07) for v in col), a, depth=6*s, seed=210)
        for k in range(5):
            carve(ctx, lambda bx=bx, k=k: ctx.rectangle(bx - 78*s + k*34*s, y - Ht - 92*s, 24*s, 34*s),
                  col, a, depth=3*s, tex=.3, seed=220 + k)
    if gate:
        ctx.new_path()
        ctx.move_to(W/2 - 92*s, y)
        ctx.line_to(W/2 - 92*s, y - 150*s)
        ctx.curve_to(W/2 - 92*s, y - 236*s, W/2 + 92*s, y - 236*s, W/2 + 92*s, y - 150*s)
        ctx.line_to(W/2 + 92*s, y); ctx.close_path()
        ctx.set_source_rgba(0, 0, 0, .9*a); ctx.fill()
    crowd(ctx, y + 4*s, [W/2 - 190*s, W/2 - 146*s, W/2 + 150*s, W/2 + 196*s, W/2 + 240*s], .8*a, s, t=t)


def hero(ctx, t, draw, lampy=120, rays=.26, hz=None, ridge=None):
    """the standard grand composition: ridges, haze, the monument, then shafts of
    light over the top of it"""
    if ridge is not None: horizon(ctx, ridge, t)
    if hz is not None: haze(ctx, hz[0], hz[1], hz[2] if len(hz) > 2 else .3)
    draw()
    godrays(ctx, W*.46, lampy, t, rays)


# ---------- outdoor skies: what actually makes a monument look grand ----------
SKIES = {
    'dawn':  ((0.055, 0.075, 0.145), (0.38, 0.26, 0.33), (0.96, 0.62, 0.32), (1.0, 0.86, 0.60)),
    'dusk':  ((0.07, 0.065, 0.12), (0.46, 0.22, 0.26), (0.92, 0.46, 0.26), (1.0, 0.78, 0.50)),
    'noon':  ((0.30, 0.42, 0.56), (0.62, 0.70, 0.76), (0.90, 0.88, 0.80), (1.0, 0.97, 0.90)),
    'storm': ((0.09, 0.10, 0.14), (0.26, 0.26, 0.30), (0.52, 0.47, 0.44), (0.78, 0.74, 0.68)),
}


def bg_sky(ctx, t, horizon_y=930, kind='dawn', sun=(0.46, 0.80), sundisc=True, a=1.):
    """An open sky with the sun low on the horizon. Monuments read as grand against
    this in a way they never do against a wall: the silhouette has somewhere to be."""
    top, mid, low, glow = SKIES[kind]
    g = cairo.LinearGradient(0, 0, 0, horizon_y)
    g.add_color_stop_rgba(0, *top, a)
    g.add_color_stop_rgba(.52, *mid, a)
    g.add_color_stop_rgba(.88, *low, a)
    g.add_color_stop_rgba(1, *glow, a)
    ctx.set_source(g); ctx.rectangle(0, 0, W, horizon_y); ctx.fill()
    sx, sy = W*sun[0], horizon_y*sun[1]
    # the sun's halo, then its disc
    hg = cairo.RadialGradient(sx, sy, 10, sx, sy, 620)
    hg.add_color_stop_rgba(0, *glow, .85*a); hg.add_color_stop_rgba(.3, *low, .35*a)
    hg.add_color_stop_rgba(1, *low, 0)
    ctx.save(); ctx.set_operator(cairo.OPERATOR_ADD); ctx.set_source(hg)
    ctx.arc(sx, sy, 620, 0, 2*math.pi); ctx.fill(); ctx.restore()
    if sundisc:
        ctx.set_source_rgba(*glow, .92*a); ctx.arc(sx, sy, 52, 0, 2*math.pi); ctx.fill()
    # low cloud bars, which give the sky a scale of its own
    rr = random.Random(6)
    for i in range(7):
        cy = horizon_y*(.30 + i*.085)
        cw = rr.uniform(260, 820); cx = (rr.uniform(0, W) + t*rr.uniform(1.5, 5)) % (W + 900) - 450
        ch = rr.uniform(8, 20)
        ctx.save(); ctx.translate(cx, cy); ctx.scale(1, ch/cw*2.4); ctx.translate(-cx, -cy)
        ctx.set_source_rgba(*low, rr.uniform(.08, .22)*a)
        ctx.arc(cx, cy, cw/2, 0, 2*math.pi); ctx.fill(); ctx.restore()
    # ground
    gg = cairo.LinearGradient(0, horizon_y, 0, H)
    gg.add_color_stop_rgba(0, S['clay'][0]*.60, S['clay'][1]*.52, S['clay'][2]*.44, a)
    gg.add_color_stop_rgba(1, S['soot'][0]*1.5, S['soot'][1]*1.4, S['soot'][2]*1.3, a)
    ctx.set_source(gg); ctx.rectangle(0, horizon_y, W, H - horizon_y); ctx.fill()
    ctx.save(); ctx.rectangle(0, horizon_y, W, H - horizon_y); ctx.clip()
    grain(ctx, .4, 8); ctx.restore()
    return (sx, sy)


def silhouette(ctx, y, a=.92, height=150, seed=12, col=None):
    """a dark foreground plane: scrub, rocks and broken walls, almost black. It is
    what makes the middle distance read as distant."""
    col = col or (0.04, 0.035, 0.03)
    rr = random.Random(seed)
    ctx.new_path(); ctx.move_to(-20, H + 20)
    x = -20
    while x < W + 40:
        h = rr.uniform(height*.25, height)
        ctx.line_to(x, y - h)
        ctx.line_to(x + rr.uniform(40, 150), y - h*rr.uniform(.5, 1.0))
        x += rr.uniform(80, 220)
    ctx.line_to(W + 40, H + 20); ctx.close_path()
    rgba(ctx, col, a); ctx.fill()


def birds(ctx, t, a=.5, n=9, seed=21):
    rr = random.Random(seed)
    for i in range(n):
        bx = (rr.uniform(0, W) + t*rr.uniform(8, 20)) % (W + 200) - 100
        by = rr.uniform(130, 420) + 9*math.sin(t*1.2 + i)
        s = rr.uniform(.6, 1.3)
        fl = math.sin(t*rr.uniform(3, 5) + i)*.5
        rgba(ctx, (0, 0, 0), a*rr.uniform(.4, 1.))
        ctx.set_line_width(2.1*s); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(bx - 9*s, by + fl*4*s); ctx.line_to(bx, by)
        ctx.line_to(bx + 9*s, by + fl*4*s); ctx.stroke()
