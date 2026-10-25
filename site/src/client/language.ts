// The Language the page is shown in, as its <html lang> says; read at the moment it's needed, so
// client text follows a Language switch.
import { defaultLanguage, languages, type Language } from "../labels";

export function pageLanguage(): Language {
  const lang = document.documentElement.lang as Language;
  return languages.includes(lang) ? lang : defaultLanguage;
}
