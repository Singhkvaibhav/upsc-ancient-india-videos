"""The Gallery of Ancient India: the hall, its cases, and one exhibit per episode.

Each episode adds an exhibit and earlier ones stay in their cases, so the museum
fills as the series runs. Exhibits are simplified carved versions drawn for this
series, never traced from a photograph. Nothing revered is depicted.
"""
import cairo, math, random
from engine.core import W, H, cl, seg, ease, eoc, eob, lerp, rgba, rrect
from engine.stone import S, carve, incise, coursed, poly, lamp, case, pot, brick, engraved, tag, grain
from engine.monument import crowd


# ---------- the exhibits, one small function each ----------
def ex_handaxe(ctx, cx, cy, s=1., a=1., t=0.):
    carve(ctx, lambda: poly(ctx, [(cx - 54*s, cy + 60*s), (cx - 30*s, cy - 62*s), (cx + 16*s, cy - 72*s),
                                  (cx + 58*s, cy - 6*s), (cx + 22*s, cy + 64*s)]),
          tuple(v*1.3 for v in S['basalt']), a, depth=5*s)
    rr = random.Random(2)
    for k in range(9):
        f = k/8
        rgba(ctx, (0, 0, 0), .22*a); ctx.set_line_width(2.4*s)
        ctx.move_to(cx - 50*s + f*100*s, cy + 56*s - f*20*s)
        ctx.line_to(cx - 26*s + f*74*s, cy - 54*s + f*44*s); ctx.stroke()


def ex_pot(ctx, cx, cy, s=1., a=1., t=0.):
    pot(ctx, cx, cy + 70*s, s*1.5, a)


def ex_seal(ctx, cx, cy, s=1., a=1., t=0.):
    """a square steatite seal. The animal is a simple carved profile; the script is
    shown as marks, because it has not been deciphered."""
    carve(ctx, lambda: rrect(ctx, cx - 92*s, cy - 92*s, 184*s, 184*s, 10*s), S['sand'], a, depth=5.5*s)
    for k in range(7):
        rgba(ctx, S['soot'], .5*a)
        ctx.rectangle(cx - 66*s + k*20*s, cy - 72*s, 11*s, 26*s - (k % 3)*7*s); ctx.fill()
    # a generic humped bovine in profile, facing left
    carve(ctx, lambda: poly(ctx, [(cx - 64*s, cy + 44*s), (cx - 58*s, cy + 4*s), (cx - 34*s, cy - 10*s),
                                  (cx - 10*s, cy - 30*s), (cx + 22*s, cy - 10*s), (cx + 58*s, cy - 4*s),
                                  (cx + 64*s, cy + 44*s), (cx + 44*s, cy + 44*s), (cx + 38*s, cy + 18*s),
                                  (cx - 38*s, cy + 18*s), (cx - 44*s, cy + 44*s)]),
          tuple(v*.82 for v in S['sand']), a, depth=3.2*s, tex=.2)


def ex_brick_drain(ctx, cx, cy, s=1., a=1., t=0.):
    """Episode 4: a standard 1:2:4 brick beside a section of covered drain"""
    brick(ctx, cx - 120*s, cy + 20*s, s*1.25, a)
    x0 = cx + 6*s
    carve(ctx, lambda: ctx.rectangle(x0, cy - 16*s, 150*s, 86*s), S['sand'], a, depth=4.4*s)
    coursed(ctx, x0, cy - 16*s, 150*s, 86*s, a*.9, seed=12, course=15*s)
    ctx.new_path(); ctx.rectangle(x0 + 26*s, cy + 4*s, 98*s, 52*s)
    ctx.set_source_rgba(0, 0, 0, .82*a); ctx.fill()
    for k in range(4):
        carve(ctx, lambda k=k: ctx.rectangle(x0 + 6*s + k*36*s, cy - 32*s, 30*s, 17*s),
              S['lime'], a, depth=2.6*s, tex=.25, seed=20 + k)


def ex_figurine(ctx, cx, cy, s=1., a=1., t=0.):
    """a small bronze figure, drawn as an abstract standing form with no face"""
    carve(ctx, lambda: ctx.rectangle(cx - 46*s, cy + 56*s, 92*s, 18*s), tuple(v*.9 for v in S['basalt']), a, depth=3*s)
    carve(ctx, lambda: poly(ctx, [(cx - 13*s, cy + 56*s), (cx - 9*s, cy - 34*s), (cx + 9*s, cy - 34*s),
                                  (cx + 15*s, cy + 56*s)]), tuple(v*1.5 for v in S['clay']), a, depth=3.6*s)
    carve(ctx, lambda: ctx.arc(cx, cy - 48*s, 15*s, 0, 2*math.pi), tuple(v*1.5 for v in S['clay']), a, depth=3*s)


def ex_stone_tool(ctx, cx, cy, s=1., a=1., t=0.):
    carve(ctx, lambda: poly(ctx, [(cx - 70*s, cy + 30*s), (cx - 20*s, cy - 46*s), (cx + 60*s, cy - 18*s),
                                  (cx + 30*s, cy + 44*s)]), tuple(v*1.25 for v in S['basalt']), a, depth=4.5*s)


EXHIBITS = {
    1: (ex_seal, 'EP 1 · SOURCES'),
    2: (ex_handaxe, 'EP 2 · HAND AXE'),
    3: (ex_pot, 'EP 3 · PAINTED POT'),
    4: (ex_brick_drain, 'EP 4 · BRICK AND DRAIN'),
    5: (ex_seal, 'EP 5 · UNICORN SEAL'),
    6: (ex_figurine, 'EP 6 · BRONZE FIGURINE'),
}


# ---------- the hall ----------
def hall(ctx, t, a=1., place=1., upto=4, cols=5, y=380, cw=300, ch=360, gap=42, t_thud=None):
    """Draw the gallery's cases along the wall. Cases up to `upto - 1` hold their
    exhibits already; case `upto` receives this episode's exhibit, lowered into
    place as `place` runs 0 to 1. Later cases stand empty, waiting."""
    total = cols*cw + (cols - 1)*gap
    x0 = (W - total)/2
    for i in range(cols):
        n = i + 1
        x = x0 + i*(cw + gap)
        filled = n < upto
        arriving = n == upto
        case(ctx, x, y, cw, ch, a, lit_=1. if (filled or arriving) else .22,
             empty=not (filled or arriving),
             label=EXHIBITS.get(n, (None, f'EP {n}'))[1] if n in EXHIBITS or True else None)
        ent = EXHIBITS.get(n)
        if not ent: continue
        draw, _ = ent
        if filled:
            draw(ctx, x + cw/2, y + ch*.62, .78, a*.92, t)
        elif arriving and place > 0:
            dy = (1 - eob(place, 1.25))*-320
            ctx.save(); ctx.translate(0, dy)
            draw(ctx, x + cw/2, y + ch*.62, .78, a*min(1, place*1.6), t)
            ctx.restore()
            if place >= 1:
                # dust kicked up where it was set down
                rr = random.Random(7)
                for k in range(26):
                    rgba(ctx, S['dust'], a*.3*rr.uniform(.1, .7))
                    ctx.arc(x + cw/2 + rr.uniform(-70, 70), y + ch*.78 + rr.uniform(-6, 14), rr.uniform(1, 3), 0, 2*math.pi)
                    ctx.fill()
    # two visitors, for scale and life
    crowd(ctx, 846, [x0 - 96, x0 - 52], .55*a, 1.15, t=t)


def walk(ctx, t, a=1., upto=44, speed=130.):
    """the final episode's slow walk past every case"""
    ox = -((t*speed) % (upto*342))
    ctx.save(); ctx.translate(ox, 0)
    for i in range(upto):
        x = 120 + i*342
        case(ctx, x, 380, 300, 360, a, lit_=1., label=EXHIBITS.get(i + 1, (None, f'EP {i+1}'))[1])
        ent = EXHIBITS.get(i + 1)
        if ent: ent[0](ctx, x + 150, 380 + 360*.62, .78, a*.92, t)
    ctx.restore()


# ---------- Unit 2 exhibits ----------
def ex_leaf(ctx, cx, cy, s=1., a=1., t=0.):
    """a bundle of palm-leaf sheets between two boards"""
    carve(ctx, lambda: rrect(ctx, cx - 110*s, cy + 36*s, 220*s, 20*s, 5*s), tuple(v*.8 for v in S['clay']), a, depth=3.4*s)
    for k in range(5):
        carve(ctx, lambda k=k: rrect(ctx, cx - 104*s + (k % 2)*4*s, cy + 22*s - k*14*s, 208*s, 13*s, 5*s),
              S['sand'], a, depth=2.4*s, tex=.25, seed=30 + k)
    carve(ctx, lambda: rrect(ctx, cx - 110*s, cy - 64*s, 220*s, 20*s, 5*s), tuple(v*.8 for v in S['clay']), a, depth=3.4*s)
    rgba(ctx, S['soot'], .5*a); ctx.arc(cx, cy - 14*s, 5*s, 0, 2*math.pi); ctx.fill()


def ex_pgw(ctx, cx, cy, s=1., a=1., t=0.):
    """a thin grey bowl with simple painted bands"""
    def body():
        ctx.move_to(cx - 86*s, cy - 46*s)
        ctx.curve_to(cx - 80*s, cy + 36*s, cx + 80*s, cy + 36*s, cx + 86*s, cy - 46*s)
        ctx.close_path()
    carve(ctx, body, tuple(v*.62 for v in S['lime']), a, depth=4*s)
    ctx.save(); ctx.new_path(); body(); ctx.clip()
    for k in range(3):
        rgba(ctx, S['soot'], .34*a); ctx.rectangle(cx - 100*s, cy - 34*s + k*16*s, 200*s, 4*s); ctx.fill()
    ctx.restore()


def ex_altar(ctx, cx, cy, s=1., a=1., t=0.):
    """a layered brick fire altar. No image, no figure — fire and geometry only."""
    for i in range(3):
        w_ = 150*s - i*26*s
        carve(ctx, lambda i=i, w_=w_: ctx.rectangle(cx - w_/2, cy + 30*s - i*26*s, w_, 24*s),
              S['terra'], a, depth=3.4*s, seed=40 + i)
    fl = .8 + .2*math.sin(t*3.1)
    lamp(ctx, cx, cy - 56*s, 120*s*fl, .5*a, core=.7)
    for k in range(3):
        h = (40 + k*14)*s*fl
        rgba(ctx, S['ochre'], .5*a)
        ctx.move_to(cx - 16*s + k*16*s, cy - 44*s)
        ctx.curve_to(cx - 26*s + k*16*s, cy - 44*s - h*.6, cx - 6*s + k*16*s, cy - 44*s - h*.8, cx - 12*s + k*16*s, cy - 44*s - h)
        ctx.curve_to(cx - 2*s + k*16*s, cy - 44*s - h*.7, cx + 6*s + k*16*s, cy - 44*s - h*.4, cx - 16*s + k*16*s, cy - 44*s)
        ctx.fill()


def ex_megalith(ctx, cx, cy, s=1., a=1., t=0.):
    """a dolmen: upright slabs under a capstone"""
    for dx in (-78, 78):
        carve(ctx, lambda dx=dx: ctx.rectangle(cx + dx*s - 20*s, cy - 40*s, 40*s, 110*s),
              tuple(v*1.15 for v in S['basalt']), a, depth=4.4*s, seed=50)
    carve(ctx, lambda: poly(ctx, [(cx - 128*s, cy - 42*s), (cx + 128*s, cy - 56*s),
                                  (cx + 120*s, cy - 86*s), (cx - 120*s, cy - 72*s)]),
          tuple(v*1.25 for v in S['basalt']), a, depth=5.2*s)


EXHIBITS.update({
    7: (ex_leaf, 'EP 7 · RIGVEDA LEAF'),
    8: (ex_pgw, 'EP 8 · PAINTED GREY WARE'),
    9: (ex_leaf, 'EP 9 · PALM-LEAF TEXTS'),
    10: (ex_altar, 'EP 10 · FIRE ALTAR'),
    11: (ex_megalith, 'EP 11 · BURIAL STONE'),
})
