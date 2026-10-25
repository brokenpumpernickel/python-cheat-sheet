// The Trail's Area dots (components/TrailView.astro): each jumps to its Area's stretch, and the dot of the
// Area at the middle of the screen is marked aria-current (the first Area's, until one reaches it).
import { motionAllowed } from "./motion";

export function startTrail(): void {
  const dots = [...document.querySelectorAll<HTMLElement>("[data-land]")];
  const lands = [...document.querySelectorAll<HTMLElement>("[data-land-section]")];
  if (!lands.length) return;

  for (const dot of dots) {
    dot.addEventListener("click", () => {
      const land = lands.find((l) => l.dataset.landSection === dot.dataset.land);
      land?.scrollIntoView({ behavior: motionAllowed() ? "smooth" : "auto", block: "start" });
    });
  }

  function mark() {
    if (lands[0].getClientRects().length === 0) return; // the Trail isn't showing
    const middle = window.innerHeight / 2;
    const current = lands.findLast((land) => land.getBoundingClientRect().top <= middle) ?? lands[0];
    for (const dot of dots) {
      if (dot.dataset.land === current.dataset.landSection) dot.setAttribute("aria-current", "true");
      else dot.removeAttribute("aria-current");
    }
  }

  let queued = false;
  const update = () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      mark();
    });
  };
  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
  // Also when the Trail appears (the toggle, or zooming out to it), which may not scroll the page.
  const appear = new IntersectionObserver(update);
  lands.forEach((land) => appear.observe(land));
}
