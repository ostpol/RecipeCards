# Recipe Cards

> [!WARNING]
> This is built with AI. Be careful.

Recipe Cards is a lightweight static web app for creating consistent, double-sided DIN A6 landscape recipe cards. It runs entirely in the browser with plain HTML, CSS, and JavaScript, so you can open it locally, edit a recipe, preview both sides, and print without a build step or server.

## What It Does

- Edits recipe content in a simple form-based sidebar
- Shows a live preview of the front and back of the card
- Prints in a fixed `A6 landscape` layout
- Imports and exports recipes as JSON
- Stores the current recipe and selected language in `localStorage`
- Embeds uploaded cover images directly into exported JSON
- Supports standalone bulk PDF generation from exported JSON files

## Project Structure

- `index.html` contains the editor UI and card preview markup
- `styles.css` contains the app styling, responsive layout, and print rules
- `script.js` handles state, rendering, import/export, image upload, and translations
- `tools/bulk_generate_pdfs.py` batch-renders exported JSON files into A6 PDFs using the existing browser layout
- `sample-recipe.json` is an example import file

## Getting Started

1. Clone or download this repository.
2. Open `index.html` in a modern browser.
3. Edit the fields in the left panel.
4. Use `Print card` to open the browser print dialog.
5. Use `Export JSON` to save the recipe for later.

No installation is required for the editor.

## Bulk PDF Generation

The repository includes a standalone Python renderer at `tools/bulk_generate_pdfs.py`.

Why this approach:

- it does not add bulk-export code to the browser app itself
- it reuses the existing `index.html`, `styles.css`, and `script.js`
- it prints through Chromium, so the PDF matches the same DOM and print CSS used by the editor

### Install Once

```bash
pip install playwright
python -m playwright install chromium
```

If Chromium is already installed elsewhere, you can also pass `--browser-executable /path/to/chrome`.

### Render One Recipe

```bash
python3 tools/bulk_generate_pdfs.py sample-recipe.json --verbose
```

This writes `pdf/sample-recipe.pdf` next to the input file.

### Render a Whole Folder

```bash
python3 tools/bulk_generate_pdfs.py exports --recursive --verbose
```

By default, PDFs are written to `exports/pdf/` and keep the same relative folder structure as the JSON input files.

### Useful Flags

- `--language en|de` forces the rendered UI language
- `--output-dir /path/to/output` changes where PDFs are written
- `--overwrite` replaces existing PDFs
- `--glob '*.json'` narrows which files are picked up

### Image Handling

The preferred workflow is still to export JSON from the editor, because embedded cover images are already stored as data URLs inside the JSON.

As a convenience, if a JSON file has no `image` value, the batch renderer will also look for a sibling image file with the same base name, for example:

- `my-recipe.json`
- `my-recipe.jpg`

Supported sidecar formats are `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.svg`, and `.bmp`.

## Ingredient Prioritization

You can prioritize ingredients by adding a trailing `!` to the end of an ingredient line.

Example:

```text
250 g pasta
1 lemon!
200 g ricotta
Parmesan!
```

Behavior:

- ingredients with a trailing `!` are shown first in the printed/previewed ingredients list
- prioritized ingredients are rendered in bold
- the trailing `!` is treated as a marker and is not shown in the preview
- the marker stays in the editor and exported JSON so the priority is preserved

## Printing Notes

For the intended card size and duplex alignment:

- Set paper size to `A6`
- Set orientation to `Landscape`
- Keep scale at `100%` or `Default`
- Turn off browser headers and footers
- For double-sided printing, use duplex with `flip on short edge`

If the printed result looks too large, the printer or browser is usually still set to `A4` or `Letter`.

## Import and Export Format

Recipes are stored as JSON objects with this general structure:

```json
{
  "title": "Tomato Galette",
  "subtitle": "Buttery pastry with mustard, herbs, and summer tomatoes",
  "prepTime": "25 min",
  "cookTime": "35 min",
  "servings": "4",
  "difficulty": "Medium",
  "ingredients": [
    "1 sheet puff pastry",
    "3 tbsp Dijon mustard"
  ],
  "instructions": [
    "Roll the pastry onto a lined tray.",
    "Spread mustard over the center, leaving a border."
  ],
  "notes": "Let it cool before slicing.",
  "image": "",
  "visibility": {
    "showCoverImage": true,
    "showSubtitle": true,
    "showBackHeader": true,
    "showMetaStrip": true,
    "showPrepTime": true,
    "showCookTime": true,
    "showServings": true,
    "showDifficulty": true,
    "showIngredients": true,
    "showInstructions": true,
    "showNotes": true
  }
}
```

Notes:

- `ingredients` and `instructions` are arrays of strings
- a trailing `!` on an ingredient marks it as prioritized for sorting and bold display
- `image` is a data URL when an image has been embedded
- missing fields are normalized to sensible defaults during import
- older JSON files without a `visibility` object can still be imported

See [`sample-recipe.json`](./sample-recipe.json) for a working example.

## Browser Storage

The app saves the current recipe in the browser using `localStorage`, which means:

- your latest recipe is preserved between refreshes on the same browser
- data is local to the browser and device you used
- very large embedded images may exceed browser storage limits

For long-term storage or sharing, export the recipe as JSON.

## Development

This is a dependency-free static project. To make changes:

1. Edit `index.html`, `styles.css`, or `script.js`
2. Reload the page in the browser
3. Test both on-screen preview and print output

Because print layout is a core feature, any layout changes should be checked in the browser print preview as well as on screen.
