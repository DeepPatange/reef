# Al Reef & Laurel — website prototype (Round 1)

Open `index.html` in Chrome or Safari. No server or install needed.

**Pages:** Home · Shop (filters, renewal-price toggle) · Product (`product.html?p=the-duo`, any product slug works) · Our farm · Field notes.

**Works for real:**
- add to bag and the bag drawer (saved in the browser)
- renewal and one-time pricing with animated price changes
- gallery with swipe and zoom
- sticky add-to-bag bar
- shop filters
- mobile menu

Checkout is not part of the prototype.

**System:**
- Brand Guidelines V2 (Quint-style). Literata for headings and Inter for text, at the same instances as the guide. The AL REEF wordmark is Quattrocento.
- Colours: Delta Linen, Laurel Mist, Deep Laurel, Nile Clay, Delta Earth.
- Kas di Kos is the reference for structure and feel:
  - a centred wordmark with spaced-out caps nav
  - crossfading full-bleed hero slides
  - a three-column values row
  - hairline-framed product cards
  - image and text splits bounded by rules
  - a dark footer with a large wordmark

**Motion:**
- hero crossfade with slow zoom, and headlines that rise line by line
- sections fade up as you scroll; images wipe in
- gentle parallax on large images
- the header hides on scroll down and returns on scroll up
- hovering a product card swaps its image and slides up "Quick add"
- underlines wipe across links on hover
- buttons fill on hover
- slow marquees that pause on hover
- the renewal tag fades and its day count runs 01 → 60 as you scroll
- page-to-page fades
- all of it switches off when the device asks for reduced motion

**Placeholders:**
- Product images are crops of the five lifestyle photos until the studio shoot.
- The founder story is a marked placeholder.
- Prices are strategy estimates.

Files: `assets/site.css` (system), `assets/site.js` (header, bag, motion), `assets/products.js` (catalogue).
