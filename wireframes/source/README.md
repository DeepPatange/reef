# Wireframe source (Round 1)

Each page in `pages/` is HTML with `{{macro|args}}` shorthands. To rebuild after editing:

    cd source
    mkdir -p dist shots
    python3 build.py pages/01-home.html          # writes dist/01-home.html (self-contained)
    python3 shoot.py dist/01-home.html           # optional: screenshots + overflow check (needs Playwright)

`SPEC.md` holds the page-by-page content spec, product and price data, and the motion codes (M01–M20).
`system.css` is the design system; `build.py` documents every macro at the top.
The built, self-contained pages are in `../pages/`; open `../index.html` in a browser to browse them.
