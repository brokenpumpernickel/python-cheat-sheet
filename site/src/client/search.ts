// The search pop-up (components/Search.astro): Ctrl/Cmd+K, "/" (unless typing) or the top bar's pill opens
// it, and the index (search.json) loads the first time it opens or the pill is pointed at. Arrow keys move
// through the results, Enter opens one, Esc closes without leaving the page. Results show in the page's
// Language and match both. Focus returns to where it was on close; opening a result moves it to the Entry.
import { label } from "../labels";
import { searcher, type SearchDoc, type Searcher, type SearchIndex } from "../search/match";
import { isTyping } from "./keys";
import { pageLanguage } from "./language";
import { goTo } from "./router";

const INDEX_URL = `${import.meta.env.BASE_URL.replace(/\/?$/, "/")}search.json`;

const isApple = /Mac|iPhone|iPad/.test(navigator.platform);

export interface Search {
  /** Shows the results and status in the Language just switched to. */
  languageSwitched(): void;
}

export function startSearch(): Search {
  const dialog = document.querySelector<HTMLDialogElement>("[data-search]")!;
  const input = dialog.querySelector<HTMLInputElement>("[data-search-input]")!;
  const list = dialog.querySelector<HTMLElement>("[data-search-results]")!;
  const status = dialog.querySelector<HTMLElement>("[data-search-status]")!;

  let find: Searcher | null = null;
  let loading: Promise<void> | null = null;
  let failed = false;
  let results: SearchDoc[] = [];
  let selected = 0;
  let opener: HTMLElement | null = null;
  let enterWhileLoading = false; // Enter before the index arrived opens the top result once it does

  if (isApple) document.querySelectorAll("[data-shortcut]").forEach((key) => (key.textContent = "⌘ K"));

  // Loads the index once; a failed load is retried the next time search opens.
  function load() {
    if (loading) return;
    failed = false;
    loading = fetch(INDEX_URL)
      .then((response) => {
        if (!response.ok) throw new Error(`${INDEX_URL}: ${response.status}`);
        return response.json() as Promise<SearchIndex>;
      })
      .then((index) => {
        find = searcher(index);
      })
      .catch((error) => {
        console.error(error);
        loading = null;
        failed = true;
      })
      .finally(() => {
        if (!dialog.open) return;
        render();
        if (enterWhileLoading && results[0]) choose(results[0]);
        enterWhileLoading = false;
      });
  }

  function option(doc: SearchDoc, index: number): HTMLLIElement {
    const lang = pageLanguage();
    const item = document.createElement("li");
    item.id = `search-result-${index}`;
    item.setAttribute("role", "option");
    item.dataset.index = String(index);
    const title = document.createElement("span");
    title.className = "title";
    title.textContent = doc.title[lang];
    const path = document.createElement("span");
    path.className = "path";
    // A Topic's own result needs only its Area.
    path.textContent = doc.route.includes("/") ? `${doc.area[lang]} › ${doc.topic[lang]}` : doc.area[lang];
    item.append(title, path);
    return item;
  }

  function select(index: number) {
    selected = index;
    const items = [...list.children] as HTMLElement[];
    items.forEach((item, k) => item.setAttribute("aria-selected", String(k === index)));
    if (items[index]) {
      input.setAttribute("aria-activedescendant", items[index].id);
      items[index].scrollIntoView({ block: "nearest" });
    } else input.removeAttribute("aria-activedescendant");
  }

  function render() {
    const query = input.value.trim();
    results = find && query ? find(query) : [];
    list.replaceChildren(...results.map(option));
    list.hidden = results.length === 0;
    input.setAttribute("aria-expanded", String(results.length > 0));
    select(Math.max(0, Math.min(selected, results.length - 1)));
    if (!query) status.textContent = "";
    else if (failed) status.textContent = label("searchFailed", pageLanguage());
    else if (!find) status.textContent = label("searchLoading", pageLanguage());
    else if (!results.length) status.textContent = `${label("searchNoMatches", pageLanguage())} “${query}”`;
    else status.textContent = "";
  }

  // Opening again keeps the last query, selected, so typing replaces it.
  function open() {
    if (!dialog.open) {
      opener = document.activeElement instanceof HTMLElement ? document.activeElement : null;
      dialog.showModal();
    }
    input.focus();
    input.select();
    selected = 0;
    render();
    load();
  }

  function close() {
    enterWhileLoading = false;
    dialog.close();
    opener?.focus({ preventScroll: true });
    opener = null;
  }

  function choose(doc: SearchDoc) {
    close();
    goTo(`#${doc.route}`); // the route moves focus to the Topic page or Entry
  }

  document.addEventListener("keydown", (event) => {
    const ctrlK = event.key.toLowerCase() === "k" && (event.ctrlKey || event.metaKey) && !event.altKey && !event.shiftKey;
    const slash =
      event.key === "/" && !event.ctrlKey && !event.metaKey && !event.altKey && !isTyping(document.activeElement);
    if (!ctrlK && !slash) return;
    event.preventDefault();
    open();
  });

  document.querySelectorAll("[data-search-open]").forEach((pill) => {
    pill.addEventListener("click", open);
    pill.addEventListener("pointerenter", load); // usually loaded before the click lands
  });

  input.addEventListener("input", () => {
    enterWhileLoading = false;
    selected = 0;
    render();
  });

  dialog.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      if (results.length) select(Math.max(0, Math.min(results.length - 1, selected + (event.key === "ArrowDown" ? 1 : -1))));
    } else if (event.key === "Enter") {
      event.preventDefault();
      if (results[selected]) choose(results[selected]);
      else if (!find && input.value.trim()) enterWhileLoading = true;
    } else if (event.key === "Escape") {
      // Closes only the pop-up: the page's own Esc (zoom out) skips a handled event.
      event.preventDefault();
      close();
    }
  });

  // Any other way the dialog closes (the browser's own close request) restores focus the same way.
  dialog.addEventListener("cancel", (event) => {
    event.preventDefault();
    close();
  });

  // A click outside the box lands on the dialog itself (its backdrop).
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) close();
  });

  list.addEventListener("mousedown", (event) => event.preventDefault()); // keeps focus in the input
  list.addEventListener("mousemove", (event) => {
    const item = (event.target as Element).closest<HTMLElement>("[data-index]");
    if (item && +item.dataset.index! !== selected) select(+item.dataset.index!);
  });
  list.addEventListener("click", (event) => {
    const item = (event.target as Element).closest<HTMLElement>("[data-index]");
    if (item) choose(results[+item.dataset.index!]);
  });

  return {
    languageSwitched() {
      if (dialog.open) render();
    },
  };
}
