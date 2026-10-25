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
  output: "Output",
  examplesRunWith: "Examples run with",
};

export type LabelKey = keyof typeof en;

const pl: Record<LabelKey, string> = {
  siteTitle: "Ściągawka z Pythona",
  map: "Mapa",
  comingSoon: "wkrótce",
  hintDive: "Kliknij bąbel, aby wejść",
  hintBack: "powrót",
  output: "Wynik",
  examplesRunWith: "Wersje użyte w przykładach:",
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
