# ADR-0002: uv for Python packaging and environments

- **Status:** Accepted
- **Date:** 2026-09-28
- **Decider:** Project owner

## Context

The project needs reproducible Python environments across developer machines,
Docker images and CI, pinned to Python 3.12 (`SPEC.md` §5). Dependency
resolution must be deterministic, and installs fast enough not to slow CI or
image builds.

## Options considered

1. **uv.** Standards-based (`pyproject.toml`, PEP 735 dependency groups),
   cross-platform lockfile, very fast resolution and installation, and can
   install the required Python version itself.
2. **Poetry.** Mature and widely known, but slower, uses its own lock format,
   and needs extra configuration for lean Docker builds.
3. **pip + pip-tools.** Minimal and universally understood, but environment
   and Python-version management are manual, and there is no single tool for
   the whole workflow.

## Decision

**Option 1 — uv.**

- `pyproject.toml` declares the project (`teachdesk`) and its dependencies.
  Development-only tools go in the `dev` dependency group.
- `uv.lock` is committed and is the single source of resolved versions.
- `.python-version` pins the interpreter to 3.12.
- Commands run through `uv run --locked`, which fails if the lockfile is out of
  date rather than silently re-resolving.

## Consequences

- Contributors need uv installed; everything else, including Python 3.12, can
  be installed through it.
- Docker and CI will install from `uv.lock`, giving identical dependency sets
  everywhere.
- Adding or upgrading a dependency is an explicit change to `pyproject.toml`
  and `uv.lock`, visible in review.
