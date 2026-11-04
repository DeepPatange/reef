# Al Reef & Laurel — Website wireframes, Round 1 — build spec

Branded mid-fidelity wireframes (real type, colour, copy; photography as labelled placeholders), desktop 1440 + mobile 390,
built as static HTML and imported into Figma with Figma's html_to_figma converter. Layout and motion reference: lulaoil.com.
Source documents: Brand Guidelines Ed.01 and Brand Strategy Ed.01 (Al Reef & Laurel, Oct 2026).

Working folder: `WIRE = /private/tmp/claude-501/-Users-deeppatange-Desktop-Reef/9b7e4461-4d52-4d5b-9091-a21d118515ba/scratchpad/wire`
- `system.css` — tokens + component classes (read it fully before writing).
- `build.py` — expands `{{macro|args}}` shorthands and inlines CSS/fonts. Read its docstring + functions.
- `shoot.py` — screenshots each frame in slices into `shots/` and prints overflow/clipping checks.
- `pages/00-foundations.html` — finished reference: shows every component in use (copy markup patterns from it).
- `pages/01-home.html` — the homepage (being written in parallel by the lead; may not exist yet).
- Reference screenshots of lulaoil.com: `../lula/desk/s00b.png … s13b.png` (desktop), `../lula/mob/*.png`.

Build + check loop (run from WIRE):
```
python3 build.py pages/NN-name.html && python3 shoot.py dist/NN-name.html
```
Then LOOK at every slice image in `shots/` (Read tool). Desktop slices are 0.5x, mobile 1x, notes 0.75x.
Fix: overflow reported by the checker, text collisions, clipped text, empty gaps, misalignment, anything ugly. Repeat until clean.
Intentionally overflowing carousels: wrap the track in an element with `data-bleed="1"` (the checker skips it; the frame clips it).

HARD RULES
- Do NOT call any Figma tool. The lead sends pages to Figma.
- Static HTML only: no JS, no CSS animation, no external URLs/images/fonts. Only `../system.css` link (build inlines it),
  macros, classes from system.css, a page-level `<style>` block if needed, and inline styles. Px units.
- No `position:sticky/fixed`. Draw sticky bars/drawers in place and annotate them.
- Every page file = `<body class="board">` containing, in order:
  1. `<section class="frame desktop" data-name="NN Page — Desktop 1440">` starting `{{announce}}{{header|active}}`, ending `{{footer}}`
  2. `<section class="frame mobile" data-name="NN Page — Mobile 390">` starting `{{mann}}{{mheader}}`, ending `{{mfooter}}`
  3. optional extra state frames (desktop or mobile class), each with a clear data-name
  4. `<section class="frame notes" data-name="NN Page — Notes">` (template below)
  Frames are height:auto (content-driven) except overlay/state frames which use a fixed viewport height (900 desktop / 844 mobile).
- Max 20 frames per file.

BRAND RULES (from the guidelines — follow strictly)
- Colours: Silt #B5583B = action only (primary buttons) + at most one other accent per screen. Ecru page bg. Basalt text, dark
  sections and SELECTED states (chips/options). Kraft for spec rail on dark. Clay #7E3A26 for small Silt-family text
  (renewal prices, links, badges). Dune placeholders/quiet bands. Steam raised cards/inputs. Smoke secondary text. NEVER green.
- Type: Cormorant Garamond for display/headings/product names, never below 28 px (except the logo). IBM Plex Sans for
  everything else. Aref Ruqaa: one meaningful Arabic word per page, never a translation. Headlines sentence case, never all caps
  (caps only for wordmark + spec rail). Italic (`<em>`) for one emphasised phrase in display lines.
- Classes: `t-display` (72/76), `t-display-m` (44/48 mobile), `t-heading` (light italic 40/48), `t-heading-m`, `t-title` (40/44),
  `t-title-m` (32/36), `t-card` (28/32), `t-body` (18/28), `t-body-s` (16/26), `t-ui` (15/22), `t-cap` (13/20), `t-spec`/`t-spec-s`
  (caps tracked rail), `t-ar` (Ruqaa).
- Eyebrow pattern: `<div class="rail"><span class="rule"></span><span class="t-spec">Text</span></div>` (on dark: `rule-k` + `c-kraft`).
- Buttons: ONE `btn-primary` per screen-height region (~900 px desktop / ~800 px mobile). Others: `btn-secondary`, `btn-dark`,
  `btn-ecru`, `btn-ghost-ecru`, `btn-s`, `tlink`. Pill shapes. Sentence case labels. Prices in labels: "Add to bag · AED 68".
- Selected chip/option = Basalt (`chip on`, `opt on`). Badges: max one per card (`badge`, `badge-clay`, `badge-dune`).
- The Window = centred 3:4 oval (`{{win|W|H|label}}`), used for hero + product imagery. Editorial images = rectangles radius 12–16
  (`{{ph|W|H|label||16}}`). Product cut-outs = circles (`{{circ|D}}`). Label images "IMG 03 · Gourds on a Damanhour trellis"
  using the brand stock list (01 Lathered loofah in hand · 02 Wringing a wet loofah · 03 Gourds on a Damanhour trellis · 04
  Seal-stamped Sabon Ghar on travertine · 05 Loofah discs on a dark field · 06 Unboxing flat-lay · 07 Seal macro on soap · 08 Linen
  tote against stone · 09 Website on laptop · 10 Three story phones · 11 Dark editorial print pages · 12 Hammam steam interior);
  other images: "IMG · short description". People: hands, never faces.
- Voice: English first, British spelling, no exclamation marks, numerals for numbers, specific (numbers and places), one light
  twist per piece, generous (teach the why), unhurried (no urgency tricks, no countdowns, no "hurry", no "only 3 left").
  Never: "ethically sourced", "exotic", "revolutionary", "loofah lovers". Prices "AED 85". Use · (middle dot) as separator.
- Pattern (`{{pattern|...}}`) only as section breaks/bands, never behind text.

LAYOUT
- Desktop: 40 px side margins, 1360 content, 12 cols (col = 91.3, gutter 24). Spans: 3 cols 322 · 4 cols 435 · 6 cols 668 ·
  8 cols 891. Section padding `.sec` 144/40 (use 96–120 for tighter bands). Mobile: `.sec-m` 88/20, content 350.
- Cards: product card image 4:5 on Dune with circle cut-outs (variant `steam`) overlapping; name `t-card`; price `w5 num`;
  strike value `t-ui strike num`; renewal line `t-ui c-clay w5`.
- Rhythm: alternate Ecru / Steam / Dune bands sparingly; max one or two Basalt sections per page.
- Header/footer/announcement only via macros. Active nav keys: rituals build little gifts farm account none.

ANNOTATION
- Motion/interaction markers: `{{mk|M06|top|left}}` absolutely positioned inside the nearest `position:relative` ancestor
  (`.sec`, `.sec-m`, `.frame`, `.rel` are relative). Put it at the top-left of the element it describes. Use the M-codes:
  M01 hero momentum · M02 Window opens on load · M03 header hide/show · M04 word reveal · M05 scrubbed specimen video ·
  M06 sticky media + active list · M07 drag carousel with momentum · M08 slow marquee (pauses on hover) · M09 line draw ·
  M10 the Fade (tag ink fades + day count, scroll-linked) · M11 parallax bleed · M12 count-up numbers · M13 price/option change ·
  M14 add to bag → drawer · M15 hover (links, cards, quick add) · M16 pinned horizontal timeline · M17 accordion ·
  M18 drawers and sheets · M19 filter reflow · M20 tag sway.
  Default (no marker needed): sections fade up 24 px on enter, 600 ms.
- Flags for open questions: `{{flag|text}}` inline, sparingly in the UI; most go in Notes.
- Notes frame template (white frame, 600 wide):
```
<section class="frame notes" data-name="NN Page — Notes">
  <div class="n-kick">NN · Page · /url</div>
  <div class="n-title">Page name</div>
  <p class="n-lead">Purpose. Who lands here and from where. The one primary action.</p>
  <div class="n-block"><div class="n-h">Sections, top to bottom</div><div class="n-list">
    <div class="n-item"><span class="n-num">01</span><span><b>Name</b> — what it does and why.</span></div> …</div></div>
  <div class="n-block"><div class="n-h">Motion and interaction</div><div class="n-list">
    <div class="n-item"><span class="n-chip">M06</span><span><b>Name</b> — behaviour, timing.<span class="n-ref">Lula: hover-image-v2.js</span></span></div> …</div></div>
  <div class="n-block"><div class="n-h">Mobile</div><div class="n-list">…</div></div>
  <div class="n-block"><div class="n-h">Content and data</div><div class="n-list">…</div></div>
  <div class="n-block"><div class="n-h">Open questions</div><div class="n-list">
    <div class="n-item"><span class="n-flag">Check</span><span>…</span></div> …</div></div>
</section>
```

PRODUCT + PRICE DATA (Brand Strategy; all prices estimates until landed cost)
Loofahs (each carries a fading cotton tag + batch QR):
- The Daily Pad — GRADE A · 58 / CM² — Oval pad, cotton back, hand strap. Gentle or Deep fibre. — AED 44
- The Hammam Mitt — GRADE A · 60 / CM² — Worn like a glove. For the weekly deep scrub. — AED 48
- The Back Strap — PREMIUM A · 65 / CM² — 75 cm band, woven handles. Reaches every part of the back. — AED 65
Soaps (Sabon Ghar):
- Laurel 16 — 150 G · 16% LAUREL — for daily use, normal and sensitive skin — AED 45
- Laurel 30 — 150 G · 30% LAUREL — stronger bar for oily and acne-prone skin — AED 55
- Guest Bar — 40 G · 16% LAUREL — hotels, spas, sampling and gift fillers — AED 15
Little Reef (kids; softer fibre, unscented olive soap, tag where a small camel walks away by day 60; "paediatric dermatology
test" + "no small parts under 3" are planned, not done):
- Cloud Sponge — AGE 0–3 — Natural wool sea sponge. No loofah under 3. — AED 55
- Soft Pebble — AGE 3–10 — 9 cm pad: fine loofah one side, terry the other. — AED 29
- Camel Mitt — AGE 3–10 — Terry mitt, soft loofah palm, embroidered face. — AED 35
- Shaped Trio — 3 × 60 G · UNSCENTED — Camel, date palm, little gourd. No laurel. — AED 39
- Gourd on a Rope — AGE 3+ — A soap that can't slip away. — AED 25
Bundles (value · price · renewal every 60 days · for):
- The Duo (hero) — Daily Pad + Laurel 16 — 89 · 85 · 68 · self-carer
- The Pair — 2 Daily Pads (Silt + Basalt tags), Back Strap, Laurel 16 + 30, soap rest — 278 · 199 · 149 · couples, weddings
- The House — 2 Daily Pads, Back Strap, Soft Pebble, Camel Mitt, 2 × Laurel 16, Laurel 30, Shaped Trio — 401 · 299 · 219 · families of 4
- Little Reef Starter — Soft Pebble, Camel Mitt, Shaped Trio, Gourd on a Rope — 128 · 99 · 69 · kids 3–10
- First Bath — Cloud Sponge, Shaped Trio, linen hooded towel — 140 · 119 · no renewal · baby gifts
- The Grooming Kit — Back Strap, Daily Pad (Deep), Laurel 30 — 164 · 129 · 99 · grooming man
- The Hammam Chest — Mitt, Back Strap, Laurel 16 + 30, rosewater, brass-stamped basalt chest — from AED 350 (350–550) · no renewal · luxury gifting
Savings vs singles: Duo 5% · Pair 28% · House 25% · Grooming Kit 21% · Little Reef Starter 23%.
Ways to buy: One-time (full price; day-50 reminder offers renewal) · Renew as you go (RECOMMENDED; pay per delivery; every 30,
60 or 90 days; skip, swap soaps, pause or cancel any time before the next ship date; Duo AED 68, Pair AED 149) · The Year of
Rituals (prepay 6 deliveries for 12 months; brass soap rest in first box; works as a gift; Duo AED 349 a year vs 408; Pair AED
769 a year; non-refundable after first box ships).
Renewal timeline: Day 0 full set (loofah, soap, box that becomes a caddy, ritual card) · Day 50 WhatsApp "Your tag is fading.
A fresh one ships Tuesday." (skip, swap or keep) · Day 60 refill: fresh loofah and soap only · Day 120, 180–300 more refills ·
Day 360 renew the year or move to pay-as-you-go.
Founding offer: 25% off the first Duo, for the launch list only. Never a sitewide sale.
Corporate gifting: from 50 sets, custom ritual card. Ounass carries The Hammam Chest and The Pair only.
Origin: Field 7, Damanhour, Nile Delta, Egypt · 31.03° N 30.47° E · harvest Sept 2026 · sun-dried 21 days · never bleached ·
Luffa aegyptiaca: dense fibre, 8–12 weeks of life (claim to verify), dries fast. Box: unbleached FSC kraft printed in Basalt,
die-cut oval window. Finish: twine, no plastic, no lamination. Everything composts or becomes the caddy.
Audiences: The Considered Self-Carer (primary; women 25–40, UAE + Saudi urban professionals; "Your loofah tells you when it's
time.") · The Gifter (Ramadan, Eid, weddings, corporate; "A Levantine ritual, beautifully given.") · The Family (parents 28–45,
kids 0–10; "One ritual, everyone's own loofah.") · The Grooming Man (men 22–45, gym, strong in KSA; "Reach every part of your back.")
Content pillars (Field notes): Field Notes 30% (farm by season) · Two-Minute Hammam 25% (how-tos, one body area) · Specimen 15%
(one backlit slice, its grade and field) · Best Before 15% (Renewal Day: faded tags, fresh deliveries) · Ask the Delta 15%
(founders answer one real question a week) + a monthly Little Reef bath-time episode.
Taglines: "Grown, not made." · "The hammam, every morning." · "When the tag fades, so should your loofah."
Ritual (4 steps): 01 Wet. Soak the loofah under warm water for 30 seconds; it softens as it drinks. · 02 Lather. Work the
Sabon Ghar into the fibre, not onto your skin. · 03 Circle. Small circles for two minutes, one area at a time; lighter where
skin is thin. · 04 Hang to dry. Hang it by the cotton tag, out of the spray. Dry fibre lasts longer.
Launch: UAE late Jan 2027 (Ramadan expected ~8 Feb 2027, Eid ~10 Mar), KSA Apr–Jun 2027 (SFDA, Snapchat, COD + BNPL), Ounass +
hotels/spas Jul–Sep 2027, GCC retail from Oct 2027. Shopify + Recharge or Skio for renewal + WhatsApp via Bitespeed.
Known flags to carry into Notes where relevant: "Bestseller" badge is untrue at launch → use "Founders' pick"; 90-day cycle
contradicts "when the tag fades (day 60)"; First Bath (baby gift) includes Shaped Trio (age 3+); guidelines banner says "Gift
sets from AED 185" but no set costs 185; founder story still a placeholder; all photography must be a real shoot (current
renders look AI-generated); delivery promises and lead times are unconfirmed; claims (8–12 weeks life, dermatology test,
compostable) need the regulatory adviser.

================================================================================================================
PAGE SPECS
(Desktop section list; mobile = same order, stacked, adapted as noted. Copy below is final-ish wireframe copy: use it.)
================================================================================================================

01 HOME  /  (lead builds this)
Hero (headline left, Window right, hanging tag) → manifesto word reveal → The Duo buy module (Lula's embedded buy box) →
Three proofs (Rooted · Renewed · Returned) → Specimen (scroll-scrubbed slice + 6 callouts, Basalt) → Comparison (loofah vs pouf
vs mitt) → The two-minute scrub (sticky image + 4 steps) → From the field (the one full-bleed image) → Renewal (the Fade +
timeline + 3 ways to buy) → Rituals carousel → Gifting split panel (marquee) → Notes from the first showers (reviews carousel)
→ Field notes (4 cards) → footer.

02 RITUALS  /collections/rituals  (agent A)
Purpose: browse all 7 sets, open one or quick-add. Primary action: open a set.
1. {{announce}} {{header|rituals}}
2. Collection header (padding ~96 top / 48 bottom): left — rail "7 sets · renew every 60 days", t-display "Rituals",
   t-body (≤560 wide) "Every set renews every 60 days, so nobody in the house keeps a loofah too long. Pick the one that fits
   your bathroom, or build your own." Right — Window ~220×293 (IMG 06 · Unboxing flat-lay) with Ruqaa طقس (Silt, ~64 px) beside it.
3. Filter row: label t-spec "Who's it for?", chips: All (on) · Just me · Two of us · The whole house · Kids · A gift · Grooming.
   Right side: toggle + t-ui "Show renewal prices", sort "Recommended" + chevron. Hairline below. Marker M19 on chips, M13 on toggle.
4. Grid 4 × 2 (cards 322 wide, image 322×402 Dune radius 12, 2 overlapping steam circles ~150, badge top-left, small image
   label bottom-left). Cards: The Duo (badge "Founders' pick") · The Pair · The House (badge-clay "Save 25%") · The Grooming Kit ·
   Little Reef Starter (badge-dune "Ages 3–10") · First Bath (badge "For new parents") · The Hammam Chest (badge "Gift") · 8th tile:
   Basalt "Build your own" tile (fibre icon Ecru, t-card Ecru "Build your own", t-ui "Pick a fibre, a soap and a cycle. The saving
   updates as you go.", btn-ghost-ecru btn-s "Build yours"). Each card: name, one-line contents (t-ui smoke), price + strike value,
   renewal line ("AED 68 on renewal" Clay; gifts "Gift set · no renewal"). Show The Pair in hover state: image zoom hint + a
   btn-dark btn-s "Quick add · AED 199" sitting at the image bottom; marker M15.
5. How renewal works band (bg-dune, padding ~96): 3 columns with 48 px brand icons (box, tag, renew): "01 Choose a set — Every set
   arrives complete: loofahs, soaps and a box that becomes a caddy." "02 Watch the tag — A cotton tag fades by day 60. We WhatsApp
   you on day 50." "03 The refill arrives — Fresh loofahs and soap only. Skip, swap or pause any time." + tlink "How renewal works".
6. Compare the sets: t-title "Compare the sets" + table: columns The Duo · The Pair · The House · The Grooming Kit · Little Reef
   Starter (header: circle 72 + t-card name). Rows (label t-spec-s smoke): For · Loofahs · Soaps · One-time · On renewal · Saving
   (values from data). Last row: btn-secondary btn-s "View" per column. Use hairlines, Steam header row.
7. FAQ two-column: left t-title "Questions, answered" + t-body-s "Still unsure? WhatsApp the founders." + tlink with whatsapp icon;
   right accordions (first open with answer): Can I mix fibres and soaps in a set? / What ships on renewal? / Can I skip or pause?
   / Do you deliver outside the UAE? (Saudi Arabia from April 2027, then the rest of the GCC.) / Is everything plastic-free?
   Marker M17.
8. {{footer}}
Mobile: header; collection header stacked (title + small Window 120×160 right); chips horizontal scroll (data-bleed) + a row
"Filter and sort" button + renewal toggle; grid 2 columns (cards 169 wide, image 169×211, circles ~78, names t-card 28 can wrap);
Build-your-own tile full width; renewal band stacked; compare table as horizontal scroll (data-bleed) with t-cap "Swipe to
compare"; FAQ accordions; footer. Extra frame "02 Rituals — Mobile 390 · Filter sheet" (390×844): dimmed page + bottom sheet:
grab bar, t-title-m "Filter and sort", Who's it for chips (wrap), Sort by options (opt rows), toggle "Show renewal prices",
btn-primary block "Show 7 sets", tlink "Clear all". Marker M18.
Notes flags: Founders' pick vs Bestseller; First Bath + Shaped Trio age; Hammam Chest final price; compare table savings are
estimates.

03 THE DUO (product page)  /products/the-duo  (agent A)
Purpose: convert, with renewal preselected. Primary action: Add to bag · AED 68.
1. {{announce}} {{header|rituals}}; breadcrumb row t-cap smoke "Rituals / The Duo" (padding 24 40).
2. Main: LEFT gallery 800 wide — main stage 800×960 Steam radius 16 with Window 480×640 (IMG · The Duo on travertine) centred,
   counter pill "1 / 6" bottom-left, two arrowbtn bottom-right; below, 2 × 2 grid of 388×485 radius 16: IMG 01 Lathered loofah in
   hand · IMG 06 Unboxing flat-lay (box becomes a caddy) · IMG 05 Loofah discs on a dark field (dark) · Video "The two-minute
   scrub" (dark, play icon in an Ecru circle, label "VIDEO · 0:45"). RIGHT buy box 520 wide (x 880→1400), annotated "sticks while
   the gallery scrolls": rail "Hero ritual · Daily Pad + Laurel 16" · t-display "The Duo" · t-heading "The hammam, every morning." ·
   price row (t-title "AED 68" + t-ui smoke "per delivery"; right t-ui "or AED 85 one-time") · t-body "A Daily Pad sun-dried for 21
   days in Damanhour and a bar of Laurel 16 Sabon Ghar, made to work together. The cotton tag fades by day 60; a fresh pair
   arrives as it does." · spec rail "Grade A · 58 / cm² · 16% laurel · 150 g" · purchase options: opt on "Renew every 60 days"
   + badge-clay "Save 20%" + helper "Skip, swap or pause any time. WhatsApp reminder on day 50." AED 68; opt "One-time purchase"
   AED 85; opt "The Year of Rituals · 6 deliveries" helper "Prepaid, with a brass soap rest in the first box. Works as a gift."
   AED 349 / year + strike 408 · "How often" chips: Every 30 days / Every 60 days · matches the tag (on) / Every 90 days · Fibre
   (label + info icon): Gentle (on) / Deep + t-cap "Gentle: softer, for daily use and sensitive skin." · Soap: Laurel 16 (on) /
   Laurel 30 + t-cap "Laurel 16: normal and sensitive skin." · row: stepper + btn-primary (flex 1) "Add to bag · AED 68" · ticks
   row: Traced to its farm · Tag fades at day 60 · Box becomes a caddy · truck icon + t-ui "Free UAE delivery on the Duo · ships
   within 2 working days" (flag confirm) · {{pay|light}} · whatsapp icon + tlink "Questions? WhatsApp the founders" · accordions:
   Spec sheet / How to use / Delivery and returns / Ingredients. Markers: M13 (options), M14 (add to bag), M07 (gallery swipe on
   mobile / arrows).
3. Traced to Field 7 (bg-dune): left map placeholder 640×480 radius 16 "MAP · Nile Delta line drawing, Field 7 pinned" with an
   origin icon (M09 draws the coast + route); right: rail "Traced to Field 7", t-display "Know exactly <em>where it grew.</em>",
   t-body "Every tag carries a QR code. Scan it to see your loofah's field, harvest month, drying dates and grade.", receipt card
   (bg-steam radius 16 padding 28, `.kv` rows): Batch F7-0926 · Field 7, Damanhour, Nile Delta · 31.03° N, 30.47° E · Harvest
   September 2026 · Sun-dried 21 days · Grade A · 58 / cm² ; tlink "See a sample batch page".
4. What's in the box: t-title + 5 columns: circ 180 + t-card + t-ui: The Daily Pad (oval pad, cotton back, hand strap) · Laurel 16
   (150 g Sabon Ghar, 16% laurel oil) · Kraft box (folds into a shower caddy) · Fading tag (cotton, fades by day 60) · Ritual card
   (the two-minute scrub, step by step).
5. Spec sheet two-column: left t-title "Spec sheet" + t-body-s "Everything we know about this loofah, and how we know it." + tlink
   "Download the PDF"; right `.kv` rows: Species Luffa aegyptiaca · Origin Field 7, Damanhour, Nile Delta, Egypt · Drying 21 days in
   the sun, never bleached · Grade A · 58 fibres per cm² · Size Oval pad, about 14 × 10 cm, cotton back, hand strap (flag confirm) ·
   Soap Laurel 16 · olive oil with 16% laurel oil · 150 g · Renewal Every 60 days, when the tag fades · Afterlife The loofah
   composts; the box becomes a caddy.
6. The two-minute scrub: t-display "The two-minute <em>scrub.</em>" + 4 columns (number t-spec, Window 260×347, t-card "Wet." etc.,
   t-ui body) using the ritual copy.
7. Choose your fibre and soap: 2 × 2 cards (bg-steam, ph 120×120 circle + t-card + t-ui): Gentle · Deep · Laurel 16 · Laurel 30.
8. Renewal (bg-basalt): rail kraft "How renewal works", t-display ecru "When the tag fades, <em>so should your loofah.</em>", left
   {{tag}} at day 41 (M10), right horizontal timeline (Silt dots + hairline): Day 0 · Day 50 · Day 60 · Every 60 days with copy from
   data, + t-ui ecru70 "Manage it all on WhatsApp or in your account: skip, swap, pause or cancel."
9. Reviews (designed future state, flagged "Sample content · hidden until 20+ verified reviews"): left summary (t-display "4.9",
   stars, "from 128 reviews" sample, 5 distribution bars); right 3 review cards (name initial, "Founding member" badge, stars, title,
   text, "Daily Pad · Gentle · Day 30").
10. FAQ two-column: Is it really a vegetable? (open: "Yes. Luffa aegyptiaca is a gourd. We grow it, dry it and cut it. Please don't
    cook it.") / How long does one loofah last? / What if my tag fades early? / How do I keep it fresh? / Can I skip or cancel
    renewal? / Do you ship to Saudi Arabia?
11. Pairs well with: t-title + 4 small cards (circ image, t-card, price, btn-secondary btn-s "Add"): The Back Strap AED 65 · The
    Hammam Mitt AED 48 · Laurel 30 AED 55 · Guest Bar AED 15.
12. Sticky add-to-bag bar: draw a 1440×88 Steam bar with shadow, positioned over the top of section 9 (absolute), containing circle
    thumb, "The Duo · Renew every 60 days", price, btn-primary "Add to bag · AED 68"; marker + t-cap note "Appears once the buy
    box scrolls out".
13. {{footer}}
Mobile: gallery swipe (full-width 390×488 Steam with Window 300×400, dots, "1 / 6"), info + options stacked, sticky bottom bar
(draw at the end of the first ~844 px region: Steam bar with price + btn-primary), then sections stacked; what's in the box as
horizontal scroll; spec sheet as kv list; ritual steps as 2 × 2 or swipe; footer.

04 BUILD YOUR RITUAL  /pages/build  (agent B)
Purpose: make a custom bundle; saving updates live. Primary action: Add ritual to bag.
1. {{announce}} {{header|build}}
2. Intro (padding ~96/48): rail "Build yours", t-display "Build your <em>ritual.</em>", t-body "Tap a fibre, a soap and a cycle.
   The saving updates as you go." Right: step indicator pills (step-n + label): 1 Who it's for (done) · 2 Loofahs (on) · 3 Soaps
   · 4 How often.
3. Two columns: LEFT (8 cols, 891) steps; RIGHT (4 cols, 435) summary card "sticky" (annotate).
   Step 1 "Who's it for?": 4 choice cards 4 × ~204 (icon, t-card, t-cap): Just me · Two of us (selected, Basalt 1.5 border + check)
   · The whole house · A gift.
   Step 2 "Choose your loofahs": 2-column grid of item cards (bg-steam radius 12 padding 20): circ 88, t-card name, t-spec-s spec,
   t-cap description, price, stepper-s. Items: Daily Pad · Gentle (1) · Daily Pad · Deep (1) · The Hammam Mitt (0) · The Back
   Strap (1) · Soft Pebble (0, badge-dune Ages 3–10) · Camel Mitt (0, Ages 3–10). Below the pads: "Tag colour" chips Silt (on) ·
   Basalt · Kraft + t-cap "So nobody borrows the wrong one."
   Step 3 "Choose your soaps": Laurel 16 (1) · Laurel 30 (1) · Shaped Trio (0) · Guest Bar (0).
   Step 4 "How often?": chips Every 30 days · Every 60 days · matches the tag (on) · Every 90 days · Just once.
   SUMMARY card (bg-steam radius 16 padding 32, shadow-s): t-title "Your ritual"; item rows (name ×qty, price): Daily Pad · Gentle
   ×1 AED 44 · Daily Pad · Deep ×1 AED 44 · The Back Strap ×1 AED 65 · Laurel 16 ×1 AED 45 · Laurel 30 ×1 AED 55; hairline;
   Value AED 253; Bundle saving −AED 58 (23%) in Clay; Today AED 195 (t-title); "Then AED 156 every 60 days" (t-ui); saving tiers
   bar (bar with 4 tick labels: 2 items 5% · 4 items 15% · 5 items 23% · 7 items 28%, filled to 5) + t-cap "Add 2 more items to
   save 28%."; btn-primary block "Add ritual to bag · AED 195"; t-cap "Skip, swap or pause any time. Cancel before any ship date."
   Markers M13 (totals roll), M18? no. Flag: tier logic illustrative, confirm against landed cost and the 70% margin floor.
4. Or start from a set: t-title + 4 compact cards (The Duo, The Pair, The House, The Grooming Kit) with btn-secondary btn-s "Load
   this set".
5. {{footer}}
Mobile: steps stacked, item cards full width rows; a sticky bottom summary bar (Steam, shadow) "5 items · AED 195 · save 23%" +
btn-dark btn-s "Review" drawn after step 2. Extra frame "04 Build — Mobile 390 · Summary sheet" (390×844): dimmed page + bottom
sheet with the full summary + btn-primary block. Marker M18.

05 LITTLE REEF  /collections/little-reef  (agent C)
Purpose: kids range + sets for parents. Primary action: Shop the Starter.
1. {{announce}} {{header|little}}
2. Hero: left — t-ar صغير (~80 px), rail "Little Reef · ages 0–10", t-display "Little Reef, <em>for skin that's new at this.</em>",
   t-body "The same honest materials, softer fibre, unscented olive soap, and a tag where a small camel walks away by day 60.",
   btn-primary "Shop the Starter · AED 99" + btn-secondary "Shop by age", spec rail "Unscented · No small parts under 3" + flag
   "Paediatric dermatology test planned, not done — don't claim yet". Right — Window 520×693 (IMG · Camel Mitt on a folded towel)
   with the kids tag ({{tag|130|20|0.3|kids}}) hanging at its edge (M20).
3. Shop by age: chips All ages (on) · 0–3 · 3–10 (M19); 5-column grid (cards 253 wide, image 253×316): Cloud Sponge · Soft Pebble ·
   Camel Mitt · Shaped Trio · Gourd on a Rope (badges = age; data from spec).
4. Sets (bg-dune): two wide cards (668 each, bg-steam radius 16): Little Reef Starter (AED 99 strike 128, "Renews at AED 69 every
   60 days", contents list, ages 3–10, btn-dark "Add to bag") · First Bath (AED 119 strike 140, "Gift set · for new parents",
   contents, flag "Shaped Trio is age 3+; swap it for the baby set?").
5. The camel tag: left — 3 kids tags at fade 0 / 0.5 / 1 with captions Day 1 · Day 30 · Day 60 (M10); right — t-display "A camel
   that <em>walks away.</em>", t-body "Little Reef tags print a small camel in fading ink. By day 60 it has wandered off, which is
   your cue for fresh ones. Children tend to notice before you do."
6. Bath time, two minutes: t-title + 3 step cards (Window 300×400, t-card, t-ui): "Splash." Warm water, not hot. / "Lather." Rub the
   soap on the terry side; no laurel, no scent. / "Rinse and hang." Hang it by the loop to dry. + a wide video placeholder (dark,
   play) "Monthly bath-time episode".
7. Our promises: 4 columns (icon 40, t-card, t-ui): No small parts under 3 · Unscented olive soap · Softer fibre · Tested with
   paediatric dermatologists (flag: planned).
8. Parents ask (FAQ two-column): From what age? (open: "Cloud Sponge from birth. Loofah from age 3, starting with the Soft Pebble.")
   / Is the soap suitable for eczema? ("Shaped Trio is unscented olive soap with no laurel. If your child has a skin condition, ask
   your paediatrician first.") / How do I clean the sponge? / Does Little Reef renew too? ("The Starter renews every 60 days at AED
   69. First Bath is a one-off gift.")
9. For the whole house: wide banner card (bg-steam) with The House (circles), "The House · AED 299 · renews at AED 219", btn-secondary.
10. {{footer}}
Mobile accordingly (grid 2 cols; sets stacked; camel tags in a row of 3 small).

06 GIFTS  /collections/gifts  (agent C)
Purpose: Ramadan/Eid/wedding/corporate gifting. Primary action: Shop gift sets.
1. {{announce|Ramadan gifts · choose your delivery date at checkout}} {{header|gifts}}
2. Hero (bg-basalt, ~720 tall): left — rail kraft "Ramadan · Eid · weddings · thank-yous", t-display ecru "Ramadan, <em>renewed.</em>",
   t-body ecru70 "Gift sets that arrive ready to give: tissue, twine and a ritual card in every box. Choose the delivery date; we
   keep prices off the packing slip.", btn-primary "Shop gift sets" + btn-ghost-ecru "Corporate gifting". Right — dark Window 480×640
   (IMG · The Hammam Chest on travertine) + t-spec kraft "The Hammam Chest · from AED 350".
3. Find the gift: t-title "Find the gift"; chip rows "For" (Her · Him · A couple · A family · A new baby · The team) and "Budget"
   (Under AED 150 · AED 150–300 · AED 300+). M19.
4. Gift grid 3 × 2 (cards 435, image 435×544): The Hammam Chest (badge "Ramadan") · The Pair · The Grooming Kit · First Bath · The
   Year of Rituals (AED 349 · "Six deliveries of the Duo, one card. The gift that renews.") · Gift card (AED 100–500 · "Sent by email
   or WhatsApp on the date you choose").
5. Every gift includes (bg-dune): 4 columns with UI icons (edit, gift, calendar, lock): Ritual card with your message · Tissue and
   twine, no plastic · Delivered on your date, anywhere in the UAE · Prices off the packing slip.
6. Inside the Hammam Chest: left dark ph 780×600 radius 16 (IMG · Chest open, contents laid out); right t-title + list rows (circ 64,
   name, note): Hammam Mitt · Back Strap · Laurel 16 · Laurel 30 · Rosewater · Basalt chest with brass stamp; "From AED 350"; btn-dark
   "Choose your chest"; t-cap "Also at Ounass."
7. Corporate gifting: left — rail "Corporate", t-display "Thank-yous, <em>by the fifty.</em>", t-body "From 50 sets. A ritual card
   printed with your logo and message, delivered to one address or many across the UAE.", 3 numbered steps (Choose sets · Add your
   card · We deliver), t-cap "Lead time about 3 weeks" (flag). Right — form card (bg-steam radius 16 padding 40): Name · Company ·
   Work email · WhatsApp number (field-sq), Number of sets chips (50–99 · 100–249 · 250+), Delivery date (field-sq + calendar
   icon), Message (textarea), btn-primary "Send enquiry".
8. FAQ: Can I add a gift message? / Can I choose the delivery date? / Will the price show? / Can I gift a renewal? / Delivery during
   Ramadan.
9. {{footer}}
Mobile accordingly. Notes flag: guidelines banner "Gift sets from AED 185" matches no set.

07 OUR FARM  /pages/our-farm  (agent D)
Purpose: origin story and proof. Primary action: Shop the Duo (end).
1. {{announce}} {{header|farm}}
2. Hero: centred rail "31.03° N · 30.47° E · Damanhour, Egypt", centred t-display "Field 7, <em>Damanhour.</em>", centred t-body
   (≤640) "Where our loofahs grow on trellises above the Nile Delta, and dry for 21 days in the sun." Below: panoramic ph 1360×640
   radius 16 (IMG 03 · Gourds on a Damanhour trellis) with M11 + flag "Real shoot needed".
3. Manifesto word reveal (M04): centred t-display "A vegetable from Damanhour, finished like a luxury object. We'd like you to know
   every step it takes." — render first ~60% of words Basalt, rest at 20% opacity (span style="opacity:.2").
4. Why we started (two columns): left ph 640×800 radius 16 (IMG · Founders' hands holding a dried gourd — hands, never faces); right
   rail "Why we started", t-title "Why we started", a dashed-border placeholder block containing t-body "[Founder story: add the
   founders' Egyptian roots here.]" + flag "Founder story to write", t-ar الريف (~64 px) with t-cap "Al Reef: the countryside".
5. From seed to shower (M16 pinned horizontal timeline): header row t-display "From seed <em>to shower.</em>" + right "03 / 08" + a
   progress line (Silt filled 3/8); track (data-bleed, overflowing right) of 8 cards 400 wide: ph 400×300 radius 12, t-spec, t-card,
   t-ui: 01 March–April · Planting — Seeds go into Delta soil as the days lengthen. / 02 May–August · The trellis — Vines climb;
   gourds hang and grow to arm's length. / 03 September · Harvest — Picked once the skin turns from green to brown and light. / 04
   21 days · Sun-drying — Dried in the open air on the farm. The colour is the sun's. / 05 Peel, seed, rinse — Skins come off by
   hand; seeds are saved for next spring. No bleach. / 06 Grade and cut — Every batch is graded for density: Grade A means 58 fibres
   per cm². / 07 The journey — Packed in kraft and twine, shipped from Egypt to Dubai (flag route). / 08 Your shower — Day 01 of 60.
   Hang it to dry.
6. Numbers (bg-basalt): 4 big numbers t-display ecru (M12): 21 days of sun · 58 fibres per cm² · 60 days per loofah · 0 plastic,
   labels t-spec kraft, hairline separators.
7. The hands behind Field 7: t-title + 3 ph 435×544 radius 12 (IMG · Hands harvesting / peeling / grading) + captions t-ui "Harvest ·
   [name], farm lead" with flag "names and consent".
8. And the soap? (bg-dune): left Window 480×640 (IMG 07 · Seal macro on soap — cut bar, green core, gold crust); right rail "From the
   Levant", t-display "And the <em>soap?</em>", t-body "Sabon Ghar: olive oil and laurel oil, cured slowly [x months] in [city]. Laurel
   16 for every day; Laurel 30 for oily skin." (flags), spec rail "Laurel 16 · 150 g · Laurel 30 · 150 g", tlink "Shop the soaps".
9. The route (M09 line draw): t-title "From Damanhour to your door"; a horizontal route diagram (SVG or divs): dots + line + labels:
   Field 7 · Damanhour → Alexandria · port → Jebel Ali · Dubai → Riyadh · from April 2027 (dashed for future), t-cap under each.
10. Field notes by season: t-title "Field notes" + tlink "All field notes" + 3 cards (ph 435×326, badge pillar, t-card title, t-ui):
    Field Notes · "Harvest week at Field 7" / Specimen · "What Grade A actually means" / Ask the Delta · "Why don't you bleach them?"
11. CTA band: centred t-display "Meet the vegetable <em>in person.</em>" + btn-primary "Shop the Duo · AED 85".
12. {{footer}}
Mobile accordingly (timeline = horizontal swipe; numbers 2 × 2).

08 BATCH PAGE (QR landing)  /batch/f7-0926  (agent D)  — MOBILE IS PRIMARY (people scan the tag with a phone)
Purpose: prove origin, teach the ritual, capture a WhatsApp reminder (turns one-time buyers and gift recipients into renewals).
Primary action: Remind me on day 50.
Mobile (put this frame FIRST in the file, then desktop): minimal header (no announcement): logo centred + "Shop" t-ui right +
menu left. 1. rail "Batch F7-0926", t-display-m "Your loofah <em>grew here.</em>", Window 350×467 (IMG 03 · Field 7, harvest week).
2. Receipt card (bg-steam radius 16, top edge dashed): `.kv` rows Field · Field 7, Damanhour / Coordinates · 31.03° N, 30.47° E /
Planted · March 2026 / Harvested · September 2026 / Sun-dried · 21 days, 8–29 Sept / Grade · A · 58 fibres per cm² / Graded by ·
[initials] / Packed · October 2026, Dubai / Soap · Laurel 16 · L16-0826 (flags: real batch data feed). 3. Day tracker: t-title-m
"Day 01 of 60", fade bar (2% fill), t-body-s "Hang it to dry after every shower. Dry fibre lasts longer." + 4 numbered mini steps.
4. Reminder card (bg-dune radius 16 padding 24): t-title-m "Want a nudge on day 50?", t-body-s "We'll send one WhatsApp when your tag
is nearly gone. Nothing else.", field-sq "+971  WhatsApp number", btn-primary block "Remind me on day 50", t-cap "Already renewing?
Your reminder is set. Manage it in your account." 5. When the tag fades: 3 steps with brand icons (compost, water?, box): Cut it
into pieces · Compost it or bury it · Keep the box: it folds into a caddy + ph 350×200 "DIAGRAM · box to caddy in 3 folds" (M09).
6. Gift card: bg-steam "Got this as a gift?" t-body-s "Start your own ritual with the Duo." btn-secondary "See the Duo". 7. Mini
footer (Basalt, compact: logo ecru, insta, WhatsApp, "alreefandlaurel.com").
Desktop: {{header|none}} then 2 columns (left Window + receipt; right tracker, reminder, afterlife) then {{footer}}.

09 YOUR RITUAL (account)  /account/rituals  (agent B)
Purpose: manage renewal without friction. Primary action: none forced; key actions Skip / Swap / Ship now.
1. {{announce}} {{header|account}}
2. Two columns: left nav (300): t-title "Hi, Noor", t-cap smoke "Founding member since February 2027", nav list (Your ritual active
   with Basalt left bar · Orders · Addresses · Payment methods · WhatsApp and email · Help · Log out). Right main (~1020):
   - rail "Your ritual" + t-display "Your <em>ritual.</em>"
   - Active ritual card (bg-steam radius 16 padding 40): circ 160 (IMG · The Pair), t-title "The Pair", t-spec "Every 60 days · AED
     149", fade bar 72% with "Day 43 of 60 · your tags are fading" / "Next refill · 29 Dec", action pills (btn-secondary btn-s, 5):
     Ship now · Skip next · Swap soaps · Change frequency · Pause (with UI icons), t-cap "Cancel any time before 24 Dec. We'll
     message you on WhatsApp on day 50." + tlink smoke "Cancel renewal"; right a {{tag|120|43|0.72}}. Markers M10, M13.
   - In your next refill: rows Daily Pad · Gentle (Silt tag) · Daily Pad · Deep (Basalt tag) · The Back Strap · Laurel 16 · Laurel
     30 → Refill price AED 149, tlink "Edit refill"; delivery "Villa 12, Al Barsha 2, Dubai" + payment "Visa ending 4242" + "Change".
   - Add to your next refill: 3 small cards Guest Bar AED 15 · The Hammam Mitt AED 48 · Soft Pebble AED 29 (btn-dark btn-s "Add")
     + t-cap "Ships free with your refill."
   - Coming up: 3 rows 29 Dec · 27 Feb · 28 Apr (Refill · AED 149 · toggle "Skip").
   - The Year of Rituals upsell (bg-basalt radius 16): rail kraft, t-title ecru "Prepay the year and <em>save 14%.</em>", t-ui ecru70
     "AED 769 for six refills of The Pair, plus a brass soap rest in the first box.", btn-ghost-ecru "Switch to the year".
   - Orders table: 31 Oct 2027 · Refill · AED 149 · Delivered / 1 Sep 2027 · Refill · AED 149 · Delivered / 4 Feb 2027 · The Pair
     · AED 199 · Delivered (Invoice links).
   - WhatsApp and email: toggles Day-50 reminder (on) · Shipping updates (on) · Letters from the Delta, monthly (off).
3. {{footer}}
Extra frames: "09 Account — Desktop · Swap soaps" (1440×900: dimmed page + centred dialog 560: t-title "Swap soaps", opt rows Laurel
16 + Laurel 30 (on, current) · 2 × Laurel 16 · 2 × Laurel 30, t-cap "Applies from the 29 Dec refill.", btn-primary "Save changes" +
tlink "Cancel"); "09 Account — Desktop · Cancel flow" (1440×900 dialog 640: t-title "Pause instead?", chips Pause 1 month · 2
months (on) · 3 months, opt rows "Change to every 90 days" / "Swap the Deep pad for Gentle", reasons list, btn-secondary "Pause for
2 months" + tlink "Cancel renewal" + t-cap "Cancelling stays one click away."); "09 Account — Mobile · Skip sheet" (390×844 bottom
sheet: "Skip the 29 Dec refill?" t-body-s "Your next one ships 27 Feb.", btn-primary block "Skip this refill", btn-secondary block
"Keep it").
Mobile main: nav as horizontal tabs (data-bleed), cards stacked, action pills 2 columns.

10 BAG, MENU AND MODALS  (agent E)
Frames (no announce/header needed inside overlays unless shown under a scrim):
1. "10 — Desktop · Mega menu" 1440×900: page beneath ({{announce}}{{header|rituals}} + a faded hero hint), panel under header (Ecru,
   shadow, padding 48 40): col 1 "Rituals" list (name + price rows: The Duo AED 85 · The Pair AED 199 · The House AED 299 · The
   Grooming Kit AED 129 · Little Reef Starter AED 99 · First Bath AED 119 · The Hammam Chest from AED 350) + tlink "Shop all rituals";
   col 2 "Loofahs" (Daily Pad · Hammam Mitt · Back Strap) + "Soaps" (Laurel 16 · Laurel 30 · Guest Bar); col 3 featured card
   (Window 200×267 + t-card "The Duo" + t-ui "The hammam, every morning." + tlink); col 4 Basalt "Build your own" tile. Scrim below
   the panel. Marker M18.
2. "10 — Desktop · Bag drawer" 1440×900: page under scrim; drawer right 480 wide full height (bg-steam): header "Your bag (2)" +
   close; "Free UAE delivery unlocked" + full bar; item 1 The Duo (circ 80, "Renew every 60 days · Gentle · Laurel 16", AED 68,
   stepper-s, "Remove"); item 2 Laurel 30 one-time AED 55 + Clay tlink "Add to your renewal instead and save AED 11"; "Add to your
   order" mini cards (Guest Bar AED 15 + Add · The Back Strap AED 65 + Add); gift row (toggle off) "This is a gift · add a ritual card
   message"; Subtotal AED 123 · Delivery Free; btn-primary block "Checkout · AED 123"; {{pay|light}}; t-cap "Renewal: AED 68 every 60
   days for the Duo. Skip, swap or cancel any time." Marker M14.
3. "10 — Desktop · Founding list" 1440×900: scrim + centred modal 880×560 (radius 20, Ecru, split): left silt Window panel; right
   rail "Founding members", t-title "25% off <em>your first Duo.</em>", t-body-s "Join the founding list for first access to the
   September harvest and 25% off your first Duo. One email when we launch, then once a month at most.", field email, field-sq
   WhatsApp (optional), btn-primary block "Join the list", tlink "No thanks", t-cap "No countdowns. No daily emails." Close icon.
4. "10 — Desktop · Search" 1440×640: header + large search field (t-title-size input text "back str|"), suggestions (Popular: The
   Duo · Back Strap · Gifts under AED 150 · Little Reef), 3 result cards (The Back Strap AED 65, The Grooming Kit AED 129, The Pair
   AED 199), tlink "See all 5 results".
5. "10 — Mobile · Menu" 390×844: Ecru full screen: top row close + logo + "Bag (0)"; big links t-title-m with chevrons (Rituals ·
   Build yours · Little Reef · Gifts · Our farm · Field notes); hairline; t-ui links (Account · Manage your renewal · Shipping and
   returns · WhatsApp us); bottom pattern band 8% + "UAE · AED" + insta icon. M18.
6. "10 — Mobile · Bag" 390×844: full-screen sheet version of the bag drawer, btn-primary at the bottom.
7. "10 — Mobile · Founding list sheet" 390×844: bottom sheet version, no timer.
8. "10 — Mobile · Day-50 WhatsApp" 390×844: a neutral chat screen (not WhatsApp branding): header "Al Reef & Laurel" with R&L avatar,
   verified-business style tick; message bubbles from the brand: "Your tag is fading. A fresh one ships Tuesday." then "The Pair ·
   refill · AED 149 · arrives Thu 31 Dec" then quick-reply pills "Ship it" · "Skip this one" · "Swap soaps"; a customer reply "Swap
   soaps" and brand response "Done: 2 × Laurel 16 this time. See you on day 60." Marker: this is the renewal touchpoint.
Notes frame: what each overlay is for, triggers (founding modal: once per visitor after 30 s or 50% scroll; never on checkout or on a
product page before add to bag; Esc and click-outside close), focus trapping, scrims, motion codes.
