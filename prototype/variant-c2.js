// PROTOTYPE - Variant C2 "Archipelago + mini-map": islands lay themselves out (no hand-placed
// coordinates), and once you zoom into a Topic the map shrinks into a side rail that is the Index.
(function () {
  const { data, byId, esc } = CS;
  const { HUE, BLOBS, pageHTML, fade } = CC;
  const app = document.getElementById("app");

  const island = (a, i) => `
    <section class="c2-island${a.placeholder ? " is-ph" : ""}" style="--hue:${HUE[a.id]};--n:${a.topics.length};--i:${i};border-radius:${BLOBS[i % 3]}">
      <div class="c-flag"><b>${esc(a.title)}</b>${a.placeholder ? "<small>coming soon</small>" : ""}</div>
      <div class="c2-bubbles">${a.topics.map((t, j) => t.placeholder
        ? `<div class="c-bubble is-ph" style="--j:${j}"><span class="c-glyph">${esc(t.glyph)}</span><span class="c-name">${esc(t.title)}</span></div>`
        : `<a class="c-bubble" href="#${t.id}" data-tile="${t.id}" style="--j:${j}"><span class="c-glyph">${esc(t.glyph)}</span><span class="c-name">${esc(t.title)}</span></a>`).join("")}
      </div>
    </section>`;

  const mini = (a, i) => `
    <div class="c2-mini${a.placeholder ? " is-ph" : ""}" style="--hue:${HUE[a.id]};border-radius:${BLOBS[(i + 1) % 3]}">
      <b>${esc(a.title)}</b>
      <div class="c2-pins">${a.topics.map((t) => t.placeholder
        ? `<span class="c2-pin is-ph">${esc(t.title)}</span>`
        : `<a class="c2-pin" href="#${t.id}" data-pin="${t.id}"><span>${esc(t.glyph)}</span>${esc(t.title)}</a>`).join("")}
      </div>
    </div>`;

  app.innerHTML = `
    <div class="c-top">
      <div class="c-logo"><span>py</span> cheat&nbsp;map</div>
      <button class="c-searchpill" type="button" data-search><span class="c-ico">⌕</span> What do you need to remember? <kbd>Ctrl K</kbd></button>
    </div>
    <div class="c2-layout" id="layout">
      <aside class="c2-rail" id="rail" aria-label="Index">
        <a class="c2-rail-home" href="#" data-home>← Whole map</a>
        ${data.areas.map(mini).join("")}
      </aside>
      <main class="c2-sea" id="sea">
        ${data.areas.map(island).join("")}
        <p class="c-hint">Click a bubble to dive in · <kbd>Ctrl K</kbd> to search · <kbd>Esc</kbd> to come back up</p>
      </main>
      <article class="c2-page" id="page" hidden tabindex="-1"></article>
    </div>`;

  const layout = document.getElementById("layout"), sea = document.getElementById("sea"), page = document.getElementById("page"), rail = document.getElementById("rail");
  app.addEventListener("click", (e) => {
    if (e.target.closest("[data-search]")) CS.openPalette();
    if (e.target.closest("[data-home]")) { e.preventDefault(); CS.go(null); }
  });

  let shown = null;
  function markPin(id) {
    rail.querySelectorAll("[data-pin]").forEach((p) => p.classList.toggle("is-here", p.dataset.pin === id));
    const here = rail.querySelector(".is-here");
    here && here.scrollIntoView({ block: "nearest", inline: "center" });
  }
  async function render(route) {
    if (route) {
      const t = byId[route.topic];
      if (shown !== t.id) {
        if (!shown) {
          const b = sea.querySelector(`[data-tile="${t.id}"]`);
          if (b) await CS.push(sea, CS.centerOf(b), "in", { scale: 4, duration: 520 });
          layout.classList.add("is-topic");
          scrollTo(0, 0);
          page.innerHTML = pageHTML(t);
          page.hidden = false;
          markPin(t.id);
          await Promise.all([fade(page, "in"), CS.reducedMotion || !CS.booted() ? null :
            CS.settle(rail.animate([{ transform: "translateX(-40px)", opacity: 0 }, { transform: "none", opacity: 1 }], { duration: 420, easing: "ease-out" }), 420)]);
        } else {
          await fade(page, "out", 160);
          page.innerHTML = pageHTML(t);
          scrollTo(0, 0);
          markPin(t.id);
          await fade(page, "in", 260);
        }
        shown = t.id;
      }
      if (route.entry) CS.flash(page.querySelector(`#e-${route.entry}`));
      else scrollTo({ top: 0 });
      page.focus({ preventScroll: true });
    } else if (shown) {
      await fade(page, "out", 220);
      page.hidden = true;
      layout.classList.remove("is-topic");
      markPin(null);
      const b = sea.querySelector(`[data-tile="${shown}"]`);
      b && b.scrollIntoView({ block: "center" });
      if (b) await CS.push(sea, CS.centerOf(b), "out", { scale: 4, duration: 520 });
      shown = null;
      b && b.focus({ preventScroll: true });
    }
  }
  CS.onRoute(render);
  render(CS.route());
})();
