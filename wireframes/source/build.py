#!/usr/bin/env python3
"""Build wireframe pages: expand {{macro|args}} shorthands, inline system.css + fonts.
Usage: python3 build.py pages/01-home.html [more...]   -> writes dist/<name>.html
Macros (args separated by |, empty args allowed):
  {{icon|name|size|color}}            brand icons (sun water laurel compost renew origin tag box fibre) + UI icons
  {{win|W|H|label|variant}}           3:4 'Window' oval placeholder. variant: '' | dark | ring | silt
  {{ph|W|H|label|variant|radius}}     image placeholder. W may be px number or e.g. 100%. variant: '' | dark | kraft | steam
  {{circ|D|label|variant}}            circular placeholder
  {{logo|size|color}}                 primary wordmark  (color: basalt | ecru)
  {{mono|size|color}}                 Three Chambers glyph
  {{rl|width|color}}                  R&L monogram in an oval
  {{mk|label|top|left}}               annotation marker (absolute). No top/left -> inline marker
  {{flag|text}}                       yellow 'check' flag (annotation)
  {{pattern|W|H|opacity|color|pitch}} Three Chambers pattern band
  {{tag|W|day|fade|variant}}          fading cotton tag illustration (fade 0..1). variant: '' | kids
  {{stars|n|size}}                    star row
  {{announce|text}} {{mann|text}}     announcement bar desktop / mobile
  {{header|active|bag}}  {{mheader|bag|variant}}   active: rituals build little gifts farm account none
  {{footer}} {{mfooter}}  {{pay|theme}}
"""
import re, sys, os, math, html

HERE = os.path.dirname(os.path.abspath(__file__))
C = {"silt":"#B5583B","ecru":"#F3EEE4","basalt":"#2B2A27","kraft":"#C4A57B","brass":"#B08D57","clay":"#7E3A26",
     "dune":"#E6DAC6","steam":"#FAF7F1","smoke":"#6F6A62","char":"#3A3833","white":"#FFFFFF"}
def col(c, default="basalt"):
    c = (c or default).strip()
    return C.get(c, c)

# ---------------- icons ----------------
def _sun():
    rays = []
    for i in range(8):
        a = math.radians(i*45)
        x1, y1 = 32+16*math.cos(a), 32+16*math.sin(a)
        x2, y2 = 32+23*math.cos(a), 32+23*math.sin(a)
        rays.append('<path d="M%.1f %.1fL%.1f %.1f"/>' % (x1,y1,x2,y2))
    return '<circle cx="32" cy="32" r="10"/>' + "".join(rays)
CHAMBERS = ('<path d="M32 6C40 6 46 12 50 20C54 28 60 38 57 46C54 54 44 57 32 57C20 57 10 54 7 46C4 38 10 28 14 20C18 12 24 6 32 6Z"/>'
            '<path d="M32 33.5V56.5M32 33.5L12.5 24M32 33.5L51.5 24"/>'
            '<circle cx="32" cy="21.5" r="7.5"/><circle cx="21.5" cy="40.5" r="7.5"/><circle cx="42.5" cy="40.5" r="7.5"/>'
            '<circle cx="32" cy="21.5" r="2"/><circle cx="21.5" cy="40.5" r="2"/><circle cx="42.5" cy="40.5" r="2"/>')
BRAND = {
 "sun": _sun(),
 "water": '<path d="M32 9C32 9 17 28 17 39a15 15 0 0 0 30 0C47 28 32 9 32 9Z"/><path d="M25 41a7 7 0 0 0 6 6"/>',
 "laurel": ('<path d="M18 54C26 42 34 30 46 12"/><path d="M24 46Q15 47 12 39Q21 37 24 46Z"/><path d="M27 42Q36 39 39 47Q30 50 27 42Z"/>'
            '<path d="M31 35Q22 36 19 28Q28 26 31 35Z"/><path d="M34 31Q43 27 47 34Q38 38 34 31Z"/><path d="M39 24Q30 23 29 15Q37 15 39 24Z"/>'
            '<path d="M43 17Q48 11 53 12Q50 18 43 17Z"/>'),
 "compost": '<path d="M12 52H52"/><path d="M32 52V30"/><path d="M32 38C24 38 18 32 18 24C26 24 32 30 32 38Z"/><path d="M32 31C32 23 38 17 46 17C46 25 40 31 32 31Z"/>',
 "renew": '<rect x="12" y="14" width="40" height="38" rx="4"/><path d="M12 24H52"/><path d="M22 9V18M42 9V18"/><path d="M39 38a7 7 0 1 1-2.2-5.1"/><path d="M37.6 28.4V33.2H32.8"/>',
 "origin": '<path d="M32 56S14 38 14 26a18 18 0 0 1 36 0c0 12-18 30-18 30Z"/><circle cx="32" cy="26" r="6"/>',
 "tag": '<path d="M24 8h16a4 4 0 0 1 4 4v40a4 4 0 0 1-4 4H24a4 4 0 0 1-4-4V12a4 4 0 0 1 4-4Z"/><circle cx="32" cy="16" r="2.6"/><path d="M26 30H38"/><path d="M26 37H38" opacity=".55"/><path d="M26 44H38" opacity=".25"/>',
 "box": '<rect x="13" y="9" width="38" height="47" rx="3"/><ellipse cx="32" cy="29" rx="9" ry="12"/><path d="M13 47H51"/>',
 "fibre": CHAMBERS,
 "hand": '<path d="M22 56V34l-6-8a3.5 3.5 0 0 1 5.5-4.3L26 27V12a3.5 3.5 0 0 1 7 0v14V9a3.5 3.5 0 0 1 7 0v17V13a3.5 3.5 0 0 1 7 0v20c0 13-6 23-15 23"/>',
 "steam": '<path d="M22 54c-6-6 6-10 0-16s6-10 0-16"/><path d="M32 54c-6-6 6-10 0-16s6-10 0-16"/><path d="M42 54c-6-6 6-10 0-16s6-10 0-16"/>',
 "camel": ('<path d="M10 50V40c0-6 3-10 8-12 4-8 8-12 12-8 3-4 7-4 10 0 3 3 3 8 7 9l5-6 4 2-3 7c-1 4-4 6-8 6v12"/><path d="M18 50V42M44 50V42"/><circle cx="53" cy="27" r=".8"/>'),
}
UI = {
 "bag": '<path d="M5.5 8.5h13l-1 11.5h-11z"/><path d="M9 8.5V7a3 3 0 0 1 6 0v1.5"/>',
 "user": '<circle cx="12" cy="8.5" r="3.8"/><path d="M4.5 20c.6-3.6 3.7-5.5 7.5-5.5s6.9 1.9 7.5 5.5"/>',
 "search": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4 4"/>',
 "menu": '<path d="M4 8h16M4 16h16"/>',
 "close": '<path d="M6 6l12 12M18 6L6 18"/>',
 "chev-down": '<path d="M6 9l6 6 6-6"/>', "chev-up": '<path d="M6 15l6-6 6 6"/>',
 "chev-right": '<path d="M9 6l6 6-6 6"/>', "chev-left": '<path d="M15 6l-6 6 6 6"/>',
 "arrow-right": '<path d="M4 12h16M14 6l6 6-6 6"/>', "arrow-left": '<path d="M20 12H4M10 6l-6 6 6 6"/>',
 "arrow-up-right": '<path d="M7 17L17 7M9 7h8v8"/>',
 "plus": '<path d="M12 5v14M5 12h14"/>', "minus": '<path d="M5 12h14"/>',
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "play": '<path d="M8 5.5v13l10.5-6.5z" fill="currentColor"/>',
 "whatsapp": '<path d="M12 3.5a8.5 8.5 0 0 0-7.3 12.8L3.5 20.5l4.3-1.1A8.5 8.5 0 1 0 12 3.5z"/><path d="M9 8.6c.3 2.8 2.6 5.3 5.6 6.1l1.2-1.4-1.9-1-.9.8a5 5 0 0 1-2.5-2.5l.8-.9-1-1.9z"/>',
 "info": '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5"/><path d="M12 7.6v.4"/>',
 "insta": '<rect x="4" y="4" width="16" height="16" rx="4.5"/><circle cx="12" cy="12" r="3.8"/><path d="M16.6 7.4v.1"/>',
 "star": '<path d="M12 3.8l2.5 5.2 5.7.7-4.2 3.9 1.1 5.6L12 16.4l-5.1 2.8 1.1-5.6L3.8 9.7l5.7-.7z" fill="currentColor" stroke="none"/>',
 "truck": '<path d="M3 7h11v9H3z"/><path d="M14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
 "gift": '<rect x="4" y="9" width="16" height="11" rx="1"/><path d="M3 9h18v3H3z"/><path d="M12 9v11"/><path d="M12 9c-2-4-6-4-6-1.5S10 9 12 9zm0 0c2-4 6-4 6-1.5S14 9 12 9z"/>',
 "skip": '<path d="M6 6.5v11l8-5.5z"/><path d="M17.5 6.5v11"/>',
 "pause": '<path d="M8.5 6v12M15.5 6v12"/>',
 "swap": '<path d="M5 8.5h13M15 5l3.5 3.5L15 12"/><path d="M19 15.5H6M9 12l-3.5 3.5L9 19"/>',
 "calendar": '<rect x="4" y="5.5" width="16" height="14.5" rx="2"/><path d="M4 10h16M8.5 3.5v4M15.5 3.5v4"/>',
 "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>',
 "leaf": '<path d="M5 19C5 10 11 5 19 5c0 8-5 14-14 14z"/><path d="M5 19l8-8"/>',
 "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.6 3.5 5.4 3.5 8.5s-1 5.9-3.5 8.5c-2.5-2.6-3.5-5.4-3.5-8.5s1-5.9 3.5-8.5z"/>',
 "qr": '<rect x="4" y="4" width="6" height="6"/><rect x="14" y="4" width="6" height="6"/><rect x="4" y="14" width="6" height="6"/><path d="M14 14h2v2h-2zM18 18h2v2h-2zM14 18h2M18 14h2"/>',
 "filter": '<path d="M4 7h16M7 12h10M10 17h4"/>',
 "edit": '<path d="M5 19l1-4 10-10 3 3-10 10z"/>',
 "refresh": '<path d="M19 12a7 7 0 1 1-2.1-5"/><path d="M17.5 3.5V7.5H13.5"/>',
 "pin": '<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
 "drop": '<path d="M12 3.5S6 10.5 6 14.5a6 6 0 0 0 12 0C18 10.5 12 3.5 12 3.5z"/>',
 "sound": '<path d="M5 10h3l4-3.5v11L8 14H5z"/><path d="M15.5 9.5a3.5 3.5 0 0 1 0 5"/>',
 "grab": '<path d="M8 13V7.5a1.5 1.5 0 0 1 3 0V12V6a1.5 1.5 0 0 1 3 0v6V7a1.5 1.5 0 0 1 3 0v7c0 4-2.5 6.5-6 6.5-2.6 0-4.2-1.4-5.4-3.4L4 13.6a1.4 1.4 0 0 1 2.3-1.6z"/>',
 "dots": '<path d="M6 12h.01M12 12h.01M18 12h.01"/>',
 "upload": '<path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v4h16v-4"/>',
 "download": '<path d="M12 4v12M7 11l5 5 5-5"/><path d="M4 16v4h16v-4"/>',
 "mail": '<rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="M4 7l8 6 8-6"/>',
 "phone": '<rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 18h2"/>',
}
def icon(name, size="24", color="", sw=""):
    size = float(size or 24)
    c = col(color, "currentColor") if color else "currentColor"
    if name in BRAND:
        vb = 64.0
        stroke = max(2.6, 1.35*vb/size)
        body = BRAND[name]
    elif name in UI:
        vb = 24.0
        stroke = 1.5 if size <= 28 else max(1.2, 1.5*24/size*1.2)
        body = UI[name]
    else:
        raise SystemExit("unknown icon: %s" % name)
    if sw: stroke = float(sw)
    return ('<svg width="%g" height="%g" viewBox="0 0 %g %g" fill="none" stroke="%s" stroke-width="%.2f" '
            'stroke-linecap="round" stroke-linejoin="round" style="flex:none">%s</svg>') % (size,size,vb,vb,c,stroke,body)

def mono(size="40", color="basalt"):
    size = float(size or 40)
    stroke = max(2.2, 1.3*64/size)
    return ('<svg width="%g" height="%g" viewBox="0 0 64 64" fill="none" stroke="%s" stroke-width="%.2f" stroke-linecap="round" '
            'stroke-linejoin="round" style="flex:none">%s</svg>') % (size,size,col(color),stroke,CHAMBERS)

def dim(v):
    v = (v or "").strip()
    if v.endswith("%") or v in ("fill","auto"):
        return "100%" if v=="fill" else v
    return "%spx" % v

def esc(t): return html.escape(t or "", quote=False)

def ph(w, h, label="", variant="", radius=""):
    v = (variant or "").strip()
    cls = "ph" + ("" if not v else " "+v)
    style = "width:%s;height:%s;" % (dim(w), dim(h))
    if radius: style += "border-radius:%spx;" % radius.strip()
    try: gs = min(float(w), float(h))*0.14
    except ValueError: gs = float(h)*0.14 if h and not h.endswith('%') else 40
    gs = max(18, min(gs, 64))
    gcol = "kraft" if v in ("", "steam", "dark") else "basalt"
    lbl = '<span class="lbl">%s</span>' % esc(label) if label and (not h or h.endswith('%') or float(h) >= 90) else ""
    return '<div class="%s" style="%s"><span class="glyph">%s</span>%s</div>' % (cls, style, mono(gs, gcol), lbl)

def win(w, h, label="", variant=""):
    W, H = float(w), float(h)
    v = (variant or "").strip()
    fill = {"dark": C["char"], "silt": C["silt"], "steam": C["steam"]}.get(v, C["dune"])
    ring = ""
    if v == "ring":
        ring = '<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="none" stroke="%s" stroke-width="1"/>' % (W/2, H/2, W/2-1, H/2-1, C["basalt"])
        inner = '<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="%s"/>' % (W/2, H/2, W/2-14, H/2-14*H/W, fill)
    else:
        inner = '<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="%s"/>' % (W/2, H/2, W/2, H/2, fill)
    gs = max(20, min(W*0.13, 72))
    gcol = "kraft"
    lbl = '<span class="lbl">%s</span>' % esc(label) if label and W >= 150 else ""
    cls = "win" + (" dark" if v == "dark" else "")
    return ('<div class="%s" style="width:%gpx;height:%gpx"><svg class="shape" width="%g" height="%g" viewBox="0 0 %g %g">%s%s</svg>'
            '<span class="glyph">%s</span>%s</div>') % (cls, W, H, W, H, W, H, ring, inner, mono(gs, gcol), lbl)

def circ(d, label="", variant=""):
    D = float(d)
    v = (variant or "").strip()
    cls = "ph circ" + ("" if not v else " "+v)
    gs = max(14, min(D*0.3, 56))
    lbl = '<span class="lbl" style="text-align:center;bottom:18%%">%s</span>' % esc(label) if label and D >= 150 else ""
    return '<div class="%s" style="width:%gpx;height:%gpx"><span class="glyph">%s</span>%s</div>' % (cls, D, D, mono(gs, "kraft"), lbl)

def logo(size="22", color="basalt"):
    return '<span class="logo" style="font-size:%spx;color:%s">AL REEF <i>&amp;</i> LAUREL</span>' % (size or 22, col(color))

def rl(width="44", color="basalt"):
    W = float(width or 44); H = W*4/3
    c = col(color)
    fs = W*0.34
    return ('<div style="position:relative;width:%gpx;height:%gpx;flex:none;display:flex;align-items:center;justify-content:center">'
            '<svg width="%g" height="%g" viewBox="0 0 %g %g" style="position:absolute;left:0;top:0"><ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="none" stroke="%s" stroke-width="1"/></svg>'
            '<span style="position:relative;font-family:var(--serif);font-weight:500;font-size:%gpx;line-height:1;color:%s;letter-spacing:.02em">R<i style="color:var(--silt)">&amp;</i>L</span></div>') % (
            W, H, W, H, W, H, W/2, H/2, W/2-.5, H/2-.5, c, fs, c)

def mk(label, top="", left=""):
    if top == "" and left == "":
        return '<span class="mk mk-inline">%s</span>' % esc(label)
    return '<span class="mk" style="top:%spx;left:%spx">%s</span>' % (top, left, esc(label))

def flag(text):
    return '<span class="flag">&#9873; %s</span>' % esc(text)

def pattern(w, h, opacity=".08", color="basalt", pitch="80"):
    W, H, P = float(w), float(h), float(pitch or 80)
    op = float(opacity or .08)
    g = []
    seed = 7
    rows = int(H // P) + 2; cols = int(W // P) + 2
    for r in range(rows):
        for c in range(cols):
            seed = (seed * 1103515245 + 12345) & 0x7fffffff
            rot = seed % 360
            x = c*P + (P/2 if r % 2 else 0) - P/4
            y = r*P - P/4
            g.append('<g transform="translate(%g %g) rotate(%d 16 16) scale(.5)">%s</g>' % (x, y, rot, CHAMBERS))
    return ('<svg width="%g" height="%g" viewBox="0 0 %g %g" fill="none" stroke="%s" stroke-width="2.6" stroke-opacity="%g" '
            'stroke-linecap="round" stroke-linejoin="round" style="display:block" data-bleed="1">%s</svg>') % (W, H, W, H, col(color), op, "".join(g))

def tag(w="160", day="41", fade="0.6", variant=""):
    W = float(w or 160); H = W*200/120
    f = max(0.0, min(1.0, float(fade or 0)))
    ops = [max(0.1, min(1.0, 1 - (f*3 - i))) for i in range(3)]
    kids = (variant or "").strip() == "kids"
    mid = ('<g transform="translate(36 56) scale(.75)" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" opacity="%.2f">%s</g>'
           % (C["basalt"], max(0.15, 1 - f), BRAND["camel"])) if kids else (
           '<ellipse cx="60" cy="80" rx="20" ry="26" fill="none" stroke="%s" stroke-width="1"/>'
           '<text x="60" y="86" text-anchor="middle" font-family="Cormorant Garamond" font-weight="500" font-size="17" fill="%s">R<tspan fill="%s" font-style="italic">&amp;</tspan>L</text>'
           % (C["basalt"], C["basalt"], C["silt"]))
    return ('<svg width="%g" height="%g" viewBox="0 0 120 200" style="flex:none;display:block">'
            '<path d="M60 2C46 2 44 18 60 34" fill="none" stroke="%s" stroke-width="1.6"/>'
            '<rect x="10" y="22" width="100" height="174" rx="12" fill="%s" stroke="%s" stroke-width="1"/>'
            '<circle cx="60" cy="36" r="5" fill="%s" stroke="%s" stroke-width="1"/>%s'
            '<rect x="30" y="128" width="60" height="4.5" rx="2" fill="%s" opacity="%.2f"/>'
            '<rect x="30" y="140" width="60" height="4.5" rx="2" fill="%s" opacity="%.2f"/>'
            '<rect x="30" y="152" width="60" height="4.5" rx="2" fill="%s" opacity="%.2f"/>'
            '<text x="60" y="178" text-anchor="middle" font-family="IBM Plex Sans" font-weight="500" font-size="8.5" letter-spacing="1.2" fill="%s">DAY %s / 60</text>'
            '</svg>') % (W, H, C["kraft"], C["steam"], "rgba(43,42,39,.3)", C["ecru"], "rgba(43,42,39,.3)", mid,
                         C["silt"], ops[0], C["silt"], ops[1], C["silt"], ops[2], C["basalt"], esc(day or "01"))

def stars(n="5", size="16"):
    return '<span class="flex g4" style="color:var(--basalt)">%s</span>' % "".join(icon("star", size) for _ in range(int(n or 5)))

def pay(theme=""):
    items = ["VISA", "Mastercard", "Apple Pay", "Google Pay", "tabby"]
    if (theme or "").strip() == "light":
        return '<div class="flex g8">%s</div>' % "".join('<span class="pay" style="border-color:var(--line2);color:var(--smoke)">%s</span>' % i for i in items)
    return '<div class="flex g8">%s</div>' % "".join('<span class="pay">%s</span>' % i for i in items)

# ---------------- chrome ----------------
def announce(text=""):
    t = text or "Founding members · 25% off your first Duo · Free UAE delivery"
    return ('<div class="announce t-spec"><span>%s</span><span class="flex g8 ac" style="position:absolute;right:40px;opacity:.6">%s<span class="t-spec-s">1 / 3</span>%s</span></div>'
            % (esc(t), icon("chev-left","16"), icon("chev-right","16")))

def mann(text=""):
    t = text or "Founding members · 25% off your first Duo"
    return '<div class="mann t-spec-s">%s</div>' % esc(t)

def header(active="", bag="0"):
    a = (active or "").strip()
    def L(key, label):
        return '<a class="%s">%s</a>' % ("on" if a == key else "", label)
    left = L("rituals","Rituals") + L("build","Build yours") + L("little","Little Reef") + L("gifts","Gifts")
    right = L("farm","Our farm") + '<span class="flex ac">%s</span>' % icon("search","20") + L("account","Account") + '<a>Bag (%s)</a>' % (bag or "0")
    return '<header class="hdr"><nav>%s</nav>%s<nav class="r">%s</nav></header>' % (left, logo("22"), right)

def mheader(bag="0", variant=""):
    v = (variant or "").strip()
    left = '<span class="flex ac g8 t-spec-s">%sMenu</span>' % icon("menu","20")
    if v == "back":
        left = '<span class="flex ac g8 t-spec-s">%sBack</span>' % icon("chev-left","20")
    return '<header class="mhdr">%s%s<span class="t-ui">Bag (%s)</span></header>' % (left, logo("15"), bag or "0")

def lockup(size="80"):
    return ('<div class="col ac g16">'
            '<div class="t-spec-s c-kraft">Luffa aegyptiaca · Grade A</div>'
            '<div class="flex ac jc g32"><span class="t-spec-s c-kraft">Harvest</span>%s<span class="t-spec-s c-kraft">2026</span></div>'
            '<div class="t-spec-s c-kraft">Damanhour · Nile Delta · 31.03° N 30.47° E</div></div>') % logo(size, "ecru")

def footer():
    cols = [("Shop", ["Rituals","The Duo","Build yours","Little Reef","Gifts","Corporate gifting"]),
            ("Learn", ["Our farm","The ritual","How renewal works","Field notes","Look up a batch"]),
            ("Help", ["Shipping &amp; returns","Manage your renewal","FAQ","Contact us","WhatsApp the founders"])]
    colhtml = "".join('<div class="ftr-col"><h5>%s</h5><div class="lk">%s</div></div>' % (h, "".join("<a>%s</a>" % x for x in items)) for h, items in cols)
    insta = "".join(ph("217","217","","dark") for _ in range(6))
    return ('<footer class="ftr">'
            '<div style="overflow:hidden;height:88px;border-bottom:1px solid var(--lined)">%s</div>'
            '<div class="flex jb" style="padding:96px 40px 72px">'
              '<div class="col g24" style="width:560px">'
                '<div class="rail"><span class="rule-k"></span><span class="t-spec c-kraft">Letters from the Delta</span></div>'
                '<div class="t-heading c-ecru">Once a month. No puns.<br>Well, one.</div>'
                '<div class="field-d" style="width:520px"><span>Email address</span><span class="btn btn-ecru btn-s">Subscribe</span></div>'
                '<div class="t-cap c-ecru50">Field notes, harvest news and early access. Unsubscribe any time.</div>'
              '</div>'
              '<div class="flex g80" style="padding-top:6px">%s</div>'
            '</div>'
            '<div style="padding:0 40px 72px"><div class="flex jb ae" style="margin-bottom:20px"><span class="t-spec c-kraft">@alreefandlaurel</span><span class="flex ac g8 t-ui c-ecru70">%sFollow on Instagram</span></div>'
              '<div class="flex g12">%s</div></div>'
            '<div style="padding:24px 40px 80px;border-top:1px solid var(--lined)">%s</div>'
            '<div class="flex jb ac" style="padding:24px 40px;border-top:1px solid var(--lined)">'
              '<span class="t-cap c-ecru50">© 2026 Al Reef &amp; Laurel · Dubai, United Arab Emirates</span>'
              '<span class="flex ac g24"><span class="flex ac g8 t-cap c-ecru70">%sUAE · AED %s</span>%s</span>'
              '<span class="flex g24 t-cap c-ecru50"><span>Privacy</span><span>Terms</span><span>Cookies</span></span>'
            '</div></footer>') % (pattern("1440","88",".10","ecru"), colhtml, icon("insta","18"), insta, lockup("78"),
                                  icon("globe","16"), icon("chev-down","14"), pay())

def mfooter():
    acc = "".join('<div class="acc acc-d"><span class="t-spec c-ecru">%s</span>%s</div>' % (h, icon("plus","18","ecru")) for h in ["Shop","Learn","Help"])
    insta = "".join(ph("150","150","","dark") for _ in range(3))
    return ('<footer class="ftr">'
            '<div style="overflow:hidden;height:64px;border-bottom:1px solid var(--lined)">%s</div>'
            '<div class="col g20" style="padding:64px 20px 48px">'
              '<div class="rail"><span class="rule-k"></span><span class="t-spec-s c-kraft">Letters from the Delta</span></div>'
              '<div class="t-heading-m c-ecru">Once a month. No puns. Well, one.</div>'
              '<div class="field-d"><span>Email address</span><span class="btn btn-ecru btn-s">Subscribe</span></div>'
            '</div>'
            '<div style="padding:0 20px 40px">%s<div style="border-top:1px solid var(--lined)"></div></div>'
            '<div style="padding:0 0 40px 20px"><div class="t-spec-s c-kraft" style="margin-bottom:14px">@alreefandlaurel</div><div class="flex g8" data-bleed="1">%s</div></div>'
            '<div class="col ac g12" style="padding:32px 20px 40px;border-top:1px solid var(--lined)">'
              '<div class="t-spec-s c-kraft">Luffa aegyptiaca · Grade A</div>%s<div class="t-spec-s c-kraft tc">Damanhour · Nile Delta<br>31.03° N 30.47° E</div></div>'
            '<div class="col g16" style="padding:24px 20px 40px;border-top:1px solid var(--lined)">'
              '<span class="flex ac g8 t-cap c-ecru70">%sUAE · AED %s</span>%s'
              '<span class="t-cap c-ecru50">© 2026 Al Reef &amp; Laurel · Dubai · Privacy · Terms</span></div>'
            '</footer>') % (pattern("390","64",".10","ecru"), acc, insta, logo("21","ecru"), icon("globe","16"), icon("chev-down","14"), pay())

def img(path, w, h, radius="0"):
    import base64
    p = os.path.join(HERE, path)
    data = base64.b64encode(open(p, "rb").read()).decode()
    mime = "image/png" if p.endswith(".png") else "image/jpeg"
    return ('<img src="data:%s;base64,%s" style="width:%s;height:%s;object-fit:cover;object-position:top;border-radius:%spx;display:block;flex:none">'
            % (mime, data, dim(w), dim(h), radius or 0))

MACROS = {"img": img, "icon": icon, "win": win, "ph": ph, "circ": circ, "logo": logo, "mono": mono, "rl": rl, "mk": mk, "flag": flag,
          "pattern": pattern, "tag": tag, "stars": stars, "pay": pay, "announce": announce, "mann": mann,
          "header": header, "mheader": mheader, "footer": footer, "mfooter": mfooter, "lockup": lockup}

def expand(src):
    def rep(m):
        parts = m.group(1).split("|")
        name, args = parts[0].strip(), parts[1:]
        if name not in MACROS:
            raise SystemExit("unknown macro: " + name)
        return MACROS[name](*args)
    prev = None
    while prev != src:
        prev = src
        src = re.sub(r"\{\{([a-z][\w-]*(?:\|[^{}]*)?)\}\}", rep, src)
    return src

def build(path):
    src = open(path, encoding="utf-8").read()
    out = expand(src)
    css = open(os.path.join(HERE, "system.css"), encoding="utf-8").read()
    fonts = open(os.path.join(HERE, "fonts.css"), encoding="utf-8").read()
    out = out.replace('<link rel="stylesheet" href="../system.css">', "<style>\n%s\n%s\n</style>" % (fonts, css))
    left = re.findall(r"\{\{[^}]*\}\}", out)
    if left: print("WARNING unexpanded macros:", left[:5])
    name = os.path.splitext(os.path.basename(path))[0]
    dst = os.path.join(HERE, "dist", name + ".html")
    open(dst, "w", encoding="utf-8").write(out)
    print("built", dst, "%.0f KB" % (len(out.encode()) / 1024))
    return dst

if __name__ == "__main__":
    for p in sys.argv[1:]:
        build(p)
