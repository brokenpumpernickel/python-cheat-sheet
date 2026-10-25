// The animations of the semantic zoom (ADR 0001). Each one settles after a timeout as well as when it
// finishes: an animation's `finished` never resolves while the browser isn't painting (a background tab),
// and navigation must still complete then.

const ZOOM_MS = 450;
const FADE_MS = 250;
const FLASH_MS = 1400;
const ZOOM_SCALE = 4;
const EASING = "cubic-bezier(.2, .8, .2, 1)";

/** False with reduced motion, and while the page isn't visible, where nobody would see the animation. */
export function motionAllowed(): boolean {
  return !matchMedia("(prefers-reduced-motion: reduce)").matches && document.visibilityState === "visible";
}

function play(element: HTMLElement, keyframes: Keyframe[], duration: number): Promise<void> {
  const animation = element.animate(keyframes, { duration, easing: EASING, fill: "both" });
  animation.finished.catch(() => {}); // it rejects when cancelled below
  const timeout = new Promise((resolve) => setTimeout(resolve, duration + 150));
  return Promise.race([animation.finished, timeout]).then(() => animation.cancel());
}

/** Scales the Overview toward the tile's centre and fades it out ("in"), or the reverse ("out"). */
export function zoomOverview(overview: HTMLElement, tile: HTMLElement, direction: "in" | "out"): Promise<void> {
  const o = overview.getBoundingClientRect();
  const t = tile.getBoundingClientRect();
  overview.style.transformOrigin = `${t.left + t.width / 2 - o.left}px ${t.top + t.height / 2 - o.top}px`;
  const keyframes = [
    { transform: "none", opacity: 1 },
    { transform: `scale(${ZOOM_SCALE})`, opacity: 0 },
  ];
  if (direction === "out") keyframes.reverse();
  return play(overview, keyframes, ZOOM_MS);
}

/** Fades a page in, growing slightly into place, or out. */
export function fadePage(page: HTMLElement, direction: "in" | "out"): Promise<void> {
  const keyframes = [
    { transform: "scale(.97)", opacity: 0 },
    { transform: "none", opacity: 1 },
  ];
  if (direction === "out") keyframes.reverse();
  return play(page, keyframes, FADE_MS);
}

const flashTimers = new WeakMap<Element, number>();

/** Highlights an Entry briefly after a jump to it, so the eye finds it. The look is the CSS of the
 * "flash" class: an animation, or a still ring with reduced motion. It ends on a timer, not on
 * animationend, so it ends in a background tab too. */
export function flash(entry: HTMLElement): void {
  entry.classList.remove("flash");
  void entry.offsetWidth; // restarts the animation if the Entry is already flashing
  entry.classList.add("flash");
  clearTimeout(flashTimers.get(entry));
  flashTimers.set(entry, window.setTimeout(() => entry.classList.remove("flash"), FLASH_MS));
}
