// Displayed maths (SymPy's `display(expr)`), typeset at build time with KaTeX (ADR 0007): HTML drawn for the
// eye and MathML for screen readers, so the page needs no maths script. KaTeX's CSS and fonts are bundled
// with the site by the import in OutputBlock.astro.
import katex from "katex";
import type { Area, Output } from "./content";

export function typeset(latex: string): string {
  return katex.renderToString(latex, { displayMode: true, output: "htmlAndMathml", throwOnError: true });
}

/** Typesets every displayed maths in the content once, so LaTeX that KaTeX can't typeset fails the build,
 * naming each Entry and its LaTeX, instead of showing broken maths. The message starts with "Content error:",
 * which the Python build (cheatsheet/build.py) picks out of Astro's log. */
export function checkMaths(areas: Area[]): void {
  const failures: string[] = [];
  const check = (output: Output | null, where: string) => {
    for (const part of output?.parts ?? []) {
      if (!("maths" in part)) continue;
      try {
        typeset(part.maths);
      } catch (error) {
        if (!(error instanceof katex.ParseError)) throw error;
        const latex = part.maths.replace(/\s+/g, " ");
        failures.push(`Content error: ${where}: KaTeX can't typeset the displayed maths ${latex} (${error.rawMessage})`);
      }
    }
  };
  for (const area of areas) {
    for (const topic of area.topics) {
      for (const entry of topic.entries) {
        const where = `${area.id}/${topic.id}.md (${topic.id}/${entry.id})`;
        check(entry.output, where);
        check(entry.pitfall?.output ?? null, `${where} Pitfall`);
      }
    }
  }
  if (failures.length) throw new Error(failures.join("\n"));
}
