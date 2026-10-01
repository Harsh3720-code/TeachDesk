# Developer guide

## Prerequisites

| Tool | Purpose | Required for |
|---|---|---|
| git | Version control | Everything |
| [uv](https://docs.astral.sh/uv/) | Python 3.12, dependencies, running commands (ADR-0002) | Everything |
| GNU Make | Command shortcuts | Everything (on Windows, see *Windows setup*) |
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

### Configuration

All settings are environment variables with the prefix `TEACHDESK_`, read by
`Settings` in `app/config.py`. `.env.example` lists every variable with its
default and a comment. To change a value locally, copy it to `.env` (which
is git-ignored) and edit it:

```bash
cp .env.example .env
```

| Variable | Values | Default |
|---|---|---|
| `TEACHDESK_ENV` | `local`, `test`, `production` | `local` |
| `TEACHDESK_LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` | `INFO` |
| `TEACHDESK_ROUTER_MODEL` | Claude model id for routing and quick checks | `claude-haiku-4-5-20251001` |
| `TEACHDESK_DRAFTING_MODEL` | Claude model id for drafting | `claude-sonnet-5-5` |

An invalid value (e.g. `TEACHDESK_ENV=staging`) stops the app at startup with
a validation error rather than running with a bad setting. Tests ignore
`.env`, so local settings never change test results.

## Commands

| Command | What it does | Status |
|---|---|---|
| `make docs` | Builds this handbook to `docs/build/TeachDesk-Engineering-Handbook.docx` and `.pdf` | **Implemented** |
| `make lint` | `ruff check`, `ruff format --check` and `mypy --strict` over `app/`, `tests/` and `scripts/` | **In progress** |
| `make test` | Runs the pytest suite | **In progress** |
| `make format` | Reformats the code with `ruff format` | **In progress** |
| `make run` | Starts the development server with auto-reload at `http://127.0.0.1:8000` (try `/health`) | **In progress** |
| `make up` | Starts the app and database with docker compose | Planned |
| `make eval` | Runs the evaluation suite | Planned |
| `make ingest` | Loads synthetic school documents into the vector store | Planned |

Tool settings (ruff, mypy, pytest) live in `pyproject.toml`. Every command
runs through `uv run --locked`, so it uses exactly the versions in `uv.lock`.

**Known warning.** `make test` currently prints a
`StarletteDeprecationWarning` recommending `httpx2` over `httpx` for the test
client. It does not affect results; replacing the dependency is an open item.

To build the Word file without LibreOffice:

```bash
uv run --locked python scripts/build_docs.py --no-pdf
```

The PDF step needs two things the uv environment cannot provide, because they
ship with LibreOffice rather than on PyPI:

| Variable | Purpose | Default |
|---|---|---|
| `SOFFICE` | Path to the LibreOffice binary | `soffice` or `libreoffice` on `PATH`, then `C:\Program Files\LibreOffice\program\soffice.exe` |
| `UNO_PYTHON` | A Python interpreter that can `import uno` | LibreOffice's bundled `python` if present, otherwise `/usr/bin/python3` |

On Debian/Ubuntu: `sudo apt install libreoffice-writer python3-uno`. On macOS
and Windows the LibreOffice installer includes both, and the defaults find
them.

## Windows setup

The project is developed on Windows 11 with Git Bash as the shell. These
steps cover what differs from Linux and macOS.

1. **GNU Make.** Windows has no `make`. Install it with:

   ```bash
   winget install ezwinports.make
   ```

   Open a new terminal afterwards so `make` is on `PATH`.

2. **uv cache on the project drive.** If the repository is not on `C:`, set
   the user environment variable `UV_CACHE_DIR` to a folder on the same drive
   (for example `D:\uv-cache`). uv installs packages by linking them from its
   cache, which only works within one drive; across drives it falls back to
   slower copying.

3. **Python is managed by uv.** No separate Python install is needed:
   `uv sync --locked` downloads the interpreter pinned in `.python-version`
   (3.12). uv prefers its own managed interpreter over any system Python on
   `PATH`; `uv python list` shows which one is in use.

4. **LibreOffice for the PDF handbook.** Install it with:

   ```bash
   winget install TheDocumentFoundation.LibreOffice
   ```

   The installer does not add LibreOffice to `PATH`. `make docs` finds it at
   the default location (`C:\Program Files\LibreOffice\program\`) and uses
   the `python.exe` bundled beside `soffice.exe` for the UNO bridge. For a
   non-default location, set `SOFFICE` (see above). A PDF viewer that has the
   previous handbook open locks the file, so close it before rebuilding.

5. **Line endings.** `.gitattributes` (`* text=auto eol=lf`) makes git store
   and check out text files with LF endings, whatever `core.autocrlf` is set
   to. Git may print "CRLF will be replaced by LF" warnings; they are
   harmless.

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
4. Run the local checks: `make lint`, `make test` and `make docs`.
5. Commit using the Conventional Commits format (ADR-0005), e.g.
   `feat: add health endpoint`.
6. Push and open a pull request into `main`.
