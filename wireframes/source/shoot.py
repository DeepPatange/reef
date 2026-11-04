#!/usr/bin/env python3
"""Screenshot every .frame in a built page as readable slices + run layout checks.
Usage: python3 shoot.py dist/01-home.html [--only desktop|mobile|notes] [--slice 1800]
Writes shots/<name>-<kind><i>-<n>.png  (desktop at 0.5x, mobile at 1x, notes at 0.75x)
Checks: elements poking outside their frame horizontally, clipped single-line text, frame sizes."""
import sys, os, asyncio, json
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))

CHECK = r"""
() => {
  const out = [];
  document.querySelectorAll('.frame').forEach((f, fi) => {
    const fr = f.getBoundingClientRect();
    const kind = f.classList.contains('desktop') ? 'desktop' : f.classList.contains('mobile') ? 'mobile' : 'notes';
    const res = {i: fi, kind, w: Math.round(fr.width), h: Math.round(fr.height), name: f.dataset.name || '', overflow: [], clipped: []};
    f.querySelectorAll('*').forEach(el => {
      if (el.closest('[data-bleed]')) return;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return;
      if (r.right > fr.right + 1 || r.left < fr.left - 1) {
        const t = (el.innerText || el.getAttribute('class') || el.tagName).trim().slice(0, 60);
        res.overflow.push(`${el.tagName}.${(el.className && el.className.baseVal === undefined ? el.className : '').toString().slice(0,30)} [${Math.round(r.left-fr.left)}→${Math.round(r.right-fr.left)}] ${t}`);
      }
      if (el.children.length === 0 && el.innerText && el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflow !== 'visible') {
        res.clipped.push(el.innerText.trim().slice(0, 60));
      }
    });
    res.overflow = [...new Set(res.overflow)].slice(0, 12);
    res.clipped = [...new Set(res.clipped)].slice(0, 12);
    out.push(res);
  });
  return out;
}
"""

async def main():
    args = sys.argv[1:]
    path = os.path.abspath(args[0])
    only = None; slice_h = None
    if "--only" in args: only = args[args.index("--only") + 1]
    if "--slice" in args: slice_h = int(args[args.index("--slice") + 1])
    name = os.path.splitext(os.path.basename(path))[0]
    outdir = os.path.join(HERE, "shots"); os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        if f.startswith(name + "-"): os.remove(os.path.join(outdir, f))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        results = None
        for kind, dsf, default_slice in [("desktop", 0.5, 1800), ("mobile", 1.0, 1000), ("notes", 0.75, 1400)]:
            if only and kind != only: continue
            ctx = await b.new_context(viewport={"width": 1600, "height": 1200}, device_scale_factor=dsf)
            page = await ctx.new_page()
            await page.goto("file://" + path)
            await page.evaluate("document.fonts.ready")
            await page.wait_for_timeout(300)
            if results is None:
                results = await page.evaluate(CHECK)
            boxes = await page.evaluate("""(k) => [...document.querySelectorAll('.frame.' + k)].map(f => {
                const r = f.getBoundingClientRect(); return {x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height}; })""", kind)
            sh = slice_h or default_slice
            for fi, bx in enumerate(boxes):
                n = 0; y = 0
                while y < bx["h"]:
                    hh = min(sh, bx["h"] - y)
                    await page.screenshot(path=os.path.join(outdir, f"{name}-{kind}{fi}-{n:02d}.png"),
                                          clip={"x": bx["x"], "y": bx["y"] + y, "width": bx["w"], "height": hh}, full_page=True)
                    y += sh; n += 1
            await ctx.close()
        await b.close()
    for r in results or []:
        print(f"[{r['kind']} #{r['i']}] {r['w']}x{r['h']}")
        for o in r["overflow"]: print("   OVERFLOW", o)
        for c in r["clipped"]: print("   CLIPPED ", c)
    shots = sorted(f for f in os.listdir(outdir) if f.startswith(name + "-"))
    print(len(shots), "slices:", " ".join(shots))

asyncio.run(main())
