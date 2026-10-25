// PROTOTYPE - Variant A "Atlas": editorial. The Overview *is* a typographic index;
// a Topic page reads like a magazine article with Pitfalls as margin notes.
(function () {
  const { data, byId, esc, md, codeHTML, outputHTML } = CS;
  const roman = ["I", "II", "III", "IV", "V", "VI", "VII"];
  const app = document.getElementById("app");
  const realTopics = CS.topics.filter((t) => !t.placeholder);

  app.innerHTML = `
    <header class="a-mast">
      <a class="a-brand" href="#" data-home>
        <span class="a-brand-mark">Py</span>
        <span><b>The Stats Lab Python Atlas</b><small>A field reference for the statistics &amp; probability lab</small></span>
      </a>
      <div class="a-mast-tools">
        <button class="a-search" type="button" data-search><span>Search the atlas…</span><kbd>Ctrl K</kbd></button>
        <button class="a-index-btn" type="button" data-index aria-expanded="false">Index</button>
      </div>
    </header>
    <main class="a-overview" id="overview">
      <p class="a-lede">Everything you learned in the intro course, <em>condensed</em>. Pick a topic, or jump straight to an entry.</p>
      ${data.areas.map((a, i) => areaHTML(a, i)).join("")}
      <footer class="a-foot">Examples executed with ${esc(data.meta.versions)}. Every output on this page was produced by running the code.</footer>
    </main>
    <article class="a-page" id="page" hidden tabindex="-1"></article>
    <aside class="a-index" id="index" hidden>
      <div class="a-index-head"><b>Index</b><button type="button" data-index-close aria-label="Close index">×</button></div>
      <nav>${data.areas.map((a, i) => `
        <div class="a-index-area${a.placeholder ? " is-ph" : ""}"><span>${roman[i]}.</span> ${esc(a.title)}</div>
        <ul>${a.topics.map((t) => t.placeholder ? `<li class="is-ph">${esc(t.title)}</li>` : `
          <li><a href="#${t.id}">${esc(t.title)}</a>
            <ul>${t.entries.map((e) => `<li><a href="#${t.id}/${e.id}">${esc(e.title)}</a></li>`).join("")}</ul></li>`).join("")}
        </ul>`).join("")}
      </nav>
    </aside>`;

  function areaHTML(a, i) {
    return `<section class="a-area${a.placeholder ? " is-ph" : ""}">
      <header class="a-area-head">
        <span class="a-area-num">${roman[i]}</span>
        <h2>${esc(a.title)}</h2>
        <p>${esc(a.blurb)}</p>
        ${a.placeholder ? `<span class="a-stamp">In preparation</span>` : ""}
      </header>
      <div class="a-topics">${a.topics.map((t, j) => t.placeholder
        ? `<div class="a-topic is-ph"><h3>${esc(t.title)}</h3><p>Coming soon</p></div>`
        : `<div class="a-topic" data-tile="${t.id}">
            <a class="a-topic-link" href="#${t.id}"><span class="a-topic-num">${roman[i]}.${j + 1}</span><h3>${esc(t.title)}</h3></a>
            <p class="a-topic-sum">${esc(t.summary)}</p>
            <p class="a-topic-entries">${t.entries.map((e) => `<a href="#${t.id}/${e.id}">${esc(e.title)}</a>`).join(" <span>·</span> ")}</p>
          </div>`).join("")}
      </div></section>`;
  }

  function pageHTML(t) {
    const ai = data.areas.indexOf(t.area), ti = t.area.topics.findIndex((x) => x.id === t.id);
    const k = realTopics.findIndex((x) => x.id === t.id);
    const prev = realTopics[k - 1], next = realTopics[k + 1];
    return `<div class="a-page-inner">
      <nav class="a-crumbs"><a href="#" data-home>Atlas</a> <span>›</span> ${esc(t.area.title)} <span>›</span> <b>${esc(t.title)}</b>
        <span class="a-crumbs-hint"><kbd>Esc</kbd> back to the atlas</span></nav>
      <header class="a-page-head">
        <span class="a-kicker">${roman[ai]}.${ti + 1} · ${esc(t.area.title)}</span>
        <h1>${esc(t.title)}</h1>
        <p class="a-dek">${esc(t.summary)}</p>
      </header>
      <div class="a-page-grid">
        <nav class="a-toc" aria-label="On this page"><b>On this page</b>
          <ol>${t.entries.map((e) => `<li><a href="#${t.id}/${e.id}">${esc(e.title)}</a></li>`).join("")}</ol></nav>
        <div class="a-entries">${t.entries.map((e, n) => entryHTML(t, e, n)).join("")}</div>
      </div>
      <nav class="a-pager">
        ${prev ? `<a href="#${prev.id}"><small>Previous</small>${esc(prev.title)}</a>` : "<span></span>"}
        ${next ? `<a href="#${next.id}" class="is-next"><small>Next</small>${esc(next.title)}</a>` : "<span></span>"}
      </nav>
    </div>`;
  }

  function entryHTML(t, e, n) {
    const see = e.see.map((s) => {
      const [tid, eid] = s.split("/"), st = byId[tid], se = st && st.entries.find((x) => x.id === eid);
      return se ? `<a href="#${s}">${esc(se.title)}</a> <small>(${esc(st.title)})</small>` : "";
    }).join(", ");
    return `<section class="a-entry" id="e-${e.id}">
      <div class="a-entry-main">
        <h2><span>§${n + 1}</span> ${esc(e.title)}</h2>
        <p>${md(e.explain)}</p>
        ${codeHTML(e.code)}
        <div class="a-out"><span class="a-label">Output</span>${outputHTML(e.output)}</div>
        ${see ? `<p class="a-see">See also: ${see}</p>` : ""}
      </div>
      ${e.pitfall ? `<aside class="a-pitfall"><span class="a-label">Pitfall</span><p>${md(e.pitfall.text)}</p>
        ${e.pitfall.code ? codeHTML(e.pitfall.code) + `<div class="a-out">${outputHTML(e.pitfall.output)}</div>` : ""}</aside>` : ""}
    </section>`;
  }

  // ---------- wiring ----------
  const overview = document.getElementById("overview"), page = document.getElementById("page"), index = document.getElementById("index");
  app.addEventListener("click", (e) => {
    if (e.target.closest("[data-search]")) CS.openPalette();
    if (e.target.closest("[data-index]")) toggleIndex(index.hidden);
    if (e.target.closest("[data-index-close]")) toggleIndex(false);
    if (e.target.closest("[data-home]")) { e.preventDefault(); CS.go(null); }
    if (e.target.closest(".a-index a")) toggleIndex(false);
  });
  function toggleIndex(open) {
    index.hidden = !open;
    app.querySelector("[data-index]").setAttribute("aria-expanded", open);
  }

  let shown = null;
  async function render(route) {
    if (route) {
      const t = byId[route.topic];
      if (shown !== t.id) {
        page.innerHTML = pageHTML(t);
        page.hidden = false;
        document.documentElement.classList.add("a-locked");
        page.scrollTop = 0;
        const tile = overview.querySelector(`[data-tile="${t.id}"]`);
        if (!shown) await CS.zoom(tile, page, "in", { radius: "2px" });
        shown = t.id;
      }
      if (route.entry) CS.flash(page.querySelector(`#e-${route.entry}`));
      else page.scrollTo({ top: 0 });
      page.focus({ preventScroll: true });
    } else if (shown) {
      const tile = overview.querySelector(`[data-tile="${shown}"]`);
      document.documentElement.classList.remove("a-locked");
      await CS.zoom(tile, page, "out", { radius: "2px" });
      page.hidden = true;
      shown = null;
      tile && tile.querySelector("a").focus({ preventScroll: true });
    }
  }
  CS.onRoute(render);
  render(CS.route());
})();
