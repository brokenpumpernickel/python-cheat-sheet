// Shows the Overview or one Topic page for the current route, with the semantic zoom between them
// (ADR 0001): zooming in scales the Overview toward the Topic's tile and fades the page in; zooming out
// reverses that and returns focus to the tile. Switching Topics crossfades. Nothing animates on first
// load (a deep link has no tile to come from) or with reduced motion.
import { isTyping } from "./keys";
import { fadePage, motionAllowed, zoomOverview } from "./motion";
import { goToOverview, onRouteChange, parseRoute } from "./router";

export function startViews(): void {
  const overview = document.querySelector<HTMLElement>("[data-overview]")!;
  const topicView = document.querySelector<HTMLElement>("[data-topic-view]")!;
  const pages = new Map(
    [...document.querySelectorAll<HTMLElement>("[data-topic]")].map((page) => [page.dataset.topic!, page]),
  );

  let shown: string | null = null; // the Topic on screen, or null for the Overview
  let booted = false;

  // The Topic's tile in the arrangement on screen (the Overview may hold more than one arrangement).
  const tileOf = (topic: string) => {
    const tiles = [...overview.querySelectorAll<HTMLElement>(`[data-tile="${CSS.escape(topic)}"]`)];
    return tiles.find((tile) => tile.getClientRects().length > 0) ?? null;
  };

  function scrollTo(page: HTMLElement, entry: string | null) {
    const target = entry && page.querySelector(`[data-entry="${CSS.escape(`${page.dataset.topic}/${entry}`)}"]`);
    if (target) target.scrollIntoView();
    else window.scrollTo(0, 0);
  }

  async function zoomIn(page: HTMLElement, animate: boolean) {
    const tile = tileOf(page.dataset.topic!);
    if (animate && tile) await zoomOverview(overview, tile, "in");
    overview.hidden = true;
    topicView.hidden = false;
    page.hidden = false;
    page.focus({ preventScroll: true });
    window.scrollTo(0, 0);
    if (animate) await fadePage(page, "in");
  }

  async function crossfade(from: HTMLElement, to: HTMLElement, animate: boolean) {
    if (animate) await fadePage(from, "out");
    from.hidden = true;
    to.hidden = false;
    to.focus({ preventScroll: true });
    window.scrollTo(0, 0);
    if (animate) await fadePage(to, "in");
  }

  async function zoomOut(page: HTMLElement, animate: boolean) {
    if (animate) await fadePage(page, "out");
    page.hidden = true;
    topicView.hidden = true;
    overview.hidden = false;
    const tile = tileOf(page.dataset.topic!);
    if (!tile) return window.scrollTo(0, 0);
    tile.scrollIntoView({ block: "center" });
    tile.focus({ preventScroll: true });
    if (animate) await zoomOverview(overview, tile, "out");
  }

  async function render() {
    const route = parseRoute(location.hash, pages);
    const animate = booted && motionAllowed();
    const from = shown === null ? null : pages.get(shown)!;
    const to = route && pages.get(route.topic)!;
    shown = route && route.topic;

    if (to && from === to) scrollTo(to, route.entry);
    else if (to) {
      await (from ? crossfade(from, to, animate) : zoomIn(to, animate));
      if (route.entry) scrollTo(to, route.entry);
    } else if (from) await zoomOut(from, animate);
  }

  // One render at a time; each reads the route afresh, so quick successive changes end on the latest.
  const report = (error: unknown) => console.error(error);
  let rendering = render().catch(report); // the first render, before anything may animate
  booted = true;
  const rerender = () => {
    rendering = rendering.then(render).catch(report);
  };

  // The route decides the scroll position; the browser restoring an old one would fight it on Back.
  history.scrollRestoration = "manual";
  onRouteChange(rerender);

  document.addEventListener("click", (event) => {
    const home = (event.target as Element).closest("[data-home]");
    if (!home || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    goToOverview();
  });

  // Esc zooms out, unless the Student is typing or something open (such as search) used the key first.
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || event.defaultPrevented || isTyping(document.activeElement)) return;
    if (parseRoute(location.hash, pages)) goToOverview();
  });
}
