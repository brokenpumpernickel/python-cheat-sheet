// Copy buttons on code examples: the button carries the exact code (data-copy), puts it on the
// clipboard and says so briefly, in the page's Language.
import { label, type LabelKey } from "../labels";
import { pageLanguage } from "./language";

const CONFIRM_MS = 1500;

async function writeClipboard(text: string): Promise<void> {
  if (navigator.clipboard) return navigator.clipboard.writeText(text);
  // Without the Clipboard API (an insecure origin), copy from a selected, off-screen text area.
  const area = document.createElement("textarea");
  area.value = text;
  area.setAttribute("readonly", "");
  area.style.cssText = "position: fixed; top: 0; left: -9999px";
  document.body.append(area);
  area.select();
  const copied = document.execCommand("copy");
  area.remove();
  if (!copied) throw new Error("copy failed");
}

export function startCopy(): void {
  const timers = new WeakMap<HTMLElement, number>();

  const show = (button: HTMLElement, key: LabelKey, state?: string) => {
    button.querySelector("[aria-live]")!.textContent = label(key, pageLanguage());
    if (state) button.dataset.state = state;
    else delete button.dataset.state;
  };

  document.addEventListener("click", async (event) => {
    const button = (event.target as Element).closest<HTMLElement>("[data-copy]");
    if (!button) return;
    let ok = true;
    try {
      await writeClipboard(button.dataset.copy!);
    } catch {
      ok = false;
    }
    show(button, ok ? "copied" : "copyFailed", ok ? "copied" : "failed");
    clearTimeout(timers.get(button));
    timers.set(button, window.setTimeout(() => show(button, "copy"), CONFIRM_MS));
  });
}
