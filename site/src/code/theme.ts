// The syntax-highlighting theme for code examples, highlighted at build time by Astro's <Code> (Shiki).
// Its colours are CSS variables (the --tk-* tokens in theme.css), so the same HTML follows light and dark.
const tk = (name: string) => `var(--tk-${name})`;

export const codeTheme = {
  name: "islands",
  type: "light",
  colors: {
    "editor.foreground": "var(--ink)",
    "editor.background": "var(--code-bg)",
  },
  tokenColors: [
    { scope: ["comment", "punctuation.definition.comment"], settings: { foreground: tk("com") } },
    { scope: ["string", "punctuation.definition.string", "storage.type.string"], settings: { foreground: tk("str") } },
    // The {expressions} inside f-strings are code again.
    { scope: ["meta.fstring.python", "constant.character.format.placeholder"], settings: { foreground: "var(--ink)" } },
    { scope: ["constant.numeric"], settings: { foreground: tk("num") } },
    {
      scope: ["keyword", "storage.type", "storage.modifier", "constant.language", "keyword.operator.logical", "keyword.operator.word"],
      settings: { foreground: tk("kw") },
    },
    { scope: ["keyword.operator", "punctuation.separator.annotation"], settings: { foreground: tk("op") } },
    { scope: ["entity.name.function", "entity.name.type", "entity.name.class"], settings: { foreground: tk("fn") } },
    { scope: ["support.function.builtin", "support.type", "support.type.exception"], settings: { foreground: tk("bi") } },
  ],
};
