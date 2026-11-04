import glob, os, itertools, sys, io
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.varLib.instancer import instantiateVariableFont
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
def metrics(font):
    cmap = font.getBestCmap(); gs = font.getGlyphSet(); hm = font["hmtx"]; upm = font["head"].unitsPerEm; out = {}
    for ch in CHARS:
        g = cmap.get(ord(ch))
        if not g: continue
        bp = BoundsPen(gs); gs[g].draw(bp)
        if bp.bounds is None: continue
        out[ch] = (hm[g][0] / upm, tuple(v / upm for v in bp.bounds))
    return out
def score(a, b):
    c = [k for k in a if k in b]
    if not c: return 9e9
    return (sum((a[k][0]-b[k][0])**2 + 0.5*sum((x-y)**2 for x, y in zip(a[k][1], b[k][1])) for k in c) / len(c)) ** 0.5 * 1000
fam, var, grid = sys.argv[1], sys.argv[2], eval(sys.argv[3])
targets = {os.path.basename(f): metrics(TTFont(f)) for f in sorted(glob.glob(f"qf/*_{fam}*.ttf"))}
raw = open(var, "rb").read(); res = {k: [] for k in targets}
for combo in itertools.product(*grid.values()):
    loc = dict(zip(grid, combo))
    m = metrics(instantiateVariableFont(TTFont(io.BytesIO(raw)), loc, inplace=False, updateFontNames=False))
    for k, t in targets.items(): res[k].append((score(t, m), loc))
for k, r in res.items():
    r.sort(key=lambda x: x[0])
    print(f"{k:34} n={len(targets[k]):2} best={r[0][1]} err={r[0][0]:.2f} | {r[1][1]} {r[1][0]:.2f} | {r[2][1]} {r[2][0]:.2f}", flush=True)
