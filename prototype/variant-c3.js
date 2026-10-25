// PROTOTYPE - Variant C3 "Trail": a vertical journey. Each Area is a land the trail winds
// through; Topics are numbered stepping stones in learning order. The Topic page puts code and
// its Output side by side and ends with "Next stop".
(function () {
  const { data, byId, esc, md, codeHTML, outputHTML } = CS;
  const { HUE, seeHTML, trailLand, landRailHTML, watchLands } = CC;
  const app = document.getElementById("app");
  const realTopics = CS.topics.filter((t) => !t.placeholder);

  app.innerHTML = `
    <div class="c3-top">
      <div class="c-logo"><span>py</span> cheat&nbsp;trail</div>
      <button class="c-searchpill" type="button" data-search><span class="c-ico">⌕</span> What do you need to remember? <kbd>Ctrl K</kbd></button>
    </div>
    ${landRailHTML(data.areas)}
    <main class="c3-trail" id="trail">
      <p class="c3-start">Start here <span>↓</span><small>Pick any stone to dive in · <kbd>Ctrl K</kbd> search · <kbd>Esc</kbd> back</small></p>
      ${data.areas.map(trailLand).join("")}
    </main>
    <article class="c3-page" id="page" hidden tabindex="-1"></article>`;

  function pageHTML(t) {
    const k = realTopics.findIndex((x) => x.id === t.id), inArea = t.area.topics.filter((x) => !x.placeholder);
    const prev = realTopics[k - 1], next = realTopics[k + 1];
    return `<div class="c3-wrap" style="--hue:${HUE[t.area.id]}">
      <header class="c3-head">
        <a class="c3-back" href="#" data-home>← Back to the trail</a>
        <div class="c3-head-stone">${esc(t.glyph)}</div>
        <small>Stop ${inArea.findIndex((x) => x.id === t.id) + 1} of ${inArea.length} · ${esc(t.area.title)}</small>
        <h1>${esc(t.title)}</h1>
        <p>${esc(t.summary)}</p>
      </header>
      <ol class="c3-steps">${t.entries.map((e) => `
        <li class="c3-card" id="e-${e.id}">
          <h2>${esc(e.title)}</h2>
          <p>${md(e.explain)}</p>
          <div class="c3-io${e.output.figures.length ? " has-fig" : ""}">
            ${codeHTML(e.code)}
            <div class="c3-out"><span>Output</span>${outputHTML(e.output)}</div>
          </div>
          ${e.pitfall ? `<div class="c3-pit"><span class="c3-pit-tag">Watch out</span><p>${md(e.pitfall.text)}</p>
            ${e.pitfall.code ? `<div class="c3-io">${codeHTML(e.pitfall.code)}<div class="c3-out"><span>Output</span>${outputHTML(e.pitfall.output)}</div></div>` : ""}</div>` : ""}
          ${seeHTML(e)}
        </li>`).join("")}
      </ol>
      <nav class="c3-next">
        ${prev ? `<a href="#${prev.id}" class="is-prev" style="--hue:${HUE[prev.area.id]}"><small>Previous stop</small>${esc(prev.title)}</a>` : "<span></span>"}
        ${next ? `<a href="#${next.id}" class="is-next" style="--hue:${HUE[next.area.id]}"><small>Next stop</small>${esc(next.title)} →</a>` : "<span></span>"}
      </nav>
    </div>`;
  }

  const page = document.getElementById("page"), trail = document.getElementById("trail");
  app.addEventListener("click", (e) => {
    if (e.target.closest("[data-search]")) CS.openPalette();
    if (e.target.closest("[data-home]")) { e.preventDefault(); CS.go(null); }
  });
  watchLands(app);

  let shown = null;
  async function render(route) {
    if (route) {
      const t = byId[route.topic];
      if (shown !== t.id) {
        const first = !shown;
        page.innerHTML = pageHTML(t);
        page.hidden = false;
        document.documentElement.classList.add("c3-locked");
        page.scrollTop = 0;
        if (first) await CS.zoom(trail.querySelector(`[data-tile="${t.id}"]`), page, "in", { radius: "50%", duration: 560 });
        shown = t.id;
      }
      if (route.entry) CS.flash(page.querySelector(`#e-${route.entry}`));
      else page.scrollTo({ top: 0 });
      page.focus({ preventScroll: true });
    } else if (shown) {
      const stone = trail.querySelector(`[data-tile="${shown}"]`);
      document.documentElement.classList.remove("c3-locked");
      stone && stone.scrollIntoView({ block: "center" });
      await CS.zoom(stone, page, "out", { radius: "50%", duration: 460 });
      page.hidden = true;
      shown = null;
      stone && stone.focus({ preventScroll: true });
    }
  }
  CS.onRoute(render);
  render(CS.route());
})();
