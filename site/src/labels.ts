// Every interface label, in both Languages (ADR 0005). Content prose comes from the content data instead.
// Plain TypeScript with no imports, so both Astro components and client modules can use it.

export const languages = ["en", "pl"] as const;
export type Language = (typeof languages)[number];
export const defaultLanguage: Language = "en";

const en = {
  siteTitle: "Python Cheat Sheet",
  map: "Map",
  comingSoon: "coming soon",
  hintDive: "Click a bubble to dive in",
  hintBack: "to come back up",
  hintSearch: "to search",
  output: "Output",
  figure: "Figure drawn by the code above",
  pitfall: "Pitfall",
  watchOut: "Watch out!",
  seeAlso: "See also",
  entries: "Entries",
  copy: "Copy",
  copied: "Copied!",
  copyFailed: "Copy failed",
  topicOrder: "Topic order",
  previousStop: "Previous stop",
  nextStop: "Next stop",
  examplesRunWith: "Examples run with",
  search: "Search",
  searchPrompt: "Search Topics, Entries and code",
  searchResults: "Results",
  searchLoading: "Loading…",
  searchFailed: "Search didn't load. Close it and try again.",
  searchNoMatches: "No matches for",
  searchMove: "move",
  searchOpen: "open",
  searchClose: "close",
};

export type LabelKey = keyof typeof en;

const pl: Record<LabelKey, string> = {
  siteTitle: "Ściągawka z Pythona",
  map: "Mapa",
  comingSoon: "wkrótce",
  hintDive: "Kliknij bąbel, aby wejść",
  hintBack: "powrót",
  hintSearch: "wyszukiwanie",
  output: "Wynik",
  figure: "Wykres narysowany przez powyższy kod",
  pitfall: "Pułapka",
  watchOut: "Uwaga!",
  seeAlso: "Zobacz też",
  entries: "Hasła",
  copy: "Kopiuj",
  copied: "Skopiowano!",
  copyFailed: "Nie udało się skopiować",
  topicOrder: "Kolejność tematów",
  previousStop: "Poprzedni przystanek",
  nextStop: "Następny przystanek",
  examplesRunWith: "Wersje użyte w przykładach:",
  search: "Szukaj",
  searchPrompt: "Szukaj tematów, haseł i kodu",
  searchResults: "Wyniki",
  searchLoading: "Wczytywanie…",
  searchFailed: "Nie udało się wczytać wyszukiwania. Zamknij je i spróbuj ponownie.",
  searchNoMatches: "Brak wyników dla",
  searchMove: "wybór",
  searchOpen: "otwórz",
  searchClose: "zamknij",
};

export const labels: Record<Language, Record<LabelKey, string>> = { en, pl };

// The build doesn't type-check, so a label missing from one Language fails here instead.
for (const language of languages) {
  for (const key of new Set([...Object.keys(en), ...Object.keys(labels[language])])) {
    if (!labels[language][key as LabelKey]?.trim()) {
      throw new Error(`labels.ts: "${key}" has no ${language} label`);
    }
  }
}

export function label(key: LabelKey, language: Language = defaultLanguage): string {
  return labels[language][key];
}
