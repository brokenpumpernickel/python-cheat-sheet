// PROTOTYPE - Variant C "Islands": the most literal map. Areas are islands on a sea, Topics
// are bubbles on them; clicking flies the camera into the bubble. Entries are rounded cards.
(function () {
  const { data, byId, esc, md, codeHTML, outputHTML } = CS;
  const app = document.getElementById("app");
  const W = 1200, H = 760;
  // Island geometry in "world" units, and a hue per Area.
  const ISLANDS = {
    "python-basics": { x: 40, y: 110, w: 640, h: 560, hue: 160, cols: 3 },
    numpy: { x: 720, y: 40, w: 440, h: 175, hue: 265, cols: 4 },
    pandas: { x: 720, y: 255, w: 300, h: 175, hue: 205, cols: 3 },
    "scipy-stats": { x: 1045, y: 200, w: 140, h: 320, hue: 335, cols: 1 },
    matplotlib: { x: 720, y: 545, w: 440, h: 195, hue: 22, cols: 3 },
  };
  const BLOBS = ["46% 54% 58% 42% / 44% 40% 60% 56%", "58% 42% 38% 62% / 52% 58% 42% 48%", "40% 60% 55% 45% / 60% 45% 55% 40%"];

  const islandHTML = (a, i) => {
    const g = ISLANDS[a.id], rows = Math.ceil(a.topics.length / g.cols);
    return `<div class="c-island${a.placeholder ? " is-ph" : ""}" style="--hue:${g.hue};left:${g.x}px;top:${g.y}px;width:${g.w}px;height:${g.h}px;border-radius:${BLOBS[i % 3]}">
      <div class="c-flag"><b>${esc(a.title)}</b>${a.placeholder ? "<small>coming soon</small>" : ""}</div>
      <div class="c-bubbles" style="grid-template-columns:repeat(${g.cols},1fr);grid-template-rows:repeat(${rows},1fr)">
        ${a.topics.map((t, j) => t.placeholder
          ? `<div class="c-bubble is-ph" style="--j:${j}"><span class="c-glyph">${esc(t.glyph)}</span><span class="c-name">${esc(t.title)}</span></div>`
          : `<a class="c-bubble" href="#${t.id}" data-tile="${t.id}" style="--j:${j}"><span class="c-glyph">${esc(t.glyph)}</span><span class="c-name">${esc(t.title)}</span></a>`).join("")}
      </div></div>`;
  };

  app.innerHTML = `
    <div class="c-top">
      <div class="c-logo"><span>py</span> cheat&nbsp;map</div>
      <button class="c-searchpill" type="button" data-search><span class="c-ico">⌕</span> What do you need to remember? <kbd>Ctrl K</kbd></button>
    </div>
    <main class="c-sea" id="sea">
      <div class="c-world" id="world" style="width:${W}px;height:${H}px">
        <svg class="c-waves" viewBox="0 0 ${W} ${H}" aria-hidden="true">${Array.from({ length: 9 }, (_, i) =>
          `<path d="M0 ${60 + i * 85} q 150 -24 300 0 t 300 0 t 300 0 t 300 0" />`).join("")}</svg>
        ${data.areas.map(islandHTML).join("")}
      </div>
      <p class="c-hint">Click a bubble to dive in · <kbd>Ctrl K</kbd> to search · <kbd>Esc</kbd> to come back up</p>
    </main>
    <article class="c-page" id="page" hidden tabindex="-1"></article>
    <button class="c-index-btn" type="button" data-index aria-expanded="false"><span>☰</span> Index</button>
    <aside class="c-index" id="index" hidden aria-label="Index">
      ${data.areas.map((a) => `<div class="c-index-area${a.placeholder ? " is-ph" : ""}" style="--hue:${ISLANDS[a.id].hue}"><i></i>${esc(a.title)}</div>
        <ul>${a.topics.map((t) => t.placeholder ? `<li class="is-ph">${esc(t.title)}</li>` : `<li><a href="#${t.id}">${esc(t.title)}</a>
          <div class="c-index-entries">${t.entries.map((e) => `<a href="#${t.id}/${e.id}">${esc(e.title)}</a>`).join("")}</div></li>`).join("")}</ul>`).join("")}
    </aside>`;

  function pageHTML(t) {
    const hue = ISLANDS[t.area.id].hue;
    return `<div class="c-page-wrap" style="--hue:${hue}">
      <header class="c-hero">
        <a class="c-back" href="#" data-home aria-label="Back to the map">← Map</a>
        <div class="c-hero-glyph">${esc(t.glyph)}</div>
        <div><small>${esc(t.area.title)}</small><h1>${esc(t.title)}</h1><p>${esc(t.summary)}</p></div>
      </header>
      <nav class="c-chips" aria-label="Entries">${t.entries.map((e) => `<a href="#${t.id}/${e.id}">${esc(e.title)}</a>`).join("")}</nav>
      <div class="c-cards">${t.entries.map((e) => `
        <section class="c-card" id="e-${e.id}">
          ${e.pitfall ? `<span class="c-sticker" aria-hidden="true">Watch out!</span>` : ""}
          <h2>${esc(e.title)}</h2>
          <p>${md(e.explain)}</p>
          ${codeHTML(e.code)}
          <div class="c-out"><span class="c-out-label">↳ output</span>${outputHTML(e.output)}</div>
          ${e.pitfall ? `<div class="c-pit"><b>Pitfall:</b> ${md(e.pitfall.text)}
            ${e.pitfall.code ? codeHTML(e.pitfall.code) + `<div class="c-out">${outputHTML(e.pitfall.output)}</div>` : ""}</div>` : ""}
          ${e.see.length ? `<div class="c-see">${e.see.map((s) => {
            const [tid, eid] = s.split("/"), st = byId[tid], se = st.entries.find((x) => x.id === eid);
            return `<a href="#${s}" style="--hue:${ISLANDS[st.area.id].hue}">${esc(se.title)}</a>`;
          }).join("")}</div>` : ""}
        </section>`).join("")}
      </div></div>`;
  }

  // ---------- fit the world to the screen ----------
  const sea = document.getElementById("sea"), world = document.getElementById("world");
  function fit() {
    const k = Math.min((sea.clientWidth - 32) / W, 1.15);
    world.style.transform = `scale(${k})`;
    world.style.marginLeft = Math.max(0, (sea.clientWidth - 32 - W * k) / 2) + "px";
    world.parentElement.style.setProperty("--world-h", H * k + "px");
  }
  addEventListener("resize", fit);
  fit();

  // ---------- wiring ----------
  const page = document.getElementById("page"), index = document.getElementById("index"), idxBtn = app.querySelector("[data-index]");
  const toggleIndex = (open) => { index.hidden = !open; idxBtn.setAttribute("aria-expanded", open); };
  app.addEventListener("click", (e) => {
    if (e.target.closest("[data-search]")) CS.openPalette();
    if (e.target.closest("[data-index]")) toggleIndex(index.hidden);
    else if (e.target.closest(".c-index a")) toggleIndex(false);
    if (e.target.closest("[data-home]")) { e.preventDefault(); CS.go(null); }
  });

  let shown = null;
  const fade = (el, dir) => CS.reducedMotion || !CS.booted() ? Promise.resolve() :
    CS.settle(el.animate([{ opacity: 0, transform: "scale(.96)" }, { opacity: 1, transform: "none" }], { duration: 380, easing: "ease-out", direction: dir === "in" ? "normal" : "reverse", fill: "both" }), 380);
  async function render(route) {
    if (route) {
      const t = byId[route.topic];
      if (shown !== t.id) {
        if (!shown) {
          const b = sea.querySelector(`[data-tile="${t.id}"]`);
          if (b) await CS.push(sea, CS.centerOf(b), "in", { scale: 5, duration: 600 });
          sea.style.visibility = "hidden";
        }
        page.innerHTML = pageHTML(t);
        page.hidden = false;
        page.scrollTop = 0;
        if (!shown) await fade(page, "in");
        shown = t.id;
      }
      if (route.entry) CS.flash(page.querySelector(`#e-${route.entry}`));
      else page.scrollTo({ top: 0 });
      page.focus({ preventScroll: true });
    } else if (shown) {
      await fade(page, "out");
      page.hidden = true;
      sea.style.visibility = "";
      const b = sea.querySelector(`[data-tile="${shown}"]`);
      if (b) await CS.push(sea, CS.centerOf(b), "out", { scale: 5, duration: 600 });
      shown = null;
      b && b.focus({ preventScroll: true });
    }
  }
  CS.onRoute(render);
  render(CS.route());
})();
