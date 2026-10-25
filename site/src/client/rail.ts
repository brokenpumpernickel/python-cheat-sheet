// The Index rail (components/IndexRail.astro): marks the current Topic "you are here" (aria-current) in
// both arrangements, which expands its Entries, keeps that Topic in view in the rail, and highlights the
// Entry in view as the Student scrolls (the scroll spy).

const SPY_SLACK = 24; // px below the sticky chips within which an Entry counts as the one being read

export interface Rail {
  /** Makes `page`'s Topic the current one, or none (null, on the Overview). */
  show(page: HTMLElement | null): void;
  /** Brings the current Topic's pin into view: centred in the phone strip, near the top of the side rail. */
  centre(): void;
  /** Highlights the Entry just jumped to, until the Student scrolls: the page may end before it can
   * scroll that Entry up to the chips. */
  jumped(entry: HTMLElement): void;
  /** The Entry highlighted as the one being read, if any. */
  current(): HTMLElement | null;
}

export function startRail(rail: HTMLElement): Rail {
  const pins = [...rail.querySelectorAll<HTMLElement>("[data-pin]")];
  const entryLinks = [...rail.querySelectorAll<HTMLElement>("[data-rail-entry]")];

  let page: HTMLElement | null = null;
  let entries: HTMLElement[] = [];
  let held: { entry: string; y: number } | null = null;
  let highlighted: string | null = null;

  const mark = (element: HTMLElement, value: string | null) =>
    value ? element.setAttribute("aria-current", value) : element.removeAttribute("aria-current");

  function highlight(entry: string | null) {
    highlighted = entry;
    for (const link of entryLinks) mark(link, link.dataset.railEntry === entry ? "true" : null);
  }

  // The Entry being read: the one that most recently scrolled up to the chips (the highest such one, in
  // two columns), or the first while none has yet.
  function inView(): string | null {
    if (!page || !entries.length) return null;
    if (held && Math.abs(window.scrollY - held.y) < 2) return held.entry;
    held = null;
    const line = (page.querySelector("[data-chips]")?.getBoundingClientRect().bottom ?? 0) + SPY_SLACK;
    let current = entries[0];
    let currentTop = -Infinity;
    for (const entry of entries) {
      const top = entry.getBoundingClientRect().top;
      if (top <= line && top > currentTop) [current, currentTop] = [entry, top];
    }
    return current.dataset.entry!;
  }

  let queued = false;
  const spy = () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      highlight(inView());
    });
  };
  window.addEventListener("scroll", spy, { passive: true });
  window.addEventListener("resize", spy);

  function centre() {
    const pin = pins.find((p) => p.hasAttribute("aria-current") && p.getClientRects().length > 0);
    if (!pin) return;
    const r = rail.getBoundingClientRect();
    const p = pin.getBoundingClientRect();
    rail.scrollLeft += p.left + p.width / 2 - (r.left + r.width / 2);
    if (p.top < r.top || p.bottom > r.bottom) rail.scrollTop += p.top - r.top - r.height / 4;
  }

  return {
    show(next) {
      page = next;
      entries = next ? [...next.querySelectorAll<HTMLElement>("[data-entry]")] : [];
      held = null;
      for (const pin of pins) mark(pin, next && pin.dataset.pin === next.dataset.topic ? "page" : null);
      highlight(inView());
      centre();
    },
    centre,
    jumped(entry) {
      held = { entry: entry.dataset.entry!, y: window.scrollY };
      highlight(held.entry);
    },
    current() {
      return entries.find((entry) => entry.dataset.entry === highlighted) ?? null;
    },
  };
}
