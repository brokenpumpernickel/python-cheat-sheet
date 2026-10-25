// PROTOTYPE - helpers shared by the Islands variations (C2, C3): hues and the card-style Topic page.
window.CC = (function () {
  const { byId, esc, md, codeHTML, outputHTML, L } = CS;
  const UI = {
    en: { map: "← Map", watch: "Watch out!", pitfall: "Pitfall:", output: "↳ output", seeAlso: "See also", prev: "Previous stop", next: "Next stop", soon: "coming soon", back: "Back to the map" },
    pl: { map: "← Mapa", watch: "Uwaga!", pitfall: "Pułapka:", output: "↳ wynik", seeAlso: "Zobacz też", prev: "Poprzedni przystanek", next: "Następny przystanek", soon: "wkrótce", back: "Wróć do mapy" },
  };
  const t = (key) => CS.t(key, UI);
  const tt = t, lang = CS.lang, UI_map = () => t("map"); // aliases for functions whose parameter `t` is a Topic
  const HUE = { "python-basics": 160, numpy: 265, pandas: 205, matplotlib: 22, "scipy-stats": 335 };
  const BLOBS = ["46% 54% 58% 42% / 44% 40% 60% 56%", "58% 42% 38% 62% / 52% 58% 42% 48%", "40% 60% 55% 45% / 60% 45% 55% 40%"];

  function seeHTML(e) {
    return e.see.length ? `<div class="c-see" data-label="${t("seeAlso")}">${e.see.map((s) => {
      const [tid, eid] = s.split("/"), st = byId[tid], se = st.entries.find((x) => x.id === eid);
      return `<a href="#${s}" style="--hue:${HUE[st.area.id]}">${esc(L(se, "title"))}</a>`;
    }).join("")}</div>` : "";
  }

  // Same Topic page as variant C: coloured hero, sticky chips, masonry of cards.
  // Previous / Next stop in Topic order (= learning order).
  function pagerHTML(t) {
    const real = CS.topics.filter((x) => !x.placeholder), k = real.findIndex((x) => x.id === t.id);
    const prev = real[k - 1], next = real[k + 1];
    return `<nav class="c3-next">
      ${prev ? `<a href="#${prev.id}" class="is-prev" style="--hue:${HUE[prev.area.id]}"><small>${tt("prev")}</small>← ${esc(L(prev, "title"))}</a>` : "<span></span>"}
      ${next ? `<a href="#${next.id}" class="is-next" style="--hue:${HUE[next.area.id]}"><small>${tt("next")}</small>${esc(L(next, "title"))} →</a>` : "<span></span>"}
    </nav>`;
  }

  function pageHTML(t, backLabel = null, opts = {}) {
    return `<div class="c-page-wrap" style="--hue:${HUE[t.area.id]}">
      <header class="c-hero">
        <a class="c-back" href="#" data-home aria-label="${tt("back")}">${backLabel || UI_map()}</a>
        <div class="c-hero-glyph">${esc(t.glyph)}</div>
        <div><small>${esc(L(t.area, "title"))}</small><h1>${esc(L(t, "title"))}</h1><p>${esc(L(t, "summary"))}</p></div>
      </header>
      <nav class="c-chips" aria-label="Entries">${t.entries.map((e) => `<a href="#${t.id}/${e.id}">${esc(L(e, "title"))}</a>`).join("")}</nav>
      <div class="c-cards">${t.entries.map((e) => `
        <section class="c-card" id="e-${e.id}">
          ${e.pitfall ? `<span class="c-sticker" aria-hidden="true">${tt("watch")}</span>` : ""}
          <h2>${esc(L(e, "title"))}</h2>
          <p>${md(L(e, "explain"))}</p>
          ${codeHTML(e.code)}
          <div class="c-out"><span class="c-out-label">${tt("output")}</span>${outputHTML(e.output)}</div>
          ${e.pitfall ? `<div class="c-pit"><b>${tt("pitfall")}</b> ${md(lang() === "pl" ? e.pl.pitfall : e.pitfall.text)}
            ${e.pitfall.code ? codeHTML(e.pitfall.code) + `<div class="c-out">${outputHTML(e.pitfall.output)}</div>` : ""}</div>` : ""}
          ${seeHTML(e)}
        </section>`).join("")}
      </div>${opts.pager ? pagerHTML(t) : ""}</div>`;
  }

  // ---------- the trail (one "land" per Area, Topics as numbered stepping stones) ----------
  const STEP = 132, TOP = 70;
  const stones = (a, ai) => a.topics.map((t, j) => ({ t, x: 50 + 30 * Math.sin(j * 1.15 + ai * 2), y: TOP + j * STEP }));
  function pathD(pts) {
    const all = [{ x: pts[0].x, y: pts[0].y - TOP }, ...pts, { x: pts[pts.length - 1].x, y: pts[pts.length - 1].y + TOP }];
    let d = `M ${all[0].x} ${all[0].y}`;
    for (let i = 1; i < all.length; i++) {
      const p = all[i - 1], q = all[i], my = (p.y + q.y) / 2;
      d += ` C ${p.x} ${my}, ${q.x} ${my}, ${q.x} ${q.y}`;
    }
    return d;
  }
  function trailLand(a, ai) {
    const pts = stones(a, ai), h = TOP * 2 + (a.topics.length - 1) * STEP;
    let n = 0;
    return `<section class="c3-land${a.placeholder ? " is-ph" : ""}" id="land-${a.id}" style="--hue:${HUE[a.id]}">
      <header class="c3-sign"><b>${esc(L(a, "title"))}</b><span>${esc(L(a, "blurb"))}</span>${a.placeholder ? `<em>${t("soon")}</em>` : ""}</header>
      <div class="c3-path" style="height:${h}px">
        <svg viewBox="0 0 100 ${h}" preserveAspectRatio="none" aria-hidden="true"><path d="${pathD(pts)}" /></svg>
        ${pts.map(({ t, x, y }) => t.placeholder
          ? `<div class="c3-stone is-ph" style="left:${x}%;top:${y}px"><span class="c3-glyph">${esc(t.glyph)}</span><span class="c3-label">${esc(L(t, "title"))}</span></div>`
          : `<a class="c3-stone${x > 50 ? " is-right" : ""}" href="#${t.id}" data-tile="${t.id}" style="left:${x}%;top:${y}px">
              <i>${++n}</i><span class="c3-glyph">${esc(t.glyph)}</span>
              <span class="c3-label"><b>${esc(L(t, "title"))}</b>${esc(L(t, "summary"))}</span></a>`).join("")}
      </div></section>`;
  }
  // Dots on the left edge that jump to each land; call watchLands() once the trail is in the DOM.
  const landRailHTML = (areas) => `<nav class="c3-rail" aria-label="Areas">${areas.map((a) => `
    <button type="button" data-land="${a.id}" style="--hue:${HUE[a.id]}" class="${a.placeholder ? "is-ph" : ""}"><i></i><span>${esc(L(a, "title"))}</span></button>`).join("")}</nav>`;
  function watchLands(root) {
    root.addEventListener("click", (e) => {
      const l = e.target.closest("[data-land]");
      if (l) document.getElementById("land-" + l.dataset.land).scrollIntoView({ behavior: CS.reducedMotion ? "auto" : "smooth" });
    });
    const io = new IntersectionObserver((es) => es.forEach((en) => {
      if (en.isIntersecting) root.querySelectorAll("[data-land]").forEach((b) => b.classList.toggle("is-on", "land-" + b.dataset.land === en.target.id));
    }), { rootMargin: "-45% 0px -50% 0px" });
    root.querySelectorAll(".c3-land").forEach((s) => io.observe(s));
  }

  const fade = (el, dir, ms = 360) => CS.reducedMotion || !CS.booted() ? Promise.resolve() :
    CS.settle(el.animate([{ opacity: 0, transform: "translateY(12px)" }, { opacity: 1, transform: "none" }],
      { duration: ms, easing: "ease-out", direction: dir === "in" ? "normal" : "reverse", fill: "both" }), ms);

  return { HUE, BLOBS, seeHTML, pageHTML, fade, trailLand, landRailHTML, watchLands, t };
})();
