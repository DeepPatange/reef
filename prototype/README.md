# Al Reef & Laurel — website prototype (Round 2)

Open `index.html` in Chrome or Safari. No server or install needed.

**Pages:** Home · Shop (category sidebar, renewal-price toggle) · Product (`product.html?p=the-duo`, any product slug works) · Renewal · Our farm · Field notes.

**Round 3 (client feedback, Nov 2026): sales-first homepage and shop-first navigation.** Same look; only the homepage, header, menu and footer changed.
- Header: Shop all · Sets · Loofahs · Soap · Gifts · Our Farm · [My subscription]. Category links open the shop already filtered. Renewal left the header; it's now explained on the homepage, with a link to its page from there and from the footer.
- Homepage order: hero (Shop the sets) → shop by category → sets you can subscribe to or buy once right from the card → how subscription works (fading tag) → singles → gifts and farm tiles → values.
- Customer-facing wording is "Subscribe and save"; "renews every 60 days" explains how it works. The renewal page itself is unchanged.
- **My subscription** (`account.html`): the customer's own view, asked for in the meeting. Opens from the boxed "My subscription" button at the end of the main nav (a person icon on phones; also in the phone menu and the footer).
  - At a glance: active subscriptions, next delivery, orders so far, total saved by subscribing.
  - Subscriptions: next delivery date with a fading-tag countdown, the day-50 WhatsApp date, and delivery every 30, 60 or 90 days. Ship now, skip, pause or resume, and cancel. Cancel asks for confirmation and offers "Pause instead".
  - Add to your next delivery: one-time extras (Laurel 16, Hammam Mitt, Guest Bar).
  - Orders: the scheduled delivery, then past orders with DHL tracking and Buy again. Profile: details, address, card, reminders.
  - Tabs can be linked directly: `account.html#orders`, `#profile`.
  - Sample customer "Layla". Dates count from today, and changes are saved in the browser. "Reset sample data" puts it back.

**Round 2 adds patterns from framacph.com:**
- word links in the header (Search, Account, Bag)
- two-up image tiles on the homepage (Renew every 60 days, Gift sets)
- a Renewal page modelled on Frama's Care Subscriptions:
  - a large statement paragraph
  - first set and refills tiles
  - 30, 60 and 90-day choices
  - how it works
  - numbered benefits
  - FAQ
- a shop with a category sidebar, an intro text cell and editorial tiles inside the grid
- on the product page:
  - a facts table with a checklist
  - a note on renewal terms
  - Complete the set rows
  - The fibre / The soap / The ritual story rows
- guide rows on the homepage

Round 1 (Kas di Kos only) is kept in `../prototype-round1-kasdikos/`.

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

**Design tokens (polish pass):** all are in `:root` at the top of `assets/site.css`. Change values there, not per page.
- Type: one scale of 12 · 13 · 14 · 16 · 18 · 20 · 24 · 32 · 44 · 64 · 88. It steps down at 1180px and 860px. Nothing is under 11px, and 500 is the only bold.
- Spacing: an 8px base (`--s-1`…`--s-12`). Sections are 128, 96 or 64. Label to heading is 12, heading to text is 24, text to buttons is 40.
- Shapes:
  - square boxes, cards and buttons (`--r-box: 0`)
  - pills for toggles and counters
  - circles for icon buttons
- Controls: 48px and 40px; on phones the small size becomes 44px. Phone tap targets are at least 44px.
- Margins: 16px on phones and up to 64px on desktop (`--gutter`). Lines are capped at about 70 characters (`--measure: 33em`).
- Contrast: secondary text is `#595E54` (5.2:1). Small accent text uses Delta Earth, because Nile Clay is only 3.5:1 on Linen. Clay stays for large numbers and decoration.
- Motion: three speeds.
  - `--t-fast` .3s for colour and opacity
  - `--t-ui` .6s for things that move
  - `--t-slow` 1.2s for images and reveals

  Every image zooms on hover by the same amount (`--zoom: 1.04`).
- Focus: a 2px ring, clay on light surfaces and cream on dark surfaces and photos. Closed drawers are out of the keyboard tab order.
- Photos: product, story and benefit photos are all 4:5.
- Tile grid: follows page 27 of the brand guide. It's a square grid with lines at 20% Delta Linen (`--grid-line`), used only on Deep Laurel or Delta Earth. Sections have 9 cells across, or 6 on phones (`--tile-cols`); boxes get a grid twice as fine. The tall stack grid is kept for social posts, gift tissue and shelf strips, not the website.

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
- the farm story (Our farm page): seven gouache paintings stay pinned while you scroll from Field 7 to the shower. Each painting brushes on over the last, the gourds turn from green to light, and counters run for days in the sun, fibres per cm² and days in your shower. With reduced motion the chapters simply stack.
- page-to-page fades
- all of it switches off when the device asks for reduced motion

**Placeholders:**
- Farm story paintings: these are in `assets/img/farm/`, made with Canva's image generator. The Canva design is "Al Reef & Laurel — Farm story paintings", with one page per painting, and `SOURCES.txt` lists which is which.
- Photos: the homepage keeps the five lifestyle photos. Every other page, and all products, use the client's placeholder photos in `assets/img/ref/` (sources are listed in `SOURCES.txt`). Each product has its own pair, and no photo repeats on a page. Several show other brands' labels, so they are for review only, not launch.
- The founder story is a marked placeholder.
- Prices are strategy estimates.

Files: `assets/site.css` (system), `assets/site.js` (header, bag, motion), `assets/products.js` (catalogue).
