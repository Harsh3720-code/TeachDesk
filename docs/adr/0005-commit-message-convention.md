# ADR-0005: Commit message convention

- **Status:** Accepted
- **Date:** 2026-10-01
- **Decider:** Project owner

## Context

Each step lands as a small branch and pull request (ADR-0004), so the history
on `main` is the project's narrative. Commit messages so far have no fixed
format. A consistent format makes the history easy to scan, shows at a glance
what kind of change each commit is, and allows a changelog or release notes to
be generated automatically later.

## Options considered

1. **Free-form messages.** No rules to learn, but the history is inconsistent
   and cannot be processed by tools.
2. **Conventional Commits.** A widely used specification
   (<https://www.conventionalcommits.org/>): a typed prefix, an optional
   scope, and a short subject. Readable by people and by changelog tools.
3. **Gitmoji.** An emoji prefix per change type. Compact, but less readable in
   plain-text tools and less common in professional codebases.

## Decision

**Option 2 — Conventional Commits.**

Format:

```text
<type>[!]: <subject>

[body: what changed and why]

[footer, e.g. BREAKING CHANGE: ...]
```

The type is chosen per change from this set:

| Type | Use for |
|---|---|
| `feat` | New behaviour visible to users or callers |
| `fix` | Correcting a defect |
| `docs` | Documentation only (handbook, ADRs, README) |
| `test` | Adding or changing tests only |
| `refactor` | Restructuring code without changing behaviour |
| `build` | Dependencies, packaging, Makefile, tool configuration |
| `ci` | Continuous-integration workflows |
| `chore` | Maintenance that fits none of the above |

Rules:

- The subject is imperative and lower-case, has no full stop, and is at most
  72 characters (e.g. `feat: add health endpoint`).
- A scope (`feat(config): ...`) is permitted by the specification but is not
  used for now; it can be introduced by a later ADR.
- The body, when present, explains *why* the change was made.
- A breaking change is marked with `!` after the type and a
  `BREAKING CHANGE:` footer.
- A commit that mixes types is split where practical. Otherwise it takes the
  type of its most significant change.

## Consequences

- Every commit message must follow the format. A commit-message linter can
  enforce this in CI later.
- The handbook changelog can, in future, be drafted from the commit history.
- Choosing a type forces each commit to have a single, clear purpose, which
  supports the small-steps rule in `CLAUDE.md`.
