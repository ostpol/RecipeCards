#!/usr/bin/env python3
"""Batch-render exported recipe JSON files to A6 landscape PDFs.

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
SUPPORTED_IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".bmp")


@dataclass(frozen=True)
class RecipeJob:
    input_path: Path
    output_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate one A6 PDF per exported recipe JSON using the existing Recipe Cards layout."
    )
    parser.add_argument("input", help="A recipe JSON file or a directory containing recipe JSON files.")
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


def collect_jobs(input_path: Path, output_dir: Path | None, glob_pattern: str, recursive: bool) -> list[RecipeJob]:
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
    jobs: list[RecipeJob] = []

    for json_path in json_paths:
        if input_path.is_dir():
            relative = json_path.relative_to(base_input_dir)
            pdf_path = (target_dir / relative).with_suffix(".pdf")
        else:
            pdf_path = (target_dir / json_path.stem).with_suffix(".pdf")
        jobs.append(RecipeJob(input_path=json_path, output_path=pdf_path))

    return jobs


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
    bootstrap_script = f"""
<script>
(() => {{
  const storage = new Map();
  const fallbackStorage = {{
    getItem(key) {{
      return storage.has(key) ? storage.get(key) : null;
    }},
    setItem(key, value) {{
      storage.set(String(key), String(value));
    }},
    removeItem(key) {{
      storage.delete(String(key));
    }},
    clear() {{
      storage.clear();
    }}
  }};

  try {{
    window.localStorage.setItem('__recipe_cards_probe__', '1');
    window.localStorage.removeItem('__recipe_cards_probe__');
  }} catch (error) {{
    Object.defineProperty(window, 'localStorage', {{
      configurable: true,
      value: fallbackStorage
    }});
  }}

  window.localStorage.setItem({json.dumps(STORAGE_KEY)}, {json.dumps(recipe_payload)});
  window.localStorage.setItem({json.dumps(LANGUAGE_KEY)}, {json.dumps(language)});
}})();
</script>
""".strip()

    html = index_html.replace(
        '<link rel="stylesheet" href="styles.css">',
        f"<style>\n{styles_css}\n</style>",
        1,
    )
    html = html.replace(
        '<script src="script.js"></script>',
        f"{bootstrap_script}\n<script>\n{script_js}\n</script>",
        1,
    )
    return html


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


async def render_job(
    page: object,
    job: RecipeJob,
    language: str,
    timeout_ms: int,
    index_html: str,
    styles_css: str,
    script_js: str,
) -> None:
    recipe_payload = load_recipe_json(job.input_path)
    html = build_inline_app_html(index_html, styles_css, script_js, recipe_payload, language)

    await page.set_content(html, wait_until="load", timeout=timeout_ms)
    await wait_for_recipe_ready(page, timeout_ms)
    await page.emulate_media(media="print")

    job.output_path.parent.mkdir(parents=True, exist_ok=True)
    await page.pdf(
        path=str(job.output_path),
        print_background=True,
        width=PDF_PAGE_WIDTH,
        height=PDF_PAGE_HEIGHT,
        margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"},
    )


async def render_all(
    jobs: list[RecipeJob],
    repo_root: Path,
    language: str,
    timeout_ms: int,
    browser_executable: str | None,
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
            page = await browser.new_page(viewport={"width": 1600, "height": 1200}, device_scale_factor=1)
            for job in jobs:
                if job.output_path.exists() and not overwrite:
                    if verbose:
                        print(f"skip  {job.output_path}")
                    continue

                try:
                    await render_job(page, job, language, timeout_ms, index_html, styles_css, script_js)
                except PlaywrightTimeoutError:
                    failures += 1
                    print(f"error Timed out while rendering {job.input_path}", file=sys.stderr)
                except Exception as exc:
                    failures += 1
                    print(f"error Failed to render {job.input_path}: {exc}", file=sys.stderr)
                else:
                    if verbose:
                        print(f"wrote {job.output_path}")
        finally:
            await browser.close()

    return failures


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    validate_repo_root(repo_root)

    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else None
    jobs = collect_jobs(input_path, output_dir, args.glob, args.recursive)

    failures = asyncio.run(
        render_all(
            jobs=jobs,
            repo_root=repo_root,
            language=args.language,
            timeout_ms=max(1, int(args.timeout_seconds * 1000)),
            browser_executable=args.browser_executable,
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
