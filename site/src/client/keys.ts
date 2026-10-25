// Shared keyboard rules: single-key shortcuts (Esc, and later "/") don't fire while the Student types.

export function isTyping(element: Element | null): boolean {
  return element instanceof HTMLElement && (element.isContentEditable || element.matches("input, textarea, select"));
}
