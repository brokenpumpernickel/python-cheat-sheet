// Printed text or maths wider than its Output scrolls sideways (OutputBlock.astro, data-scrolls). A keyboard
// can scroll only what it can focus, so a block that scrolls joins the tab order, and leaves it once it fits
// (in a wider window). Blocks on a hidden Topic page have no size until it is shown, so sizes are watched.
export function startScrollers(): void {
  const observer = new ResizeObserver((entries) => {
    for (const { target } of entries) {
      if (target.scrollWidth > target.clientWidth) target.setAttribute("tabindex", "0");
      else target.removeAttribute("tabindex");
    }
  });
  for (const block of document.querySelectorAll("[data-scrolls]")) observer.observe(block);
}
