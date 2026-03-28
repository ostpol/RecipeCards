# Recipe Cards

> [!WARNING]
> This is built with AI. Be careful.

Recipe Cards is a small static web app for creating printable recipe cards in `DIN A6 landscape`.

The project has two parts:

- the browser editor for creating and printing individual cards
- a standalone Python script for generating PDFs from exported recipe JSON files

The editor runs locally in the browser. There is no build step, no framework, and no server.

## What This Repo Is For

Use this repo when you want to:

- write or update a recipe in a fixed card layout
- preview front and back before printing
- store recipes as JSON files
- print a single card directly from the browser
- generate PDFs in bulk from exported JSON files

## Quick Start

1. Open `index.html` in a modern browser.
2. Edit the recipe fields in the left panel.
3. Optionally upload a cover image.
4. Use `Export JSON` to save the recipe.
5. Use `Print card` if you want to print directly from the browser.

That is the whole basic workflow.

## How The Editor Works

The editor is a live preview tool:

- the left side is the form
- the right side is the printable preview
- changes are saved in the browser automatically
- the current recipe and selected language are stored in `localStorage`

Supported editor features:

- English and German UI
- optional cover image
- JSON import and export
- per-section visibility toggles
- front and back preview
- print styling for `A6 landscape`

## Recipe Writing Conventions

The ingredients field supports two small formatting conventions.

### Prioritized Ingredients

Add a trailing `!` to mark an ingredient as important.

Example:

```text
Butter!
Flour
Eggs!
Milk
```

What happens:

- prioritized ingredients are shown first
- prioritized ingredients are printed in bold
- the trailing `!` is not shown in the preview
- the marker stays in the editor and exported JSON

### Ingredient Categories

Add a line starting with `#` to begin a category.

Example:

```text
# Dough
Flour
Water
Salt!

# Filling
Spinach
Ricotta!
Nutmeg
```

What happens:

- category lines become headings in the preview
- ingredients stay grouped under their category
- prioritization still works, but only inside each category
- uncategorized ingredients before the first category are still allowed

## Printing

The browser editor is designed for `A6 landscape`.

Recommended print settings:

- paper size: `A6`
- orientation: `Landscape`
- scale: `100%` or `Default`
- headers and footers: off
- margins: `None` or `Default`

For duplex printing:

- use `flip on short edge`

Important practical note:

Many printers do not support automatic duplex printing on `A6`. In practice, manual turning is often necessary.

If the output looks too large, the printer or browser is usually still set to `A4` or `Letter`.

## JSON Workflow

The editor exports recipes as JSON.

This is the recommended long-term workflow:

1. Create or edit the recipe in the browser.
2. Export it as JSON.
3. Keep the JSON file as the canonical saved version.
4. Re-import it later when you want to continue editing.

Why this matters:

- browser storage is local to one browser profile
- embedded images can make browser storage too large
- exported JSON is portable, versionable, and easier to back up

## Bulk PDF Generation

The repository includes `tools/bulk_generate_pdfs.py`.

This script exists so PDF generation can reuse the exact same HTML, CSS, and JavaScript as the browser editor.

### Install Once

```bash
pip install playwright
python -m playwright install chromium
```

If Chromium is already installed elsewhere, you can also pass:

```bash
--browser-executable /path/to/chrome
```

### A6 PDFs

Render one recipe:

```bash
python3 tools/bulk_generate_pdfs.py sample-recipe.json --verbose
```

Render a whole folder:

```bash
python3 tools/bulk_generate_pdfs.py exports --recursive --verbose
```

By default, PDFs are written to a `pdf/` folder next to the input location.

### A5 Workaround For Manual Turning

If your printer cannot duplex `A6`, use:

```bash
python3 tools/bulk_generate_pdfs.py sample-recipe.json --sheet-layout a5-2up --verbose
```

In `a5-2up` mode:

- the script accepts one or two explicit JSON files
- one JSON places one card on the top half of the A5 sheet
- two JSON files place two cards on the sheet, stacked vertically
- page 1 contains the front sides
- page 2 contains the matching back sides
- the front page includes a light gray guide line in the exact middle

Two-card example:

```bash
python3 tools/bulk_generate_pdfs.py recipe-one.json recipe-two.json --sheet-layout a5-2up --verbose
```

Directory input is only supported in the default `a6` mode.

### Sidecar Images

If a JSON file does not contain an embedded `image`, the PDF generator also looks for an image file with the same base name.

Example:

- `my-recipe.json`
- `my-recipe.jpg`

Supported sidecar formats:

- `.png`
- `.jpg`
- `.jpeg`
- `.webp`
- `.gif`
- `.svg`
- `.bmp`

## Files In This Repo

- `index.html`
  The app structure and preview markup.
- `styles.css`
  Screen layout, print layout, and card styling.
- `script.js`
  Editor state, rendering, import/export, language switching, ingredient logic, and browser storage handling.
- `tools/bulk_generate_pdfs.py`
  Playwright-based PDF generator that renders exported JSON through the same app layout.
- `sample-recipe.json`
  Small example import file.

## If You Come Back Later

If you open this repo again in a few months and want to remember how to work with it, use this checklist:

1. Open `index.html` for normal editing.
2. Export recipes as JSON when you want to keep them.
3. Use browser print for single cards.
4. Use `tools/bulk_generate_pdfs.py` for batch PDFs.
5. Use `--sheet-layout a5-2up` when A6 duplex printing is impractical.
6. Treat the exported JSON files as the real saved data, not browser storage.

## Development Notes

This project is intentionally simple.

- no build step
- no package manager
- no frontend framework
- no backend

When changing the app:

1. edit `index.html`, `styles.css`, `script.js`, or `tools/bulk_generate_pdfs.py`
2. reload the browser
3. test both screen preview and print preview
4. if you changed PDF generation, also test the Python script

Because printing is the core feature, visual checks matter more than usual. Always verify both layout and paper assumptions after changing card dimensions, spacing, or print rules.
