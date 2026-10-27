# 18: Widgets in Outputs: capture ipywidgets controls and draw them as static pictures

**What to build:** An example that calls `interact` (ipywidgets) shows sliders, dropdowns and checkboxes above its plot in Jupyter. Today the build keeps only the figure at the starting values, and the controls are lost. The Author wants Students to see the controls too ("please do include static visualisations of the widgets"). So the build captures every control an example displays, with its settings and starting value, and the site draws them above the figure as a static, non-interactive picture. Ticket 19 (the Interactive plots Topic) needs this.

Checked before writing this ticket, with a kernel and no frontend, as in the build:

- The kernel sends a `comm_open` message (target `jupyter.widget`) for every widget model, with its full `state`. Later `comm_msg` messages with `method: "update"` change parts of that state. For example, interact sets `description` afterwards, and sets `value` from the function's default.
- `interact(plot, mu=(-3.0, 3.0), n=(0, 100, 5), kind=["a", "b"], show=True, name="x")` opens a `VBoxModel` whose `children` are `IPY_MODEL_<id>` references. The children are, in order, `FloatSliderModel` (`min`, `max`, `step`, `value`, `readout_format: ".2f"`), `IntSliderModel` (`readout_format: "d"`), `DropdownModel` (`_options_labels`, `index`), `CheckboxModel` (`value`), `TextModel` (`value`), and an `OutputModel`. There are also `LayoutModel` and `*StyleModel` models.
- A `display_data` message with `application/vnd.jupyter.widget-view+json` carries the `model_id` of the displayed `VBox`. The plot comes as an ordinary figure, drawn once with the starting values, and the build already captures it.

Decided (the Author accepted every recommendation and asked for the static controls):

- **Setup:** add ipywidgets with `uv add ipywidgets` (pinned) and add it to `EXAMPLE_LIBRARIES`, so the footer shows its version. Update `test_meta_lists_the_versions_examples_ran_with` and the authoring guide's Libraries line.
- **Capture** (`cheatsheet/execute.py`):
  - Collect widget states from `comm_open` messages with target `jupyter.widget`, and apply `comm_msg` updates.
  - For each `display_data` that carries a widget view, walk the displayed model's `children`, depth first and in order. Keep the controls; walk through containers (`VBox`, `HBox`, `Box`); skip `OutputModel`.
  - The result is a new `Run.widgets` tuple, in display order, alongside `figures`.
- **Supported controls** and their data in `generated/content.json` (`output.widgets`, also on a Pitfall's Output):
  - `IntSlider` / `FloatSlider` → `{"kind": "slider", "description", "min", "max", "step", "value", "readout"}`. `readout` is the value formatted with the widget's `readout_format` (`".2f"` → `0.00`, `"d"` → `10`), using Python's `format()`, as Jupyter shows it.
  - `Dropdown` → `{"kind": "dropdown", "description", "options": [labels], "value": <selected label>}`.
  - `Checkbox` → `{"kind": "checkbox", "description", "value": true/false}`.
  - `Text` → `{"kind": "text", "description", "value"}`.
- **Any other control** (e.g. the button `interact_manual` adds, `FloatLogSlider`, `RadioButtons`) stops the build. It is listed with the other example failures: `the example displays a <ButtonModel> widget, which the site can't draw yet`. Add that row to the guide's validation table.
- **Site** (`OutputBlock` and a new component):
  - The controls are drawn inside the Output, above its figures, in display order, in the site's look and the Area's hue, and laid out like Jupyter's.
  - A slider is the description on the left, then a track filled up to the value with a round knob at the value's position, then the readout on the right. A dropdown is a box with the selected option and ▾. A checkbox is a ticked or empty box, then its description. A text box shows its value.
  - It is a picture, not a form: no `input`/`select` elements, nothing focusable, `pointer-events: none`.
  - A small caption, styled like the Output's label, says it's a picture of the Jupyter controls ("Controls in Jupyter" / "Kontrolki w Jupyterze", in `labels.ts`), so nobody tries to drag the knob.
  - It works in both themes and at card width on a phone (375px) with no sideways scrolling.
- **Accessibility:** the drawing is `aria-hidden`. A visually hidden list reads each control in the page's Language, with the phrasing in `labels.ts`. For example:
  - EN "mu: slider from -3.00 to 3.00, at 0.00" / PL "mu: suwak od -3.00 do 3.00, ustawiony na 0.00"
  - EN "kind: dropdown with a, b; a selected" / PL "kind: lista rozwijana z a, b; wybrane a"
  - EN "show: checkbox, checked" / PL "show: pole wyboru, zaznaczone"
  - EN "name: text box, x" / PL "name: pole tekstowe, x"

  The agent may improve the wording. Descriptions and values are code and stay as they are. axe passes in both themes.
- **Tests:**
  - Fixture content with an `interact` example that uses every supported kind, including an int slider with a step and a value set by the function's default.
  - A content-build test of the captured `widgets` data.
  - A build test that an unsupported widget fails with the message above.
  - Browser tests for the drawing: it is above the figure, the knob sits at the value's proportion of the track, nothing is focusable, and the screen-reader text is right in both Languages.
  - The accessibility tests cover the new fixture.
- **Authoring guide:** a short "Widgets" section.
  - The Output is the figure at the starting values, with the controls drawn above it.
  - The function's defaults set the starting values.
  - Which controls are supported.
  - The figure description describes the plot at the starting values. The controls get their own screen-reader text, so it doesn't list them.

**Blocked by:** none.

**Status:** ready-for-agent

- [ ] ipywidgets is installed with uv and pinned, it is in `EXAMPLE_LIBRARIES` and in the footer, and the tests and guide match.
- [ ] The build captures the controls an example displays, in order and with their final state, as `output.widgets` (Entry and Pitfall), for the four supported kinds; containers are walked and Output widgets skipped.
- [ ] An unsupported widget fails the build with the decided message, listed with the other example failures, and the guide's validation table has the row.
- [ ] The site draws the controls above the figure as a static picture, with the caption, in both themes and at phone width, and nothing in it can be focused or used.
- [ ] Screen readers hear each control in the page's Language, and axe passes.
- [ ] Content-build and browser tests cover the above, with a new fixture.
- [ ] The authoring guide has the Widgets section.
- [ ] `uv run cheatsheet build` and `uv run pytest` pass; the fixture page was looked at in both Languages and both themes.
- [ ] One session and one PR, which also adds this ticket and ticket 19.

## Comments
