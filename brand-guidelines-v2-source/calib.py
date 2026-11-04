import asyncio, os, json
from playwright.async_api import async_playwright
NS, LIT, INT = "'Noto Serif'", "'Literata'", "'Inter'"
R = [  # key, text, quint width px, family, weight, size, italic
 ("hd", "Quint Home Brand Style Guide", 226, NS, 300, 16, 0),
 ("ttl", "Welcome", 271, NS, 300, 66.3, 0), ("ttl", "Brand Messaging", 501, NS, 300, 66.3, 0), ("ttl", "Tone of Voice", 384, NS, 300, 66.3, 0), ("ttl", "Monogram", 325, NS, 300, 66.3, 0), ("ttl", "Index", 167, NS, 300, 66.3, 0),
 ("bd16", "If you’re reading this, you’re helping bring Quint Home to life.", 455, NS, 300, 16, 0),
 ("bd13", "The Quint Home logo represents the brand as a whole.", 333, NS, 300, 13.3, 0), ("bd13", "derived from the initials of the brand name, designed", 327, NS, 300, 13.3, 0),
 ("tvp", "We avoid generic wellness terms like “freshness” or", 282, NS, 300, 13.3, 0), ("tvp", "We communicate with clarity and", 188, NS, 300, 13.3, 0),
 ("tvh", "1. Clear & Grounded", 223, NS, 300, 26.7, 0), ("tvh", "5. Beyond Wellness Language", 329, NS, 300, 26.7, 0),
 ("ixh", "Typography", 229, NS, 400, 40, 0), ("ixh", "Brand Colours", 273, NS, 400, 40, 0), ("ixh", "Graphic Assets", 280, NS, 400, 40, 0),
 ("msg", "Air, Elevated", 249 - 0, NS, 300, 40, 0),
 ("ibh", "LOGO MINIMUM SIZING", 144, NS, 400, 13.3, 0), ("ibh", "MONOGRAM MINIMUM SIZING", 187, NS, 400, 13.3, 0),
 ("ibp", "This version is intended for extremely small sizes. The", 265, NS, 300, 10.7, 0),
 ("ibs", ".25\" OR 16PX", 77, NS, 300, 13.3, 0),
 ("pill", "SECTION ONE", 129, NS, 300, 20.1, 0),
 ("dvt", "About", 325, LIT, 300, 126.3, 0),
 ("dvp", "The About section deﬁnes the foundation of Quint Home — its vision, mission, values, and brand voice. It", 642, NS, 300, 13.3, 0),
 ("cover", "Quint Home Brand Guidelines", 535, LIT, 300, 43.2, 0),
 ("sub", "Primary Typeface", 189, NS, 300, 25.4, 0), ("sub", "Secondary Typeface", 213, NS, 300, 25.4, 0),
 ("spf", "Literata Font Family", 288, LIT, 400, 30.3, 0), ("spfi", "Inter Font Family", 237, INT, 400, 30.3, 0),
 ("spg", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", 245, LIT, 400, 13.3, 0), ("spgli", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", 220, LIT, 300, 13.3, 1),
 ("spgsb", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", 251, LIT, 650, 13.3, 0), ("spgbi", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", 247, LIT, 730, 13.3, 1),
 ("spgi", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", 236, INT, 400, 13.3, 0),
 ("sw1", "Stardust Veil", 224, LIT, 300, 45.6, 1), ("sw2", "Aerial Mist", 136, LIT, 300, 31.4, 1), ("sw2", "Verdant Void", 158, LIT, 300, 31.4, 1),
 ("swi", "#EEE4D8", 64, INT, 300, 14.7, 0), ("swi", "238, 228, 216", 93, INT, 300, 14.7, 0),
 ("pl", "10% HIGHLIGHT COLOR", 194, NS, 300, 18.5, 0),
 ("thank", "Thank You", 120, NS, 300, 26.7, 0),
 ("air", "AIR ELEVATED", 110, INT, 400, 16, 0),
 ("pairL", "Literata - Heading", 283, LIT, 400, 33.3, 0), ("pairH", "Thoughtfully designed", 521, LIT, 400, 49.3, 0), ("pairI", "Inter - Body Copy", 279, INT, 400, 33.3, 0),
 ("wlh", "QUINT HOME FAVICON", 137, NS, 400, 13.3, 0), ("wlp", "Our favicon, a 32px × 32px icon that is displayed in the", 268, NS, 300, 10.7, 0),
 ("smp", "For use in markets where the trademark is ﬁled but not", 271, NS, 300, 10.7, 0),
 ("lic", "Brand Colours", 345, NS, 300, 55.1, 0),
 ("xh", "x height", 59, NS, 300, 15.9, 0),
]
async def main():
    fonts = open("fonts.css").read()
    spans = "".join(f'<span id="s{i}" style="font-family:{f};font-weight:{w};font-size:{s}px;font-style:{"italic" if it else "normal"};white-space:pre;'
                    f'font-variation-settings:\'opsz\' {14 if f == INT else 42}">{t}</span><br>' for i, (k, t, q, f, w, s, it) in enumerate(R))
    html = f"<html><head><style>{fonts}</style></head><body>{spans}</body></html>"
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); await pg.set_content(html); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
        out = {}
        for i, (k, t, q, f, w, s, it) in enumerate(R):
            mw = await pg.evaluate(f"document.getElementById('s{i}').getBoundingClientRect().width")
            n = max(1, len(t) - 1)
            em = (q - mw) / n / s
            out.setdefault(k, []).append(em)
            print(f"{k:6} {t[:34]:36} quint={q:4} mine={mw:7.1f}  ratio={q/mw:.3f}  tracking={em*1000:+6.1f}/1000em")
        await b.close()
    print({k: round(sum(v) / len(v) * 1000, 1) for k, v in out.items()})
asyncio.run(main())
