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


# ---------- Unit 3 exhibits ----------
def ex_punchcoin(ctx, cx, cy, s=1., a=1., t=0.):
    """a punch-marked coin: an irregular silver piece with several separate marks
    and no ruler's name on it."""
    carve(ctx, lambda: poly(ctx, [(cx - 86*s, cy - 62*s), (cx + 60*s, cy - 80*s), (cx + 88*s, cy + 34*s),
                                  (cx + 12*s, cy + 82*s), (cx - 78*s, cy + 46*s)]),
          tuple(v*1.08 for v in S['lime']), a, depth=4.4*s)
    rr = random.Random(11)
    for k in range(5):
        px, py = cx + rr.uniform(-54, 50)*s, cy + rr.uniform(-42, 44)*s
        rgba(ctx, S['soot'], .46*a)
        if k % 3 == 0:
            ctx.arc(px, py, 13*s, 0, 2*math.pi); ctx.fill()
        elif k % 3 == 1:
            for j in range(6):
                ang = j*math.pi/3
                ctx.move_to(px, py); ctx.line_to(px + 15*s*math.cos(ang), py + 15*s*math.sin(ang))
            ctx.set_line_width(3.2*s); ctx.stroke()
        else:
            ctx.rectangle(px - 11*s, py - 11*s, 22*s, 22*s); ctx.fill()


def ex_wallsection(ctx, cx, cy, s=1., a=1., t=0.):
    """a cut section of rampart: earth core, brick face, and the stumps of a
    timber palisade along the top."""
    carve(ctx, lambda: poly(ctx, [(cx - 130*s, cy + 76*s), (cx - 96*s, cy - 46*s), (cx + 96*s, cy - 46*s),
                                  (cx + 130*s, cy + 76*s)]), tuple(v*.86 for v in S['clay']), a, depth=5*s)
    carve(ctx, lambda: ctx.rectangle(cx - 100*s, cy - 46*s, 200*s, 42*s), S['sand'], a, depth=3.6*s, seed=61)
    coursed(ctx, cx - 100*s, cy - 46*s, 200*s, 42*s, a*.85, seed=62, course=13*s)
    for k in range(5):
        carve(ctx, lambda k=k: ctx.rectangle(cx - 86*s + k*40*s, cy - 80*s, 15*s, 36*s),
              tuple(v*.78 for v in S['clay']), a, depth=2.6*s, tex=.3, seed=70 + k)


def ex_bodhi(ctx, cx, cy, s=1., a=1., t=0.):
    """the Bodhi tree above an empty throne, with footprints before it: the
    aniconic way early Indian art showed the Buddha. No figure is drawn."""
    carve(ctx, lambda: ctx.rectangle(cx - 13*s, cy - 72*s, 26*s, 98*s),
          tuple(v*.78 for v in S['clay']), a, depth=3.4*s)
    # the canopy: one solid heart-leaved mass, notched at the rim
    def canopy():
        ctx.move_to(cx - 118*s, cy - 78*s)
        ctx.curve_to(cx - 132*s, cy - 136*s, cx - 62*s, cy - 178*s, cx, cy - 172*s)
        ctx.curve_to(cx + 62*s, cy - 178*s, cx + 132*s, cy - 136*s, cx + 118*s, cy - 78*s)
        ctx.curve_to(cx + 70*s, cy - 50*s, cx - 70*s, cy - 50*s, cx - 118*s, cy - 78*s)
        ctx.close_path()
    carve(ctx, canopy, tuple(v*.92 for v in S['clay']), a, depth=4.2*s, tex=.24, seed=80)
    ctx.save(); ctx.new_path(); canopy(); ctx.clip()
    for k in range(9):                      # a few leaf veins, so it reads as foliage
        lx = cx - 100*s + k*25*s
        rgba(ctx, S['soot'], .18*a); ctx.set_line_width(3*s)
        ctx.move_to(lx, cy - 58*s); ctx.line_to(lx + 12*s, cy - 148*s); ctx.stroke()
    ctx.restore()
    for k in range(7):                      # heart-shaped leaves along the rim
        lx = cx - 96*s + k*32*s
        ly = cy - 62*s - 14*s*math.sin(k*.9)
        carve(ctx, lambda lx=lx, ly=ly: poly(ctx, [(lx, ly + 24*s), (lx - 16*s, ly),
                                                   (lx, ly - 18*s), (lx + 16*s, ly)]),
              tuple(v*.86 for v in S['clay']), a*.95, depth=2.*s, tex=.2, seed=90 + k)
    # the empty seat
    carve(ctx, lambda: ctx.rectangle(cx - 56*s, cy + 22*s, 112*s, 20*s), S['sand'], a, depth=4*s, seed=91)
    for dx in (-44, 44):
        carve(ctx, lambda dx=dx: ctx.rectangle(cx + dx*s - 9*s, cy + 42*s, 18*s, 32*s), S['sand'], a, depth=3*s, seed=92)
    # footprints before it
    for dx in (-19, 19):
        carve(ctx, lambda dx=dx: rrect(ctx, cx + dx*s - 11*s, cy + 82*s, 22*s, 34*s, 10*s),
              tuple(v*.9 for v in S['sand']), a, depth=2.2*s, tex=.25, seed=95)


def ex_stupamodel(ctx, cx, cy, s=1., a=1., t=0.):
    """a small stupa: dome, railing, mast and tiered umbrellas"""
    carve(ctx, lambda: ctx.rectangle(cx - 104*s, cy + 44*s, 208*s, 26*s), S['sand'], a, depth=4*s)
    carve(ctx, lambda: (ctx.save(), ctx.translate(cx, cy + 44*s), ctx.scale(1, .86),
                        ctx.arc(0, 0, 86*s, math.pi, 2*math.pi), ctx.restore(), ctx.close_path()),
          S['lime'], a, depth=5*s, seed=101)
    for k in range(7):
        carve(ctx, lambda k=k: ctx.rectangle(cx - 104*s + k*30*s, cy + 44*s, 9*s, 30*s),
              tuple(v*.9 for v in S['sand']), a, depth=2*s, tex=.2, seed=110 + k)
    carve(ctx, lambda: ctx.rectangle(cx - 24*s, cy - 58*s, 48*s, 26*s), S['sand'], a, depth=3*s, seed=120)
    carve(ctx, lambda: ctx.rectangle(cx - 4*s, cy - 104*s, 8*s, 50*s), tuple(v*.8 for v in S['clay']), a, depth=2.4*s)
    for k in range(3):
        w_ = (46 - k*12)*s
        carve(ctx, lambda k=k, w_=w_: ctx.rectangle(cx - w_, cy - 100*s + k*15*s, w_*2, 7*s),
              S['ochre'], a, depth=2*s, tex=.2, seed=130 + k)


def ex_ayagapata(ctx, cx, cy, s=1., a=1., t=0.):
    """an ayagapata, a Jain votive tablet: a square slab with symbols and a band
    of ornament around an empty central panel. Nothing revered is depicted."""
    carve(ctx, lambda: rrect(ctx, cx - 98*s, cy - 98*s, 196*s, 196*s, 8*s), S['sand'], a, depth=5*s)
    carve(ctx, lambda: ctx.arc(cx, cy, 62*s, 0, 2*math.pi), tuple(v*.94 for v in S['sand']), a, depth=3*s, seed=141)
    # a lotus-petal band, and corner symbols
    for k in range(16):
        ang = k*math.pi/8
        px, py = cx + 44*s*math.cos(ang), cy + 44*s*math.sin(ang)
        rgba(ctx, S['soot'], .34*a)
        ctx.arc(px, py, 8*s, 0, 2*math.pi); ctx.fill()
    for dx, dy in ((-70, -70), (70, -70), (-70, 70), (70, 70)):
        rgba(ctx, S['soot'], .4*a)
        ctx.rectangle(cx + dx*s - 13*s, cy + dy*s - 13*s, 26*s, 26*s); ctx.fill()
    for k in range(4):
        rgba(ctx, S['soot'], .34*a)
        ctx.rectangle(cx - 58*s, cy + 74*s + k*0, 116*s, 5*s); ctx.fill()


def ex_greekcoin(ctx, cx, cy, s=1., a=1., t=0.):
    """a Greek-style silver coin: a round flan with a generic profile in relief and
    lettering round the rim. The head is an invented generic form, not a portrait."""
    carve(ctx, lambda: ctx.arc(cx, cy, 92*s, 0, 2*math.pi), tuple(v*1.06 for v in S['lime']), a, depth=5.4*s)
    carve(ctx, lambda: poly(ctx, [(cx - 34*s, cy + 46*s), (cx - 40*s, cy - 6*s), (cx - 22*s, cy - 40*s),
                                  (cx + 14*s, cy - 46*s), (cx + 34*s, cy - 18*s), (cx + 26*s, cy + 16*s),
                                  (cx + 32*s, cy + 46*s)]),
          tuple(v*.9 for v in S['lime']), a, depth=3.4*s, tex=.2, seed=151)
    for k in range(18):
        ang = k*math.pi/9
        rgba(ctx, S['soot'], .34*a)
        ctx.rectangle(cx + 78*s*math.cos(ang) - 3*s, cy + 78*s*math.sin(ang) - 3*s, 6*s, 6*s); ctx.fill()


EXHIBITS.update({
    12: (ex_punchcoin, 'EP 12 · PUNCH-MARKED COIN'),
    13: (ex_wallsection, 'EP 13 · CITY WALL SECTION'),
    14: (ex_bodhi, 'EP 14 · TREE AND EMPTY THRONE'),
    15: (ex_stupamodel, 'EP 15 · STUPA'),
    16: (ex_ayagapata, 'EP 16 · VOTIVE TABLET'),
    17: (ex_greekcoin, 'EP 17 · GREEK-STYLE COIN'),
})


# ---------- Unit 4 exhibits ----------
def ex_arthashastra(ctx, cx, cy, s=1., a=1., t=0.):
    """a palm-leaf manuscript of the Arthashastra, open rather than bound shut:
    a manual, so it is shown as a book in use."""
    carve(ctx, lambda: poly(ctx, [(cx - 128*s, cy + 44*s), (cx - 4*s, cy + 22*s),
                                  (cx - 4*s, cy - 34*s), (cx - 122*s, cy - 12*s)]),
          S['sand'], a, depth=3.6*s, seed=160)
    carve(ctx, lambda: poly(ctx, [(cx + 128*s, cy + 44*s), (cx + 4*s, cy + 22*s),
                                  (cx + 4*s, cy - 34*s), (cx + 122*s, cy - 12*s)]),
          S['sand'], a, depth=3.6*s, seed=161)
    for side in (-1, 1):
        for k in range(5):
            rgba(ctx, S['soot'], .4*a)
            ctx.rectangle(cx + side*22*s - (0 if side > 0 else 84*s), cy - 18*s + k*13*s, 84*s, 4.4*s)
            ctx.fill()
    carve(ctx, lambda: rrect(ctx, cx - 140*s, cy + 40*s, 280*s, 18*s, 5*s),
          tuple(v*.78 for v in S['clay']), a, depth=3*s)


def ex_bullcapital(ctx, cx, cy, s=1., a=1., t=0.):
    """the Rampurva bull capital: a standing bull on a bell-shaped lotus base.
    This is NOT the Sarnath lion capital, whose use is restricted by law."""
    carve(ctx, lambda: ctx.rectangle(cx - 34*s, cy + 56*s, 68*s, 36*s), tuple(v*.9 for v in S['sand']), a, depth=4*s)
    # the inverted lotus bell
    def bell():
        ctx.move_to(cx - 72*s, cy + 56*s)
        ctx.curve_to(cx - 62*s, cy + 10*s, cx - 34*s, cy + 2*s, cx - 28*s, cy - 4*s)
        ctx.line_to(cx + 28*s, cy - 4*s)
        ctx.curve_to(cx + 34*s, cy + 2*s, cx + 62*s, cy + 10*s, cx + 72*s, cy + 56*s)
        ctx.close_path()
    carve(ctx, bell, S['lime'], a, depth=4.4*s, seed=170)
    ctx.save(); ctx.new_path(); bell(); ctx.clip()
    for k in range(9):
        rgba(ctx, S['soot'], .2*a); ctx.set_line_width(2.6*s)
        ctx.move_to(cx - 72*s + k*18*s, cy + 56*s); ctx.line_to(cx - 26*s + k*6.6*s, cy - 4*s); ctx.stroke()
    ctx.restore()
    # the abacus the bull stands on
    carve(ctx, lambda: ctx.rectangle(cx - 66*s, cy - 22*s, 132*s, 18*s), S['sand'], a, depth=3*s, seed=171)
    # a standing bull in profile, facing left: body, hump, head, legs, tail
    col = tuple(v*.96 for v in S['lime'])
    carve(ctx, lambda: rrect(ctx, cx - 50*s, cy - 78*s, 104*s, 40*s, 14*s), col, a, depth=3.6*s, tex=.2, seed=172)
    carve(ctx, lambda: (ctx.save(), ctx.translate(cx + 4*s, cy - 78*s), ctx.scale(1, .62),
                        ctx.arc(0, 0, 30*s, math.pi, 2*math.pi), ctx.restore(), ctx.close_path()),
          col, a, depth=3.2*s, tex=.2, seed=173)            # the hump
    carve(ctx, lambda: poly(ctx, [(cx - 50*s, cy - 72*s), (cx - 78*s, cy - 66*s), (cx - 88*s, cy - 52*s),
                                  (cx - 76*s, cy - 40*s), (cx - 50*s, cy - 44*s)]),
          col, a, depth=3.*s, tex=.2, seed=174)              # the head, lowered
    carve(ctx, lambda: poly(ctx, [(cx - 84*s, cy - 66*s), (cx - 92*s, cy - 80*s), (cx - 74*s, cy - 70*s)]),
          col, a, depth=2.4*s, tex=.2, seed=175)             # a horn
    for dx in (-38, -16, 26, 46):
        carve(ctx, lambda dx=dx: ctx.rectangle(cx + dx*s - 6*s, cy - 42*s, 12*s, 24*s),
              col, a, depth=2.6*s, tex=.2, seed=176)         # legs
    rgba(ctx, S['soot'], .3*a); ctx.set_line_width(4*s)
    ctx.move_to(cx + 54*s, cy - 70*s); ctx.curve_to(cx + 68*s, cy - 58*s, cx + 64*s, cy - 38*s, cx + 58*s, cy - 26*s)
    ctx.stroke()                                             # the tail


def ex_rockedict(ctx, cx, cy, s=1., a=1., t=0.):
    """a boulder face carved with lines of early Brahmi, shown as incised bands"""
    carve(ctx, lambda: poly(ctx, [(cx - 118*s, cy + 76*s), (cx - 132*s, cy - 18*s), (cx - 64*s, cy - 80*s),
                                  (cx + 56*s, cy - 86*s), (cx + 130*s, cy - 10*s), (cx + 116*s, cy + 76*s)]),
          tuple(v*1.12 for v in S['basalt']), a, depth=5.6*s, seed=180)
    rr = random.Random(19)
    for k in range(7):
        w_ = rr.uniform(.6, 1.) * 170*s
        rgba(ctx, S['lime'], .34*a)
        ctx.rectangle(cx - w_/2, cy - 52*s + k*17*s, w_, 5.5*s); ctx.fill()


def ex_pillarsection(ctx, cx, cy, s=1., a=1., t=0.):
    """a drum of polished Mauryan sandstone, with a mirror sheen"""
    carve(ctx, lambda: ctx.rectangle(cx - 56*s, cy - 84*s, 112*s, 168*s), S['sand'], a, depth=5*s, seed=190)
    g = cairo.LinearGradient(cx - 56*s, 0, cx + 56*s, 0)
    g.add_color_stop_rgba(0., 1, 1, 1, 0)
    g.add_color_stop_rgba(.34, 1, .99, .95, .34*a)
    g.add_color_stop_rgba(.52, 1, 1, 1, .08*a)
    g.add_color_stop_rgba(1., 0, 0, 0, .18*a)
    ctx.rectangle(cx - 56*s, cy - 84*s, 112*s, 168*s); ctx.set_source(g); ctx.fill()
    carve(ctx, lambda: ctx.rectangle(cx - 68*s, cy + 84*s, 136*s, 20*s), tuple(v*.9 for v in S['sand']), a, depth=3.4*s)


EXHIBITS.update({
    18: (ex_arthashastra, 'EP 18 · ARTHASHASTRA'),
    19: (ex_bullcapital, 'EP 19 · RAMPURVA BULL CAPITAL'),
    20: (ex_rockedict, 'EP 20 · ROCK EDICT'),
    21: (ex_pillarsection, 'EP 21 · POLISHED PILLAR'),
})


# ---------- Unit 5 exhibits ----------
def ex_torana(ctx, cx, cy, s=1., a=1., t=0.):
    """a stupa gateway: two posts and three crossbars, crowded with small panels.
    The panels are ornament only; nothing revered is depicted."""
    for dx in (-86, 86):
        carve(ctx, lambda dx=dx: ctx.rectangle(cx + dx*s - 17*s, cy - 70*s, 34*s, 160*s),
              S['sand'], a, depth=4.4*s, seed=200)
        for k in range(4):
            rgba(ctx, S['soot'], .26*a)
            ctx.rectangle(cx + dx*s - 12*s, cy - 58*s + k*38*s, 24*s, 26*s); ctx.fill()
    for k in range(3):
        y = cy - 76*s - k*30*s
        w_ = (124 - k*4)*s
        carve(ctx, lambda y=y, w_=w_: rrect(ctx, cx - w_, y - 17*s, w_*2, 21*s, 4*s),
              S['sand'], a, depth=3.4*s, seed=210 + k)
        for j in range(7):
            rgba(ctx, S['soot'], .22*a)
            ctx.rectangle(cx - w_ + 12*s + j*(w_*2 - 24*s)/7, y - 13*s, 11*s, 13*s); ctx.fill()
    carve(ctx, lambda: ctx.rectangle(cx - 110*s, cy + 90*s, 220*s, 16*s),
          tuple(v*.86 for v in S['clay']), a, depth=3*s)


def ex_bicoin(ctx, cx, cy, s=1., a=1., t=0.):
    """a bilingual Indo-Greek coin: a generic profile, and lettering in two
    different scripts around the two edges. The head is an invented form."""
    carve(ctx, lambda: ctx.arc(cx, cy, 88*s, 0, 2*math.pi), tuple(v*1.05 for v in S['lime']), a, depth=5*s)
    carve(ctx, lambda: poly(ctx, [(cx - 30*s, cy + 42*s), (cx - 36*s, cy - 4*s), (cx - 18*s, cy - 36*s),
                                  (cx + 12*s, cy - 42*s), (cx + 30*s, cy - 16*s), (cx + 22*s, cy + 14*s),
                                  (cx + 28*s, cy + 42*s)]),
          tuple(v*.9 for v in S['lime']), a, depth=3.2*s, tex=.2, seed=220)
    for k in range(10):                       # one script, upper arc: upright marks
        ang = math.pi + k*math.pi/9
        rgba(ctx, S['soot'], .34*a)
        ctx.rectangle(cx + 74*s*math.cos(ang) - 2.5*s, cy + 74*s*math.sin(ang) - 6*s, 5*s, 12*s); ctx.fill()
    for k in range(9):                        # the other, lower arc: sloped marks
        ang = k*math.pi/8
        rgba(ctx, S['soot'], .34*a)
        ctx.save(); ctx.translate(cx + 74*s*math.cos(ang), cy + 74*s*math.sin(ang)); ctx.rotate(.6)
        ctx.rectangle(-2.5*s, -6*s, 5*s, 12*s); ctx.fill(); ctx.restore()


def ex_goldcoin(ctx, cx, cy, s=1., a=1., t=0.):
    """a thick Kushana gold coin: a standing figure one side, an emblem the other"""
    carve(ctx, lambda: ctx.arc(cx, cy, 86*s, 0, 2*math.pi), S['ochre'], a, depth=6.5*s)
    carve(ctx, lambda: ctx.arc(cx, cy, 70*s, 0, 2*math.pi), tuple(v*1.08 for v in S['ochre']),
          a, depth=3*s, tex=.18, seed=230)
    carve(ctx, lambda: poly(ctx, [(cx - 14*s, cy + 44*s), (cx - 11*s, cy - 18*s), (cx - 24*s, cy - 10*s),
                                  (cx - 18*s, cy - 26*s), (cx + 18*s, cy - 26*s), (cx + 24*s, cy - 10*s),
                                  (cx + 11*s, cy - 18*s), (cx + 14*s, cy + 44*s)]),
          tuple(v*.84 for v in S['ochre']), a, depth=3*s, tex=.2, seed=231)
    carve(ctx, lambda: ctx.arc(cx, cy - 38*s, 13*s, 0, 2*math.pi),
          tuple(v*.84 for v in S['ochre']), a, depth=2.6*s, seed=232)
    for k in range(14):
        ang = k*math.pi/7
        rgba(ctx, S['soot'], .22*a)
        ctx.arc(cx + 78*s*math.cos(ang), cy + 78*s*math.sin(ang), 3.4*s, 0, 2*math.pi); ctx.fill()


def ex_herostone(ctx, cx, cy, s=1., a=1., t=0.):
    """a hero stone: an upright slab, a standing figure in low relief, and lines
    of early Tamil-Brahmi beneath it."""
    carve(ctx, lambda: poly(ctx, [(cx - 62*s, cy + 92*s), (cx - 62*s, cy - 58*s), (cx, cy - 96*s),
                                  (cx + 62*s, cy - 58*s), (cx + 62*s, cy + 92*s)]),
          tuple(v*1.1 for v in S['basalt']), a, depth=5.4*s, seed=240)
    carve(ctx, lambda: ctx.rectangle(cx - 9*s, cy - 56*s, 18*s, 54*s),
          tuple(v*1.3 for v in S['basalt']), a, depth=3*s, tex=.2, seed=241)
    carve(ctx, lambda: ctx.arc(cx, cy - 66*s, 11*s, 0, 2*math.pi),
          tuple(v*1.3 for v in S['basalt']), a, depth=2.6*s, seed=242)
    for dx in (-1, 1):
        rgba(ctx, S['lime'], .3*a); ctx.set_line_width(4.4*s)
        ctx.move_to(cx + dx*8*s, cy - 46*s); ctx.line_to(cx + dx*30*s, cy - 22*s); ctx.stroke()
    for k in range(3):
        rgba(ctx, S['lime'], .3*a)
        ctx.rectangle(cx - 44*s, cy + 22*s + k*20*s, 88*s - (k % 2)*22*s, 6*s); ctx.fill()


def ex_tamilleaf(ctx, cx, cy, s=1., a=1., t=0.):
    """a Tamil palm-leaf manuscript: long narrow leaves on a cord, boards either end"""
    for k in range(6):
        carve(ctx, lambda k=k: rrect(ctx, cx - 134*s + (k % 2)*5*s, cy - 46*s + k*17*s, 268*s, 14*s, 6*s),
              S['sand'], a, depth=2.2*s, tex=.26, seed=250 + k)
        for j in range(9):
            rgba(ctx, S['soot'], .3*a)
            ctx.rectangle(cx - 112*s + j*25*s, cy - 42*s + k*17*s, 15*s, 4*s); ctx.fill()
    for dy in (-62, 60):
        carve(ctx, lambda dy=dy: rrect(ctx, cx - 142*s, cy + dy*s, 284*s, 18*s, 5*s),
              tuple(v*.76 for v in S['clay']), a, depth=3.2*s, seed=260)
    rgba(ctx, S['soot'], .44*a); ctx.set_line_width(3*s)
    ctx.move_to(cx - 70*s, cy - 64*s); ctx.line_to(cx - 70*s, cy + 80*s); ctx.stroke()


def ex_amphora(ctx, cx, cy, s=1., a=1., t=0.):
    """a Roman amphora: a tall two-handled jar with a pointed base"""
    def body():
        ctx.move_to(cx - 44*s, cy - 52*s)
        ctx.curve_to(cx - 62*s, cy + 10*s, cx - 26*s, cy + 56*s, cx, cy + 96*s)
        ctx.curve_to(cx + 26*s, cy + 56*s, cx + 62*s, cy + 10*s, cx + 44*s, cy - 52*s)
        ctx.close_path()
    carve(ctx, body, tuple(v*1.3 for v in S['terra']), a, depth=5*s, seed=270)
    carve(ctx, lambda: ctx.rectangle(cx - 17*s, cy - 94*s, 34*s, 46*s),
          tuple(v*1.2 for v in S['terra']), a, depth=3.4*s, seed=271)
    carve(ctx, lambda: rrect(ctx, cx - 27*s, cy - 106*s, 54*s, 18*s, 6*s),
          tuple(v*1.24 for v in S['terra']), a, depth=3*s, seed=272)
    for dx in (-1, 1):
        rgba(ctx, tuple(v*1.1 for v in S['terra']), .95*a); ctx.set_line_width(11*s)
        ctx.move_to(cx + dx*20*s, cy - 86*s)
        ctx.curve_to(cx + dx*58*s, cy - 80*s, cx + dx*56*s, cy - 46*s, cx + dx*38*s, cy - 40*s)
        ctx.stroke()


EXHIBITS.update({
    22: (ex_torana, 'EP 22 · STUPA GATEWAY'),
    23: (ex_bicoin, 'EP 23 · BILINGUAL COIN'),
    24: (ex_goldcoin, 'EP 24 · KUSHANA GOLD'),
    25: (ex_herostone, 'EP 25 · HERO STONE'),
    26: (ex_tamilleaf, 'EP 26 · TAMIL MANUSCRIPT'),
    27: (ex_amphora, 'EP 27 · ROMAN AMPHORA'),
})


# ---------- Unit 6 exhibits ----------
def ex_guptacoin(ctx, cx, cy, s=1., a=1., t=0.):
    """a Gupta gold coin: a standing archer one face, a seated figure the other,
    both as simple carved forms, with a Sanskrit legend round the rim."""
    carve(ctx, lambda: ctx.arc(cx, cy, 84*s, 0, 2*math.pi), S['ochre'], a, depth=5.6*s)
    carve(ctx, lambda: ctx.arc(cx, cy, 68*s, 0, 2*math.pi), tuple(v*1.07 for v in S['ochre']),
          a, depth=2.6*s, tex=.18, seed=500)
    carve(ctx, lambda: poly(ctx, [(cx - 10*s, cy + 46*s), (cx - 8*s, cy - 20*s), (cx - 20*s, cy - 30*s),
                                  (cx + 2*s, cy - 36*s), (cx + 18*s, cy - 24*s), (cx + 10*s, cy - 16*s),
                                  (cx + 14*s, cy + 46*s)]),
          tuple(v*.84 for v in S['ochre']), a, depth=3*s, tex=.2, seed=501)
    rgba(ctx, S['soot'], .36*a); ctx.set_line_width(4*s)   # the bow
    ctx.new_path(); ctx.arc(cx - 34*s, cy + 4*s, 30*s, -1.2, 1.2); ctx.stroke()
    for k in range(16):
        ang = k*math.pi/8
        rgba(ctx, S['soot'], .22*a)
        ctx.rectangle(cx + 76*s*math.cos(ang) - 2.4*s, cy + 76*s*math.sin(ang) - 5*s, 5*s, 10*s); ctx.fill()


def ex_copperplate(ctx, cx, cy, s=1., a=1., t=0.):
    """two copper plates joined by a ring, engraved on the inner faces"""
    for i, dx in enumerate((-96, 96)):
        carve(ctx, lambda dx=dx: rrect(ctx, cx + dx*s - 86*s, cy - 62*s, 172*s, 128*s, 6*s),
              tuple(v*1.18 for v in S['terra']), a, depth=4.2*s, seed=510 + i)
        for k in range(6):
            rgba(ctx, S['soot'], .4*a)
            ctx.rectangle(cx + dx*s - 64*s, cy - 44*s + k*18*s, 128*s - (k % 3)*30*s, 5*s); ctx.fill()
    rgba(ctx, tuple(v*1.1 for v in S['terra']), .95*a); ctx.set_line_width(8*s)
    ctx.new_path(); ctx.arc(cx, cy + 2*s, 26*s, 0, 2*math.pi); ctx.stroke()


def ex_ironpillar(ctx, cx, cy, s=1., a=1., t=0.):
    """the Iron Pillar: a tall tapering shaft with an inscription band and a
    fluted capital. Dark metal, almost unrusted."""
    iron = (0.22, 0.20, 0.19)
    carve(ctx, lambda: poly(ctx, [(cx - 20*s, cy + 96*s), (cx - 13*s, cy - 78*s),
                                  (cx + 13*s, cy - 78*s), (cx + 20*s, cy + 96*s)]),
          iron, a, depth=4.6*s, seed=520)
    carve(ctx, lambda: ctx.rectangle(cx - 22*s, cy - 94*s, 44*s, 18*s), iron, a, depth=3*s, seed=521)
    for k in range(4):
        w_ = (30 - k*5)*s
        carve(ctx, lambda k=k, w_=w_: ctx.rectangle(cx - w_, cy - 112*s + k*9*s, w_*2, 7*s),
              tuple(v*1.5 for v in iron), a, depth=2.2*s, tex=.2, seed=530 + k)
    for k in range(4):                       # the inscription band
        rgba(ctx, S['dust'], .34*a)
        ctx.rectangle(cx - 14*s, cy - 46*s + k*13*s, 28*s, 4*s); ctx.fill()
    carve(ctx, lambda: ctx.rectangle(cx - 44*s, cy + 96*s, 88*s, 18*s),
          tuple(v*.9 for v in S['sand']), a, depth=3.4*s)


def ex_sealedplate(ctx, cx, cy, s=1., a=1., t=0.):
    """a single engraved plate with a round seal fixed to one edge"""
    carve(ctx, lambda: rrect(ctx, cx - 120*s, cy - 70*s, 212*s, 142*s, 6*s),
          tuple(v*1.16 for v in S['terra']), a, depth=4.4*s, seed=540)
    for k in range(7):
        rgba(ctx, S['soot'], .4*a)
        ctx.rectangle(cx - 100*s, cy - 52*s + k*18*s, 170*s - (k % 3)*36*s, 5*s); ctx.fill()
    carve(ctx, lambda: ctx.arc(cx + 116*s, cy + 36*s, 32*s, 0, 2*math.pi),
          tuple(v*1.04 for v in S['clay']), a, depth=4*s, seed=541)
    carve(ctx, lambda: ctx.arc(cx + 116*s, cy + 36*s, 19*s, 0, 2*math.pi),
          tuple(v*.92 for v in S['clay']), a, depth=2.4*s, seed=542)


def ex_painted(ctx, cx, cy, s=1., a=1., t=0.):
    """a fragment of painted plaster: a floral and geometric border, colours
    still readable. Ornament only; no figures."""
    carve(ctx, lambda: poly(ctx, [(cx - 132*s, cy + 76*s), (cx - 142*s, cy - 58*s),
                                  (cx - 40*s, cy - 82*s), (cx + 112*s, cy - 70*s),
                                  (cx + 136*s, cy + 44*s), (cx + 40*s, cy + 84*s)]),
          S['lime'], a, depth=4.4*s, seed=550)
    ctx.save(); ctx.new_path()
    poly(ctx, [(cx - 132*s, cy + 76*s), (cx - 142*s, cy - 58*s), (cx - 40*s, cy - 82*s),
               (cx + 112*s, cy - 70*s), (cx + 136*s, cy + 44*s), (cx + 40*s, cy + 84*s)])
    ctx.clip()
    for k in range(3):
        rgba(ctx, S['terra'], (.5 - k*.08)*a)
        ctx.rectangle(cx - 150*s, cy - 58*s + k*46*s, 300*s, 11*s); ctx.fill()
    for k in range(7):                       # a row of simple rosettes
        px = cx - 120*s + k*38*s
        rgba(ctx, S['ochre'], .5*a); ctx.arc(px, cy + 4*s, 13*s, 0, 2*math.pi); ctx.fill()
        rgba(ctx, S['clay'], .5*a); ctx.arc(px, cy + 4*s, 6*s, 0, 2*math.pi); ctx.fill()
    for k in range(9):                       # a lotus-petal band beneath
        px = cx - 128*s + k*32*s
        rgba(ctx, S['pine'] if 'pine' in S else S['clay'], .34*a)
        ctx.move_to(px, cy + 52*s); ctx.curve_to(px - 12*s, cy + 32*s, px + 12*s, cy + 32*s, px, cy + 52*s)
        ctx.fill()
    ctx.restore()


def ex_ratha(ctx, cx, cy, s=1., a=1., t=0.):
    """a monolithic ratha: a small temple cut whole from one boulder, with a
    stepped tower and a dark empty doorway."""
    carve(ctx, lambda: ctx.rectangle(cx - 92*s, cy + 40*s, 184*s, 48*s), S['sand'], a, depth=4.6*s, seed=560)
    for k in range(4):
        w_ = (78 - k*17)*s
        carve(ctx, lambda k=k, w_=w_: ctx.rectangle(cx - w_, cy + 34*s - k*28*s, w_*2, 26*s),
              S['sand'], a, depth=3.4*s, tex=.24, seed=570 + k)
        for j in range(4 - k):
            rgba(ctx, S['soot'], .2*a)
            ctx.rectangle(cx - w_ + 10*s + j*(w_*2 - 20*s)/max(1, 4 - k), cy + 40*s - k*28*s, 9*s, 13*s)
            ctx.fill()
    carve(ctx, lambda: ctx.arc(cx, cy - 86*s, 26*s, math.pi, 2*math.pi), S['sand'], a, depth=3*s, seed=580)
    ctx.new_path()                           # the sanctum: a dark, empty opening
    ctx.rectangle(cx - 19*s, cy + 36*s, 38*s, 52*s)
    ctx.set_source_rgba(0, 0, 0, .84*a); ctx.fill()


def ex_kailasa(ctx, cx, cy, s=1., a=1., t=0.):
    """Kailasa at Ellora: a temple standing free in a courtyard cut down into
    the rock around it. Architecture only; the sanctum stays empty."""
    # the cut pit: rock walls on three sides, the courtyard floor between them
    for dx in (-150, 150):
        carve(ctx, lambda dx=dx: ctx.rectangle(cx + dx*s - 46*s, cy - 104*s, 92*s, 200*s),
              tuple(v*1.06 for v in S['basalt']), a, depth=5*s, seed=590)
    carve(ctx, lambda: ctx.rectangle(cx - 104*s, cy + 72*s, 208*s, 26*s),
          tuple(v*.96 for v in S['basalt']), a, depth=3*s, seed=591)
    # the temple itself, left standing in the middle
    carve(ctx, lambda: ctx.rectangle(cx - 62*s, cy + 6*s, 124*s, 72*s), S['sand'], a, depth=4.4*s, seed=592)
    for k in range(5):
        w_ = (54 - k*10)*s
        carve(ctx, lambda k=k, w_=w_: ctx.rectangle(cx - w_, cy + 2*s - k*22*s, w_*2, 20*s),
              S['sand'], a, depth=3.2*s, tex=.24, seed=600 + k)
    carve(ctx, lambda: ctx.arc(cx, cy - 104*s, 18*s, math.pi, 2*math.pi), S['sand'], a, depth=2.6*s, seed=610)
    ctx.new_path(); ctx.rectangle(cx - 15*s, cy + 34*s, 30*s, 44*s)
    ctx.set_source_rgba(0, 0, 0, .84*a); ctx.fill()


EXHIBITS.update({
    28: (ex_guptacoin, 'EP 28 · GUPTA GOLD COIN'),
    29: (ex_copperplate, 'EP 29 · COPPER-PLATE GRANT'),
    30: (ex_ironpillar, 'EP 30 · THE IRON PILLAR'),
    31: (ex_sealedplate, 'EP 31 · SEALED COPPER PLATE'),
    32: (ex_painted, 'EP 32 · PAINTED PANEL'),
    33: (ex_ratha, 'EP 33 · MONOLITHIC RATHA'),
    34: (ex_kailasa, 'EP 34 · KAILASA AT ELLORA'),
})
