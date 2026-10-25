// Hash routes: "" → the Overview, "#topic" → that Topic, "#topic/entry" → that Topic at the Entry.
// A route to an unknown or planned Topic is the Overview. Back/forward follow the hash.

export interface Route {
  topic: string;
  entry: string | null;
}

/** The route in `hash`, or null for the Overview; `topics` are the ids of the Topics that have a page. */
export function parseRoute(hash: string, topics: { has(id: string): boolean }): Route | null {
  let path: string;
  try {
    path = decodeURIComponent(hash.replace(/^#/, ""));
  } catch {
    return null; // a malformed escape such as "#%"
  }
  const [topic = "", entry = ""] = path.split("/");
  return topics.has(topic) ? { topic, entry: entry || null } : null;
}

/** Calls `listener` whenever the route may have changed. */
export function onRouteChange(listener: () => void): void {
  window.addEventListener("hashchange", listener);
}

/** Navigates to the Overview as a new history entry, leaving no "#" behind in the URL. */
export function goToOverview(): void {
  if (!location.hash) return;
  history.pushState(null, "", location.pathname + location.search);
  window.dispatchEvent(new HashChangeEvent("hashchange"));
}

/** Navigates to `hash` ("#topic" or "#topic/entry"). If that is already the route, it is shown again,
 * which scrolls back to its Entry and flashes it. */
export function goTo(hash: string): void {
  if (location.hash === hash) window.dispatchEvent(new HashChangeEvent("hashchange"));
  else location.hash = hash;
}
