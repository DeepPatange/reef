#!/usr/bin/env python3
"""Al Reef & Laurel — Brand Guidelines V2, built on the Quint Home guideline grid.
All positions are in px on a 1123 × 794 page (A4 landscape at 96 dpi), measured from the Quint Home PDF.
Writes guide.html next to this script; render with render.py (--pdf <out>)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = open(os.path.join(HERE, "fonts.css")).read()

VEIL, MIST, VOID, CLAY, EARTH = "#EEE4D8", "#77918D", "#293329", "#C15A27", "#6A2E0C"
CREAM, WHITE = "#FBF5EC", "#FFFFFF"
INK = "#252825"      # headers, titles (Quint samples 37,40,37)
TXT = "#3E443D"      # body copy (Quint samples 62,68,61)
LOGO_INK = "#3E443D" # logo pages (Quint samples 62,68,61)
ON_DARK = "#FBF5EC"
DATE = "Updated November 2026"
GUIDE = "Al Reef &amp; Laurel Brand Style Guide"

# ---------------------------------------------------------------- marks
import sys
sys.path.insert(0, HERE)
import mark as _mark

def mono(size, color=VOID, sw=4.4, style=""):
    """The monogram: a hand-drawn loofah cross-section (skin, three chambers, Y-shaped fibre walls).
    sw values across this file were set for a single-stroke mark; the cross-section has more lines, so it runs 0.8× lighter."""
    return _mark.svg(size, color, round(sw * 0.8, 2), "hand", style)

def wordmark(size=64, color=VOID, sub_ratio=0.25, spans=False):
    a = "AL REEF"
    if spans:
        a = "".join(f'<span class="L{i}">{c}</span>' for i, c in enumerate(a))
    return (f'<div class="wm" style="color:{color}"><div class="wm-a" style="font-size:{size}px">{a}</div>'
            f'<div class="wm-b" style="font-size:{size*sub_ratio:.1f}px;margin-top:{size*0.17:.0f}px">&amp; LAUREL</div></div>')

# ---------------------------------------------------------------- page furniture
def head(section, mid_color=INK, right_color=INK, left_color=INK):
    return (f'<div class="hd" style="left:60px;color:{left_color}">{GUIDE}</div>'
            f'<div class="hd" style="left:519px;color:{mid_color}">{section}</div>'
            f'<div class="hd" style="right:60px;color:{right_color}">{DATE}</div>')

def title(text, top=190, size=66.3, lh=80, color=INK, left=60):
    # top = Quint bbox top; Noto Serif Light sits ~9px below the element top at lh 80
    return f'<div class="ttl" style="left:{left}px;top:{top+3}px;font-size:{size}px;line-height:{lh}px;color:{color}">{text}</div>'

def body(html, bottom=661, width=340, left=60, color=TXT, size=13.3, lh=17.75, top=None):
    pos = f"top:{top}px" if top is not None else f"bottom:{794-bottom-1}px"
    return (f'<div class="bd" style="left:{left}px;{pos};width:{width}px;color:{color};font-size:{size}px;line-height:{lh}px">{html}</div>')

def divider(num, name, text):
    return (f'<section class="pg grid" style="background-color:{CLAY}"><div class="pill">SECTION {num}</div>'
            f'<div class="dv-t">{name}</div><p class="dv-p">{text}</p></section>')

def infobox(left_html, label, text, top=536):
    return (f'<div class="ib" style="top:{top}px"><div class="ib-l">{left_html}</div>'
            f'<div class="ib-r"><div class="ib-h">{label}</div><div class="ib-p">{text}</div></div></div>')

# ---------------------------------------------------------------- images
IMG = {"sink-mitt.jpg": (1122, 1402), "olive-niche.jpg": (1086, 1448), "green-vanity.jpg": (1089, 1445),
       "mosaic-wall.jpg": (1086, 1449), "still-life.jpg": (1122, 1402)}
def im(src, w, h, fx=0.5, fy=0.5, zoom=1.0, extra=""):
    """Fill a w×h frame with the whole photo (cover fit, no distortion), centred on the product.
    fx/fy = product position as fractions of the photo; zoom > 1 only where a frame must leave something out."""
    iw, ih = IMG[src]
    s = max(w / iw, h / ih) * zoom
    dw, dh = iw * s, ih * s
    left = min(0.0, max(w - dw, w / 2 - fx * dw))
    top = min(0.0, max(h - dh, h / 2 - fy * dh))
    return (f'<div class="crop" style="width:{w}px;height:{h}px;{extra}"><img src="img/{src}" '
            f'style="width:{dw:.1f}px;height:{dh:.1f}px;left:{left:.1f}px;top:{top:.1f}px"></div>')

def at(x, y, html, extra=""):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;{extra}">{html}</div>'

pages = []

# 01 COVER ---------------------------------------------------------------
pages.append(f'''<section class="pg" style="background:#E8DDD1">
  {at(330, -300, mono(1060, "#DCD1C6", 3.4))}
  <div style="position:absolute;right:133px;top:606px;font:300 43.2px/70px 'Literata';color:#2E2A26;letter-spacing:-.05em;white-space:nowrap">Al Reef &amp; Laurel Brand Guidelines</div>
</section>''')

# 02 INDEX ---------------------------------------------------------------
def ix_sec(name, rows):
    r = "".join(f'<div class="ix-r"><span>{a}</span><span class="ix-d"></span><span>{n:02d}</span></div>' for a, n in rows)
    return f'<div class="ix-h">{name}</div>{r}'
L = [("About", [("Welcome", 4), ("Our Vision", 5), ("Brand Messaging", 6), ("Tone of Voice", 7)]),
     ("Brand Logo", [("Primary Logo", 9), ("Monogram", 10), ("Boxed Logo", 11), ("Service Marks", 12), ("Anatomy of Logo", 13), ("Usage on the Web", 14)])]
R = [("Typography", [("Logo Typeface", 16), ("Primary Typeface", 17), ("Secondary Typeface", 18), ("Font Pairing", 19)]),
     ("Brand Colours", [("Primary Colour", 21), ("Secondary Colour", 22), ("Colour Usage Proportions", 23), ("P.L in Brand Colours", 24), ("M. in Brand Colours", 25)]),
     ("Graphic Assets", [("The Tile Grid", 27), ("The Range", 28), ("Mockups", 29), ("Imagery", 30), ("Brand Film", 32)])]
pages.append(f'''<section class="pg" style="background:{WHITE}">
  {title("Index", top=76)}
  <div class="ix" style="left:60px;top:190px;width:398px">{ix_sec(*L[0])}<div style="height:10px"></div>{ix_sec(*L[1])}</div>
  <div class="ix" style="left:551px;top:62px;width:478px">{ix_sec(*R[0])}<div style="height:16px"></div>{ix_sec(*R[1])}<div style="height:16px"></div>{ix_sec(*R[2])}</div>
</section>''')

# 03 SECTION ONE ---------------------------------------------------------
pages.append(divider("ONE", "About", "The About section defines the foundation of Al Reef &amp; Laurel — its vision, mission, values and brand voice. It sets out the thinking, purpose and emotional direction behind every experience the brand creates."))

# 04 WELCOME -------------------------------------------------------------
pages.append(f'''<section class="pg" style="background:{WHITE}">{head("Introduction")}
  {title("Welcome", top=181)}
  {body("""<p>If you’re reading this, you’re helping bring Al Reef &amp; Laurel to life.</p>
  <p>This guide exists to protect the clarity of our brand and ensure everything we create reflects our values: real materials, honest craft and quiet confidence.</p>
  <p>We’re not interested in jargon or fluff. What matters is how people experience Al Reef &amp; Laurel visually, verbally and in the hand. Our identity is built through consistency and care.</p>
  <p>Inside, you’ll find practical guidelines to help you work with our brand. These aren’t hard rules for the sake of rules; they’re tools. Use them to stay aligned, make decisions and create work that feels distinctly ours.</p>
  <p>Whether you’re designing a product page, packing a gift set or introducing Al Reef &amp; Laurel to someone new, thank you for being a part of this.</p>""",
  top=318, width=505, size=16, lh=20, color=INK)}
  {at(730, 208, im("sink-mitt.jpg", 393, 586, 0.68, 0.5, 1.12))}
  <div style="position:absolute;left:730px;width:393px;top:250px;display:flex;justify-content:center">{wordmark(34, ON_DARK)}</div>
  <div style="position:absolute;left:730px;width:393px;top:654px;height:140px;background:linear-gradient(180deg,rgba(40,22,12,0),rgba(40,22,12,.48))"></div>
  <div style="position:absolute;left:730px;width:393px;top:740px;text-align:center;font:400 16px/20px Inter;letter-spacing:0;color:{ON_DARK}">GROWN, NOT MADE</div>
</section>''')

# 05 VISION --------------------------------------------------------------
pages.append(f'''<section class="pg">{head("Introduction")}
  {title("Our<br>Vision", top=181)}
  {body("""<p>To make the honest, traceable bath ritual the everyday standard in Gulf homes: a loofah grown in Egypt’s Nile Delta and a bar of Levantine laurel soap, renewed every 60 days.</p>
  <p>In the near term, Al Reef &amp; Laurel launches in the UAE in early 2027 with a founding-member community, The Duo and a Ramadan gifting range, sold on our own store where renewal lives.</p>
  <p>Over the next 5 years, the brand grows across the GCC: Saudi Arabia from 2027, luxury retail through Ounass, boutique hotels and spas in Dubai, Abu Dhabi and Riyadh, and selected beauty retail.</p>
  <p>In the longer term, Al Reef &amp; Laurel aims to take the Nile Delta loofah and the Levantine laurel ritual beyond the Gulf.</p>""",
  top=384, width=600, size=16, lh=20, color=INK)}
  {at(746, 197, im("olive-niche.jpg", 377, 597, 0.60, 0.5))}
</section>''')

# 06 MESSAGING -----------------------------------------------------------
msgs = ["Grown, not made.", "The hammam, every morning.", "When the tag fades, so should your loofah.", "Know exactly where it grew."]
mhtml = "".join(f'<div class="msg" style="top:{439 + i*70}px">{i+1}. {m}</div>' for i, m in enumerate(msgs))
pages.append(f'''<section class="pg">{head("Introduction")}
  {title("Brand Messaging", top=181)}
  {body("A short list of approved mottos and brand messaging: clear, versatile phrases that capture our voice and point of view.", top=287, width=500, size=13.3, lh=20)}
  {mhtml}
</section>''')

# 07 TONE OF VOICE -------------------------------------------------------
tone = [(60, 344, "1. Specific &amp; Grounded", "Numbers and places persuade. We write “sun-dried for 21 days in Damanhour”, never “ethically sourced from exotic lands”.", 222),
        (60, 508, "2. Precise &amp; Human", "Refined without feeling clinical. We teach the ritual and the reason behind it, with one light twist per piece.", 222),
        (359, 344, "3. Calm Confidence", "No hype, no urgency tricks and no exclamation marks. The brand speaks with quiet confidence rather than loud persuasion.", 222),
        (359, 508, "4. Sensory &amp; Material", "We speak about fibre, water and steam, and how a bathroom feels on a weekday morning.", 222),
        (675, 344, "5. Beyond Wellness Language", "We avoid generic terms like “detox”, “pamper” or “revolutionary exfoliation”. We say what it is, where it grew and what it does.", 300),
        (675, 508, "6. One Word of Arabic", "English first, British spelling, numerals for numbers. Arabic appears as one meaningful word, never as a translation.", 300)]
thtml = "".join(f'<div class="tv-h" style="left:{x}px;top:{y}px">{h}</div><div class="tv-p" style="left:{x+24}px;top:{y+43}px;width:{w}px">{p}</div>' for x, y, h, p, w in tone)
pages.append(f'''<section class="pg">{head("Introduction")}
  {title("Tone of Voice", top=181)}
  {thtml}
</section>''')

# 08 SECTION TWO ---------------------------------------------------------
pages.append(divider("TWO", "Brand Logo", "The Al Reef &amp; Laurel logo is simple but deliberate, designed to feel precise, timeless and grounded. This section outlines how to use it correctly and how not to."))

def mini_logo(text):
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:9px">{wordmark(19, LOGO_INK)}'
            f'<div style="width:58px;height:1px;background:{LOGO_INK}"></div><div class="ib-s">{text}</div></div>')

# 09 PRIMARY LOGO --------------------------------------------------------
pages.append(f'''<section class="pg">{head("Brand Logo")}
  {title("Primary<br>Logo", top=271, color=LOGO_INK)}
  {body("The Al Reef &amp; Laurel logo represents the brand as a whole. Use it across products, packaging, marketing and any official communication. It is a carefully crafted mark and should never be altered or redrawn.")}
  <div style="position:absolute;left:518px;width:462px;top:252px;display:flex;justify-content:center">{wordmark(116, LOGO_INK)}</div>
  {infobox(mini_logo('1" OR 120PX'), "LOGO MINIMUM SIZING", "This version is intended for small sizes. The minimum width is 1&quot; for print applications and 120px for digital applications.")}
</section>''')

# 10 MONOGRAM ------------------------------------------------------------
pages.append(f'''<section class="pg">{head("Brand Logo")}
  {title("Monogram", top=271, color=LOGO_INK)}
  {body("<p>The Al Reef &amp; Laurel monogram is a loofah cut in half: the outer skin, three seed chambers and the fibre walls between them, drawn by hand in one even line. It is the first thing you see when you slice a gourd from Field 7.</p><p>Rather than serving as an abbreviation of the primary logo, it is a standalone mark that captures the brand in its most distilled form. Use it on favicons, social avatars, cotton tags, wax seals and soap stamps, always from approved artwork.</p>")}
  {at(612, 150, mono(300, LOGO_INK, 4.2))}
  {infobox('<div style="display:flex;flex-direction:column;align-items:center;gap:9px">' + mono(34, LOGO_INK, 5.6) + f'<div style="width:58px;height:1px;background:{LOGO_INK}"></div><div class="ib-s">.40" OR 30PX</div></div>', "MONOGRAM MINIMUM SIZING", "This version is intended for extremely small sizes. The minimum height is .40&quot; for print applications and 30px for digital applications.")}
</section>''')

# 11 BOXED LOGO ----------------------------------------------------------
pages.append(f'''<section class="pg">{head("Brand Logo")}
  {title("Boxed<br>Logo", top=238, color=LOGO_INK)}
  {body("<p>The boxed logo is a denser version of the Al Reef &amp; Laurel mark, placed within a solid container. The container can be square, circular or have rounded corners set to 5% of its width (6px corners at 120px wide).</p><p>Use this variation when clear space is limited, contrast is needed, or a bold, self-contained presence fits the context: cotton tags, soap bands and social tiles.</p>")}
  <div class="box" style="position:absolute;left:519px;top:206px;width:206px;height:206px;background:{LOGO_INK}">{wordmark(31, ON_DARK)}</div>
  <div class="box" style="position:absolute;left:774px;top:206px;width:206px;height:206px;background:{LOGO_INK}">{mono(132, ON_DARK, 4.8)}</div>
  {infobox(f'<div style="display:flex;flex-direction:column;align-items:center;gap:9px"><div class="box" style="width:46px;height:46px;background:{LOGO_INK}">{mono(34, ON_DARK, 6)}</div><div class="ib-s">.75" OR 96PX</div></div>', "LOGO MINIMUM SIZING", "This version is not intended for extremely small sizes. The minimum height is .75&quot; for print applications and 96px for digital applications.")}
</section>''')

# 12 SERVICE MARKS -------------------------------------------------------
def sm_card(x, mark, label, p1, p2):
    return (f'<div class="smc" style="left:{x}px">'
            f'<div style="position:absolute;left:0;right:0;top:44px;display:flex;justify-content:center"><div style="position:relative">{wordmark(40, LOGO_INK)}'
            f'<span class="sm-m" style="left:100%;top:-4px">{mark}</span></div></div>'
            f'<div style="position:absolute;left:0;right:0;top:168px;display:flex;justify-content:center"><div style="position:relative">{mono(118, LOGO_INK, 4.6)}'
            f'<span class="sm-m" style="left:92%;top:6px">{mark}</span></div></div>'
            f'<div class="sm-h">{label}</div><div class="sm-p" style="top:344px">{p1}</div><div class="sm-p" style="top:398px">{p2}</div></div>')
pages.append(f'''<section class="pg">{head("Brand Logo", )}
  {title("Service<br>Marks", top=160, color=LOGO_INK)}
  {body("<p>The primary logo and monogram have service mark variations, used to indicate trademark status where required.</p><p>These include both trademark (™) and registered trademark (®) versions, depending on the level of legal protection in each market.</p><p>When in doubt, use the version without a mark. The standard logo is appropriate for most day-to-day use.</p><p>The service mark and the logo scale independently, with priority given to keeping the mark legible at any size.</p>", width=330)}
  {sm_card(432, "™", "TRADEMARK VERSIONS", "For markets where the trademark is filed but not yet registered, such as the UAE and Saudi Arabia during launch. This is the default mark.", "Include the ™ only on the first or most prominent use of the logo in any given context.")}
  {sm_card(766, "®", "REGISTERED TRADEMARK VERSIONS", "Only in regions where the Al Reef &amp; Laurel trademark is fully and officially registered. Do not use this mark in unregistered territories.", "Include the ® only on the first or most prominent use of the logo in any given context.")}
</section>''')

# 13 ANATOMY -------------------------------------------------------------
pages.append(f'''<section class="pg">{head("Brand Logo")}
  {title("Anatomy<br>of the Logo", top=181, color=LOGO_INK)}
  {body("<p>The Al Reef &amp; Laurel logo is constructed with carefully balanced proportions, spacing and alignment to ensure clarity and consistency across every application.</p><p>“AL REEF” is set in Quattrocento capitals. “&amp; LAUREL” sits beneath in tracked Inter at one quarter of the cap height, centred. Do not stretch, condense, rotate or redraw any part of the logo, and never set the name on one line.</p>")}
  <div id="anat" style="position:absolute;left:524px;top:228px;width:458px;height:190px;border:1px solid {LOGO_INK}">
    <div id="anat-wm" style="position:absolute;left:0;right:0;top:18px;display:flex;justify-content:center">{wordmark(104, LOGO_INK, spans=True)}</div>
  </div>
  <div id="anat-lbl" style="position:absolute;left:996px;font:300 15.9px/20px 'Noto Serif';color:{INK};white-space:nowrap">cap height</div>
</section>''')

# 14 WEB -----------------------------------------------------------------
pages.append(f'''<section class="pg">{head("Brand Logo")}
  {title("Usage on<br>the web", top=190, color=LOGO_INK)}
  {body("The Al Reef &amp; Laurel logo is adapted for various digital touchpoints, each with its own format and constraints.", bottom=662)}
  <div class="box" style="position:absolute;left:512px;top:183px;width:45px;height:45px;background:{LOGO_INK}">{mono(34, ON_DARK, 6.2)}</div>
  <div class="wl" style="top:239px"><div class="wl-h">AL REEF &amp; LAUREL FAVICON</div><div class="wl-p">Our favicon, a 32px × 32px icon displayed in the browser next to the URL, uses the boxed monogram.</div></div>
  <div class="box" style="position:absolute;left:512px;top:324px;width:80px;height:80px;background:{LOGO_INK}">{mono(60, ON_DARK, 5.4)}</div>
  <div class="box" style="position:absolute;left:612px;top:324px;width:80px;height:80px;background:{LOGO_INK};border-radius:50%">{mono(56, ON_DARK, 5.4)}</div>
  <div class="wl" style="top:417px"><div class="wl-h">SOCIAL MEDIA AVATARS</div><div class="wl-p">The layout of these avatars should not be altered. Approved secondary brand colours may be used for Ramadan, Eid and the harvest season.</div></div>
  <div class="box" style="position:absolute;left:512px;top:511px;width:80px;height:80px;background:{LOGO_INK};border-radius:16px">{mono(60, ON_DARK, 5.4)}</div>
  <div class="wl" style="top:602px"><div class="wl-h">DEVICE ICON</div><div class="wl-p">If our website is saved as a bookmark on a phone’s home screen, this graphic will be displayed. Default size is 192px square.</div></div>
</section>''')

# 15 SECTION THREE -------------------------------------------------------
pages.append(divider("THREE", "Typography", "The Al Reef &amp; Laurel type system is designed to feel refined, balanced and legible across every touchpoint. This section outlines the logo, primary and secondary typefaces and their intended use."))

def specimen_page(t1, sub, fam, rows, text, aa_family=None, sample_css=""):
    aa_family = aa_family or fam
    r = ""
    y = 291
    for name, css, gl in rows:
        r += (f'<div class="sp-n" style="top:{y}px;font-family:\'{fam}\';{css}">{name}</div>'
              f'<div class="sp-g" style="top:{y+24}px;font-family:\'{fam}\';{css}">{gl}</div>')
        y += 100
    return f'''<section class="pg">{head("Typography")}
  {title(t1, top=190)}
  <div class="sub" style="top:364px">{sub}</div>
  {body(text)}
  <div style="position:absolute;left:652px;top:78px;font:400 155.8px/1 '{aa_family}';color:#DDD7CC">Aa</div>
  <div style="position:absolute;left:637px;top:224px;font:400 30.3px/44px '{fam}';color:{INK};{sample_css}">{fam} Font Family</div>
  {r}
</section>'''

GL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br>1234567890!@£$%^&amp;*()"
# 16 LOGO TYPEFACE
pages.append(specimen_page("Logo<br>Typeface", "Wordmark Typeface", "Quattrocento",
    [("Regular", "font-weight:400", GL), ("Bold", "font-weight:700", GL)],
    "<p>The wordmark and display moments on packaging are set in Quattrocento, a classical serif with calm, generous capitals. It is free for commercial use.</p><p>Canela (commercial licence) is the optional upgrade for print and packaging. If licensed, it replaces Quattrocento in the wordmark only.</p>"))
# 17 PRIMARY
pages.append(specimen_page("Website<br>Typeface", "Primary Typeface", "Literata",
    [("Regular", "font-weight:400", GL), ("Light italic", "font-weight:300;font-style:italic", GL), ("Semi Bold", "font-weight:650", GL), ("Bold Italic", "font-weight:730;font-style:italic", GL)],
    "<p>The type system is built around a carefully selected pair of primary and secondary typefaces, designed to work together across digital and print. The primary typeface, Literata, carries the brand’s refined and recognisable character.</p><p>Together, these typefaces create a balanced visual rhythm. Consistent use keeps hierarchy clear and the identity cohesive.</p>"))
# 18 SECONDARY
pages.append(specimen_page("Website<br>Type", "Secondary Typeface", "Inter",
    [("Regular", "font-weight:400", GL), ("Light italic", "font-weight:300;font-style:italic", GL), ("Semi Bold", "font-weight:600", GL), ("Bold Italic", "font-weight:700;font-style:italic", GL)],
    "<p>Inter supports readability, structure and functional communication: body copy, prices, buttons and labels, and the specification line on packaging, set in tracked capitals: GRADE A · 58 / CM².</p><p>Use Inter for every price and number in running copy, with tabular figures in tables and carts.</p>"))

# 19 FONT PAIRING
pages.append(f'''<section class="pg">{head("Typography")}
  {title("Font<br>Pairing", top=181)}
  <div style="position:absolute;left:405px;top:192px;font:400 33.3px/54px 'Literata';color:{LOGO_INK}">Literata - Heading</div>
  <div style="position:absolute;left:405px;top:251px;width:640px;font:400 49.3px/53.3px 'Literata';color:{LOGO_INK};letter-spacing:0">A loofah grown in the Nile Delta, finished for the everyday shower.</div>
  <div style="position:absolute;left:405px;top:441px;font:400 33.3px/48px 'Inter';color:{LOGO_INK}">Inter - Body Copy</div>
  <div style="position:absolute;left:405px;top:490px;width:660px;font:300 26.7px/33.3px 'Inter';color:{LOGO_INK};text-align:justify;letter-spacing:0">Al Reef &amp; Laurel pairs a loofah sun-dried for 21 days in Damanhour with a bar of Levantine laurel soap. Every loofah carries a cotton tag that fades by day 60, and a fresh one arrives as it does.</div>
</section>''')

# 20 SECTION FOUR --------------------------------------------------------
pages.append(divider("FOUR", "Brand Colours", "The Al Reef &amp; Laurel colour palette is designed to feel grounded, timeless and refined: the warm linen of the hammam, the green of laurel and olive tile, and the clay and earth of the Nile Delta."))

# 21 PRIMARY COLOUR
pages.append(f'''<section class="pg" style="background:{WHITE}">
  <div style="position:absolute;left:456px;top:0;right:0;bottom:0;background:{EARTH}"></div>
  {head("Brand Colours", mid_color="#F3E6D8", right_color="#F3E6D8")}
  {title("Primary<br>Colour", top=190)}
  {body("A soft linen inspired by hammam marble, unbleached cotton and quiet luxury. Delta Linen brings warmth, calm and understated elegance to the palette, creating a refined foundation that feels both modern and enduring.", bottom=664, width=290)}
  <div class="swc" style="left:519px;top:269px;width:542px">
    <div style="height:183px;background:{VEIL};position:relative"><span class="sw-n" style="font-size:45.6px;color:{INK};left:24px;top:12px">Delta Linen</span></div>
    <div class="sw-i" style="padding:7px 24px 12px"><span>Hex</span><span>#EEE4D8</span><span>RGB</span><span>238, 228, 216</span><span>CMYK</span><span>6, 8, 13, 0</span></div>
  </div>
  <div style="position:absolute;left:525px;top:603px;width:536px;height:49px;background:linear-gradient(90deg,#BDB2A4,{VEIL} 45%,#FBF8F1)"></div>
</section>''')

# 22 SECONDARY COLOUR
def sw2(x, y, name, hexv, rgb, cmyk):
    return (f'<div class="swc" style="left:{x}px;top:{y}px;width:231px;border-radius:0">'
            f'<div style="height:140px;background:{hexv};position:relative"><span class="sw-n" style="font-size:31.4px;color:{ON_DARK};left:8px;top:6px">{name}</span></div>'
            f'<div class="sw-i" style="padding:6px 8px 10px;grid-template-columns:68px 1fr"><span>Hex</span><span>{hexv}</span><span>RGB</span><span>{rgb}</span><span>CMYK</span><span>{cmyk}</span></div></div>')
pages.append(f'''<section class="pg">{head("Brand Colours")}
  {title("Secondary<br>Colour", top=190)}
  {body("The secondary palette complements Delta Linen with a curated range of supporting tones that add depth, contrast and flexibility: the green of laurel leaves and olive tile, and the clay and earth of the Delta. Each tone works across digital, print, packaging and space.", bottom=698, width=305)}
  {sw2(519, 194, "Laurel Mist", MIST, "119, 145, 141", "57, 33, 42, 3")}
  {sw2(830, 194, "Deep Laurel", VOID, "41, 51, 41", "72, 56, 72, 63")}
  {sw2(519, 471, "Nile Clay", CLAY, "193, 90, 39", "18, 76, 100, 6")}
  {sw2(830, 471, "Delta Earth", EARTH, "106, 46, 12", "35, 80, 100, 47")}
</section>''')

# 23 PROPORTIONS
pages.append(f'''<section class="pg" style="background:#FFFEFD">{head("Brand Colours")}
  {title("Colour Usage<br>Proportions", top=161)}
  {body("""<p>Colour helps create structure, guide attention and set tone. To keep our compositions balanced, we follow a simple framework: 60 / 30 / 10.</p>
  <p>60% Dominant: Delta Linen. This is the foundation. It holds the layout together and sets the mood: backgrounds and large containers.</p>
  <p>30% Secondary: Laurel Mist and Deep Laurel. Contrast and support: frames, panels and type.</p>
  <p>10% Highlight: Nile Clay and Delta Earth. Where the eye goes first: actions, seals and key moments.</p>
  <p>This ratio isn’t a rule; it’s a guide. The goal is to use colour intentionally, with restraint and clarity.</p>""", top=368, width=335)}
  <div style="position:absolute;left:574px;top:195px;width:462px;height:462px;border-radius:50%;background:{VEIL}"></div>
  <div class="pl" style="left:770px;top:423px">60% DOMINANT COLOUR</div>
  <div style="position:absolute;left:619px;top:181px;width:104px;height:104px;border-radius:50%;background:{CLAY}"></div>
  <div style="position:absolute;left:645px;top:197px;width:76px;height:76px;border-radius:50%;background:{EARTH}"></div>
  <div class="pl" style="left:561px;top:293px">10% HIGHLIGHT COLOUR</div>
  <div style="position:absolute;left:556px;top:511px;width:167px;height:167px;border-radius:50%;background:{MIST}"></div>
  <div style="position:absolute;left:605px;top:560px;width:118px;height:118px;border-radius:50%;background:{VOID}"></div>
  <div class="pl" style="left:545px;top:681px">30% SECONDARY COLOUR</div>
</section>''')

# 24 LOGO IN COLOURS
def lchip(cx, cy, bg, fg):
    box = f"background:{bg};" if bg else ""
    return (f'<div class="box" style="position:absolute;left:{cx-95}px;top:{cy-40}px;width:190px;height:80px;{box}">{wordmark(31, fg)}</div>')
chips = "".join([lchip(658, 373, None, MIST), lchip(910, 373, None, CLAY), lchip(658, 475, None, VOID), lchip(910, 475, None, EARTH),
                 lchip(658, 578, MIST, ON_DARK), lchip(910, 578, CLAY, ON_DARK), lchip(658, 682, VOID, ON_DARK), lchip(910, 682, EARTH, ON_DARK)])
pages.append(f'''<section class="pg" style="background:{WHITE}">
  <div style="position:absolute;left:0;top:0;width:464px;bottom:0;background:{CREAM}"></div>
  {head("Brand Colours")}
  {title("Primary<br>Logo in<br>Brand Colours", top=190, size=55.1, lh=66)}
  {body("The primary Al Reef &amp; Laurel logo is designed to work seamlessly across the core brand palette, ensuring clarity, elegance and strong recognition in every application.", bottom=707, width=310)}
  <div style="position:absolute;left:560px;width:450px;top:168px;display:flex;justify-content:center">{wordmark(84, "#E8DED1")}</div>
  {chips}
</section>''')

# 25 MONOGRAM IN COLOURS
rows = [(VEIL, INK), (MIST, ON_DARK), (VOID, ON_DARK), (CLAY, ON_DARK), (EARTH, ON_DARK)]
mg = ""
for i, (c, fg) in enumerate(rows):
    cy = 190 + i * 114.5
    plain_col = c if c != VEIL else "#E2D6C6"
    mg += at(688 - 44, cy - 44, mono(88, plain_col, 5))
    mg += f'<div class="box" style="position:absolute;left:{802-40}px;top:{cy-40:.0f}px;width:80px;height:80px;background:{c}">{mono(62, fg, 5.6)}</div>'
    mg += f'<div class="box" style="position:absolute;left:{916-42}px;top:{cy-42:.0f}px;width:84px;height:84px;border-radius:50%;background:{c}">{mono(60, fg, 5.6)}</div>'
pages.append(f'''<section class="pg" style="background:{WHITE}">
  <div style="position:absolute;left:0;top:0;width:464px;bottom:0;background:{CREAM}"></div>
  {head("Brand Colours")}
  {title("Monogram<br>Logo in<br>Brand Colours", top=190, size=55.1, lh=66)}
  {body("The Al Reef &amp; Laurel monogram is a compact symbolic mark crafted to adapt effortlessly across the brand colours, offering a refined and distinctive presence in minimal applications.", bottom=707, width=310)}
  {mg}
</section>''')

# 26 SECTION FIVE --------------------------------------------------------
pages.append(divider("FIVE", "Graphic Assets", "The graphic assets combine the tile grid, lifestyle imagery and product mockups to present Al Reef &amp; Laurel in a refined, immersive way, showing how the brand lives in real bathrooms, real hands and real materials."))

# 27 TILE GRID
def gridbox(x, y, bg, cell, stack, label):
    v = f"repeating-linear-gradient(90deg, rgba(251,245,236,.20) 0 1px, transparent 1px {cell}px)"
    h = f"repeating-linear-gradient(0deg, rgba(251,245,236,.20) 0 1px, transparent 1px {cell*3 if stack else cell}px)"
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:258px;height:200px;background-color:{bg};background-image:{v},{h}"></div>'
            f'<div class="cap-s" style="left:{x}px;top:{y+212}px">{label}</div>')
pages.append(f'''<section class="pg">{head("Graphic Asset")}
  {title("The Tile<br>Grid", top=190)}
  {body("<p>Our box pattern borrows from the walls our products live on: hammam marble, mosaic and the long stacked tiles of a Gulf bathroom.</p><p>The square grid opens sections, lines packaging flaps and breaks website sections. The tall stack grid is for social tiles, gift tissue and shelf strips.</p><p>Use it on Nile Clay, Deep Laurel or Delta Earth only, with hairlines at 20% Delta Linen.</p>")}
  {gridbox(518, 183, CLAY, 43, False, "SQUARE GRID · NILE CLAY")}
  {gridbox(803, 183, VOID, 43, False, "SQUARE GRID · DEEP LAUREL")}
  {gridbox(518, 446, EARTH, 29, True, "STACK GRID · DELTA EARTH")}
  {gridbox(803, 446, MIST, 29, True, "STACK GRID · LAUREL MIST")}
</section>''')

# 28 THE RANGE
rng = [("LOOFAHS", [("The Daily Pad", "Grade A · Gentle or Deep"), ("The Hammam Mitt", "Grade A · 60 / cm²"), ("The Back Strap", "Premium A · 75 cm")]),
       ("SABON GHAR", [("Laurel 16", "150 g · 16% laurel oil"), ("Laurel 30", "150 g · 30% laurel oil"), ("Guest Bar", "40 g · 16% laurel oil")]),
       ("RITUALS", [("The Duo", "Daily Pad + Laurel 16"), ("The Pair", "For two"), ("The House", "For a family of four")]),
       ("LITTLE REEF", [("Soft Pebble", "Ages 3–10"), ("Camel Mitt", "Ages 3–10"), ("Shaped Trio", "Unscented · 3 × 60 g")])]
rh = ""
for i, (h, items) in enumerate(rng):
    x = 60 + (i % 2) * 300
    y = 352 + (i // 2) * 178
    rh += f'<div class="cap-s" style="left:{x}px;top:{y}px;color:{CLAY}">{h}</div>'
    for j, (n, d) in enumerate(items):
        rh += (f'<div style="position:absolute;left:{x}px;top:{y+26+j*46}px;width:270px"><div style="font:400 17px/22px Literata;color:{INK}">{n}</div>'
               f'<div style="font:400 11.5px/17px Inter;color:{TXT}">{d}</div></div>')
pages.append(f'''<section class="pg">{head("Graphic Asset")}
  {title("The Range", top=190)}
  {body("A tight range where every piece has one clear job. Each loofah carries a fading cotton tag and a batch QR traced to Field 7, Damanhour.", top=280, width=540)}
  {rh}
  {at(699, 147, im("still-life.jpg", 424, 647, 0.55, 0.5))}
</section>''')

# 29 MOCKUPS
def tag_mock(scale=1.0):
    return (f'<div style="width:{118*scale:.0f}px;height:{196*scale:.0f}px;background:{VEIL};border-radius:{10*scale:.0f}px;position:relative;box-shadow:0 10px 24px rgba(0,0,0,.14);display:flex;flex-direction:column;align-items:center;padding-top:{44*scale:.0f}px;gap:{13*scale:.0f}px">'
            f'<div style="position:absolute;top:{14*scale:.0f}px;width:{12*scale:.0f}px;height:{12*scale:.0f}px;border-radius:50%;background:#D8CCBB"></div>{mono(int(54*scale), VOID, 5)}'
            f'<div style="width:{62*scale:.0f}px;height:3px;background:{CLAY}"></div><div style="width:{62*scale:.0f}px;height:3px;background:{CLAY};opacity:.55"></div><div style="width:{62*scale:.0f}px;height:3px;background:{CLAY};opacity:.2"></div>'
            f'<div style="font:500 {7*scale:.1f}px Inter;letter-spacing:.16em;color:{VOID}">DAY 01 / 60</div></div>')
seal = (f'<div style="width:124px;height:124px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#A64A1E,#7A2F0E);box-shadow:0 8px 20px rgba(0,0,0,.25),inset 0 0 0 9px rgba(0,0,0,.08);display:flex;align-items:center;justify-content:center">{mono(74, "#C8653A", 6)}</div>')
soap = (f'<div style="width:138px;height:200px;background:#E8DCC6;border-radius:8px;position:relative;box-shadow:0 10px 24px rgba(0,0,0,.14);overflow:hidden">'
        f'<div style="position:absolute;left:0;right:0;top:66px;height:68px;background:{VOID};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px">{mono(32, VEIL, 5.5)}'
        f'<div style="font:500 6.5px Inter;letter-spacing:.18em;color:{VEIL}">LAUREL 16</div></div></div>')
box = (f'<div style="width:132px;height:190px;background:#C9A87B;border-radius:4px;position:relative;box-shadow:0 12px 26px rgba(0,0,0,.18);overflow:hidden">'
       f'<div style="position:absolute;left:31px;top:34px;width:70px;height:94px;border-radius:50%;background:#D9C08F;box-shadow:inset 0 0 0 2px rgba(0,0,0,.08)"></div>'
       f'<div style="position:absolute;left:0;right:0;bottom:0;height:42px;background:{VOID};display:flex;align-items:center;justify-content:center">{wordmark(12, VEIL)}</div></div>')
def mtile(x, y, content, bg):
    return f'<div class="box" style="position:absolute;left:{x}px;top:{y}px;width:174px;height:248px;background:{bg}">{content}</div>'
pages.append(f'''<section class="pg">{head("Graphic Asset")}
  {title("Mockups", top=190)}
  {body("These mockups show how the Al Reef &amp; Laurel identity comes to life on the objects people hold: the fading cotton tag, the wax seal on a gift, the soap band and the kraft box. Final artwork is printed on unbleached stock, with no plastic and no lamination.", bottom=662, width=330)}
  {mtile(638, 155, tag_mock(1.0), "#E4DCCF")}{mtile(823, 155, seal, "#EDE6DB")}
  {mtile(638, 415, soap, "#DDD4C5")}{mtile(823, 415, box, "#E9E1D4")}
</section>''')

# 30 IMAGERY
pages.append(f'''<section class="pg">{head("Graphic Asset")}
  {title("Imagery", top=190)}
  {body("Our imagery reflects the world of Al Reef &amp; Laurel: warm, tiled bathrooms in clay, olive and deep green, lit by one warm source. The loofah is shown honestly, hanging, wet or in the hand, within a considered space. Hands and shoulders, never posed faces.", bottom=662, width=350)}
  {at(699, 147, im("mosaic-wall.jpg", 424, 647, 0.6, 0.42, 1.45))}
</section>''')

# 31 IMAGERY SPREAD
pages.append(f'''<section class="pg">{head("Graphic Asset")}
  <div style="position:absolute;left:0;top:132px;display:flex">
    {im("green-vanity.jpg", 380, 662, 0.68, 0.5, 1.17)}
    {im("olive-niche.jpg", 440, 662, 0.55, 0.5)}
    {im("mosaic-wall.jpg", 303, 662, 0.60, 0.5)}
  </div>
</section>''')

# 32 BRAND FILM
frames = [
    ("0:00–0:04", "Field 7 at first light. Gourds hang on the trellis.", f'<div class="box" style="width:100%;height:100%;background:linear-gradient(180deg,#3B4A3B,{VOID})"><span style="font:500 9px Inter;letter-spacing:.16em;color:{VEIL}">FIELD 7 · 05:52</span></div>'),
    ("0:04–0:09", "Water runs. A hand takes the mitt from its hook.", im("sink-mitt.jpg", 196, 200, 0.74, 0.52, 1.5)),
    ("0:09–0:15", "Lather, then small circles. Steam rises.", im("olive-niche.jpg", 196, 200, 0.66, 0.56, 1.45)),
    ("0:15–0:20", "Hung to dry on the tile. The tag reads Day 01.", im("mosaic-wall.jpg", 196, 200, 0.645, 0.47, 1.6)),
    ("0:20–0:25", "Time passes. The ink on the tag fades.", f'<div class="box" style="width:100%;height:100%;background:{VEIL}">{tag_mock(0.8)}</div>'),
    ("0:25–0:30", "Grown, not made.", f'<div class="box grid-s" style="width:100%;height:100%;background-color:{CLAY}">{wordmark(20, ON_DARK)}</div>'),
]
fh = ""
for i, (t, d, v) in enumerate(frames):
    x = 432 + (i % 3) * 216
    y = 150 + (i // 3) * 270
    fh += (f'<div style="position:absolute;left:{x}px;top:{y}px;width:196px"><div style="width:196px;height:200px;overflow:hidden;position:relative">{v}</div>'
           f'<div style="margin-top:10px;font:500 10.5px/14px Inter;letter-spacing:.1em;color:{CLAY}">{t}</div>'
           f'<div style="margin-top:4px;font:300 13.3px/16px \'Noto Serif\';letter-spacing:-.05em;color:{TXT}">{d}</div></div>')
pages.append(f'''<section class="pg">{head("Graphic Asset")}
  {title("Brand<br>Film", top=190)}
  {body("<p>“Grown, not made.” A 30-second launch film for Instagram, TikTok and the website hero, cut to 15 and 6 seconds for paid social.</p><p>No voice-over: water, fibre and a single line of type at the end, shot in one warm bathroom and on Field 7.</p>", bottom=662, width=320)}
  {fh}
</section>''')

# 33 THANK YOU
pages.append(f'''<section class="pg" style="background:
  radial-gradient(ellipse 34% 40% at 14% 18%, rgba(193,118,80,.95), rgba(193,118,80,0) 100%),
  radial-gradient(ellipse 30% 30% at 36% 6%, rgba(190,145,116,.8), rgba(190,145,116,0) 100%),
  radial-gradient(ellipse 34% 38% at 90% 8%, rgba(176,190,186,.9), rgba(176,190,186,0) 100%),
  radial-gradient(ellipse 30% 34% at 60% 90%, rgba(150,168,164,.85), rgba(150,168,164,0) 100%),
  radial-gradient(ellipse 50% 50% at 50% 50%, rgba(190,182,164,.8), rgba(190,182,164,0) 100%),
  linear-gradient(180deg, #DCD3C6, #ECE7DE)">
  <div class="grain"></div>
  <div style="position:absolute;left:0;right:0;top:250px;display:flex;justify-content:center">{mono(240, "#252825", 4.6)}</div>
  <div style="position:absolute;left:0;right:0;top:712px;text-align:center;font:300 26.7px/38px 'Noto Serif';letter-spacing:-.05em;color:#2E2A26">Thank You</div>
</section>''')

# ---------------------------------------------------------------- CSS
CSS = f"""
@page {{ size: 297mm 210mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #888; }}
body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; text-rendering: geometricPrecision; -webkit-font-smoothing: antialiased; }}
.pg {{ width: 1123px; height: 794px; position: relative; overflow: hidden; background: {CREAM}; page-break-after: always; break-after: page; font-family: 'Noto Serif', serif; color: {INK}; font-kerning: normal; }}
.hd {{ position: absolute; top: 76px; font: 300 16px/20px 'Noto Serif'; white-space: nowrap; z-index: 3; }}
.ttl {{ position: absolute; font-family: 'Noto Serif'; font-weight: 300; letter-spacing: -.025em; white-space: nowrap; }}
.sub {{ position: absolute; left: 60px; font: 300 25.4px/36px 'Noto Serif'; color: {INK}; letter-spacing: -.05em; }}
.bd {{ position: absolute; font-family: 'Noto Serif'; font-weight: 300; }}
.bd p + p {{ margin-top: 1lh; }}
.grid {{ background-image: repeating-linear-gradient(90deg, rgba(251,245,236,.17) 0 1px, transparent 1px 124.8px), repeating-linear-gradient(0deg, rgba(251,245,236,.17) 0 1px, transparent 1px 132.3px); }}
.grid-s {{ background-image: repeating-linear-gradient(90deg, rgba(251,245,236,.2) 0 1px, transparent 1px 24.5px), repeating-linear-gradient(0deg, rgba(251,245,236,.2) 0 1px, transparent 1px 25px); }}
.pill {{ position: absolute; left: 50%; top: 56px; transform: translateX(-50%); height: 51px; padding: 0 30px; display: flex; align-items: center; border: 1px solid rgba(251,245,236,.8); border-radius: 999px; font: 300 20.1px 'Noto Serif'; color: #FBF5EC; white-space: nowrap; }}
.dv-t {{ position: absolute; left: 0; right: 0; top: 278px; text-align: center; font: 300 126.3px/160px 'Literata'; color: #FBF5EC; letter-spacing: -.05em; white-space: nowrap; }}
.dv-p {{ position: absolute; left: 226px; width: 672px; top: 644px; font: 300 13.3px/18px 'Noto Serif'; color: #F7EADF; }}
.wm {{ display: flex; flex-direction: column; align-items: center; line-height: 1; }}
.wm-a {{ font-family: 'Quattrocento'; font-weight: 400; letter-spacing: .07em; white-space: nowrap; margin-right: -.07em; }}
.wm-b {{ font-family: 'Inter'; font-weight: 500; letter-spacing: .42em; white-space: nowrap; margin-right: -.42em; }}
.ix {{ position: absolute; display: flex; flex-direction: column; }}
.ix-h {{ font: 400 40px/52px 'Noto Serif'; color: {INK}; }}
.ix-r {{ display: flex; align-items: baseline; gap: 6px; font: 300 26.7px/38.5px 'Noto Serif'; color: {INK}; }}
.ix-d {{ flex: 1; height: 1px; background-image: radial-gradient(circle, {INK} 0.9px, transparent 1.1px); background-size: 6px 2px; background-repeat: repeat-x; transform: translateY(-3px); opacity: .8; }}
.msg {{ position: absolute; left: 60px; font: 300 40px/56px 'Noto Serif'; letter-spacing: -.05em; color: {INK}; white-space: pre; }}
.tv-h {{ position: absolute; font: 300 26.7px/38px 'Noto Serif'; color: {INK}; letter-spacing: -.05em; white-space: nowrap; }}
.tv-p {{ position: absolute; font: 300 13.3px/16px 'Noto Serif'; letter-spacing: -.05em; color: {TXT}; }}
.ib {{ position: absolute; left: 518px; width: 462px; height: 128px; border: 1px solid {LOGO_INK}; display: flex; align-items: center; }}
.ib-l {{ width: 150px; flex: none; display: flex; justify-content: center; }}
.ib-r {{ padding: 0 22px 0 14px; }}
.ib-h {{ font: 400 13.3px/18px 'Noto Serif'; color: {INK}; letter-spacing: -.05em; }}
.ib-p {{ font: 300 10.7px/13.5px 'Noto Serif'; color: {TXT}; margin-top: 1px; }}
.ib-s {{ font: 300 13.3px/18px 'Noto Serif'; color: {INK}; white-space: nowrap; }}
.box {{ display: flex; align-items: center; justify-content: center; }}
.smc {{ position: absolute; top: 183px; width: 315px; height: 483px; border: 1px solid {LOGO_INK}; }}
.sm-m {{ position: absolute; font: 400 13px Inter; color: {LOGO_INK}; }}
.sm-h {{ position: absolute; left: 23px; top: 318px; font: 400 13.3px/18px 'Noto Serif'; letter-spacing: -.05em; color: {INK}; white-space: nowrap; }}
.sm-p {{ position: absolute; left: 23px; width: 272px; font: 300 10.7px/13.4px 'Noto Serif'; color: {TXT}; }}
.wl {{ position: absolute; left: 512px; width: 320px; }}
.wl-h {{ font: 400 13.3px/18px 'Noto Serif'; color: {INK}; letter-spacing: -.05em; }}
.wl-p {{ font: 300 10.7px/13.4px 'Noto Serif'; color: {TXT}; margin-top: 1px; }}
.sp-n {{ position: absolute; left: 638px; font-size: 13.3px; line-height: 20px; color: {INK}; }}
.sp-g {{ position: absolute; left: 637px; font-size: 13.3px; line-height: 16px; color: {INK}; white-space: nowrap; }}
.swc {{ position: absolute; background: #FFFFFF; border-radius: 7px; overflow: hidden; }}
.sw-n {{ position: absolute; font-family: 'Literata'; font-weight: 300; font-style: italic; white-space: nowrap; letter-spacing: -.05em; }}
.sw-i {{ display: grid; grid-template-columns: 66px 1fr; font: 300 14.7px/18.7px Inter; color: #262824; }}
.pl {{ position: absolute; font: 300 18.5px/27px 'Noto Serif'; letter-spacing: -.05em; color: {INK}; white-space: nowrap; }}
.cap-s {{ position: absolute; font: 500 10.5px/14px Inter; letter-spacing: .14em; color: {TXT}; white-space: nowrap; }}
.crop {{ position: relative; overflow: hidden; flex: none; }}
.crop img {{ position: absolute; display: block; }}
.grain {{ position: absolute; inset: 0; opacity: .22; mix-blend-mode: multiply;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 .55 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }}
.anat-bar {{ position: absolute; background: rgba(150,150,145,.42); mix-blend-mode: multiply; }}
.anat-dot {{ position: absolute; border-radius: 50%; background: rgba(120,120,115,.5); mix-blend-mode: multiply; }}
.anat-line {{ position: absolute; left: 0; right: 0; height: 1px; background: {LOGO_INK}; }}
"""

# Anatomy page: measure the letters after fonts load and draw stem bars, guide lines and the cap-height bracket.
JS = """
<script>
document.fonts.ready.then(() => {
  const box = document.getElementById('anat'); if (!box) return;
  const b = box.getBoundingClientRect();
  const wmA = box.querySelector('.wm-a'), wmB = box.querySelector('.wm-b');
  const fs = parseFloat(getComputedStyle(wmA).fontSize);
  const c = document.createElement('canvas').getContext('2d');
  c.font = '400 ' + fs + 'px Quattrocento';
  const m = c.measureText('AL REEF'), asc = m.fontBoundingBoxAscent, desc = m.fontBoundingBoxDescent, cap = m.actualBoundingBoxAscent;
  const ra = wmA.getBoundingClientRect();
  const baseline = ra.top + (ra.height - (asc + desc)) / 2 + asc - b.top;
  const capTop = baseline - cap;
  const fsB = parseFloat(getComputedStyle(wmB).fontSize);
  c.font = '500 ' + fsB + 'px Inter';
  const mb = c.measureText('& LAUREL');
  const rb = wmB.getBoundingClientRect();
  const baseB = rb.top + (rb.height - (mb.fontBoundingBoxAscent + mb.fontBoundingBoxDescent)) / 2 + mb.fontBoundingBoxAscent - b.top;
  const capB = baseB - mb.actualBoundingBoxAscent;
  const add = (cls, st, front) => { const d = document.createElement('div'); d.className = cls; Object.assign(d.style, st); if (front) box.appendChild(d); else box.insertBefore(d, box.firstChild); };
  [capTop, baseline, capB, baseB].forEach(y => add('anat-line', {top: y + 'px'}));
  const stem = fs * 0.115;
  [1, 3, 4, 5, 6].forEach(i => { const s = box.querySelector('.L' + i).getBoundingClientRect();
    add('anat-bar', {left: (s.left - b.left + fs*0.03 - stem*0.5) + 'px', width: (stem*2.1) + 'px', top: '0px', height: (baseline + 8) + 'px'}, true); });
  [[3, .78], [4, .5], [5, .62], [6, .62]].forEach(([i, f]) => { const s = box.querySelector('.L' + i).getBoundingClientRect(); const d = fs * .15;
    add('anat-dot', {left: (s.left - b.left + s.width * f - d/2) + 'px', top: (capTop - d/2) + 'px', width: d + 'px', height: d + 'px'}, true);
    add('anat-dot', {left: (s.left - b.left + s.width * f - d/2) + 'px', top: (baseline - d/2) + 'px', width: d + 'px', height: d + 'px'}, true); });
  const br = document.createElement('div');
  Object.assign(br.style, {position: 'absolute', left: (b.width + 10) + 'px', top: capTop + 'px', height: (baseline - capTop) + 'px', width: '9px', borderTop: '1px solid #252825', borderBottom: '1px solid #252825'});
  const ln = document.createElement('div');
  Object.assign(ln.style, {position: 'absolute', left: '4px', top: '0', bottom: '0', width: '1px', background: '#252825'}); br.appendChild(ln);
  box.appendChild(br);
  const lbl = document.getElementById('anat-lbl'); lbl.style.top = (b.top + capTop + (baseline - capTop)/2 - 10 - box.offsetParent.getBoundingClientRect().top) + 'px';
  lbl.style.left = (b.right - box.offsetParent.getBoundingClientRect().left + 26) + 'px';
  document.body.dataset.ready = '1';
});
</script>"""

import re as _re
def _inter_opsz(h):
    h = _re.sub(r'style="([^"]*Inter[^"]*)"', lambda m: 'style="' + m.group(1).rstrip('; ') + ";font-variation-settings:'opsz' 14\"", h)
    return h
html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Al Reef &amp; Laurel — Brand Guidelines V2</title>
<style>{FONTS}\n{CSS}</style></head><body>{''.join(pages)}{JS}</body></html>"""
open(os.path.join(HERE, "guide.html"), "w", encoding="utf-8").write(html)
print("pages:", len(pages))
