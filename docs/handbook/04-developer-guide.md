# Developer guide

## Prerequisites

| Tool | Purpose | Required for |
|---|---|---|
| git | Version control | Everything |
| [uv](https://docs.astral.sh/uv/) | Python 3.12, dependencies, running commands (ADR-0002) | Everything |
| GNU Make | Command shortcuts | Everything |
| LibreOffice (with Writer) and its Python UNO bridge | Exporting the handbook to PDF | `make docs` (PDF step only) |
| Docker + docker compose | Running the app and database | Planned (Week 1) |

## First-time setup

```bash
git clone https://github.com/Harsh3720-code/TeachDesk.git
cd TeachDesk
uv sync --locked      # installs Python 3.12 if needed, plus dependencies
```

`uv sync --locked` refuses to run if `uv.lock` is out of date with
`pyproject.toml`, so every machine gets exactly the same dependency versions.

## Commands

| Command | What it does | Status |
|---|---|---|
| `make docs` | Builds this handbook to `docs/build/TeachDesk-Engineering-Handbook.docx` and `.pdf` | **Implemented** |
| `make up` | Starts the app and database with docker compose | Planned |
| `make test` | Runs the pytest suite | Planned |
| `make eval` | Runs the evaluation suite | Planned |
| `make lint` | Runs ruff and mypy | Planned |
| `make ingest` | Loads synthetic school documents into the vector store | Planned |

To build the Word file without LibreOffice:

```bash
uv run --locked python scripts/build_docs.py --no-pdf
```

The PDF step needs two things the uv environment cannot provide, because they
ship with LibreOffice rather than on PyPI:

| Variable | Purpose | Default |
|---|---|---|
| `SOFFICE` | Path to the LibreOffice binary | `soffice` or `libreoffice` on `PATH` |
| `UNO_PYTHON` | A Python interpreter that can `import uno` | LibreOffice's bundled `python` if present, otherwise `/usr/bin/python3` |

On Debian/Ubuntu: `sudo apt install libreoffice-writer python3-uno`. On macOS
and Windows the LibreOffice installer includes both, and the defaults find
them.

## Working on the documentation

### Structure

```text
docs/
├── handbook/        chapters, NN-title.md, built in numeric order
├── adr/             decision records, NNNN-title.md
├── templates/
│   └── reference.docx   Word style template (fonts, colours, A4 layout)
└── build/           generated .docx/.pdf (git-ignored)
```

### Rules

- Update the handbook in the **same pull request** as the change it describes.
- Each chapter starts with exactly one level-1 heading (`# Title`); do not
  number headings by hand, because the build numbers them.
- Each ADR starts with a level-1 heading (`# ADR-NNNN: Title`); the build
  demotes it to sit beneath the *Decision log* chapter.
- Mark behavioural sections with a status label: **Implemented**,
  **In progress** or **Planned** (see *Overview*).
- Diagrams are text (code blocks) or image files under `docs/`.
- Adding a chapter or ADR requires the file name to be approved first
  (ADR-0004).

### Changing the visual style

Open `docs/templates/reference.docx` in Word or LibreOffice, modify the
*styles* (not the text), save, and run `make docs`. Pandoc takes all
formatting from this file's styles.

## Contribution workflow

1. Agree the scope and every new name with the project owner (ADR-0004).
2. Create the approved `feature/<name>` branch from `main`.
3. Implement the change with tests; update the handbook and changelog.
4. Run the local checks (`make docs` now; `make lint` and `make test` once they
   exist).
5. Push and open a pull request into `main`.
