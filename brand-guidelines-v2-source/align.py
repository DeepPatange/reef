import asyncio, base64, os, sys
from playwright.async_api import async_playwright
# (mine page, quint page, label, x0, y0, x1, y1): finds first/last rows that contain ink inside the box
CHECKS = [
 (4, 4, "header", 60, 60, 300, 105), (4, 4, "title Welcome", 60, 150, 400, 280), (4, 4, "body line1", 60, 300, 520, 345),
 (5, 5, "title Our", 60, 150, 300, 245), (6, 6, "title BrandMsg", 60, 150, 600, 280), (6, 6, "msg list", 60, 400, 600, 760),
 (7, 7, "tone heads", 60, 330, 330, 395), (9, 9, "title Primary", 60, 250, 360, 445), (9, 9, "body", 60, 570, 450, 680),
 (9, 9, "infobox", 515, 520, 985, 700), (10, 10, "title Monogram", 60, 250, 400, 360), (12, 12, "title Service", 60, 130, 300, 330),
 (13, 13, "title Anatomy", 60, 150, 400, 330), (14, 14, "title Usage", 60, 160, 360, 350), (17, 16, "title Website", 40, 160, 360, 350),
 (17, 16, "subtitle", 40, 350, 360, 420), (17, 16, "Aa+family", 600, 50, 1000, 290), (19, 18, "pair label", 400, 170, 800, 245),
 (21, 20, "title Primary C", 40, 160, 400, 350), (22, 21, "title Second", 40, 160, 400, 350), (23, 22, "title Colour U", 40, 130, 460, 330),
 (24, 23, "title P.Logo in", 40, 170, 460, 420), (29, 26, "title Mockups", 40, 160, 400, 260), (30, 27, "title Imagery", 40, 160, 400, 260),
 (3, 3, "pill", 300, 40, 820, 110), (3, 3, "divider word", 100, 200, 1020, 480), (3, 3, "divider para", 200, 630, 920, 690),
 (2, 2, "Index", 40, 60, 330, 160), (33, 30, "Thank You", 300, 690, 820, 780), (1, 1, "cover title", 400, 580, 1100, 700),
]
JS = """async ([src, x0, y0, x1, y1]) => { const i = new Image(); i.src = src; await i.decode();
  const c = document.createElement('canvas'); c.width = i.width; c.height = i.height; const g = c.getContext('2d'); g.drawImage(i, 0, 0);
  const d = g.getImageData(x0, y0, x1 - x0, y1 - y0).data, W = x1 - x0, H = y1 - y0;
  const bg = [d[0], d[1], d[2]]; let top = -1, bot = -1, left = 1e9, right = -1;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { const p = (y * W + x) * 4;
    if (Math.abs(d[p] - bg[0]) + Math.abs(d[p+1] - bg[1]) + Math.abs(d[p+2] - bg[2]) > 90) { if (top < 0) top = y; bot = y; left = Math.min(left, x); right = Math.max(right, x); } }
  return [top + y0, bot + y0, left + x0, right + x0]; }"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.goto("about:blank")
        def src(path): return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()
        for mp, qp, lab, x0, y0, x1, y1 in CHECKS:
            q = await pg.evaluate(JS, [src(f"q96/q-{qp:02d}.png"), x0, y0, x1, y1])
            m = await pg.evaluate(JS, [src(f"out/p{mp:02d}.png"), x0, y0, x1, y1])
            flag = "" if abs(q[0] - m[0]) <= 3 and abs(q[2] - m[2]) <= 3 else "   <-- off"
            print(f"p{mp:02d}/{qp:02d} {lab:16} quint top{q[0]:4} bot{q[1]:4} left{q[2]:5} | mine top{m[0]:4} bot{m[1]:4} left{m[2]:5} | dTop{m[0]-q[0]:+4} dLeft{m[2]-q[2]:+4}{flag}")
        await b.close()
asyncio.run(main())
