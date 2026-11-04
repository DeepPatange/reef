#!/usr/bin/env python3
"""The Al Reef & Laurel monogram: a loofah cross-section drawn in one even line.
Outer skin, three seed chambers and the Y-shaped fibre walls between them, after the client's sketch.
Exposes mark_paths(variant) -> list of SVG path strings in a 124 × 124 viewBox."""
import math

def closed_curve(pts, tension=1.0):
    """Closed Catmull-Rom spline through pts, returned as an SVG path."""
    n = len(pts)
    d = f"M {pts[0][0]:.2f} {pts[0][1]:.2f} "
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * tension, p1[1] + (p2[1] - p0[1]) / 6 * tension)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * tension, p2[1] - (p3[1] - p1[1]) / 6 * tension)
        d += f"C {c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {p2[0]:.2f} {p2[1]:.2f} "
    return d + "Z"

def blob(cx, cy, rx, ry, rot_deg, wobble, n=8, flat=None):
    """Organic closed shape. wobble: list of radial multipliers (len n). flat: (angle_deg, amount) flattens one side."""
    pts = []
    rot = math.radians(rot_deg)
    for i in range(n):
        a = 2 * math.pi * i / n
        k = wobble[i % len(wobble)]
        if flat:
            fa, amt = math.radians(flat[0]), flat[1]
            k *= 1 - amt * max(0.0, math.cos(a - fa)) ** 3
        x, y = rx * k * math.cos(a), ry * k * math.sin(a)
        pts.append((cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot)))
    return closed_curve(pts)

def mark_paths(variant="hand"):
    if variant == "hand":       # closest to the sketch: wobbly skin, irregular chambers
        outer = closed_curve([(67, 10.5), (97.5, 23.5), (114.5, 61), (103.5, 98.5), (70, 113.5), (27.5, 104),
                              (9.5, 66), (24, 27)])
        a = blob(37.5, 57.5, 13.8, 14.8, -12, [1.0, .96, 1.04, .98, 1.02, .95, 1.03, .99], flat=(0, .16))
        b = blob(80.5, 46.5, 14.2, 15.6, 10, [1.02, .97, 1.0, 1.04, .96, 1.01, .98, 1.03], flat=(135, .16))
        c = blob(69.5, 90.5, 14.4, 13.4, 4, [.99, 1.03, .97, 1.02, 1.0, .96, 1.04, .98], flat=(-110, .16))
        y = "M 62 66.5 L 55.5 33.5 M 62 66.5 L 39.5 88 M 62 66.5 L 95 75"
    elif variant == "refined":  # same drawing, calmer: rounder skin and chambers, centred Y
        outer = closed_curve([(63, 10), (96, 22.5), (114, 60), (104, 99), (66, 114), (27, 103), (10, 64), (26, 25)])
        a = blob(38.5, 54.5, 14.2, 14.6, -18, [1.0, .99, 1.01, 1.0, 1.0, .99, 1.01, 1.0], flat=(10, .14))
        b = blob(79.5, 48.5, 14.2, 14.8, 18, [1.0, 1.0, .99, 1.01, 1.0, 1.0, .99, 1.01], flat=(140, .14))
        c = blob(64.5, 89.5, 14.6, 13.8, 0, [1.0, 1.01, .99, 1.0, 1.0, .99, 1.01, 1.0], flat=(-95, .14))
        y = "M 61 64 L 57.5 33 M 61 64 L 37.5 84 M 61 64 L 93.5 72"
    else:                       # geometric: true circle skin, even chambers at 120°
        outer = closed_curve([(62 + 52 * math.cos(t), 62 + 52 * math.sin(t)) for t in [i * math.pi / 4 for i in range(8)]])
        chambers = []
        for ang in (-150, -30, 90):
            r = math.radians(ang)
            chambers.append(blob(62 + 25 * math.cos(r), 62 + 25 * math.sin(r), 13.5, 13.5, ang, [1.0], flat=(180, .12)))
        a, b, c = chambers
        y = " ".join(f"M 62 62 L {62 + 36 * math.cos(math.radians(t)):.2f} {62 + 36 * math.sin(math.radians(t)):.2f}" for t in (-90, 30, 150))
    return [outer, a, b, c, y]

def svg(size, color, sw, variant="hand", style=""):
    paths = "".join(f'<path d="{p}"/>' for p in mark_paths(variant))
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 124 124" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" style="display:block;{style}">{paths}</svg>')

if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    cells = []
    for v in ("hand", "refined", "geometric"):
        for sw in (3.4, 4.2):
            cells.append(f'<div class="c"><div class="big">{svg(300, "#3E443D", sw, v)}</div>'
                         f'<div class="row">{svg(96, "#3E443D", sw*1.15, v)}'
                         f'<div class="bx">{svg(62, "#FBF5EC", sw*1.35, v)}</div>{svg(30, "#3E443D", sw*1.6, v)}'
                         f'<div class="bx s">{svg(24, "#FBF5EC", sw*1.8, v)}</div></div><div class="l">{v} · stroke {sw}</div></div>')
    ref = os.path.join(here, "ref-mark.png")
    html = (f'<html><body style="margin:0;background:#FBF5EC;font:13px Inter, sans-serif;color:#3E443D">'
            f'<style>.g{{display:grid;grid-template-columns:repeat(3,360px);gap:24px;padding:24px}}.c{{background:#fff;padding:20px;border-radius:6px}}'
            f'.row{{display:flex;align-items:center;gap:16px;margin-top:12px}}.bx{{width:82px;height:82px;background:#3E443D;display:flex;align-items:center;justify-content:center}}'
            f'.bx.s{{width:32px;height:32px}}.l{{margin-top:8px}}</style>'
            f'<div style="padding:24px 24px 0;display:flex;gap:20px;align-items:center"><img src="file://{ref}" style="width:220px">Client sketch</div>'
            f'<div class="g">{"".join(cells)}</div></body></html>')
    open(os.path.join(here, "mark-test.html"), "w").write(html)
    print("ok")
