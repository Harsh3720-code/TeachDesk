"""Build the TeachDesk Engineering Handbook (.docx and .pdf) from Markdown.

Source of truth is Markdown under ``docs/``; the Word and PDF files are build
outputs written to ``docs/build/`` and are never committed (see ADR-0001).

Pipeline:
    docs/handbook/*.md + docs/adr/*.md
        -> pandoc (styled by docs/templates/reference.docx) -> .docx
        -> LibreOffice (headless)                           -> .pdf

Usage:
    uv run python scripts/build_docs.py            # .docx and .pdf
    uv run python scripts/build_docs.py --no-pdf   # .docx only
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterable
from pathlib import Path

import pypandoc  # type: ignore[import-untyped]  # ships no type information

ROOT = Path(__file__).resolve().parents[1]
HANDBOOK_DIR = ROOT / "docs" / "handbook"
ADR_DIR = ROOT / "docs" / "adr"
REFERENCE_DOCX = ROOT / "docs" / "templates" / "reference.docx"
BUILD_DIR = ROOT / "docs" / "build"

TITLE = "TeachDesk Engineering Handbook"
SUBTITLE = "AI admin assistant for UK secondary school teachers"
OUTPUT_STEM = "TeachDesk-Engineering-Handbook"

# ADRs are inserted directly after the chapter whose file name starts with this.
ADR_ANCHOR_PREFIX = "03-"

_FENCE = re.compile(r"^(```|~~~)")
_HEADING = re.compile(r"^#{1,5} ")


class BuildError(RuntimeError):
    """Raised when the handbook cannot be built."""


def ordered_sources() -> list[Path]:
    """Return handbook chapters in file-name order, with ADRs after chapter 03."""
    chapters = sorted(HANDBOOK_DIR.glob("[0-9][0-9]-*.md"))
    adrs = sorted(ADR_DIR.glob("[0-9][0-9][0-9][0-9]-*.md"))
    if not chapters:
        raise BuildError(f"No chapters found in {HANDBOOK_DIR}")

    ordered: list[Path] = []
    for chapter in chapters:
        ordered.append(chapter)
        if chapter.name.startswith(ADR_ANCHOR_PREFIX):
            ordered.extend(adrs)
    return ordered


def demote_headings(markdown: str) -> str:
    """Demote every ATX heading one level, ignoring fenced code blocks.

    ADRs use a level-1 heading so they read correctly on their own (e.g. on
    GitHub); inside the handbook they sit beneath the decision-log chapter.
    """
    out: list[str] = []
    in_fence = False
    for line in markdown.splitlines(keepends=True):
        if _FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence and _HEADING.match(line):
            line = "#" + line
        out.append(line)
    return "".join(out)


def assemble_markdown(sources: Iterable[Path]) -> str:
    """Concatenate sources into one document, demoting ADR headings."""
    parts: list[str] = []
    for path in sources:
        text = path.read_text(encoding="utf-8")
        if path.parent == ADR_DIR:
            text = demote_headings(text)
        parts.append(text.rstrip() + "\n")
    return "\n\n".join(parts)


def git_revision() -> str:
    """Short commit hash of the working tree, marked '-dirty' if modified."""
    try:
        result = subprocess.run(
            ["git", "describe", "--always", "--dirty"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return result.stdout.strip()


# Pandoc lays out GFM tables at natural width with equal columns. This filter
# gives every table the full text width, with columns proportional to their
# longest cell (clamped so one long cell cannot starve the others), and never
# narrower than their longest word, so words are not broken mid-word.
_TABLE_WIDTH_FILTER = """
local MIN, MAX, WORD = 8, 60, 1.4
function Table(tbl)
  local n = #tbl.colspecs
  local longest = {}
  for i = 1, n do longest[i] = MIN end
  local function measure(rows)
    for _, row in ipairs(rows) do
      for i, cell in ipairs(row.cells) do
        if i <= n then
          local text = pandoc.utils.stringify(cell.contents)
          longest[i] = math.max(longest[i], math.min(#text, MAX))
          for word in text:gmatch("%S+") do
            longest[i] = math.max(longest[i], math.min(#word * WORD, MAX))
          end
        end
      end
    end
  end
  measure(tbl.head.rows)
  for _, body in ipairs(tbl.bodies) do measure(body.body) end
  local total = 0
  for i = 1, n do total = total + longest[i] end
  for i = 1, n do tbl.colspecs[i][2] = longest[i] / total end
  return tbl
end
"""


def build_docx(markdown: str, output: Path) -> None:
    """Render the assembled Markdown to a styled .docx with pandoc."""
    if not REFERENCE_DOCX.is_file():
        raise BuildError(f"Missing Word style template: {REFERENCE_DOCX}")

    today = dt.date.today().isoformat()
    with tempfile.TemporaryDirectory() as tmp:
        table_filter = Path(tmp) / "table-widths.lua"
        table_filter.write_text(_TABLE_WIDTH_FILTER, encoding="utf-8")
        _run_pandoc(markdown, output, table_filter, today)


def _run_pandoc(markdown: str, output: Path, table_filter: Path, today: str) -> None:
    pypandoc.convert_text(
        markdown,
        to="docx",
        format="gfm+yaml_metadata_block",
        outputfile=str(output),
        extra_args=[
            f"--reference-doc={REFERENCE_DOCX}",
            f"--lua-filter={table_filter}",
            f"--resource-path={ROOT / 'docs'}",
            "--toc",
            "--toc-depth=2",
            "--number-sections",
            f"--metadata=title:{TITLE}",
            f"--metadata=subtitle:{SUBTITLE}",
            f"--metadata=date:{today} · build {git_revision()}",
            "--metadata=toc-title:Contents",
        ],
    )


def find_soffice() -> str:
    """Locate the LibreOffice binary (override with the SOFFICE env var)."""
    if override := os.environ.get("SOFFICE"):
        if not Path(override).is_file():
            raise BuildError(f"SOFFICE={override} does not exist.")
        return override
    candidate = shutil.which("soffice") or shutil.which("libreoffice")
    if not candidate:
        raise BuildError(
            "LibreOffice not found; install it or set SOFFICE, or run with --no-pdf."
        )
    return candidate


def find_uno_python(soffice: str) -> str:
    """Locate a Python interpreter that can ``import uno``.

    LibreOffice's scripting bridge is not installable from PyPI, so it cannot
    live in the uv environment. Windows/macOS builds bundle a ``python`` next
    to ``soffice``; Linux distributions ship it for the system interpreter.
    Override with the UNO_PYTHON env var.
    """
    if override := os.environ.get("UNO_PYTHON"):
        return override
    program_dir = Path(soffice).resolve().parent
    for name in ("python", "python.exe", "python3"):
        bundled = program_dir / name
        if bundled.is_file():
            return str(bundled)
    return "/usr/bin/python3"


# Runs under LibreOffice's Python (see find_uno_python), not the uv environment.
# argv: soffice, profile_dir, pipe_name, docx_path, pdf_path
_UNO_EXPORT = r"""
import subprocess, sys, time
from pathlib import Path
import uno
from com.sun.star.beans import PropertyValue

soffice, profile, pipe, src, dst = sys.argv[1:6]

def props(**kw):
    out = []
    for k, v in kw.items():
        p = PropertyValue(); p.Name = k; p.Value = v; out.append(p)
    return tuple(out)

office = subprocess.Popen(
    [soffice, f"-env:UserInstallation={Path(profile).as_uri()}", "--headless",
     "--invisible", "--nologo", "--norestore", f"--accept=pipe,name={pipe};urp;"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)
try:
    resolver = uno.getComponentContext().ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", uno.getComponentContext())
    for _ in range(120):
        try:
            ctx = resolver.resolve(f"uno:pipe,name={pipe};urp;StarOffice.ComponentContext")
            break
        except Exception:
            time.sleep(0.5)
    else:
        sys.exit("could not connect to LibreOffice")
    desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    doc = desktop.loadComponentFromURL(Path(src).resolve().as_uri(), "_blank", 0, props(Hidden=True))
    if doc is None:
        sys.exit(f"LibreOffice could not load {src}")
    indexes = doc.getDocumentIndexes()
    for _ in range(2):  # second pass settles page numbers shifted by the TOC itself
        for i in range(indexes.getCount()):
            indexes.getByIndex(i).update()
        doc.getTextFields().refresh()
    doc.storeToURL(Path(dst).resolve().as_uri(), props(FilterName="writer_pdf_Export"))
    doc.close(True)
    try:
        desktop.terminate()
    except Exception:
        pass  # the bridge drops as LibreOffice exits
finally:
    try:
        office.wait(timeout=30)
    except subprocess.TimeoutExpired:
        office.kill()
"""


def build_pdf(docx: Path, output_dir: Path) -> Path:
    """Export the .docx to PDF through LibreOffice, refreshing the TOC first.

    pandoc emits the table of contents as an unpopulated Word field; a plain
    ``soffice --convert-to pdf`` would leave it empty. Driving LibreOffice over
    UNO lets us update every index (with page numbers) before exporting. A
    throwaway profile keeps the run independent of any open LibreOffice.
    """
    soffice = find_soffice()
    pdf = output_dir / f"{docx.stem}.pdf"
    pdf.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory() as profile:
        result = subprocess.run(
            [
                find_uno_python(soffice),
                "-c",
                _UNO_EXPORT,
                soffice,
                profile,
                f"teachdesk-docs-{os.getpid()}",
                str(docx),
                str(pdf),
            ],
            capture_output=True,
            text=True,
            timeout=300,
        )
    if result.returncode != 0 or not pdf.is_file():
        detail = (result.stderr or result.stdout).strip().splitlines()
        raise BuildError(
            "LibreOffice PDF export failed"
            + (f": {detail[-1]}" if detail else "")
            + " (set UNO_PYTHON to a Python that can `import uno`, or use --no-pdf)"
        )
    return pdf


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0] if __doc__ else None
    )
    parser.add_argument("--no-pdf", action="store_true", help="build the .docx only")
    args = parser.parse_args(argv)

    try:
        BUILD_DIR.mkdir(parents=True, exist_ok=True)
        docx = BUILD_DIR / f"{OUTPUT_STEM}.docx"
        build_docx(assemble_markdown(ordered_sources()), docx)
        print(f"Built {docx.relative_to(ROOT)}")
        if not args.no_pdf:
            pdf = build_pdf(docx, BUILD_DIR)
            print(f"Built {pdf.relative_to(ROOT)}")
    except (BuildError, subprocess.SubprocessError, OSError) as exc:
        print(f"docs build failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
