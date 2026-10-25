// PROTOTYPE - Variant B "Workbench": IDE layout. Permanent file-tree Index, an Overview of
// live miniatures (each tile is the real Topic page, scaled down), Topic pages as notebook cells.
(function () {
  const { data, byId, esc, md, codeHTML, outputHTML } = CS;
  const app = document.getElementById("app");
  const file = (t) => t.id.replace(/-/g, "_") + ".py";

  app.innerHTML = `
    <div class="b-shell">
      <nav class="b-activity" aria-label="Panels">
        <button type="button" class="is-on" data-toggle-tree title="Explorer (Index)" aria-label="Toggle Index">⧉</button>
        <button type="button" data-search title="Search (Ctrl+K)" aria-label="Search">⌕</button>
        <a href="#" data-home title="Overview" aria-label="Overview">▦</a>
      </nav>
      <aside class="b-tree" id="tree" aria-label="Index">
        <div class="b-tree-title">INDEX</div>
        ${data.areas.map((a) => `
          <div class="b-folder${a.placeholder ? " is-ph" : ""}"><span class="b-chev">▾</span> ${a.id}/</div>
          <ul>${a.topics.map((t) => t.placeholder
            ? `<li class="b-file is-ph"><span class="b-ico">◇</span>${file(t)}<em>soon</em></li>`
            : `<li class="b-file" data-file="${t.id}"><a href="#${t.id}"><span class="b-ico">◆</span>${file(t)}</a>
                <ul class="b-outline">${t.entries.map((e) => `<li><a href="#${t.id}/${e.id}" data-ent="${t.id}/${e.id}"><span class="b-sym">ƒ</span>${esc(e.title)}</a></li>`).join("")}</ul></li>`).join("")}
          </ul>`).join("")}
      </aside>
      <section class="b-main">
        <div class="b-tabs" role="tablist">
          <a class="b-tab" href="#" data-home data-tab="overview"><span class="b-ico">▦</span> overview.md</a>
          <span class="b-tab is-topic" data-tab="topic" hidden></span>
          <button class="b-search" type="button" data-search>⌕ Search entries, code… <kbd>Ctrl K</kbd></button>
        </div>
        <div class="b-crumbs" id="crumbs"></div>
        <div class="b-editor" id="editor">
          <div class="b-overview" id="overview">
            <h1 class="b-h1"><span class="tk-com"># Python cheat sheet</span> for the stats lab</h1>
            <p class="b-sub">Click a file to zoom in. <kbd>Ctrl K</kbd> searches everything, <kbd>Esc</kbd> zooms back out.</p>
            ${data.areas.map((a) => `
              <section class="b-area${a.placeholder ? " is-ph" : ""}">
                <h2><span class="tk-com">#</span> ${esc(a.title)} <small>${esc(a.blurb)}</small></h2>
                <div class="b-grid">${a.topics.map((t) => t.placeholder
                  ? `<div class="b-tile is-ph"><div class="b-tile-head"><span class="b-ico">◇</span>${file(t)}</div><div class="b-tile-body"><span class="tk-com"># TODO: ${esc(t.title)}</span></div></div>`
                  : `<div class="b-tile" data-tile="${t.id}">
                      <a class="b-tile-head" href="#${t.id}"><span class="b-ico">◆</span>${file(t)}<span class="b-count">${t.entries.length} entries</span></a>
                      <div class="b-tile-body" aria-hidden="true" inert><div class="b-mini">${cellsHTML(t, true)}</div></div>
                      <div class="b-tile-foot">${esc(t.summary)}</div>
                    </div>`).join("")}
                </div>
              </section>`).join("")}
          </div>
          <article class="b-page" id="page" hidden tabindex="-1"></article>
        </div>
      </section>
      <footer class="b-status">
        <span>● ${esc(data.meta.versions)}</span>
        <span id="status-pos">overview</span>
        <span class="b-status-r">outputs: executed at build ✓</span>
      </footer>
    </div>`;

  function cellsHTML(t, mini) {
    return t.entries.map((e, n) => `
      <section class="b-cell" id="e-${e.id}">
        <div class="b-md"><h2>${esc(e.title)}</h2><p>${md(e.explain)}</p></div>
        <div class="b-io"><span class="b-prompt">In [${n + 1}]:</span>${codeHTML(e.code)}</div>
        <div class="b-io is-out"><span class="b-prompt">Out[${n + 1}]:</span><div class="b-out">${outputHTML(e.output)}</div></div>
        ${e.pitfall ? `<div class="b-lint"><div class="b-lint-head"><span class="b-warn">⚠</span> <b>Pitfall</b> <span class="b-lint-text">${md(e.pitfall.text)}</span></div>
          ${e.pitfall.code ? `<div class="b-lint-body">${codeHTML(e.pitfall.code)}<div class="b-out">${outputHTML(e.pitfall.output)}</div></div>` : ""}</div>` : ""}
        ${e.see.length && !mini ? `<div class="b-see"><span class="tk-com"># see also:</span> ${e.see.map((s) => {
          const [tid, eid] = s.split("/"), st = byId[tid], se = st.entries.find((x) => x.id === eid);
          return `<a href="#${s}">${file(st)} › ${esc(se.title)}</a>`;
        }).join(", ")}</div>` : ""}
      </section>`).join("");
  }

  // ---------- wiring ----------
  const shell = app.querySelector(".b-shell"), overview = document.getElementById("overview"), page = document.getElementById("page");
  const crumbs = document.getElementById("crumbs"), topicTab = app.querySelector('[data-tab="topic"]'), pos = document.getElementById("status-pos");
  const narrow = matchMedia("(max-width: 760px)");
  if (narrow.matches) shell.classList.add("no-tree");
  app.addEventListener("click", (e) => {
    if (e.target.closest("[data-search]")) CS.openPalette();
    if (e.target.closest("[data-toggle-tree]")) shell.classList.toggle("no-tree");
    if (e.target.closest("[data-home]")) { e.preventDefault(); CS.go(null); }
    if (narrow.matches && e.target.closest(".b-tree a")) shell.classList.add("no-tree");
    const tile = e.target.closest("[data-tile]");
    if (tile && !e.target.closest("a")) CS.go(tile.dataset.tile);
  });

  let shown = null;
  function chrome(route) {
    app.querySelectorAll(".b-file").forEach((f) => f.classList.toggle("is-open", !!route && f.dataset.file === route.topic));
    app.querySelectorAll("[data-ent]").forEach((a) => a.classList.toggle("is-cur", !!route && a.dataset.ent === route.topic + "/" + route.entry));
    app.querySelector('[data-tab="overview"]').classList.toggle("is-active", !route);
    topicTab.hidden = !route;
    if (route) {
      const t = byId[route.topic], e = route.entry && t.entries.find((x) => x.id === route.entry);
      topicTab.classList.add("is-active");
      topicTab.innerHTML = `<span class="b-ico">◆</span> ${file(t)} <a href="#" data-home aria-label="Close tab">×</a>`;
      crumbs.innerHTML = `<a href="#" data-home>cheat-sheet</a> › ${t.area.id} › <b>${file(t)}</b>${e ? ` › <span class="b-sym">ƒ</span> ${esc(e.title)}` : ""}`;
      pos.textContent = `${file(t)}${e ? " · " + e.title : ""}`;
    } else {
      crumbs.innerHTML = `<a href="#" data-home>cheat-sheet</a> › <b>overview.md</b>`;
      pos.textContent = "overview";
    }
  }
  async function render(route) {
    chrome(route);
    if (route) {
      const t = byId[route.topic];
      if (shown !== t.id) {
        page.innerHTML = `<header class="b-page-head"><h1><span class="tk-com">#</span> ${esc(t.title)}</h1><p>${esc(t.summary)}</p></header>${cellsHTML(t)}`;
        page.hidden = false;
        page.scrollTop = 0;
        if (!shown) await CS.zoom(overview.querySelector(`[data-tile="${t.id}"] .b-tile-body`), page, "in", { radius: "6px", duration: 560 });
        shown = t.id;
      }
      if (route.entry) CS.flash(page.querySelector(`#e-${route.entry}`));
      else page.scrollTo({ top: 0 });
      page.focus({ preventScroll: true });
    } else if (shown) {
      const tile = overview.querySelector(`[data-tile="${shown}"]`);
      tile && tile.scrollIntoView({ block: "nearest" });
      await CS.zoom(tile && tile.querySelector(".b-tile-body"), page, "out", { radius: "6px", duration: 420 });
      page.hidden = true;
      shown = null;
      tile && tile.querySelector("a").focus({ preventScroll: true });
    }
  }
  CS.onRoute(render);
  render(CS.route());
})();
