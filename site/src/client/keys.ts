// Shared keyboard rules: single-key shortcuts (Esc, and later "/") don't fire while the Student types.
// Radio buttons and checkboxes (the Map | Trail toggle) are inputs too, but nothing is typed into them.

export function isTyping(element: Element | null): boolean {
  return (
    element instanceof HTMLElement &&
    (element.isContentEditable || element.matches('input:not([type="radio"], [type="checkbox"]), textarea, select'))
  );
}
