"""Turn the guide's variable fonts into one static font per weight actually used.
Chromium prints variable fonts as Type 3 fonts, which many PDF viewers load slowly or not at all;
static TrueType fonts embed normally."""
import re, base64, io, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
SRC, OUT = sys.argv[1], sys.argv[2]
NEED = {("Inter", "normal"): [300, 400, 500, 600], ("Inter", "italic"): [300, 700],
        ("Literata", "normal"): [300, 400, 650], ("Literata", "italic"): [300, 730],
        ("Noto Serif", "normal"): [300, 400]}
WN = {300: "Light", 400: "Regular", 500: "Medium", 600: "SemiBold", 650: "SemiBold650", 700: "Bold", 730: "Bold730"}
css = open(SRC).read(); out = []
for m in re.finditer(r"@font-face \{[^}]*?font-family: '([^']+)'; font-style: (\w+); font-weight: ([\d ]+);[^}]*?src: url\(data:font/woff2;base64,([^)]+)\)[^}]*\}", css, re.S):
    fam, style, raw = m.group(1), m.group(2), base64.b64decode(m.group(4))
    for w in NEED.get((fam, style), []):
        f = TTFont(io.BytesIO(raw))
        st = instantiateVariableFont(f, {"wght": w})
        sub = WN[w] + ("Italic" if style == "italic" else "")
        ps = fam.replace(" ", "") + "-" + sub
        nm = st["name"]
        for rec in list(nm.names):
            if rec.nameID in (1, 2, 3, 4, 6, 16, 17, 25): nm.removeNames(nameID=rec.nameID)
        for nid, val in ((1, f"{fam} {sub}"), (2, "Regular"), (3, ps), (4, f"{fam} {sub}"), (6, ps), (16, fam), (17, sub)):
            nm.setName(val, nid, 3, 1, 0x409); nm.setName(val, nid, 1, 0, 0)
        st["OS/2"].usWeightClass = w
        if "STAT" in st: del st["STAT"]
        buf = io.BytesIO(); st.flavor = "woff2"; st.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        out.append(f"@font-face {{ font-family: '{fam}'; font-style: {style}; font-weight: {w}; font-display: block; src: url(data:font/woff2;base64,{b64}) format('woff2'); }}")
        print(f"{ps:28} {len(buf.getvalue())//1024:4} KB")
# keep every non-variable face (Quattrocento) exactly as it was
for m in re.finditer(r"@font-face \{[^}]*\}", css, re.S):
    if not any(f"font-family: '{fam}'" in m.group(0) for fam, _ in NEED): out.append(m.group(0))
open(OUT, "w").write("\n".join(out) + "\n"); print("faces", len(out))
