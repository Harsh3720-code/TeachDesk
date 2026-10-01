# Changelog

One entry per completed step, newest first. Each entry records what changed,
why, and the key point worth being able to explain.

## 2026-10-01 — `feature/app-skeleton`: application skeleton and tooling

**What changed**

- Added ADR-0005: commit messages follow Conventional Commits, with the type
  (`feat`, `fix`, `docs`, `test`, `refactor`, `build`, `ci`, `chore`) chosen
  per change.
- Added `.gitattributes` so text files always use LF line endings, whatever
  each machine's git settings are.
- Added the first application code: `create_app()` (an application factory)
  in `app/main.py`, `Settings` in `app/config.py`, and `GET /health`.
- Configuration comes from four `TEACHDESK_*` environment variables, listed
  with defaults in `.env.example`. The two model names default to the values
  in `SPEC.md` §4 and appear nowhere else in the code.
- Added FastAPI, uvicorn and pydantic-settings, and the dev tools pytest,
  httpx, ruff and mypy. Their settings live in `pyproject.toml`.
- New make targets: `lint` (ruff + `mypy --strict`), `test`, `format`, `run`.
- Seven tests: the health endpoint, settings defaults, overrides and
  validation, and LibreOffice discovery.
- `make docs` now finds LibreOffice in its default Windows location, since
  the Windows installer does not add it to `PATH`.
- Developer guide: configuration table, new commands, and a *Windows setup*
  section.
- Added continuous integration (`.github/workflows/ci.yml`). Every pull request
  into `main`, and every push to `main`, runs `uv sync --locked`, `make lint`,
  `make test` and a Word-only handbook build on Ubuntu. Superseded pull-request
  runs are cancelled; runs on `main` are not.
- Added "Pin GitHub Actions to commit SHAs (with Dependabot)" to the open
  questions.

**Why**

Every later feature needs somewhere to live and a way to be checked. Getting
the app factory, typed configuration and quality gates in place first means
each feature from here on is a small, tested change on a known-good base.

**Key point**

"The app is built by a factory, not a global, so tests can build it with their
own settings and never pick up a developer's `.env`. Configuration is typed and
validated at startup, so a typo in an environment variable fails loudly instead
of silently running with a bad value."

## 2026-09-28 — `feature/project-info`: project information and documentation pipeline

**What changed**

- Added `SPEC.md` (product requirements) and `CLAUDE.md` (engineering rules)
  to the repository.
- Added a `README.md` front page.
- Created this Engineering Handbook as Markdown chapters in `docs/handbook/`,
  and the first four Architecture Decision Records in `docs/adr/`.
- Added `scripts/build_docs.py` and `make docs`, which build the handbook into
  a styled Word document and a PDF in `docs/build/`. The PDF step drives
  LibreOffice through its scripting bridge so the contents page is filled in
  with page numbers before export.
- Set up the Python project with uv: `pyproject.toml`, `uv.lock` and
  `.python-version` (3.12). The only dependency so far is `pypandoc-binary`
  (development), which bundles a pinned pandoc.
- Added `docs/templates/reference.docx`, the Word style template (A4, house
  fonts and colours).

**Why**

Documentation had to exist in Word/PDF form, but binary files cannot be
reviewed or diffed. Keeping Markdown as the source and generating Word/PDF gives
both: reviewable text in pull requests and professional documents on demand.
Recording decisions as ADRs from day one means every "why did you choose X?"
has a written, dated answer.

**Key point**

"Documentation is treated like code: it lives next to the code, is reviewed in
the same pull request, and is built reproducibly — the pandoc version is pinned
in the lockfile, and every built copy is stamped with the git commit it came
from."

## 2026-09-28 — `main`: repository initialised

**What changed**

- Created the default branch `main` with a root commit containing only
  `.gitignore`.

**Why**

A pull request needs a base branch. Committing `.gitignore` first means
secrets (`.env`, key files), virtual environments, caches and generated
documents are excluded before any other file is added.
