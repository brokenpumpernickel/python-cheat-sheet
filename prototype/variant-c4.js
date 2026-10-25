// PROTOTYPE - Variant C4 "Map + trail": C2 with a Map | Trail toggle. The Overview is either the
// self-arranging archipelago or the stepping-stone trail; inside a Topic the side rail (the Index)
// follows the same choice: mini islands, or a compact numbered mini-trail. EN | PL switches Language.
(function () {
  const { data, byId, esc, L } = CS;
  const { HUE, BLOBS, pageHTML, fade, trailLand, landRailHTML, watchLands } = CC;
  const app = document.getElementById("app");
  const UI = {
    en: { map: "Map", trail: "Trail", whole: "← Whole", search: "What do you need to remember?", soon: "coming soon",
          hintMap: "Click a bubble to dive in · <kbd>Ctrl K</kbd> to search · <kbd>Esc</kbd> to come back up",
          start: "Start here", hintTrail: "Pick any stone to dive in · <kbd>Ctrl K</kbd> search · <kbd>Esc</kbd> back", style: "Overview style", language: "Language" },
    pl: { map: "Mapa", trail: "Szlak", whole: "← Cała", search: "Co chcesz sobie przypomnieć?", soon: "wkrótce",
          hintMap: "Kliknij bąbel, aby wejść · <kbd>Ctrl K</kbd> szukaj · <kbd>Esc</kbd> powrót",
          start: "Zacznij tutaj", hintTrail: "Wybierz kamień, aby wejść · <kbd>Ctrl K</kbd> szukaj · <kbd>Esc</kbd> powrót", style: "Widok przeglądu", language: "Język" },
  };
  const t = (key) => CS.t(key, UI);

  let view = "map";
  try { view = localStorage.getItem("cs-proto-view") === "trail" ? "trail" : "map"; } catch {}

  // Bubbles sit on rings (one in the centre once there are 5+), so they always fit a round island.
  const GAP = 16, PAD = 30;
  const SOFT_BLOBS = ["50% 47% 52% 49% / 48% 52% 49% 51%", "48% 52% 49% 51% / 51% 48% 52% 49%", "52% 48% 50% 50% / 49% 51% 48% 52%"];
  const ringR = (m, step) => (m < 2 ? 0 : step / (2 * Math.sin(Math.PI / m)));
  function radial(n, d) {
    const step = d + GAP, pts = [];
    const ring = (m, r, phase) => { for (let k = 0; k < m; k++) { const a = -Math.PI / 2 + phase + (k / m) * 2 * Math.PI; pts.push([r * Math.cos(a), r * Math.sin(a)]); } };
    if (n < 5) ring(n, ringR(n, step), n === 2 ? Math.PI / 2 : 0);
    else if (n <= 13) { pts.push([0, 0]); ring(n - 1, Math.max(step, ringR(n - 1, step)), 0); }
    else { pts.push([0, 0]); ring(6, step, 0); ring(n - 7, Math.max(2 * step, ringR(n - 7, step)), 0.3); }
    return { pts, R: Math.max(...pts.map(([x, y]) => Math.hypot(x, y))) + d / 2 };
  }
  const island = (a, i) => {
    const d = a.topics.some((tp) => !tp.placeholder) ? 116 : 78, { pts, R } = radial(a.topics.length, d), size = 2 * (R + PAD);
    return `
    <section class="c2-island c4-island${a.placeholder ? " is-ph" : ""}" style="--hue:${HUE[a.id]};--i:${i};width:${size}px;height:${size}px;border-radius:${SOFT_BLOBS[i % 3]}">
      <div class="c-flag"><b>${esc(L(a, "title"))}</b>${a.placeholder ? `<small>${t("soon")}</small>` : ""}</div>
      ${a.topics.map((tp, j) => {
        const pos = `--j:${j};left:calc(50% + ${pts[j][0].toFixed(1)}px);top:calc(50% + ${pts[j][1].toFixed(1)}px)`;
        return tp.placeholder
          ? `<div class="c-bubble is-ph" style="${pos}"><span class="c-glyph">${esc(tp.glyph)}</span><span class="c-name">${esc(L(tp, "title"))}</span></div>`
          : `<a class="c-bubble" href="#${tp.id}" data-tile="${tp.id}" style="${pos}"><span class="c-glyph">${esc(tp.glyph)}</span><span class="c-name">${esc(L(tp, "title"))}</span></a>`;
      }).join("")}
    </section>`;
  };

  const miniIsland = (a, i) => `
    <div class="c2-mini${a.placeholder ? " is-ph" : ""}" style="--hue:${HUE[a.id]};border-radius:${BLOBS[(i + 1) % 3]}">
      <b>${esc(L(a, "title"))}</b>
      <div class="c2-pins">${a.topics.map((tp) => tp.placeholder
        ? `<span class="c2-pin is-ph">${esc(L(tp, "title"))}</span>`
        : `<a class="c2-pin" href="#${tp.id}" data-pin="${tp.id}"><span>${esc(tp.glyph)}</span>${esc(L(tp, "title"))}</a>`).join("")}
      </div>
    </div>`;

  const miniTrail = (a) => {
    let n = 0;
    return `<div class="c4-mt${a.placeholder ? " is-ph" : ""}" style="--hue:${HUE[a.id]}">
      <b>${esc(L(a, "title"))}</b>
      <ol>${a.topics.map((tp) => tp.placeholder
        ? `<li class="is-ph"><i></i>${esc(L(tp, "title"))}</li>`
        : `<li><a href="#${tp.id}" data-pin="${tp.id}"><i>${++n}</i>${esc(L(tp, "title"))}</a></li>`).join("")}</ol>
    </div>`;
  };

  const seg = (name, label, opts, current) => `<div class="c4-toggle" role="radiogroup" aria-label="${label}">${opts.map(([k, txt]) =>
    `<button type="button" role="radio" data-${name}="${k}" aria-checked="${k === current}">${txt}</button>`).join("")}</div>`;

  let layout, page, rail;
  function build() {
    app.innerHTML = `
      <div class="c-top c4-top">
        <div class="c-logo"><span>py</span> cheat&nbsp;map</div>
        ${seg("view", t("style"), [["map", t("map")], ["trail", t("trail")]], view)}
        ${seg("lang", t("language"), [["en", "EN"], ["pl", "PL"]], CS.lang())}
        <button class="c-searchpill" type="button" data-search><span class="c-ico">⌕</span> ${t("search")} <kbd>Ctrl K</kbd></button>
      </div>
      <div class="c2-layout" id="layout">
        <aside class="c2-rail" id="rail" aria-label="Index">
          <a class="c2-rail-home" href="#" data-home>${t("whole")} <span data-view-name></span></a>
          <div class="c4-rail-map">${data.areas.map(miniIsland).join("")}</div>
          <div class="c4-rail-trail">${data.areas.map(miniTrail).join("")}</div>
        </aside>
        <main class="c2-sea c4-overview" id="sea">
          ${data.areas.map(island).join("")}
          <p class="c-hint">${t("hintMap")}</p>
        </main>
        <main class="c3-trail c4-overview" id="trail">
          ${landRailHTML(data.areas)}
          <p class="c3-start">${t("start")} <span>↓</span><small>${t("hintTrail")}</small></p>
          ${data.areas.map(trailLand).join("")}
        </main>
        <article class="c2-page" id="page" hidden tabindex="-1"></article>
      </div>`;
    layout = document.getElementById("layout");
    page = document.getElementById("page");
    rail = document.getElementById("rail");
    watchLands(document.getElementById("trail"));
    setView(view);
  }
  const overviewEl = () => document.getElementById(view === "map" ? "sea" : "trail");

  function setView(v) {
    view = v;
    try { localStorage.setItem("cs-proto-view", v); } catch {}
    layout.classList.toggle("view-map", v === "map");
    layout.classList.toggle("view-trail", v === "trail");
    app.querySelectorAll("[data-view]").forEach((b) => b.setAttribute("aria-checked", b.dataset.view === v));
    app.querySelector("[data-view-name]").textContent = t(v).toLowerCase();
  }
  build();

  // Re-render in place on a Language switch, keeping the Topic and the scroll position.
  CS.onLang(() => {
    const y = scrollY, route = CS.route();
    build();
    if (shown) {
      layout.classList.add("is-topic");
      showTopic(byId[shown], route && route.entry);
    }
    scrollTo(0, y);
  });

  app.addEventListener("click", (e) => {
    if (e.target.closest("[data-search]")) CS.openPalette();
    if (e.target.closest("[data-home]")) { e.preventDefault(); CS.go(null); }
    const v = e.target.closest("[data-view]");
    if (v && v.dataset.view !== view) {
      setView(v.dataset.view);
      if (!shown) { scrollTo(0, 0); fade(overviewEl(), "in", 300); }
      else markPin(shown);
    }
    const l = e.target.closest("[data-lang]");
    if (l && l.dataset.lang !== CS.lang()) CS.setLang(l.dataset.lang);
  });

  let shown = null, spy = null;
  // The current Topic's pin(s) in the rail expand to list its Entries; the one in view is highlighted.
  function markPin(id) {
    rail.querySelectorAll(".c4-ents").forEach((x) => x.remove());
    rail.querySelectorAll("[data-pin]").forEach((p) => {
      const here = p.dataset.pin === id;
      p.classList.toggle("is-here", here);
      if (here) p.insertAdjacentHTML(p.closest("li") ? "afterend" : "afterend", `<div class="c4-ents">${byId[id].entries.map((en) =>
        `<a href="#${id}/${en.id}" data-ent="${en.id}">${esc(L(en, "title"))}</a>`).join("")}</div>`);
    });
    const here = [...rail.querySelectorAll(".is-here")].find((p) => p.offsetParent);
    here && here.scrollIntoView({ block: "nearest", inline: "center" });
  }
  function markEntry(entryId) {
    rail.querySelectorAll("[data-ent]").forEach((a) => a.classList.toggle("is-cur", a.dataset.ent === entryId));
  }
  function showTopic(tp, entryId) {
    page.innerHTML = pageHTML(tp, null, { pager: true });
    page.hidden = false;
    markPin(tp.id);
    spy && spy.disconnect();
    spy = new IntersectionObserver((es) => es.forEach((en) => en.isIntersecting && markEntry(en.target.id.slice(2))), { rootMargin: "-35% 0px -60% 0px" });
    page.querySelectorAll(".c-card").forEach((c) => spy.observe(c));
    markEntry(entryId || tp.entries[0].id);
  }
  async function render(route) {
    if (route) {
      const tp = byId[route.topic];
      if (shown !== tp.id) {
        if (!shown) {
          const ov = overviewEl(), b = ov.querySelector(`[data-tile="${tp.id}"]`);
          if (b) await CS.push(ov, CS.centerOf(b), "in", { scale: 4, duration: 520 });
          layout.classList.add("is-topic");
          scrollTo(0, 0);
          showTopic(tp, route.entry);
          await Promise.all([fade(page, "in"), CS.reducedMotion || !CS.booted() ? null :
            CS.settle(rail.animate([{ transform: "translateX(-40px)", opacity: 0 }, { transform: "none", opacity: 1 }], { duration: 420, easing: "ease-out" }), 420)]);
        } else {
          await fade(page, "out", 160);
          scrollTo(0, 0);
          showTopic(tp, route.entry);
          await fade(page, "in", 260);
        }
        shown = tp.id;
      }
      if (route.entry) { CS.flash(page.querySelector(`#e-${route.entry}`)); markEntry(route.entry); }
      else scrollTo({ top: 0 });
      page.focus({ preventScroll: true });
    } else if (shown) {
      spy && spy.disconnect();
      await fade(page, "out", 220);
      page.hidden = true;
      layout.classList.remove("is-topic");
      markPin(null);
      const ov = overviewEl(), b = ov.querySelector(`[data-tile="${shown}"]`);
      b && b.scrollIntoView({ block: "center" });
      if (b) await CS.push(ov, CS.centerOf(b), "out", { scale: 4, duration: 520 });
      shown = null;
      b && b.focus({ preventScroll: true });
    }
  }
  CS.onRoute(render);
  render(CS.route());
})();
