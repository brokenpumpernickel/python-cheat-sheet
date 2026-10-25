// The Map | Trail toggle: which arrangement the Overview shows, and the Index rail with it. The choice is
// the <html> element's data-arrangement (theme.css shows only what's marked for it) and is remembered per
// visitor. A script in the page's head applies the remembered choice before the first paint.

export type Arrangement = "map" | "trail";
export const ARRANGEMENT_KEY = "cheatsheet.arrangement"; // localStorage

export function currentArrangement(): Arrangement {
  return document.documentElement.dataset.arrangement === "trail" ? "trail" : "map";
}

/** Runs the toggle; `onSwitch` runs after each switch, once the new arrangement shows. */
export function startArrangement(onSwitch: () => void): void {
  const choices = [...document.querySelectorAll<HTMLInputElement>("[data-arrangement-choice]")];
  const sync = () => choices.forEach((choice) => (choice.checked = choice.value === currentArrangement()));
  sync();

  for (const choice of choices) {
    choice.addEventListener("change", () => {
      if (!choice.checked || choice.value === currentArrangement()) return;
      document.documentElement.dataset.arrangement = choice.value;
      try {
        localStorage.setItem(ARRANGEMENT_KEY, choice.value);
      } catch {
        // Storage may be blocked (a private window); the choice then lasts until the page closes.
      }
      sync();
      onSwitch();
    });
  }
}
