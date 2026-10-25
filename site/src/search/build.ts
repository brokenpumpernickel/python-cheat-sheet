// Builds the search index from the content data at build time (served as search.json, fetched the first
// time search opens). Planned Topics have no page, so they are left out.
import type { Area } from "../content";
import type { SearchDoc, SearchIndex } from "./match";

const ENTITIES: Record<string, string> = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'" };

/** The text of the content build's inline HTML (explanations, Pitfall text), without its tags. */
export function plainText(html: string): string {
  return html
    .replace(/<[^>]*>/g, "")
    .replace(/&(?:#(\d+)|#x([0-9a-f]+)|(\w+));/gi, (whole, dec, hex, name) =>
      dec ? String.fromCodePoint(+dec) : hex ? String.fromCodePoint(parseInt(hex, 16)) : (ENTITIES[name] ?? whole),
    );
}

const join = (parts: (string | null | undefined)[]) => parts.filter(Boolean).join("\n");

export function buildIndex(areas: Area[]): SearchIndex {
  const docs: SearchDoc[] = [];
  for (const area of areas) {
    const areaTitle = { en: area.title, pl: area.pl.title };
    for (const topic of area.topics) {
      if (topic.planned) continue;
      const topicTitle = { en: topic.title, pl: topic.pl.title };
      const path = { area: areaTitle, topic: topicTitle };
      docs.push({ route: topic.id, title: topicTitle, ...path, body: join([topic.summary, topic.pl.summary]) });
      for (const entry of topic.entries) {
        const { pitfall } = entry;
        docs.push({
          route: `${topic.id}/${entry.id}`,
          title: { en: entry.title, pl: entry.pl.title },
          ...path,
          body: join([
            plainText(entry.explain),
            plainText(entry.pl.explain),
            entry.code,
            entry.raises,
            pitfall && plainText(pitfall.text),
            entry.pl.pitfall && plainText(entry.pl.pitfall),
            pitfall?.code,
            pitfall?.raises,
          ]),
        });
      }
    }
  }
  return { docs };
}
