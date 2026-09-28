# ADR-0001: Documentation as Markdown, built to Word and PDF

- **Status:** Accepted
- **Date:** 2026-09-28
- **Decider:** Project owner

## Context

The project owner requires all project documentation in a Word document or
PDF. The documentation must stay accurate as the code evolves, be reviewable
alongside code changes, and be professional in presentation.

Word files are binary: git cannot show what changed between versions,
concurrent edits cannot be merged, and reviewers cannot comment on a line in a
pull request. Documentation kept separately from the code tends to drift.

## Options considered

1. **Markdown source in the repository, built to .docx and .pdf.** Text-based,
   diffable and reviewable; outputs are generated and consistently styled.
2. **A Python script that generates the .docx directly** (python-docx). Full
   programmatic control of layout, but prose lives inside code and is awkward
   to edit and review.
3. **A hand-maintained .docx.** Simplest to start, but not diffable, prone to
   drift and merge conflicts, and styling degrades over time.

## Decision

**Option 1.** Documentation is written in GitHub-flavoured Markdown under
`docs/` and built with `make docs`:

- `docs/handbook/NN-*.md` — handbook chapters, ordered by number.
- `docs/adr/NNNN-*.md` — decision records, inserted after the decision-log
  chapter with their headings demoted one level.
- `docs/templates/reference.docx` — the Word style template (fonts, colours,
  heading styles, A4 page setup).
- `scripts/build_docs.py` — assembles the sources, renders `.docx` with pandoc
  (with an embedded Lua filter that sizes table columns to their content), and
  exports `.pdf` by driving headless LibreOffice over its UNO scripting bridge.
  UNO is used rather than a plain `soffice --convert-to pdf` because pandoc
  writes the table of contents as an unpopulated Word field; LibreOffice must
  refresh it before export for the PDF to have a contents page with page
  numbers.

Pandoc is supplied by the `pypandoc-binary` development dependency, so its
version is pinned in `uv.lock` rather than depending on the host. The PDF is
produced from the `.docx`, so both formats share one style definition.

Built files go to `docs/build/`, which is git-ignored. They are rebuilt on
demand with `make docs` and never committed. The title page carries the build
date and git revision so any copy can be traced to a commit.

## Consequences

- Documentation changes are reviewed in the same pull request as the code they
  describe.
- Anyone who wants the Word or PDF version must run `make docs` (or, later,
  download it from CI; see *Open questions*).
- PDF generation requires LibreOffice (including Writer) and a Python that
  can `import uno` on the build machine; `--no-pdf` builds the `.docx` alone.
- The `.docx` contains a table-of-contents field that Word fills in when the
  file is opened (Word may ask to update fields); the PDF is already complete.
- Diagrams must be text-based (code blocks) or images under `docs/`; Mermaid
  is not rendered by pandoc without an additional filter.
