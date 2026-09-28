# Decision log

## How decisions are recorded

Every significant technical or process decision is captured as an
**Architecture Decision Record (ADR)**: a short, immutable document stating the
context, the options considered, the decision taken and its consequences. ADRs
make the reasoning behind the system auditable and prevent settled questions
from being re-opened without new information.

- **Location:** `docs/adr/NNNN-short-title.md`, numbered sequentially.
- **Decider:** the project owner. Options and a recommendation are prepared in
  advance; the owner chooses.
- **Immutability:** an accepted ADR is not edited in substance. A changed
  decision gets a new ADR that *supersedes* the old one, and the old one's
  status is updated to point to it.
- **Statuses:** `Proposed` → `Accepted` → (`Superseded by ADR-NNNN` |
  `Deprecated`).

Each ADR follows the same structure: *Status, Date, Decider, Context, Options
considered, Decision, Consequences.*

## Index

| ADR | Title | Status | Date |
|---|---|---|---|
| 0001 | Documentation as Markdown, built to Word and PDF | Accepted | 2026-09-28 |
| 0002 | uv for Python packaging and environments | Accepted | 2026-09-28 |
| 0003 | SQLAlchemy 2.0 (async) and Alembic for data access | Accepted | 2026-09-28 |
| 0004 | Git workflow and naming governance | Accepted | 2026-09-28 |

## Open questions

Decisions identified but not yet taken. Each will become an ADR once decided.

| Topic | Why it matters | Needed by |
|---|---|---|
| Authentication and rate limiting for the live demo | `SPEC.md` has no login; a public link without limits exposes the API budget to abuse. | Week 5 (design earlier) |
| Model price table for cost logging | Hard rule 6 requires cost per call; prices must live in configuration and be kept current. | Week 1 (F1 audit logging) |
| Commit message convention | Consistent history and possible changelog automation. | Before the next branch |
| Publishing built documents from CI | Whether CI attaches the built handbook to each run. | When CI is introduced |
