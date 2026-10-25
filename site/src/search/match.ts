// Search over the build-time index (src/search/build.ts, served as search.json): both Languages match
// whichever is active, every query word must match, and results rank title prefix > title contains >
// Topic name > body. Plain TypeScript with type-only imports, so the client and Node can both run it.
import type { Language } from "../labels";

export type Bilingual = Record<Language, string>;

/** One searchable Topic or Entry, as the build writes it. */
export interface SearchDoc {
  route: string; // "topic" or "topic/entry"
  title: Bilingual;
  area: Bilingual; // the Area title, for the result's path
  topic: Bilingual; // the Topic title, for the path and the "Topic name" rank
  body: string; // summary, or explanations, Pitfall and code, as plain text in both Languages
}

export interface SearchIndex {
  docs: SearchDoc[];
}

/** A document with its fields folded once, ready for many queries. */
interface Prepared {
  doc: SearchDoc;
  titles: string[];
  topic: string;
  body: string;
}

export type Searcher = (query: string) => SearchDoc[];

const TITLE_PREFIX = 8;
const TITLE_CONTAINS = 4;
const TOPIC_NAME = 2;
const BODY = 1;

/** Lower case without diacritics, so "slownik" finds "słownik" and "Potegi" finds "Potęgi". */
export function fold(text: string): string {
  return text.toLowerCase().normalize("NFD").replace(/\p{M}/gu, "").replaceAll("ł", "l");
}

function score(doc: Prepared, word: string): number {
  if (doc.titles.some((title) => title.startsWith(word))) return TITLE_PREFIX;
  if (doc.titles.some((title) => title.includes(word))) return TITLE_CONTAINS;
  if (doc.topic.includes(word)) return TOPIC_NAME;
  if (doc.body.includes(word)) return BODY;
  return 0;
}

/** A search function over `index`: the best `limit` matches for a query, best first; ties keep index
 * order (Topic order, each Topic before its Entries). */
export function searcher(index: SearchIndex, limit = 20): Searcher {
  const docs: Prepared[] = index.docs.map((doc) => ({
    doc,
    titles: [fold(doc.title.en), fold(doc.title.pl)],
    topic: `${fold(doc.topic.en)}\n${fold(doc.topic.pl)}`,
    body: fold(doc.body),
  }));

  return (query) => {
    const words = fold(query).split(/\s+/).filter(Boolean);
    if (!words.length) return [];
    const hits: { doc: SearchDoc; score: number }[] = [];
    for (const doc of docs) {
      let total = 0;
      for (const word of words) {
        const points = score(doc, word);
        if (!points) {
          total = 0;
          break;
        }
        total += points;
      }
      if (total) hits.push({ doc: doc.doc, score: total });
    }
    return hits
      .sort((a, b) => b.score - a.score) // stable, so ties stay in index order
      .slice(0, limit)
      .map((hit) => hit.doc);
  };
}
