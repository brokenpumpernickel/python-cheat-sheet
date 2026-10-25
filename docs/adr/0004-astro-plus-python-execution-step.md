# Astro site with a separate Python execution step

The site is built with Astro (Markdown content with schema validation, plain static HTML output) and a small client-side layer for zoom, Index and search. Before Astro runs, a Python step executes every Entry in a Jupyter kernel with pinned library versions and stores the Outputs and figures for Astro to render. We rejected hand-rolled HTML/JS (we'd rebuild the content pipeline ourselves) and a React SPA (heavier than a static reference needs).
