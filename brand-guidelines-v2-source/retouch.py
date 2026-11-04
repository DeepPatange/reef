#!/usr/bin/env python3
"""Remove third-party brand text from the product photos (inpainting in a headless browser canvas).
Writes full-resolution clean PNGs to img-clean/ and 1500px JPEGs to img/ for the guide."""
import asyncio, base64, os, subprocess
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/Users/deeppatange/Desktop/Reef/Product images "
OUT = os.path.join(HERE, "img-clean"); os.makedirs(OUT, exist_ok=True)

# rect = [x0, y0, x1, y1] in full-res pixels; mode: light | dark | abs; thr = luminance deviation from local background
JOBS = {
    "mosaic-wall": ("Warm Mosaic Wall with Robe, Tote, and Loofah.png", [
        {"rect": [486, 722, 610, 774], "mode": "dark", "thr": 22, "r": 9, "dil": 2},
    ]),
    "still-life": ("Warm Bathroom Body Care Still Life.png", [
        {"rect": [384, 596, 432, 1100], "mode": "light", "thr": 24, "r": 7, "dil": 2},
        {"rect": [720, 356, 770, 448], "mode": "poly", "poly": [[730, 372.5], [749.5, 369], [761, 435.5], [741.25, 439]],
         "lumMax": 100, "green": -20, "thr": 0, "r": 1, "dil": 2},
    ]),
    "green-vanity": ("Moody Green Tile Spa Vanity.png", [
        {"rect": [662, 976, 727, 1160], "mode": "abs", "thr": 9, "r": 6, "dil": 2},
    ]),
    "sink-mitt": ("Warm Spa Sink with Hanging Scrub Mitt.png", []),
    "olive-niche": ("Wet Olive-Tile Shower Niche.png", []),
}

JS = r"""
async ([src, jobs]) => {
  const img = new Image(); img.src = src; await img.decode();
  const W = img.width, H = img.height;
  const cv = document.createElement('canvas'); cv.width = W; cv.height = H;
  const g = cv.getContext('2d'); g.drawImage(img, 0, 0);
  const id = g.getImageData(0, 0, W, H), d = id.data;
  const lum = (i) => 0.299*d[i] + 0.587*d[i+1] + 0.114*d[i+2];
  let masked = 0;
  for (const j of jobs) {
    const [x0, y0, x1, y1] = j.rect, r = j.r;
    const w = x1 - x0, h = y1 - y0;
    // local background = box blur of luminance over a padded window
    const bg = new Float32Array(w*h);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      let s = 0, n = 0;
      for (let dy = -r; dy <= r; dy += 2) for (let dx = -r; dx <= r; dx += 2) {
        const xx = Math.min(W-1, Math.max(0, x0+x+dx)), yy = Math.min(H-1, Math.max(0, y0+y+dy));
        s += lum((yy*W+xx)*4); n++;
      }
      bg[y*w+x] = s/n;
    }
    let m = new Uint8Array(w*h);
    const inside = new Uint8Array(w*h).fill(1);
    if (j.poly) {
      const P = j.poly;
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        const px = x0+x+0.5, py = y0+y+0.5; let c = false;
        for (let a = 0, b = P.length-1; a < P.length; b = a++)
          if (((P[a][1] > py) !== (P[b][1] > py)) && (px < (P[b][0]-P[a][0])*(py-P[a][1])/(P[b][1]-P[a][1]) + P[a][0])) c = !c;
        inside[y*w+x] = c ? 1 : 0;
      }
    }
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      if (j.poly) { const p = ((y0+y)*W + x0+x)*4;
        if (inside[y*w+x] && (lum(p) < j.lumMax || d[p+1] - d[p] > j.green)) m[y*w+x] = 1; continue; }
      const dv = lum(((y0+y)*W + x0+x)*4) - bg[y*w+x];
      if ((j.mode === 'light' && dv > j.thr) || (j.mode === 'dark' && dv < -j.thr) || (j.mode === 'abs' && Math.abs(dv) > j.thr)) m[y*w+x] = 1;
    }
    for (let k = 0; k < j.dil; k++) {           // dilate
      const m2 = m.slice();
      for (let y = 1; y < h-1; y++) for (let x = 1; x < w-1; x++) if (!m[y*w+x] && inside[y*w+x])
        if (m[y*w+x-1] || m[y*w+x+1] || m[(y-1)*w+x] || m[(y+1)*w+x]) m2[y*w+x] = 1;
      m = m2;
    }
    // keep a clean 1px border so the fill grows from real pixels
    for (let x = 0; x < w; x++) { m[x] = 0; m[(h-1)*w+x] = 0; }
    for (let y = 0; y < h; y++) { m[y*w] = 0; m[y*w+w-1] = 0; }
    for (let i = 0; i < m.length; i++) masked += m[i];
    // onion-peel inpaint: fill masked pixels from known neighbours, outside in
    const known = new Uint8Array(w*h); for (let i = 0; i < w*h; i++) known[i] = m[i] ? 0 : (inside[i] ? 1 : 2);
    let left = 1, guard = 0;
    while (left && guard++ < 400) {
      left = 0; const fill = [];
      for (let y = 1; y < h-1; y++) for (let x = 1; x < w-1; x++) {
        if (known[y*w+x]) continue;
        let r_ = 0, g_ = 0, b_ = 0, n = 0;
        for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) {
          const yy = y+dy, xx = x+dx; if (yy < 0 || yy >= h || xx < 0 || xx >= w || known[yy*w+xx] !== 1) continue;
          const wt = 1 / (Math.abs(dx) + Math.abs(dy));
          const p = ((y0+yy)*W + x0+xx)*4; r_ += d[p]*wt; g_ += d[p+1]*wt; b_ += d[p+2]*wt; n += wt;
        }
        if (n > 1.2) fill.push([x, y, r_/n, g_/n, b_/n]); else left++;
      }
      for (const [x, y, r1, g1, b1] of fill) { const p = ((y0+y)*W + x0+x)*4; d[p] = r1; d[p+1] = g1; d[p+2] = b1; known[y*w+x] = 1; }
      if (!fill.length) break;
    }
    // light grain over filled pixels so they match the photo
    let seed = 7;
    const rnd = () => { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff - 0.5; };
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (m[y*w+x]) {
      const p = ((y0+y)*W + x0+x)*4, n = rnd() * 7; d[p] += n; d[p+1] += n; d[p+2] += n;
    }
  }
  g.putImageData(id, 0, 0);
  return {png: cv.toDataURL('image/png'), masked, W, H};
}
"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.goto("about:blank")
        for key, (fname, jobs) in JOBS.items():
            src = "data:image/png;base64," + base64.b64encode(open(os.path.join(SRC, fname), "rb").read()).decode()
            r = await pg.evaluate(JS, [src, jobs])
            png = os.path.join(OUT, key + ".png")
            open(png, "wb").write(base64.b64decode(r["png"].split(",", 1)[1]))
            subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "84", "-Z", "1500", png,
                            "--out", os.path.join(HERE, "img", key + ".jpg")], capture_output=True, check=True)
            print(key, r["W"], r["H"], "masked px:", r["masked"])
        await b.close()
asyncio.run(main())
