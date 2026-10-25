// The search index, written as a static file next to the page so the first view doesn't carry it.
import { loadContent } from "../content";
import { buildIndex } from "../search/build";

export function GET(): Response {
  return new Response(JSON.stringify(buildIndex(loadContent().areas)), {
    headers: { "Content-Type": "application/json" },
  });
}
