#!/usr/bin/env python3
"""Batch-render exported recipe JSON files to printable PDFs.

The script reuses the existing Recipe Cards web app renderer by inlining the
repository's HTML, CSS, and JavaScript into a temporary page, seeding
localStorage with each recipe JSON, and asking Playwright/Chromium to print the
page. This keeps the generated PDFs aligned with the web app editor and print
layout without implementing bulk export inside the HTML app itself.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import json
import mimetypes
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

STORAGE_KEY = "recipe-card-current"
LANGUAGE_KEY = "recipe-card-language"
PDF_PAGE_WIDTH = "148mm"
PDF_PAGE_HEIGHT = "105mm"
A5_SHEET_WIDTH = "148mm"
A5_SHEET_HEIGHT = "210mm"
SUPPORTED_IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".bmp")


@dataclass(frozen=True)
class RenderJob:
    input_paths: tuple[Path, ...]
    output_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate printable PDFs from exported recipe JSON using the existing Recipe Cards layout."
    )
    parser.add_argument(
        "input",
        nargs="+",
        help="One input path for A6 mode, or one to two exported recipe JSON files for a5-2up mode.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        help="Directory where PDFs should be written. Defaults to <input>/pdf or <input parent>/pdf.",
    )
    parser.add_argument(
        "--language",
        default="en",
        choices=("en", "de"),
        help="Language to force inside the renderer. Defaults to en.",
    )
    parser.add_argument(
        "--sheet-layout",
        default="a6",
        choices=("a6", "a5-2up"),
        help="PDF layout: single A6 landscape card per page or two cards per A5 portrait sheet. Defaults to a6.",
    )
    parser.add_argument(
        "--browser-executable",
        help="Optional path to an installed Chromium or Chrome executable.",
    )
    parser.add_argument(
        "--glob",
        default="*.json",
        help="Glob to use when the input is a directory. Defaults to *.json.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search directories recursively for JSON files.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing PDFs instead of skipping them.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=30,
        help="Per-file render timeout. Defaults to 30 seconds.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print each rendered output path.",
    )
    return parser.parse_args()


def ensure_playwright() -> tuple[object, object]:
    try:
        from playwright.async_api import TimeoutError as PlaywrightTimeoutError
        from playwright.async_api import async_playwright
    except ImportError as exc:
        raise SystemExit(
            "Playwright is required. Install it with `pip install playwright` and then run "
            "`python -m playwright install chromium` once."
        ) from exc

    return async_playwright, PlaywrightTimeoutError


def validate_repo_root(repo_root: Path) -> None:
    required = [repo_root / "index.html", repo_root / "styles.css", repo_root / "script.js"]
    missing = [path.name for path in required if not path.exists()]
    if missing:
        raise SystemExit(f"Repository root is missing required app files: {', '.join(missing)}")


def collect_jobs(
    input_paths: list[Path],
    output_dir: Path | None,
    glob_pattern: str,
    recursive: bool,
    sheet_layout: str,
) -> list[RenderJob]:
    if sheet_layout == "a5-2up":
        return collect_a5_sheet_jobs(input_paths, output_dir)

    if len(input_paths) != 1:
        raise SystemExit("A6 mode expects exactly one input path.")

    input_path = input_paths[0]
    if input_path.is_file():
        json_paths = [input_path]
        base_input_dir = input_path.parent
    elif input_path.is_dir():
        pattern_iter: Iterable[Path]
        pattern_iter = input_path.rglob(glob_pattern) if recursive else input_path.glob(glob_pattern)
        json_paths = sorted(path for path in pattern_iter if path.is_file() and path.suffix.lower() == ".json")
        base_input_dir = input_path
    else:
        raise SystemExit(f"Input path does not exist: {input_path}")

    if not json_paths:
        raise SystemExit(f"No JSON files found in {input_path}")

    target_dir = output_dir or (base_input_dir / "pdf")
    jobs: list[RenderJob] = []

    for json_path in json_paths:
        if input_path.is_dir():
            relative = json_path.relative_to(base_input_dir)
            pdf_path = (target_dir / relative).with_suffix(".pdf")
        else:
            pdf_path = (target_dir / json_path.stem).with_suffix(".pdf")
        jobs.append(RenderJob(input_paths=(json_path,), output_path=pdf_path))

    return jobs


def collect_a5_sheet_jobs(input_paths: list[Path], output_dir: Path | None) -> list[RenderJob]:
    if not 1 <= len(input_paths) <= 2:
        raise SystemExit("A5 2-up mode expects one or two JSON files.")

    resolved_inputs = [path.resolve() for path in input_paths]
    for path in resolved_inputs:
        if not path.exists():
            raise SystemExit(f"Input path does not exist: {path}")
        if not path.is_file() or path.suffix.lower() != ".json":
            raise SystemExit("A5 2-up mode only supports explicit JSON files, not directories.")

    base_dir = resolved_inputs[0].parent
    target_dir = output_dir or (base_dir / "pdf")
    stem = "__".join(path.stem for path in resolved_inputs)
    pdf_path = (target_dir / stem).with_suffix(".pdf")
    return [RenderJob(input_paths=tuple(resolved_inputs), output_path=pdf_path)]


def infer_sidecar_image(recipe: object, json_path: Path) -> object:
    if not isinstance(recipe, dict):
        return recipe

    if recipe.get("image"):
        return recipe

    for suffix in SUPPORTED_IMAGE_SUFFIXES:
        candidate = json_path.with_suffix(suffix)
        if not candidate.exists():
            continue

        mime_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        encoded = base64.b64encode(candidate.read_bytes()).decode("ascii")
        hydrated = dict(recipe)
        hydrated["image"] = f"data:{mime_type};base64,{encoded}"
        return hydrated

    return recipe


def load_recipe_json(json_path: Path) -> str:
    try:
        parsed = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {json_path}: {exc}") from exc

    hydrated = infer_sidecar_image(parsed, json_path)
    return json.dumps(hydrated, ensure_ascii=False)


def load_app_assets(repo_root: Path) -> tuple[str, str, str]:
    return (
        (repo_root / "index.html").read_text(encoding="utf-8"),
        (repo_root / "styles.css").read_text(encoding="utf-8"),
        (repo_root / "script.js").read_text(encoding="utf-8"),
    )


def build_inline_app_html(index_html: str, styles_css: str, script_js: str, recipe_payload: str, language: str) -> str:
    script_prelude = f"""
const __recipeCardStorageMap = new Map();
const __recipeCardLocalStorage = {{
  getItem(key) {{
    return __recipeCardStorageMap.has(key) ? __recipeCardStorageMap.get(key) : null;
  }},
  setItem(key, value) {{
    __recipeCardStorageMap.set(String(key), String(value));
  }},
  removeItem(key) {{
    __recipeCardStorageMap.delete(String(key));
  }},
  clear() {{
    __recipeCardStorageMap.clear();
  }}
}};
__recipeCardLocalStorage.setItem({json.dumps(STORAGE_KEY)}, {json.dumps(recipe_payload)});
__recipeCardLocalStorage.setItem({json.dumps(LANGUAGE_KEY)}, {json.dumps(language)});
const localStorage = __recipeCardLocalStorage;
try {{
  Object.defineProperty(window, 'localStorage', {{
    configurable: true,
    value: __recipeCardLocalStorage
  }});
}} catch (error) {{
  // The inline script uses the lexical localStorage binding above, so this is optional.
}}
""".strip()

    html = index_html.replace(
        '<link rel="stylesheet" href="styles.css">',
        f"<style>\n{styles_css}\n</style>",
        1,
    )
    html = html.replace(
        '<script src="script.js"></script>',
        f"<script>\n{script_prelude}\n{script_js}\n</script>",
        1,
    )
    return html


def sanitize_card_markup(card_html: str) -> str:
    return card_html.replace(" print-page", "").replace("print-page ", "").replace("print-page", "")


def build_a5_sheet_html(styles_css: str, front_cards: list[str], back_cards: list[str]) -> str:
    def build_slots(cards: list[str]) -> str:
        slots: list[str] = []
        for index in range(2):
            inner = sanitize_card_markup(cards[index]) if index < len(cards) else ""
            slots.append(f'<div class="sheet-card-slot">{inner}</div>')
        return "\n".join(slots)

    front_slots = build_slots(front_cards)
    back_slots = build_slots(back_cards)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Recipe Cards A5 Sheet</title>
  <style>
{styles_css}

html,
body {{
  margin: 0;
  background: #ffffff;
}}

body {{
  width: 148mm;
}}

.preview-stack {{
  display: grid;
  gap: 0;
  justify-content: start;
  padding: 0;
}}

.print-sheet {{
  position: relative;
  width: 148mm;
  height: 210mm;
  display: grid;
  grid-template-rows: repeat(2, 105mm);
  background: #ffffff;
  overflow: hidden;
}}

.sheet-card-slot {{
  width: 148mm;
  height: 105mm;
  overflow: hidden;
}}

.sheet-card-slot:empty {{
  background: #ffffff;
}}

.sheet-card-slot > .recipe-card {{
  width: 148mm;
  height: 105mm;
  border-radius: 0;
  box-shadow: none;
}}

.sheet-divider {{
  position: absolute;
  left: 0;
  right: 0;
  top: calc(105mm - 0.2mm);
  height: 0.4mm;
  background: rgba(0, 0, 0, 0.18);
  pointer-events: none;
  z-index: 30;
}}

@media print {{
  @page {{
    size: A5 portrait;
    margin: 0;
  }}

  .print-sheet {{
    width: 148mm;
    height: 210mm;
    break-after: page;
    page-break-after: always;
  }}

  .print-sheet:last-child {{
    break-after: auto;
    page-break-after: auto;
  }}
}}
  </style>
</head>
<body>
  <div class="preview-stack">
    <section class="print-sheet print-sheet-front">
      <div class="sheet-divider"></div>
{front_slots}
    </section>
    <section class="print-sheet print-sheet-back">
{back_slots}
    </section>
  </div>
</body>
</html>
"""


async def wait_for_recipe_ready(page: object, timeout_ms: int) -> None:
    await page.wait_for_selector(".recipe-card-front", timeout=timeout_ms)
    await page.wait_for_function(
        """
        async () => {
          const images = Array.from(document.images);
          await Promise.all(images.map((img) => img.complete ? Promise.resolve() : new Promise((resolve, reject) => {
            img.addEventListener('load', resolve, { once: true });
            img.addEventListener('error', reject, { once: true });
          })));
          return true;
        }
        """,
        timeout=timeout_ms,
    )


async def render_recipe_cards(
    browser: object,
    recipe_path: Path,
    language: str,
    timeout_ms: int,
    index_html: str,
    styles_css: str,
    script_js: str,
) -> tuple[str, str]:
    recipe_payload = load_recipe_json(recipe_path)
    html = build_inline_app_html(index_html, styles_css, script_js, recipe_payload, language)

    page = await browser.new_page(viewport={"width": 1600, "height": 1200}, device_scale_factor=1)
    try:
        await page.set_content(html, wait_until="load", timeout=timeout_ms)
        await wait_for_recipe_ready(page, timeout_ms)
        return await page.evaluate(
            """
            () => {
              const front = document.querySelector(".recipe-card-front");
              const back = document.querySelector(".recipe-card-back");

              if (!front || !back) {
                throw new Error("Could not find rendered recipe cards.");
              }

              return [front.outerHTML, back.outerHTML];
            }
            """
        )
    finally:
        await page.close()


async def render_job(
    browser: object,
    page: object,
    job: RenderJob,
    language: str,
    timeout_ms: int,
    index_html: str,
    styles_css: str,
    script_js: str,
    sheet_layout: str,
) -> None:
    if sheet_layout == "a6":
        recipe_payload = load_recipe_json(job.input_paths[0])
        html = build_inline_app_html(index_html, styles_css, script_js, recipe_payload, language)
        await page.set_content(html, wait_until="load", timeout=timeout_ms)
        await wait_for_recipe_ready(page, timeout_ms)
    else:
        front_cards: list[str] = []
        back_cards: list[str] = []

        for recipe_path in job.input_paths:
            front_html, back_html = await render_recipe_cards(
                browser=browser,
                recipe_path=recipe_path,
                language=language,
                timeout_ms=timeout_ms,
                index_html=index_html,
                styles_css=styles_css,
                script_js=script_js,
            )
            front_cards.append(front_html)
            back_cards.append(back_html)

        html = build_a5_sheet_html(styles_css, front_cards, back_cards)
        await page.set_content(html, wait_until="load", timeout=timeout_ms)

    await page.emulate_media(media="print")

    job.output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_width = PDF_PAGE_WIDTH if sheet_layout == "a6" else A5_SHEET_WIDTH
    pdf_height = PDF_PAGE_HEIGHT if sheet_layout == "a6" else A5_SHEET_HEIGHT
    await page.pdf(
        path=str(job.output_path),
        print_background=True,
        width=pdf_width,
        height=pdf_height,
        margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"},
    )


async def render_all(
    jobs: list[RenderJob],
    repo_root: Path,
    language: str,
    timeout_ms: int,
    browser_executable: str | None,
    sheet_layout: str,
    overwrite: bool,
    verbose: bool,
) -> int:
    async_playwright, PlaywrightTimeoutError = ensure_playwright()
    failures = 0
    index_html, styles_css, script_js = load_app_assets(repo_root)

    async with async_playwright() as playwright:
        launch_kwargs = {"headless": True}
        if browser_executable:
            launch_kwargs["executable_path"] = browser_executable

        browser = await playwright.chromium.launch(**launch_kwargs)
        try:
            for job in jobs:
                if job.output_path.exists() and not overwrite:
                    if verbose:
                        print(f"skip  {job.output_path}")
                    continue

                page = await browser.new_page(viewport={"width": 1600, "height": 1200}, device_scale_factor=1)
                try:
                    await render_job(browser, page, job, language, timeout_ms, index_html, styles_css, script_js, sheet_layout)
                except PlaywrightTimeoutError:
                    failures += 1
                    print(f"error Timed out while rendering {', '.join(str(path) for path in job.input_paths)}", file=sys.stderr)
                except Exception as exc:
                    failures += 1
                    print(f"error Failed to render {', '.join(str(path) for path in job.input_paths)}: {exc}", file=sys.stderr)
                else:
                    if verbose:
                        print(f"wrote {job.output_path}")
                finally:
                    await page.close()
        finally:
            await browser.close()

    return failures


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    validate_repo_root(repo_root)

    input_paths = [Path(raw_input).expanduser().resolve() for raw_input in args.input]
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else None
    jobs = collect_jobs(input_paths, output_dir, args.glob, args.recursive, args.sheet_layout)

    failures = asyncio.run(
        render_all(
            jobs=jobs,
            repo_root=repo_root,
            language=args.language,
            timeout_ms=max(1, int(args.timeout_seconds * 1000)),
            browser_executable=args.browser_executable,
            sheet_layout=args.sheet_layout,
            overwrite=args.overwrite,
            verbose=args.verbose,
        )
    )

    if failures:
        print(f"Completed with {failures} failure(s).", file=sys.stderr)
        return 1

    print(f"Generated {len(jobs)} PDF(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
