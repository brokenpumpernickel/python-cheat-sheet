// Loads the generated content data (written by the Python content build) through a typed schema,
// the second safety net after the content build's own validation (ADR 0004).
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { z } from "astro/zod";

// An ipywidgets control the example displayed, with its starting state (cheatsheet/execute.py).
const Widget = z.discriminatedUnion("kind", [
  z.strictObject({
    kind: z.literal("slider"),
    description: z.string(),
    min: z.number(),
    max: z.number(),
    step: z.number(),
    value: z.number(),
    readout: z.string(), // the value as Jupyter shows it, with the slider's readout_format
    minReadout: z.string(),
    maxReadout: z.string(),
  }),
  z.strictObject({
    kind: z.literal("dropdown"),
    description: z.string(),
    options: z.array(z.string()),
    value: z.string().nullable(), // the selected option's label
  }),
  z.strictObject({ kind: z.literal("checkbox"), description: z.string(), value: z.boolean() }),
  z.strictObject({ kind: z.literal("text"), description: z.string(), value: z.string() }),
]);

const Output = z.strictObject({
  text: z.string(),
  error: z.string().nullable(),
  figures: z.array(z.string()),
  widgets: z.array(Widget),
});

const Entry = z.strictObject({
  id: z.string().min(1),
  title: z.string().min(1),
  explain: z.string().min(1), // inline HTML rendered by the content build
  code: z.string().min(1),
  raises: z.string().nullable(),
  figure: z.string().min(1).nullable(), // the description of the example's figures, their accessible name
  see: z.array(z.string().regex(/^[a-z0-9-]+\/[a-z0-9-]+$/)),
  pitfall: z
    .strictObject({
      text: z.string().min(1),
      code: z.string().nullable(),
      raises: z.string().nullable(),
      figure: z.string().min(1).nullable(),
      output: Output.nullable(),
    })
    .nullable(),
  output: Output,
  pl: z.strictObject({
    title: z.string().min(1),
    explain: z.string().min(1),
    pitfall: z.string().nullable(),
    figure: z.string().min(1).nullable(),
    pitfallFigure: z.string().min(1).nullable(),
  }),
});

const Topic = z.strictObject({
  id: z.string().min(1),
  title: z.string().min(1),
  summary: z.string().nullable(),
  glyph: z.string().min(1),
  planned: z.boolean(),
  pl: z.strictObject({ title: z.string().min(1), summary: z.string().nullable() }),
  entries: z.array(Entry),
});

const Area = z.strictObject({
  id: z.string().min(1),
  title: z.string().min(1),
  blurb: z.string().min(1),
  hue: z.number().int().min(0).max(360),
  planned: z.boolean(),
  pl: z.strictObject({ title: z.string().min(1), blurb: z.string().min(1) }),
  topics: z.array(Topic),
});

const Content = z.strictObject({
  areas: z.array(Area),
  meta: z.strictObject({
    versions: z.array(z.strictObject({ name: z.string(), version: z.string() })),
  }),
});

export type Content = z.infer<typeof Content>;
export type Area = z.infer<typeof Area>;
export type Topic = z.infer<typeof Topic>;
export type Entry = z.infer<typeof Entry>;
export type Output = z.infer<typeof Output>;
export type Widget = z.infer<typeof Widget>;

const path = process.env.CHEATSHEET_CONTENT_DATA ?? resolve("../generated/content.json");

export function loadContent(): Content {
  const result = Content.safeParse(JSON.parse(readFileSync(path, "utf8")));
  if (!result.success) {
    throw new Error(`${path} does not match the content schema:\n${z.prettifyError(result.error)}`);
  }
  return result.data;
}
