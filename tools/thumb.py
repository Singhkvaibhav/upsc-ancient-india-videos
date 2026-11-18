"""Designed thumbnails for Ancient India, Simply Unearthed.

A thumbnail is drawn, never grabbed from a video frame: no caption box, no corner
tag, no timeline ribbon. The subject sits right, the title sits left, and the
lamp does the work.

usage:  python3 tools/thumb.py <EP> "<TITLE LINE 1>" "<TITLE LINE 2>" [kicker] [out.png]
"""
import sys, os, math, cairo, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine.core import W, H, lerp, rgba, rrect
from engine.stone import (S, carve, incise, coursed, poly, lamp, dust, vignette, grain,
                          bg_stone, bg_trench, bg_museum, brush, drain_section, house,
                          platform, brick, pot, filmgrain)
from engine.monument import (bg_sky, horizon, haze, godrays, crowd, silhouette, birds,
                             stupa, temple, chaitya, pillar, fort)
from engine import museum


def big(ctx, s, x, y, size, col, align='l', stroke=17, serif=True):
    ctx.select_font_face('DejaVu Serif' if serif else 'Inter',
                         cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    e = ctx.text_extents(s)
    dx = -e.x_advance/2 if align == 'c' else (-e.x_advance if align == 'r' else 0)
    ctx.save()
    ctx.move_to(x + dx + 8, y + 10); ctx.text_path(s)
    ctx.set_source_rgba(0, 0, 0, .66); ctx.fill()
    ctx.move_to(x + dx, y); ctx.text_path(s)
    ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(stroke)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
    rgba(ctx, col); ctx.fill()
    ctx.restore()
    return e.x_advance


def kicker(ctx, s, x, y, col=None, size=34):
    col = col or S['ochre']
    ctx.select_font_face('Inter', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    e = ctx.text_extents(s); w, h = e.x_advance + 46, size*1.9
    rgba(ctx, (0.04, 0.035, 0.03), .94); rrect(ctx, x, y - h/2, w, h, 8); ctx.fill()
    rgba(ctx, col); ctx.set_line_width(5); rrect(ctx, x, y - h/2, w, h, 8); ctx.stroke()
    rgba(ctx, S['lime']); ctx.move_to(x + 23, y + size*.36); ctx.show_text(s)


def frame_dark(ctx, fx=.70, fy=.52):
    """a heavy vignette biased away from the title side, so the words stay readable"""
    g = cairo.RadialGradient(W*fx, H*fy, 220, W/2, H/2, 1260)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, .72)
    ctx.set_source(g); ctx.paint()
    lg = cairo.LinearGradient(0, 0, W*.62, 0)
    lg.add_color_stop_rgba(0, 0, 0, 0, .64); lg.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(lg); ctx.paint()


# ---------- one subject function per episode that needs its own ----------
def subj_ep04(ctx, t=3.0):
    bg_trench(ctx, t)
    ctx.save(); ctx.translate(430, 90); ctx.scale(1.16, 1.16)
    drain_section(ctx, 520, 520, 1080, 1., slabs=9, depth=7.)
    ctx.restore()
    rr = random.Random(4)
    for i in range(700):
        x, y = rr.uniform(1180, 1920), rr.uniform(480, 860)
        f = max(0., (x - 1180)/740)
        rgba(ctx, S['clay'], rr.uniform(.15, .9)*min(1, f*1.7))
        ctx.arc(x, y, rr.uniform(1.2, 4.6), 0, 2*math.pi); ctx.fill()
    brush(ctx, 1290, 430, 1.0, 1., 1.9)
    lamp(ctx, 1240, 330, 760, .34)


SUBJECTS = {4: subj_ep04}


def generic(ctx, ep, t=3.0):
    """default: the episode's exhibit, lit in the dark, on the museum wall"""
    bg_stone(ctx, t, lampx=W*.70, lampy=420, beam=False)
    ent = museum.EXHIBITS.get(ep)
    lamp(ctx, 1320, 540, 620, .40)
    if ent:
        ctx.save(); ctx.translate(1320, 560); ctx.scale(3.0, 3.0); ctx.translate(-1320, -560)
        ent[0](ctx, 1320, 560, 1., 1., t)
        ctx.restore()
    dust(ctx, t, .5, cx=1320, r=560)


def build(ep, l1, l2=None, kick=None, out=None):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    (SUBJECTS.get(ep) or (lambda c, t=3.0: generic(c, ep, t)))(ctx)
    frame_dark(ctx)
    y = 430 if l2 else 520
    big(ctx, l1, 80, y, 136, (1, 1, 1))
    if l2: big(ctx, l2, 80, y + 150, 136, S['ochre'])
    if kick: kicker(ctx, kick, 86, y + 250)
    ctx.select_font_face('Inter', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(32); rgba(ctx, (1, 1, 1), .82)
    s = 'GyaanXstudios'; e = ctx.text_extents(s)
    ctx.move_to(W - 70 - e.x_advance, H - 56); ctx.show_text(s)
    filmgrain(ctx, 2.0, .04)
    out = out or f'Anc{ep:02d}_thumb.png'
    surf.write_to_png(out)
    return out


if __name__ == '__main__':
    ep = int(sys.argv[1])
    l1 = sys.argv[2]
    l2 = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else None
    kick = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] else None
    out = sys.argv[5] if len(sys.argv) > 5 else None
    print(build(ep, l1, l2, kick, out))
