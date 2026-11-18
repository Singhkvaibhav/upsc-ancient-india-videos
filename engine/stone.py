"""Ancient India, Simply Unearthed — the carved-stone look.

Light is the star here. Shapes are cut into stone rather than laid on paper, and a
raking lamp sweeps across them to reveal the carving. Everything static is cached;
only light, dust and the camera move per frame.

Never used here: drop shadows (stone has bevels, not shadows), gradients except for
lamplight and vignette, and faces of revered figures (see CLAUDE.md).
"""
import cairo, math, random
from engine.core import W, H, hx, cl, seg, ease, eoc, eob, lerp, rgba, rrect, font

# ---------- palette ----------
S = {k: hx(v) for k, v in dict(
    lime='EFE7DA',      # limestone: the main carved surface and text on dark
    sand='E0C49A',      # sandstone
    terra='A8492A',     # terracotta
    ochre='C9973A',     # ochre, the warm accent
    clay='8B6B4A',      # river clay
    basalt='3A3A3F',    # the wall
    soot='2B2622',      # the darkest ground
    verd='4FA39A',      # verdigris — ONLY the inscription tip
    dust='D8C9AE',      # motes in the beam
    deep='1A1715',      # trench shadow
    lampw='FFD9A0',     # lamp warmth
).items()}

LIGHT = (-0.62, -0.78)      # default raking direction (up and to the left)

# ---------- cached textures ----------
_cache = {}

def _grain_tile(seed=1, size=256, density=.5):
    key = ('grain', seed, size)
    if key in _cache: return _cache[key]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context(surf)
    rr = random.Random(seed)
    for _ in range(int(size*size*density/22)):
        x, y = rr.uniform(0, size), rr.uniform(0, size)
        r = rr.uniform(.4, 1.9)
        v = rr.uniform(0, 1)
        ctx.set_source_rgba(v, v*.95, v*.88, rr.uniform(.05, .22))
        ctx.arc(x, y, r, 0, 2*math.pi); ctx.fill()
    # a few longer striations, so it reads as stone and not TV static
    for _ in range(size//8):
        x, y = rr.uniform(0, size), rr.uniform(0, size)
        ln = rr.uniform(10, 50); ang = rr.uniform(-.4, .4)
        ctx.set_source_rgba(0, 0, 0, rr.uniform(.03, .09)); ctx.set_line_width(rr.uniform(.6, 1.6))
        ctx.move_to(x, y); ctx.line_to(x + ln*math.cos(ang), y + ln*math.sin(ang)); ctx.stroke()
    surf.flush()
    pat = cairo.SurfacePattern(surf); pat.set_extend(cairo.EXTEND_REPEAT)
    _cache[key] = pat
    return pat


def grain(ctx, a=.5, seed=1):
    """stone grain over the current clip"""
    if a <= 0: return
    ctx.save(); ctx.set_source(_grain_tile(seed)); ctx.paint_with_alpha(a); ctx.restore()


def cached(key, draw, w=W, h=H):
    """render `draw(ctx)` once into an image surface and reuse it every frame"""
    if key in _cache: return _cache[key]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w), int(h))
    c = cairo.Context(surf); draw(c); surf.flush()
    _cache[key] = surf
    return surf


def blit(ctx, surf, x=0, y=0, a=1.):
    ctx.save(); ctx.set_source_surface(surf, x, y); ctx.paint_with_alpha(a); ctx.restore()


# ---------- the core primitive ----------
def carve(ctx, path, col, a=1., depth=5.0, light=LIGHT, tex=.42, seed=1, rim=True,
          raised=True, occl=.42, shade=.30):
    """A block of stone standing proud of the plane behind it.

    Relief only reads if three things happen at once: the face is shaded across the
    light direction, the edges facing the lamp catch a bright lip while the opposite
    edges fall into shadow, and the block drops a tight contact shadow onto the plane
    behind. That contact shadow is ambient occlusion, not the paper series' drop
    shadow -- it stays within a few pixels of the edge.
    """
    if a <= 0: return
    lx, ly = light
    # contact shadow on the plane behind, hugging the shaded side
    if raised and occl > 0:
        ctx.save()
        ctx.translate(-lx*depth*0.85, -ly*depth*0.85)
        ctx.new_path(); path()
        ctx.set_line_width(depth*2.6); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_source_rgba(0, 0, 0, occl*a*.55); ctx.stroke()
        ctx.new_path(); path(); ctx.set_source_rgba(0, 0, 0, occl*a); ctx.fill()
        ctx.restore()
    ctx.save()
    ctx.new_path(); path(); rgba(ctx, col, a); ctx.fill_preserve()
    ctx.clip()
    # the face is not flat: it falls away from the light across the shape
    x0, y0, x1, y1 = ctx.clip_extents()
    if shade > 0 and x1 > x0:
        g = cairo.LinearGradient(x0 - lx*(x1 - x0), y0 - ly*(y1 - y0), x1 - lx*(x1 - x0)*.2, y1 - ly*(y1 - y0)*.2)
        g.add_color_stop_rgba(0, 1, .97, .9, shade*.55*a)
        g.add_color_stop_rgba(.55, 0, 0, 0, 0)
        g.add_color_stop_rgba(1, 0, 0, 0, shade*a)
        ctx.set_source(g); ctx.paint()
    if tex: grain(ctx, tex*a, seed)
    # the lit lip, wide enough to see
    ctx.save(); ctx.translate(lx*depth, ly*depth)
    ctx.new_path(); path()
    ctx.set_line_width(depth*2.4); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(1, .97, .9, .78*a); ctx.stroke(); ctx.restore()
    # the shaded lip
    ctx.save(); ctx.translate(-lx*depth, -ly*depth)
    ctx.new_path(); path()
    ctx.set_line_width(depth*2.4); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(0, 0, 0, .62*a); ctx.stroke(); ctx.restore()
    ctx.restore()
    if rim:
        ctx.save(); ctx.new_path(); path()
        ctx.set_line_width(1.3); ctx.set_source_rgba(0, 0, 0, .42*a); ctx.stroke(); ctx.restore()


def incise(ctx, path, a=1., width=7., glow=None, ga=0.):
    """A groove cut into stone: dark channel with a lit upper lip. `glow` fills the
    groove with colour (verdigris, for the inscription tip only)."""
    if a <= 0: return
    ctx.save()
    ctx.new_path(); path(); ctx.set_line_width(width)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(0, 0, 0, .55*a); ctx.stroke()
    ctx.save(); ctx.translate(LIGHT[0]*1.6, LIGHT[1]*1.6)
    ctx.new_path(); path(); ctx.set_line_width(width*.42)
    ctx.set_source_rgba(1, .97, .9, .34*a); ctx.stroke(); ctx.restore()
    if glow and ga > 0:
        for lw, al in ((width*2.6, .10), (width*1.5, .20), (width*.62, .95)):
            ctx.new_path(); path(); ctx.set_line_width(lw)
            rgba(ctx, glow, al*ga*a); ctx.stroke()
    ctx.restore()


# ---------- light ----------
def lamp(ctx, x, y, r, a=1., warm=None, core=.92):
    """a warm pool of lamplight, added over the scene"""
    if a <= 0: return
    warm = warm or S['lampw']
    g = cairo.RadialGradient(x, y, r*.04, x, y, r)
    g.add_color_stop_rgba(0, warm[0], warm[1], warm[2], core*a)
    g.add_color_stop_rgba(.42, warm[0]*.92, warm[1]*.76, warm[2]*.52, .34*a)
    g.add_color_stop_rgba(1, warm[0]*.6, warm[1]*.4, warm[2]*.2, 0)
    ctx.save(); ctx.set_operator(cairo.OPERATOR_ADD)
    ctx.set_source(g); ctx.arc(x, y, r, 0, 2*math.pi); ctx.fill(); ctx.restore()


def rake(ctx, p, a=.55, width=620, ang=-0.35, warm=None):
    """A raking band of light sweeping left to right across the frame. `p` is 0..1.
    This is the series' signature reveal: carving appears as the light crosses it."""
    if a <= 0: return
    warm = warm or S['lampw']
    cx = lerp(-width, W + width, cl(p))
    ctx.save(); ctx.set_operator(cairo.OPERATOR_ADD)
    ctx.translate(cx, H/2); ctx.rotate(ang); ctx.translate(-cx, -H/2)
    g = cairo.LinearGradient(cx - width/2, 0, cx + width/2, 0)
    g.add_color_stop_rgba(0, *warm, 0)
    g.add_color_stop_rgba(.5, warm[0], warm[1]*.9, warm[2]*.72, .30*a)
    g.add_color_stop_rgba(1, *warm, 0)
    ctx.set_source(g); ctx.rectangle(cx - width/2, -H, width, H*3); ctx.fill()
    ctx.restore()


def lit(p, x, soft=360., width=620, ang=-0.35):
    """How lit a thing at screen x is, for a rake at phase p. Use it to fade carving
    in as the light crosses it, so the reveal and the light agree."""
    cx = lerp(-width, W + width, cl(p))
    return cl(1 - (x - cx)/soft) if cx < x else 1.


def vignette(ctx, a=.55, fx=.5, fy=.45, inner=320, outer=1250):
    g = cairo.RadialGradient(W*fx, H*fy, inner, W/2, H/2, outer)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, a)
    ctx.set_source(g); ctx.paint()


def dust(ctx, t, a=.5, n=90, cx=None, r=620, seed=5, rise=-9.):
    """motes drifting in the lamp beam"""
    if a <= 0: return
    cx = W*.52 if cx is None else cx
    rr = random.Random(seed)
    for i in range(n):
        bx = rr.uniform(cx - r, cx + r); by = rr.uniform(80, H)
        sp = rr.uniform(.4, 1.5)
        x = bx + 16*math.sin(t*sp*.5 + i)
        y = (by + t*rise*sp) % (H + 120) - 60
        d = abs(x - cx)/r
        al = a*max(0., 1 - d*d)*(.35 + .65*(.5 + .5*math.sin(t*sp + i)))
        rgba(ctx, S['dust'], al*rr.uniform(.4, 1.))
        ctx.arc(x, y, rr.uniform(.8, 2.4), 0, 2*math.pi); ctx.fill()


# ---------- camera (motion rules: nothing stands still) ----------
def camera(ctx, t, D, zoom=(1.0, 1.045), cx=None, cy=None, pan=(0, 0), depth=1.0):
    """Slow push-in/pan over a beat. `depth` scales the move, so layers drawn at
    different depths move at different speeds and the frame has parallax."""
    cx = W/2 if cx is None else cx; cy = H/2 if cy is None else cy
    q = ease(cl(t/max(D, .001)))
    z = 1 + (lerp(zoom[0], zoom[1], q) - 1)*depth
    dx, dy = pan[0]*q*depth, pan[1]*q*depth
    ctx.translate(cx + dx, cy + dy); ctx.scale(z, z); ctx.translate(-cx, -cy)


# ---------- backgrounds ----------
def _wall(c):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *S['soot']); g.add_color_stop_rgb(1, *[v*.72 for v in S['basalt']])
    c.set_source(g); c.paint()
    rr = random.Random(11)
    # coarse block courses, barely visible — they give the lamp something to catch
    for y in range(120, H, 168):
        c.set_source_rgba(0, 0, 0, .22); c.rectangle(0, y, W, 2.5); c.fill()
        c.set_source_rgba(1, .95, .88, .045); c.rectangle(0, y + 2.5, W, 1.5); c.fill()
        off = rr.uniform(0, 320)
        for x in range(int(off) - 320, W + 320, 330):
            c.set_source_rgba(0, 0, 0, .16); c.rectangle(x, y, 2, 168); c.fill()
    c.save(); c.set_source(_grain_tile(2)); c.paint_with_alpha(.55); c.restore()


def bg_stone(ctx, t, lampx=None, lampy=380, a=1., beam=True):
    """a dark basalt wall with a warm pool of lamplight, drifting slightly"""
    blit(ctx, cached('wall', _wall))
    lx = (W*.56 if lampx is None else lampx) + 26*math.sin(t*.17)
    ly = lampy + 14*math.sin(t*.23 + 1.1)
    lamp(ctx, lx, ly, 980, .55*a)
    if beam: dust(ctx, t, .42*a, cx=lx, r=560)
    vignette(ctx, .62, .54, .40)


def _hall(c):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *[v*.55 for v in S['soot']]); g.add_color_stop_rgb(.62, *S['soot'])
    g.add_color_stop_rgb(1, *[v*1.5 for v in S['soot']])
    c.set_source(g); c.paint()
    # floor line and its faint reflection band
    c.set_source_rgba(1, .9, .74, .10); c.rectangle(0, 812, W, 2); c.fill()
    g2 = cairo.LinearGradient(0, 814, 0, H)
    g2.add_color_stop_rgba(0, 1, .86, .66, .055); g2.add_color_stop_rgba(1, 1, .86, .66, 0)
    c.set_source(g2); c.rectangle(0, 814, W, H - 814); c.fill()
    c.save(); c.set_source(_grain_tile(4)); c.paint_with_alpha(.4); c.restore()


def bg_museum(ctx, t, a=1.):
    """the gallery hall: dark walls, a floor line, a row of lamp glows"""
    blit(ctx, cached('hall', _hall))
    for i in range(5):
        x = 190 + i*385
        lamp(ctx, x, 150, 330, .20*a)
        rgba(ctx, S['lampw'], .14*a*(.8 + .2*math.sin(t*.9 + i)))
        ctx.arc(x, 132, 7, 0, 2*math.pi); ctx.fill()
    lamp(ctx, W*.5 + 30*math.sin(t*.15), 560, 900, .26*a)
    dust(ctx, t, .22*a, cx=W*.5, r=760, seed=9)
    vignette(ctx, .66)


def _soil(c):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *[v*.9 for v in S['soot']]); g.add_color_stop_rgb(1, *S['deep'])
    c.set_source(g); c.paint()
    rr = random.Random(17)
    # strata: bands of clay and sand, each with its own grain
    y = 250
    cols = [S['clay'], S['sand'], S['clay'], S['terra'], S['clay']]
    for i in range(5):
        h = rr.uniform(120, 190)
        c.save()
        c.new_path(); c.move_to(-20, y)
        for x in range(-20, W + 61, 60):
            c.line_to(x, y + 9*math.sin(x*.004 + i*1.7) + 5*math.sin(x*.011 + i))
        c.line_to(W + 40, y + h + 40); c.line_to(-20, y + h + 40); c.close_path()
        col = cols[i % len(cols)]
        c.set_source_rgba(col[0]*.52, col[1]*.46, col[2]*.40, 1); c.fill_preserve()
        c.clip(); c.set_source(_grain_tile(20 + i)); c.paint_with_alpha(.62)
        c.restore()
        # the lit lip of each stratum
        c.new_path(); c.move_to(-20, y)
        for x in range(-20, W + 61, 60):
            c.line_to(x, y + 9*math.sin(x*.004 + i*1.7) + 5*math.sin(x*.011 + i))
        c.set_line_width(2); c.set_source_rgba(1, .92, .78, .10); c.stroke()
        y += h
    c.save(); c.set_source(_grain_tile(3)); c.paint_with_alpha(.5); c.restore()


def bg_trench(ctx, t, a=1.):
    """a soil cross-section with layered strata, lit from above by a working lamp"""
    blit(ctx, cached('soil', _soil))
    lx = W*.46 + 30*math.sin(t*.2)
    lamp(ctx, lx, 210, 880, .50*a)
    dust(ctx, t, .50*a, cx=lx, r=520, seed=13, rise=-6.)
    vignette(ctx, .66, .46, .28)


# ---------- excavation reveal (the series' transition device) ----------
def unearth(ctx, path, col, p, t, a=1., spread=180, seed=7, **kw):
    """A carved thing emerges from soil: the shape fades up under a scatter of
    particles that blow away. `p` runs 0..1."""
    p = cl(p)
    if p <= 0: return
    carve(ctx, path, col, a*ease(min(p*1.5, 1)), **kw)
    if p < 1:
        rr = random.Random(seed)
        ctx.save(); ctx.new_path(); path(); ctx.clip()
        for i in range(140):
            x, y = rr.uniform(0, W), rr.uniform(0, H)
            off = (1 - p)*spread
            rgba(ctx, S['clay'], a*(1 - p)*rr.uniform(.3, .95))
            ctx.arc(x + rr.uniform(-off, off)*.2, y - off*rr.uniform(0, 1), rr.uniform(1.2, 4.5), 0, 2*math.pi)
            ctx.fill()
        ctx.restore()


def brush(ctx, x, y, ang, a=1., s=1.):
    """an archaeologist's brush, in silhouette"""
    if a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s)
    carve(ctx, lambda: rrect(ctx, -14, -190, 28, 150, 8), S['clay'], a, depth=2.2, tex=.3)
    carve(ctx, lambda: rrect(ctx, -22, -46, 44, 26, 5), S['basalt'], a, depth=2., tex=.2)
    rr = random.Random(2)
    for i in range(16):
        bx = -19 + i*2.5
        rgba(ctx, S['sand'], a*rr.uniform(.45, .95)); ctx.set_line_width(1.8)
        ctx.move_to(bx, -22); ctx.line_to(bx + rr.uniform(-3, 3), rr.uniform(14, 26)); ctx.stroke()
    ctx.restore()


# ---------- type ----------
def engraved(ctx, s, x, y, size, a=1., col=None, align='c', serif=True, bold=True, lit_=.34):
    """lettering cut into stone: a dark groove with a lit upper lip"""
    if a <= 0: return
    col = col or S['lime']
    font(ctx, size, bold, serif)
    e = ctx.text_extents(s)
    xx = x - (e.x_advance/2 if align == 'c' else e.x_advance if align == 'r' else 0)
    ctx.save()
    ctx.move_to(xx + 2.2, y + 2.6); ctx.text_path(s); ctx.set_source_rgba(0, 0, 0, .62*a); ctx.fill()
    ctx.move_to(xx - 1.4, y - 1.6); ctx.text_path(s); ctx.set_source_rgba(1, .96, .88, lit_*a); ctx.fill()
    ctx.move_to(xx, y); ctx.text_path(s); rgba(ctx, col, a); ctx.fill()
    ctx.restore()
    return e.x_advance


def kinetic(ctx, words, x, y, size, t, t0, col=None, a=1., gap=.14, align='c', serif=True):
    """words land one at a time (motion rule: kinetic type)"""
    col = col or S['lime']
    font(ctx, size, True, serif)
    widths = [ctx.text_extents(w).x_advance for w in words]
    sp = ctx.text_extents(' ').x_advance
    total = sum(widths) + sp*(len(words) - 1)
    cx = x - (total/2 if align == 'c' else total if align == 'r' else 0)
    for i, w in enumerate(words):
        q = seg(t, t0 + i*gap, t0 + i*gap + .34)
        if q <= 0: continue
        dy = (1 - eob(q, 1.8))*26
        engraved(ctx, w, cx, y + dy, size, a*ease(min(q*2, 1)), col, 'l', serif)
        cx += widths[i] + sp


def ribbon(ctx, period, span=(-3000, 500), a=1., t=0., y=92):
    """the thin carved BCE/CE timeline band along the top of every scene"""
    if a <= 0: return
    carve(ctx, lambda: ctx.rectangle(0, y - 34, W, 70), S['basalt'], .96*a, depth=2.4, tex=.3)
    lo, hi = span
    def X(v): return 90 + (v - lo)/(hi - lo)*(W - 180)
    rgba(ctx, S['lime'], .26*a); ctx.rectangle(90, y - 2, W - 180, 1.6); ctx.fill()
    step = 500
    v = int(lo//step)*step
    while v <= hi:
        xx = X(v)
        rgba(ctx, S['lime'], .34*a); ctx.rectangle(xx, y - 9, 1.4, 12); ctx.fill()
        lab = f'{abs(v)} {"BCE" if v < 0 else "CE"}' if v else '0'
        font(ctx, 15, False, False)
        e = ctx.text_extents(lab)
        rgba(ctx, S['lime'], .46*a); ctx.move_to(xx - e.x_advance/2, y + 22); ctx.show_text(lab)
        v += step
    if period:
        p0, p1 = period
        x0, x1 = X(p0), X(p1)
        rgba(ctx, S['ochre'], .92*a); ctx.rectangle(x0, y - 6, max(x1 - x0, 3), 9); ctx.fill()
        lamp(ctx, (x0 + x1)/2, y - 2, 150 + 12*math.sin(t*1.6), .34*a)


def tag(ctx, s, x, y, a=1., col=None, size=20, align='l'):
    """a small excavation tag: a cream card with ink lettering"""
    if a <= 0: return
    col = col or S['lime']
    font(ctx, size, True, False)
    e = ctx.text_extents(s); w, h = e.x_advance + 30, size*1.95
    x0 = x - (w/2 if align == 'c' else w if align == 'r' else 0)
    carve(ctx, lambda: rrect(ctx, x0, y - h/2, w, h, 5), S['basalt'], .93*a, depth=2., tex=.26)
    rgba(ctx, col, .9*a); ctx.rectangle(x0, y - h/2, 4, h); ctx.fill()
    rgba(ctx, S['lime'], a)
    ctx.move_to(x0 + 18, y + size*.35); ctx.show_text(s)
    return w


def corner(ctx, ep, a=1.):
    font(ctx, 19, True, False)
    s = f'ANCIENT INDIA  ·  EP {ep}'
    e = ctx.text_extents(s)
    rgba(ctx, S['lime'], .40*a)
    ctx.move_to(W - 70 - e.x_advance, 150); ctx.show_text(s)


def filmgrain(ctx, t, a=.05):
    """a light moving grain over the finished frame, so flat fills don't look digital"""
    if a <= 0: return
    ctx.save()
    ctx.translate((t*61) % 256, (t*37) % 256)
    ctx.set_source(_grain_tile(int(t*12) % 4 + 30))
    ctx.paint_with_alpha(a); ctx.restore()


# ---------- drawn forms (relief needs silhouettes, not rectangles) ----------
def poly(ctx, pts, close=True):
    ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    if close: ctx.close_path()


def coursed(ctx, x, y, w, h, a=1., rows=None, col=None, seed=3, course=22):
    """brick coursing cut into a face already drawn — the detail that sells masonry"""
    col = col or S['soot']
    rows = rows or max(1, int(h//course))
    rr = random.Random(seed)
    ctx.save(); ctx.rectangle(x, y, w, h); ctx.clip()
    for r in range(1, rows):
        yy = y + r*(h/rows)
        ctx.set_source_rgba(0, 0, 0, .30*a); ctx.rectangle(x, yy, w, 1.6); ctx.fill()
        ctx.set_source_rgba(1, .95, .86, .13*a); ctx.rectangle(x, yy + 1.6, w, 1.1); ctx.fill()
        off = (r % 2)*(course*1.1) + rr.uniform(0, 8)
        bx = x + off
        while bx < x + w:
            ctx.set_source_rgba(0, 0, 0, .22*a); ctx.rectangle(bx, yy - h/rows, 1.4, h/rows); ctx.fill()
            bx += course*2.2
    ctx.restore()


def platform(ctx, x, y, w, h, a=1., col=None, step=3, depth=5.):
    """a stepped mud-brick platform, wider at the base — the citadel form"""
    col = col or S['clay']
    for i in range(step):
        f = i/step
        xx = x + w*.055*i; ww = w - w*.11*i
        yy = y - h*(i + 1)/step; hh = h/step + 2
        carve(ctx, lambda xx=xx, yy=yy, ww=ww, hh=hh: ctx.rectangle(xx, yy, ww, hh),
              tuple(min(1, v*(1 + f*.10)) for v in col), a, depth=depth, seed=10 + i)
        coursed(ctx, xx, yy, ww, hh, a*.9, seed=20 + i)


def house(ctx, x, y, w, h, a=1., col=None, door=True, parapet=True, depth=4.4, seed=5):
    """a flat-roofed mud-brick house in elevation, with a stepped parapet and a doorway"""
    col = col or S['sand']
    carve(ctx, lambda: ctx.rectangle(x, y - h, w, h), col, a, depth=depth, seed=seed)
    coursed(ctx, x, y - h, w, h, a*.85, seed=seed + 40)
    if parapet:
        n = max(2, int(w//26))
        for k in range(n):
            bx = x + 4 + k*(w - 8)/n
            carve(ctx, lambda bx=bx, n=n: ctx.rectangle(bx, y - h - 13, (w - 8)/n - 5, 15),
                  col, a, depth=2.4, tex=.25, seed=seed + k)
    if door and h > 52:
        dw = min(26, w*.3)
        ctx.save()
        ctx.new_path(); ctx.rectangle(x + w/2 - dw/2, y - h*.52, dw, h*.52)
        ctx.set_source_rgba(0, 0, 0, .66*a); ctx.fill()
        ctx.new_path(); ctx.rectangle(x + w/2 - dw/2, y - h*.52, dw, 3)
        ctx.set_source_rgba(1, .95, .86, .20*a); ctx.fill()
        ctx.restore()


def drain_section(ctx, x, y, w, a=1., slabs=8, depth=5.):
    """a covered street drain in true cross-section: slabs on top, a dark channel,
    brick cheeks either side"""
    ch = 86
    carve(ctx, lambda: ctx.rectangle(x, y, w, ch + 34), S['sand'], a, depth=depth)
    coursed(ctx, x, y, w, ch + 34, a*.9, seed=61)
    ctx.save()
    ctx.new_path(); ctx.rectangle(x + 46, y + 26, w - 92, ch - 16)
    ctx.set_source_rgba(0, 0, 0, .80*a); ctx.fill()
    g = cairo.LinearGradient(0, y + 26, 0, y + 26 + ch - 16)
    g.add_color_stop_rgba(0, 0, 0, 0, .5*a); g.add_color_stop_rgba(1, *S['clay'], .34*a)
    ctx.new_path(); ctx.rectangle(x + 46, y + 26, w - 92, ch - 16); ctx.set_source(g); ctx.fill()
    ctx.restore()
    for k in range(slabs):
        sw = (w - 20)/slabs
        sx = x + 10 + k*sw
        carve(ctx, lambda sx=sx, sw=sw: ctx.rectangle(sx, y - 20, sw - 6, 30),
              S['lime'], a, depth=3.0, tex=.3, seed=70 + k)


def case(ctx, x, y, w, h, a=1., lit_=1., empty=False, label=None):
    """a museum glass case on a plinth"""
    carve(ctx, lambda: ctx.rectangle(x - 14, y + h, w + 28, 34), S['basalt'], a, depth=3.4, tex=.3)
    if not empty:
        lamp(ctx, x + w/2, y + 24, h*.95, .30*a*lit_)
    # the glass
    g = cairo.LinearGradient(x, y, x + w, y + h)
    g.add_color_stop_rgba(0, 1, .95, .86, .085*a)
    g.add_color_stop_rgba(.45, 1, .95, .86, .020*a)
    g.add_color_stop_rgba(1, 1, .95, .86, .070*a)
    ctx.new_path(); ctx.rectangle(x, y, w, h); ctx.set_source(g); ctx.fill()
    # frame
    for rx, rw in ((x - 5, 9), (x + w - 4, 9)):
        carve(ctx, lambda rx=rx, rw=rw: ctx.rectangle(rx, y - 6, rw, h + 12), S['basalt'], a, depth=2.4, tex=.2)
    for ry, rh in ((y - 8, 11), (y + h - 3, 11)):
        carve(ctx, lambda ry=ry, rh=rh: ctx.rectangle(x - 6, ry, w + 12, rh), S['basalt'], a, depth=2.4, tex=.2)
    # a diagonal sheen so it reads as glass
    ctx.save(); ctx.rectangle(x, y, w, h); ctx.clip()
    ctx.set_source_rgba(1, .97, .9, .055*a)
    poly(ctx, [(x - 60, y + h), (x + w*.55, y - 40), (x + w*.78, y - 40), (x - 10, y + h + 30)])
    ctx.fill(); ctx.restore()
    if label:
        tag(ctx, label, x + w/2, y + h + 76, a*.9, size=19, align='c')


def pot(ctx, x, y, s, a=1., col=None, depth=4.):
    """a round-bodied painted pot in elevation"""
    col = col or S['terra']
    def body():
        ctx.move_to(x - 22*s, y - 86*s); ctx.line_to(x + 22*s, y - 86*s)
        ctx.curve_to(x + 30*s, y - 70*s, x + 56*s, y - 46*s, x + 52*s, y - 24*s)
        ctx.curve_to(x + 48*s, y - 4*s, x + 26*s, y, x, y)
        ctx.curve_to(x - 26*s, y, x - 48*s, y - 4*s, x - 52*s, y - 24*s)
        ctx.curve_to(x - 56*s, y - 46*s, x - 30*s, y - 70*s, x - 22*s, y - 86*s)
        ctx.close_path()
    carve(ctx, body, col, a, depth=depth)
    ctx.save(); ctx.new_path(); body(); ctx.clip()
    for k in range(3):
        ctx.set_source_rgba(0, 0, 0, .28*a)
        ctx.rectangle(x - 60*s, y - (56 - k*13)*s, 120*s, 3.4*s); ctx.fill()
    ctx.restore()


def brick(ctx, x, y, s, a=1., ratio=(1, 2, 4), depth=5.):
    """the standard 1:2:4 brick, drawn in simple axonometric"""
    th, wd, ln = [v*12*s for v in ratio]
    top = [(x, y), (x + ln, y - ln*.22), (x + ln + wd*.5, y - ln*.22 + wd*.34), (x + wd*.5, y + wd*.34)]
    front = [(x, y), (x + ln, y - ln*.22), (x + ln, y - ln*.22 + th), (x, y + th)]
    side = [(x + ln, y - ln*.22), (x + ln + wd*.5, y - ln*.22 + wd*.34),
            (x + ln + wd*.5, y - ln*.22 + wd*.34 + th), (x + ln, y - ln*.22 + th)]
    carve(ctx, lambda: poly(ctx, front), S['sand'], a, depth=depth*.7, raised=True)
    carve(ctx, lambda: poly(ctx, side), tuple(v*.72 for v in S['sand']), a, depth=depth*.6, raised=False)
    carve(ctx, lambda: poly(ctx, top), tuple(min(1, v*1.12) for v in S['sand']), a, depth=depth*.6, raised=False)
