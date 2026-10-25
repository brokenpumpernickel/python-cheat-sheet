// PROTOTYPE - throwaway. Plumbing shared by the three mockup variants:
// routing, search, highlighting, zoom animation, variant switcher.
(function () {
  const data = window.CONTENT;
  const topics = [];
  for (const area of data.areas) for (const t of area.topics) topics.push({ ...t, area });
  const byId = Object.fromEntries(topics.map((t) => [t.id, t]));

  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---------- Language (ADR 0005): English default, remembered per visitor, ?lang=pl forces it ----------
  const UI = {
    en: { copy: "Copy", copied: "Copied", search: "Search topics, entries and code…", noMatch: "No matches for", move: "move", open: "open", close: "close" },
    pl: { copy: "Kopiuj", copied: "Skopiowano", search: "Szukaj tematów, haseł i kodu…", noMatch: "Brak wyników dla", move: "wybór", open: "otwórz", close: "zamknij" },
  };
  const urlLang = new URLSearchParams(location.search).get("lang");
  let lang = "en";
  try { lang = localStorage.getItem("cs-proto-lang") || "en"; } catch {}
  if (urlLang === "pl" || urlLang === "en") lang = urlLang;
  document.documentElement.lang = lang;
  const langListeners = [];
  function setLang(l) {
    lang = l;
    document.documentElement.lang = l;
    try { localStorage.setItem("cs-proto-lang", l); } catch {}
    const u = new URL(location.href);
    if (u.searchParams.has("lang")) { u.searchParams.set("lang", l); history.replaceState(history.state, "", u); }
    langListeners.forEach((fn) => fn(l));
  }
  const t = (key, dict) => ((dict || UI)[lang] || {})[key] ?? (dict || UI).en[key];
  // Field of a content object in the current Language (content carries Polish under .pl).
  const L = (obj, field) => (lang === "pl" && obj.pl && obj.pl[field] != null ? obj.pl[field] : obj[field]);
  // No zoom on the very first render (a deep link has no tile to come from).
  let booted = false;
  setTimeout(() => (booted = true), 100);
  // anim.finished never settles while a page isn't painting (background tab), so race a timer.
  const settle = (anim, ms) => Promise.race([anim.finished, new Promise((r) => setTimeout(r, ms + 150))]).then(() => anim.cancel());

  // ---------- routing: #topic or #topic/entry ----------
  function parse() {
    const [topic, entry] = decodeURIComponent(location.hash.slice(1)).split("/");
    return topic && byId[topic] && !byId[topic].placeholder ? { topic, entry: entry || null } : null;
  }
  let current = parse();
  const listeners = [];
  addEventListener("hashchange", () => {
    const prev = current;
    current = parse();
    listeners.forEach((fn) => fn(current, prev));
  });
  function go(topic, entry) {
    const h = topic ? "#" + topic + (entry ? "/" + entry : "") : "";
    if (h === location.hash || (!h && !location.hash)) {
      listeners.forEach((fn) => fn(current, current));
      return;
    }
    if (h) location.hash = h;
    else history.pushState(null, "", location.pathname + location.search), window.dispatchEvent(new HashChangeEvent("hashchange"));
  }

  // ---------- text helpers ----------
  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  function md(s) {
    return esc(s)
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/\*([^*]+)\*/g, "<em>$1</em>");
  }
  const KW = new Set("def return if elif else for while in not and or is import from as lambda True False None break continue pass with try except raise class".split(" "));
  const BI = new Set("print len sum min max range enumerate zip sorted type int float str list dict set tuple round abs".split(" "));
  function highlight(code) {
    const re = /(#[^\n]*)|("(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)|([^\w\s])/g;
    let out = "", last = 0, m, prevWord = "";
    while ((m = re.exec(code))) {
      out += esc(code.slice(last, m.index));
      last = re.lastIndex;
      const [tok, com, str, num, word] = m;
      if (com) out += `<span class="tk-com">${esc(tok)}</span>`;
      else if (str) out += `<span class="tk-str">${esc(tok)}</span>`;
      else if (num) out += `<span class="tk-num">${tok}</span>`;
      else if (word) {
        const cls = KW.has(word) ? "tk-kw" : BI.has(word) ? "tk-bi" : prevWord === "def" ? "tk-fn" : "";
        out += cls ? `<span class="${cls}">${word}</span>` : word;
        prevWord = word;
        continue;
      } else out += `<span class="tk-op">${esc(tok)}</span>`;
      prevWord = "";
    }
    return out + esc(code.slice(last));
  }
  function codeHTML(code) {
    return `<div class="cs-code"><button class="cs-copy" type="button" data-copy="${esc(code).replace(/"/g, "&quot;")}" aria-label="${t("copy")}">${t("copy")}</button><pre><code>${highlight(code)}</code></pre></div>`;
  }
  function outputHTML(o) {
    let h = "";
    if (o.text) h += `<pre class="cs-out-text">${esc(o.text)}</pre>`;
    if (o.error) h += `<pre class="cs-out-error">${esc(o.error)}</pre>`;
    for (const svg of o.figures) h += `<img class="cs-out-fig" alt="Figure produced by the code above" src="data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}">`;
    return h;
  }
  document.addEventListener("click", async (e) => {
    const b = e.target.closest(".cs-copy");
    if (!b) return;
    const ta = document.createElement("textarea");
    ta.innerHTML = b.dataset.copy;
    try { await navigator.clipboard.writeText(ta.value); } catch {}
    b.textContent = t("copied");
    setTimeout(() => (b.textContent = t("copy")), 1200);
  });

  // ---------- search ----------
  const docs = [];
  for (const t of topics) {
    if (t.placeholder) continue;
    // Both Languages are searchable, whichever one is active.
    docs.push({ topic: t, entry: null, title: t.title + "\n" + t.pl.title, body: t.summary + "\n" + t.pl.summary });
    for (const e of t.entries) docs.push({ topic: t, entry: e, title: e.title + "\n" + e.pl.title, body: [e.explain, e.pl.explain, e.code].join("\n") });
  }
  function search(q) {
    const words = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!words.length) return [];
    const res = [];
    for (const d of docs) {
      const title = d.title.toLowerCase(), tt = (d.topic.title + " " + d.topic.pl.title).toLowerCase(), body = d.body.toLowerCase();
      let score = 0;
      for (const w of words) {
        if (title.split("\n").some((x) => x.startsWith(w))) score += 6;
        else if (title.includes(w)) score += 4;
        else if (tt.includes(w)) score += 2;
        else if (body.includes(w)) score += 1;
        else { score = 0; break; }
      }
      if (score) res.push({ ...d, score });
    }
    return res.sort((a, b) => b.score - a.score).slice(0, 12);
  }

  // ---------- search palette (markup shared, each variant styles it) ----------
  let palette;
  function openPalette() {
    if (palette && palette.lang !== lang) { palette.remove(); palette = null; }
    if (!palette) {
      palette = document.createElement("div");
      palette.className = "cs-palette";
      palette.lang = lang;
      palette.innerHTML = `<div class="cs-palette-backdrop"></div><div class="cs-palette-box" role="dialog" aria-label="Search">
        <input class="cs-palette-input" type="search" placeholder="${t("search")}" aria-label="${t("search")}" autocomplete="off">
        <ul class="cs-palette-list" role="listbox"></ul>
        <div class="cs-palette-hint"><span><kbd>↑</kbd><kbd>↓</kbd> ${t("move")}</span><span><kbd>Enter</kbd> ${t("open")}</span><span><kbd>Esc</kbd> ${t("close")}</span></div></div>`;
      document.body.appendChild(palette);
      const input = palette.querySelector("input"), list = palette.querySelector("ul");
      let sel = 0, results = [];
      const render = () => {
        results = search(input.value);
        sel = Math.min(sel, Math.max(results.length - 1, 0));
        list.innerHTML = input.value && !results.length
          ? `<li class="cs-palette-empty">${t("noMatch")} “${esc(input.value)}”</li>`
          : results.map((r, i) => `<li role="option" class="cs-palette-item${i === sel ? " is-sel" : ""}" data-i="${i}">
              <span class="cs-palette-title">${esc(L(r.entry || r.topic, "title"))}</span>
              <span class="cs-palette-path">${esc(L(r.topic.area, "title"))} › ${esc(L(r.topic, "title"))}</span></li>`).join("");
      };
      const pick = (r) => { closePalette(); go(r.topic.id, r.entry && r.entry.id); };
      input.addEventListener("input", () => { sel = 0; render(); });
      input.addEventListener("keydown", (e) => {
        if (e.key === "ArrowDown") { sel = Math.min(sel + 1, results.length - 1); render(); e.preventDefault(); }
        if (e.key === "ArrowUp") { sel = Math.max(sel - 1, 0); render(); e.preventDefault(); }
        if (e.key === "Enter" && results[sel]) pick(results[sel]);
      });
      list.addEventListener("click", (e) => { const li = e.target.closest("[data-i]"); if (li) pick(results[+li.dataset.i]); });
      palette.querySelector(".cs-palette-backdrop").addEventListener("click", closePalette);
      palette.render = render;
    }
    palette.classList.add("is-open");
    const input = palette.querySelector("input");
    input.value = "";
    palette.render();
    input.focus();
  }
  function closePalette() { palette && palette.classList.remove("is-open"); }
  const paletteOpen = () => palette && palette.classList.contains("is-open");

  const typing = (el) => el && (el.matches("input, textarea, [contenteditable]"));
  addEventListener("keydown", (e) => {
    if ((e.key === "k" && (e.ctrlKey || e.metaKey)) || (e.key === "/" && !typing(document.activeElement))) {
      e.preventDefault();
      openPalette();
    } else if (e.key === "Escape") {
      if (paletteOpen()) closePalette();
      else if (current && !typing(document.activeElement)) go(null);
    }
  });

  // ---------- semantic zoom (FLIP between a tile and a page) ----------
  // Animates `page` so it appears to grow out of `tile` (or shrink back into it).
  function zoom(tile, page, direction, opts = {}) {
    if (reducedMotion || !booted || !tile || !page) return Promise.resolve();
    const a = tile.getBoundingClientRect(), b = page.getBoundingClientRect();
    const sx = a.width / b.width, sy = a.height / b.height;
    const from = `translate(${a.left - b.left}px, ${a.top - b.top}px) scale(${sx}, ${sy})`;
    const frames = [
      { transform: from, opacity: 0, borderRadius: opts.radius || "16px" },
      { transform: "none", opacity: 1, borderRadius: "0px" },
    ];
    if (direction === "out") frames.reverse();
    page.style.transformOrigin = "0 0";
    const anim = page.animate(frames, { duration: opts.duration || 520, easing: "cubic-bezier(.2,.8,.2,1)", fill: "both" });
    return settle(anim, opts.duration || 520);
  }
  // Scales the overview "into" a point, like a camera moving forward.
  function push(el, origin, direction, opts = {}) {
    if (reducedMotion || !booted || !el) return Promise.resolve();
    const r = el.getBoundingClientRect();
    el.style.transformOrigin = `${origin.x - r.left}px ${origin.y - r.top}px`;
    const frames = [{ transform: "scale(1)", opacity: 1 }, { transform: `scale(${opts.scale || 3})`, opacity: 0 }];
    if (direction === "out") frames.reverse();
    const anim = el.animate(frames, { duration: opts.duration || 520, easing: "cubic-bezier(.2,.8,.2,1)", fill: "both" });
    return settle(anim, opts.duration || 520);
  }
  function centerOf(el) {
    const r = el.getBoundingClientRect();
    return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
  }
  function flash(el) {
    if (!el) return;
    el.scrollIntoView({ block: "start", behavior: reducedMotion ? "auto" : "smooth" });
    el.classList.remove("cs-flash");
    void el.offsetWidth;
    el.classList.add("cs-flash");
  }

  // ---------- theme (for judging light/dark; real site follows the system) ----------
  const THEMES = ["system", "light", "dark"];
  function applyTheme(t) {
    if (t === "system") document.documentElement.removeAttribute("data-theme");
    else document.documentElement.setAttribute("data-theme", t);
    try { localStorage.setItem("cs-proto-theme", t); } catch {}
  }
  let theme = "system";
  try { theme = localStorage.getItem("cs-proto-theme") || "system"; } catch {}
  applyTheme(theme);

  // ---------- prototype variant switcher ----------
  function mountSwitcher(variants, currentKey) {
    const bar = document.createElement("div");
    bar.className = "proto-switcher";
    const i = variants.findIndex((v) => v.key === currentKey);
    const goVariant = (d) => {
      const v = variants[(i + d + variants.length) % variants.length];
      const u = new URL(location.href);
      u.searchParams.set("variant", v.key);
      location.href = u.toString();
    };
    bar.innerHTML = `<button type="button" aria-label="Previous variant">‹</button>
      <span class="proto-label"><b>${variants[i].key}</b> ${variants[i].name}</span>
      <button type="button" aria-label="Next variant">›</button>
      <span class="proto-sep"></span>
      <button type="button" class="proto-theme" aria-label="Toggle theme">◐ ${theme}</button>`;
    const [prev, next] = bar.querySelectorAll("button");
    prev.onclick = () => goVariant(-1);
    next.onclick = () => goVariant(1);
    bar.querySelector(".proto-theme").onclick = (e) => {
      theme = THEMES[(THEMES.indexOf(theme) + 1) % THEMES.length];
      applyTheme(theme);
      e.currentTarget.textContent = "◐ " + theme;
    };
    addEventListener("keydown", (e) => {
      if (typing(document.activeElement) || paletteOpen() || e.ctrlKey || e.metaKey || e.altKey) return;
      if (e.key === "ArrowLeft") goVariant(-1);
      if (e.key === "ArrowRight") goVariant(1);
    });
    document.body.appendChild(bar);
  }

  window.CS = {
    data, topics, byId, reducedMotion,
    lang: () => lang, setLang, onLang: (fn) => langListeners.push(fn), t, L,
    route: () => current, settle, booted: () => booted, onRoute: (fn) => listeners.push(fn), go,
    esc, md, highlight, codeHTML, outputHTML, search,
    openPalette, closePalette, zoom, push, centerOf, flash, mountSwitcher,
  };
})();
