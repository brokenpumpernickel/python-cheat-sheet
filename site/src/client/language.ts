// The Language (ADR 0005) and the EN | PL switch. The page holds every piece of prose in both Languages
// (components/Text.astro) and theme.css shows the one in <html lang>, so a switch re-renders nothing: it
// sets lang, the page title and the labelled attributes (aria-label, placeholder), which CSS can't switch.
// The choice is remembered per visitor; a ?lang= parameter overrides it and follows the switch. A script
// in the page's head applies the chosen Language before the first paint.
import { defaultLanguage, label, languages, type LabelKey, type Language } from "../labels";

export const LANGUAGE_KEY = "cheatsheet.language"; // localStorage
export const LANGUAGE_PARAM = "lang";

/** The Language the page is shown in, as its <html lang> says; read at the moment it's needed, so client
 * text follows a switch. */
export function pageLanguage(): Language {
  const lang = document.documentElement.lang as Language;
  return languages.includes(lang) ? lang : defaultLanguage;
}

function applyLanguage(language: Language): void {
  document.documentElement.lang = language;
  document.title = label("siteTitle", language);
  for (const element of document.querySelectorAll<HTMLElement>("[data-label-attributes]")) {
    for (const pair of element.dataset.labelAttributes!.split(" ")) {
      const [name, key] = pair.split("=");
      element.setAttribute(name, label(key as LabelKey, language));
    }
  }
}

/** Runs the switch. `around` performs each switch, given the change to make, so that the views can keep
 * the Student's place across it. */
export function startLanguage(around: (change: () => void) => void): void {
  const choices = [...document.querySelectorAll<HTMLInputElement>("[data-language-choice]")];
  const sync = () => choices.forEach((choice) => (choice.checked = choice.value === pageLanguage()));
  sync();
  applyLanguage(pageLanguage()); // the build rendered the attributes in the default Language

  for (const choice of choices) {
    choice.addEventListener("change", () => {
      const language = choice.value as Language;
      if (!choice.checked || language === pageLanguage()) return;
      around(() => applyLanguage(language));
      try {
        localStorage.setItem(LANGUAGE_KEY, language);
      } catch {
        // Storage may be blocked (a private window); the choice then lasts until the page closes.
      }
      const url = new URL(location.href);
      if (url.searchParams.has(LANGUAGE_PARAM)) {
        url.searchParams.set(LANGUAGE_PARAM, language);
        history.replaceState(history.state, "", url);
      }
      sync();
    });
  }
}
