/* Al Reef & Laurel — prototype runtime: shared chrome, bag, motion. No dependencies. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const AED = (n) => `AED ${Number(n).toLocaleString("en-GB")}`;
  window.AED = AED;

  /* ---------------------------------------------------------------- icons + marks */
  const MONO = `<svg class="mono" viewBox="0 0 124 124" aria-hidden="true"><path d="M 67.00 10.50 C 79.25 9.92 89.58 15.08 97.50 23.50 C 105.42 31.92 113.50 48.50 114.50 61.00 C 115.50 73.50 110.92 89.75 103.50 98.50 C 96.08 107.25 82.67 112.58 70.00 113.50 C 57.33 114.42 37.58 111.92 27.50 104.00 C 17.42 96.08 10.08 78.83 9.50 66.00 C 8.92 53.17 14.42 36.25 24.00 27.00 C 33.58 17.75 54.75 11.08 67.00 10.50 Z"/><path d="M 48.84 55.09 C 49.46 58.24 49.47 62.02 48.12 64.93 C 46.76 67.84 43.67 71.79 40.70 72.56 C 37.73 73.32 33.11 71.54 30.28 69.52 C 27.45 67.50 24.38 63.73 23.73 60.43 C 23.08 57.12 24.60 52.68 26.37 49.70 C 28.13 46.73 31.33 43.20 34.33 42.59 C 37.33 41.98 41.96 43.96 44.38 46.04 C 46.80 48.13 48.22 51.94 48.84 55.09 Z"/><path d="M 94.76 49.02 C 94.03 52.62 91.04 56.73 88.23 58.73 C 85.43 60.73 80.95 61.70 77.94 60.99 C 74.94 60.28 71.87 57.25 70.19 54.47 C 68.50 51.68 67.46 47.72 67.83 44.27 C 68.21 40.82 69.89 35.90 72.45 33.77 C 75.00 31.63 79.79 30.89 83.15 31.44 C 86.52 32.00 90.72 34.18 92.66 37.11 C 94.59 40.04 95.50 45.41 94.76 49.02 Z"/><path d="M 83.72 91.49 C 83.61 94.65 81.80 98.97 79.28 100.97 C 76.76 102.96 72.06 103.72 68.59 103.47 C 65.12 103.21 60.69 101.74 58.47 99.42 C 56.24 97.09 54.73 92.42 55.23 89.50 C 55.73 86.58 58.95 83.75 61.47 81.91 C 63.99 80.06 67.26 78.42 70.34 78.44 C 73.43 78.47 77.74 79.86 79.97 82.04 C 82.20 84.21 83.84 88.34 83.72 91.49 Z"/><path d="M 62 66.5 L 55.5 33.5 M 62 66.5 L 39.5 88 M 62 66.5 L 95 75"/></svg>`;
  window.MONO = MONO;
  const I = {
    search: '<svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 20 20"/></svg>',
    user: '<svg viewBox="0 0 24 24"><circle cx="12" cy="8.5" r="3.8"/><path d="M4.8 20c.7-3.7 3.6-5.6 7.2-5.6s6.5 1.9 7.2 5.6"/></svg>',
    bag: '<svg viewBox="0 0 24 24"><path d="M5.5 8.5h13l-1.1 11.5H6.6z"/><path d="M9 8.5V7a3 3 0 0 1 6 0v1.5"/></svg>',
    menu: '<svg viewBox="0 0 24 24"><path d="M4 9h16M4 15h16"/></svg>',
    close: '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    insta: '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="4.5"/><circle cx="12" cy="12" r="3.8"/><path d="M16.6 7.4v.1"/></svg>',
    wa: '<svg viewBox="0 0 24 24"><path d="M12 3.5a8.5 8.5 0 0 0-7.3 12.8L3.5 20.5l4.3-1.1A8.5 8.5 0 1 0 12 3.5z"/><path d="M9 8.6c.3 2.8 2.6 5.3 5.6 6.1l1.2-1.4-1.9-1-.9.8a5 5 0 0 1-2.5-2.5l.8-.9-1-1.9z"/></svg>',
    tiktok: '<svg viewBox="0 0 24 24"><path d="M14 4v10.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 4c.4 2.6 2.2 4.4 5 4.6"/></svg>',
  };
  const ARROW = '<svg class="arrow" viewBox="0 0 22 10" fill="none" stroke="currentColor" stroke-width="1.1"><path d="M0 5h21M16.5 1 21 5l-4.5 4"/></svg>';
  window.ARROW = ARROW;
  const WM = '<span class="wm"><b>AL REEF</b><i>&amp; LAUREL</i></span>';

  /* ---------------------------------------------------------------- shared chrome */
  const page = document.body.dataset.page || "";
  // shop-first navigation: categories go straight to the filtered shop; subscription lives on the homepage, PDP and footer
  // My subscription closes the row as a boxed button: the customer's own subscription view (account.html)
  const nav = [["shop", "shop.html", "Shop all"], ["rituals", "shop.html#rituals", "Sets"], ["loofahs", "shop.html#loofahs", "Loofahs"], ["soap", "shop.html#soap", "Soap"], ["gifts", "shop.html#gifts", "Gifts"], ["farm", "farm.html", "Our Farm"], ["account", "account.html", "My subscription"]];
  const navKey = () => (page === "shop" ? ({ rituals: 1, loofahs: 1, soap: 1, gifts: 1 }[location.hash.slice(1)] ? location.hash.slice(1) : "shop") : page);
  const navHTML = nav.map(([k, h, t]) => `<a href="${h}" data-k="${k}"${k === "account" ? ' class="nav-btn"' : ""}>${t}</a>`).join("");
  const tick = ["Founding members · 25% off your first Duo", "Free UAE delivery on every order", "Subscribe and save at least 20% · skip or pause any time", "Harvest September 2026 · now shipping"];
  const tickHTML = [...tick, ...tick].map((t) => `<span>${t}</span>`).join("");

  document.body.insertAdjacentHTML("afterbegin", `
    <div class="page-fade" aria-hidden="true"></div>
    <div class="announce" role="region" aria-label="Announcements"><div class="track">${tickHTML}${tickHTML}</div></div>
    <header class="site-header">
      <div class="wrap hdr-top">
        <div class="hdr-left">
          <button class="icon-btn menu-btn" data-open="menu" aria-label="Menu">${I.menu}</button>
          <button class="txt-link" onclick="window.toast('Search is not part of this prototype')">Search</button>
        </div>
        <a href="index.html" aria-label="Al Reef &amp; Laurel, home">${WM}</a>
        <div class="hdr-right">
          <a class="icon-btn sub-icon" href="account.html" data-k="account" aria-label="My subscription">${I.user}</a>
          <button class="txt-link" data-open="bag">Bag (<span class="num" data-bag-txt>0</span>)</button>
          <button class="icon-btn bag-icon" data-open="bag" aria-label="Bag">${I.bag}<span class="bag-count num">0</span></button>
        </div>
      </div>
      <nav class="hdr-nav" aria-label="Main">${navHTML}</nav>
    </header>
    <aside class="rail" aria-label="Elsewhere">
      <a href="#" aria-label="Instagram">${I.insta}</a><a href="#" aria-label="TikTok">${I.tiktok}</a><a href="#" aria-label="WhatsApp">${I.wa}</a>
      <a href="#letters" class="tab">Letters</a>
    </aside>`);

  document.body.insertAdjacentHTML("beforeend", `
    <footer class="site-footer" id="letters">
      <div class="wrap">
        <div class="ftr-grid">
          <div><h5>Shop</h5><ul><li><a href="shop.html">Shop all</a></li><li><a href="product.html?p=the-duo">The Duo</a></li><li><a href="shop.html#rituals">Sets</a></li><li><a href="shop.html#loofahs">Loofahs</a></li><li><a href="shop.html#soap">Soap</a></li><li><a href="shop.html#gifts">Gifts</a></li></ul></div>
          <div><h5>Learn</h5><ul><li><a href="renewal.html">How subscription works</a></li><li><a href="farm.html">Our farm</a></li><li><a href="notes.html">Field notes</a></li><li><a href="#">Look up a batch</a></li></ul></div>
          <div><h5>Help</h5><ul><li><a href="#">Shipping &amp; returns</a></li><li><a href="account.html">Manage your subscription</a></li><li><a href="#">FAQ</a></li><li><a href="#">WhatsApp us</a></li></ul></div>
          <div><h5>Letters from the Delta</h5>
            <form class="letter" onsubmit="event.preventDefault(); window.toast('Thank you. Your first letter arrives next month.'); this.reset();">
              <label class="sr" for="em">Email</label><input id="em" type="email" placeholder="Enter your email" required><button aria-label="Subscribe">${ARROW}</button></form>
            <p class="ftr-note">Field notes, harvest news and early access, once a month. No puns. Well, one.</p></div>
        </div>
        <div class="ftr-mark" data-reveal>${WM}</div>
        <div class="ftr-base"><span>© 2026 Al Reef &amp; Laurel · Dubai, United Arab Emirates</span>
          <nav><a href="#">Privacy</a><a href="#">Terms</a><a href="#">Shipping</a><a href="#">Cookies</a></nav></div>
      </div>
    </footer>
    <div class="scrim" data-close></div>
    <aside class="drawer" id="bag" aria-label="Bag" aria-hidden="true">
      <div class="drawer-head"><span class="caps">Your bag <span class="num" data-bag-n>(0)</span></span><button class="icon-btn" data-close aria-label="Close">${I.close}</button></div>
      <div class="ship-bar"><span class="small" data-ship>Free UAE delivery on every ritual</span><div class="bar"><i style="width:0"></i></div></div>
      <div class="drawer-body" data-lines></div>
      <div class="drawer-foot">
        <div class="totals"><span class="caps">Subtotal</span><span class="num" data-sub>AED 0</span></div>
        <button class="btn btn-clay btn-block" onclick="window.toast('Checkout is not part of this prototype')">Checkout</button>
        <p class="small soft center" style="margin-top:var(--s-3)">Renewals ship every 60 days. Skip, swap or pause any time.</p>
      </div>
    </aside>
    <aside class="drawer left" id="menu" aria-label="Menu" aria-hidden="true">
      <div class="drawer-head">${WM}<button class="icon-btn" data-close aria-label="Close">${I.close}</button></div>
      <div class="drawer-body menu-links">${nav.map(([k, h, t]) => `<a href="${h}" data-k="${k}">${t}${ARROW}</a>`).join("")}
        <div style="margin-top:var(--s-7)" class="stack"><a class="small" href="renewal.html">How subscription works</a><a class="small" href="notes.html">Field notes</a><a class="small" href="#">WhatsApp us</a></div></div>
    </aside>
    <div class="toast" role="status" aria-live="polite"></div>`);

  /* ---------------------------------------------------------------- current nav item (shop categories follow the hash) */
  window.syncNav = () => { const k = navKey(); $$(".site-header [data-k], .menu-links > a").forEach((a) => (a.dataset.k === k ? a.setAttribute("aria-current", "page") : a.removeAttribute("aria-current"))); };
  addEventListener("hashchange", window.syncNav);
  window.syncNav();

  /* ---------------------------------------------------------------- toast */
  let toastT;
  window.toast = (msg) => { const t = $(".toast"); t.textContent = msg; t.classList.add("on"); clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove("on"), 2600); };

  /* ---------------------------------------------------------------- drawers */
  const scrim = $(".scrim");
  const open = (id) => { const d = $("#" + id); d.classList.add("on"); d.setAttribute("aria-hidden", "false"); scrim.classList.add("on"); document.documentElement.style.overflow = "hidden"; setTimeout(() => d.querySelector("button, a")?.focus(), 300); };
  const close = () => { $$(".drawer.on").forEach((d) => { d.classList.remove("on"); d.setAttribute("aria-hidden", "true"); }); scrim.classList.remove("on"); document.documentElement.style.overflow = ""; };
  window.openDrawer = open;
  document.addEventListener("click", (e) => {
    const o = e.target.closest("[data-open]"); if (o) { e.preventDefault(); open(o.dataset.open); }
    if (e.target.closest("[data-close]")) close();
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });

  /* ---------------------------------------------------------------- bag */
  const KEY = "arl-bag-v1";
  let bag = [];
  try { bag = JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { bag = []; }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(bag)); } catch (e) {} };
  const imgStyle = (im) => `--fx:${im.fx}%;--fy:${im.fy}%;--z:${im.z}`;
  const renderBag = () => {
    const n = bag.reduce((a, l) => a + l.qty, 0);
    const sub = bag.reduce((a, l) => a + l.qty * l.price, 0);
    const c = $(".bag-count"); c.textContent = n; c.classList.toggle("on", n > 0); $("[data-bag-txt]").textContent = n;
    $("[data-bag-n]").textContent = `(${n})`; $("[data-sub]").textContent = AED(sub);
    $(".ship-bar i").style.width = n ? "100%" : "0";
    $("[data-ship]").textContent = n ? "Free UAE delivery unlocked" : "Free UAE delivery on every ritual";
    const box = $("[data-lines]");
    if (!bag.length) { box.innerHTML = `<div class="empty"><div style="width:var(--s-9);margin:0 auto var(--s-4);opacity:.5">${MONO}</div><p class="h4">Your bag is empty</p><p class="small soft" style="margin:var(--s-2) auto var(--s-5)">Start with the Duo: a loofah and a bar of laurel soap.</p><a class="btn" href="product.html?p=the-duo">Shop the Duo</a></div>`; return; }
    box.innerHTML = bag.map((l, i) => { const p = window.findProduct(l.slug); const im = p.images[0];
      return `<div class="line"><div class="thumb"><img src="${im.sm}" style="${imgStyle(im)}" alt=""></div>
        <div><div class="h4">${p.name}</div><div class="small soft">${l.mode === "renew" ? "Renews every " + (l.cycle || 60) + " days" : "One-time"}${l.variant ? " · " + l.variant : ""}</div>
        <div class="qty"><button data-q="${i}" data-d="-1" aria-label="Less">−</button><span class="num">${l.qty}</span><button data-q="${i}" data-d="1" aria-label="More">+</button></div></div>
        <div class="num" style="text-align:right">${AED(l.price * l.qty)}<br><button class="small soft" data-rm="${i}" style="margin-top:var(--s-6);text-decoration:underline">Remove</button></div></div>`; }).join("");
  };
  window.addToBag = (slug, opts = {}) => {
    const p = window.findProduct(slug);
    const mode = opts.mode || (p.renew ? "renew" : "once");
    const price = mode === "renew" && p.renew ? p.renew : p.price;
    const ex = bag.find((l) => l.slug === slug && l.mode === mode && l.variant === opts.variant);
    if (ex) ex.qty += opts.qty || 1; else bag.push({ slug, mode, price, qty: opts.qty || 1, variant: opts.variant || "", cycle: opts.cycle || 60 });
    save(); renderBag();
    const c = $(".bag-count"); c.classList.remove("bump"); void c.offsetWidth; c.classList.add("bump");
    setTimeout(() => open("bag"), 380);
  };
  document.addEventListener("click", (e) => {
    const q = e.target.closest("[data-q]"); if (q) { const l = bag[+q.dataset.q]; l.qty += +q.dataset.d; if (l.qty < 1) bag.splice(+q.dataset.q, 1); save(); renderBag(); }
    const r = e.target.closest("[data-rm]"); if (r) { bag.splice(+r.dataset.rm, 1); save(); renderBag(); }
    const a = e.target.closest("[data-add]"); if (a) { e.preventDefault(); e.stopPropagation(); const lbl = a.innerHTML; a.textContent = "Added"; window.addToBag(a.dataset.add, a.dataset.mode ? { mode: a.dataset.mode } : {}); setTimeout(() => (a.innerHTML = lbl), 1400); }
  });
  renderBag();

  /* ---------------------------------------------------------------- product card markup (used by pages) */
  window.cardHTML = (p, d = 0) => {
    const [a, b] = p.images;
    const price = p.from ? `From ${AED(p.price)}` : AED(p.price);
    return `<a class="card" href="product.html?p=${p.slug}" data-reveal style="--d:${d}s" data-type="${p.type}">
      <div class="card-media">${p.badge ? `<span class="card-badge caps-s">${p.badge}</span>` : ""}
        <div class="ph"><img src="${a.sm}" alt="${p.name}" loading="lazy" style="${imgStyle(a)}"></div>
        ${b ? `<div class="ph alt"><img src="${b.sm}" alt="" loading="lazy" style="${imgStyle(b)}"></div>` : ""}
        <button class="quick" data-add="${p.slug}">${p.renew ? `Subscribe · ${AED(p.renew)}` : `Quick add · ${price}`}</button></div>
      <div class="card-info"><div><div class="card-name">${p.name}</div><div class="card-sub">${p.sub}</div></div>
        <div class="card-price num">${price}${p.renew ? `<span class="renew">${AED(p.renew)} subscribed</span>` : ""}</div></div></a>`;
  };
  window.imgStyle = imgStyle;

  /* ---------------------------------------------------------------- header hide / show */
  const hdr = $(".site-header"); let lastY = scrollY;
  addEventListener("scroll", () => {
    const y = scrollY;
    hdr.classList.toggle("is-scrolled", y > 40);
    if (!document.querySelector(".drawer.on")) hdr.classList.toggle("is-hidden", y > 400 && y > lastY + 2);
    if (y < lastY - 2) hdr.classList.remove("is-hidden");
    lastY = y;
  }, { passive: true });

  /* ---------------------------------------------------------------- split headings into lines */
  $$("[data-split]").forEach((el) => {
    el.innerHTML = el.innerHTML.split(/<br\s*\/?>/i).map((l, i) => `<span class="split-line"><span style="transition-delay:${0.12 * i + (+el.dataset.split || 0)}s">${l}</span></span>`).join("");
  });

  /* ---------------------------------------------------------------- reveal on scroll */
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
  window.observeReveal = (root = document) => $$("[data-reveal], [data-split]", root).forEach((el) => (reduce ? el.classList.add("is-in") : io.observe(el)));
  window.observeReveal();

  /* ---------------------------------------------------------------- parallax */
  const par = $$("[data-parallax]");
  if (par.length && !reduce) {
    const run = () => { const vh = innerHeight; par.forEach((el) => { const r = el.parentElement.getBoundingClientRect(); if (r.bottom < 0 || r.top > vh) return; const p = (r.top + r.height / 2 - vh / 2) / vh; el.style.transform = `translate3d(0, ${(-p * (+el.dataset.parallax || 8)).toFixed(2)}%, 0)`; }); };
    addEventListener("scroll", () => requestAnimationFrame(run), { passive: true }); run();
  }

  /* ---------------------------------------------------------------- hero slideshow */
  const hero = $(".hero");
  if (hero) {
    const slides = $$(".slide", hero), dots = $(".hero-dots", hero), meta = $(".hero-meta", hero);
    let i = 0, t;
    dots.innerHTML = slides.map((_, k) => `<button aria-label="Slide ${k + 1}"><i></i></button>`).join("");
    const go = (k) => { slides[i].classList.remove("on"); dots.children[i].classList.remove("on"); i = (k + slides.length) % slides.length; slides[i].classList.add("on"); const b = dots.children[i]; b.classList.remove("on"); void b.offsetWidth; b.classList.add("on"); if (meta) meta.textContent = slides[i].dataset.meta || ""; clearTimeout(t); if (!reduce) t = setTimeout(() => go(i + 1), 6500); };
    dots.addEventListener("click", (e) => { const b = e.target.closest("button"); if (b) go([...dots.children].indexOf(b)); });
    go(0);
  }

  /* ---------------------------------------------------------------- the fade: tag ink + day count follow scroll */
  const fade = $("[data-fade]");
  if (fade) {
    const ink = $$(".ink i", fade), day = $(".day", fade);
    const run = () => { const r = fade.getBoundingClientRect(); const p = Math.min(1, Math.max(0, (innerHeight * 0.85 - r.top) / (r.height + innerHeight * 0.3)));
      const d = Math.max(1, Math.round(p * 60)); day.textContent = `DAY ${String(d).padStart(2, "0")} / 60`;
      ink.forEach((el, k) => (el.style.opacity = Math.max(0.08, Math.min(1, 1 - (p * 3 - k)))).toFixed?.(2)); };
    addEventListener("scroll", () => requestAnimationFrame(run), { passive: true }); run();
  }

  /* ---------------------------------------------------------------- smooth accordions */
  $$("details.acc").forEach((d) => {
    const s = d.querySelector("summary"), b = d.querySelector(".acc-body");
    s.addEventListener("click", (e) => { if (reduce) return; e.preventDefault();
      if (d.open) { b.animate([{ height: b.scrollHeight + "px" }, { height: "0px" }], { duration: 420, easing: "cubic-bezier(.7,0,.3,1)" }).onfinish = () => (d.open = false); }
      else { d.open = true; b.animate([{ height: "0px" }, { height: b.scrollHeight + "px" }], { duration: 520, easing: "cubic-bezier(.22,1,.36,1)" }); } });
  });

  /* ---------------------------------------------------------------- page transitions */
  addEventListener("pageshow", () => document.documentElement.classList.remove("leaving"));
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a[href]"); if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || a.target) return;
    const href = a.getAttribute("href"); if (!href || href.startsWith("#") || href.startsWith("http") || href.startsWith("mailto")) return;
    // same page with a new #hash (shop categories from the shop): let the browser jump, no fade, or the cover never lifts
    const to = new URL(href, location.href); if (to.hash && to.pathname === location.pathname && to.search === location.search) return;
    if (reduce) return; e.preventDefault(); document.documentElement.classList.add("leaving"); setTimeout(() => (location.href = href), 320);
  });
  const ready = () => requestAnimationFrame(() => document.documentElement.classList.add("loaded"));
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(ready); setTimeout(ready, 1200);
})();
