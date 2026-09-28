# Architecture

**Status: Planned.** This chapter describes the target architecture from
`SPEC.md` §4. Component, module and table names are provisional until approved
(ADR-0004); each will be fixed as the milestone that builds it lands.

## System context

TeachDesk is a single web application used by school staff through a browser.
It depends on two external services: the Claude API for language-model calls
and a Postgres database for documents, embeddings, drafts and audit records.
Embeddings are computed locally, so school documents are never sent to a
third party for embedding.

```text
 ┌──────────────────┐        HTTPS         ┌───────────────────────────┐
 │ Teacher / admin  │ ───────────────────▶ │  TeachDesk web application │
 │   (browser)      │ ◀─────────────────── │  (FastAPI + Jinja2/HTMX)   │
 └──────────────────┘                      └─────┬───────────────┬─────┘
                                                 │               │
                              redacted prompts   │               │  SQL
                                                 ▼               ▼
                                   ┌───────────────────┐  ┌──────────────────┐
                                   │    Claude API     │  │ Postgres 16 +    │
                                   │ (Anthropic, SaaS) │  │ pgvector         │
                                   └───────────────────┘  └──────────────────┘
```

## Components

```text
FastAPI backend
 ├── Router agent ........ picks F1 / F2 / F3 / clarify / refuse (small, fast model)
 ├── PII redactor ........ roster name → token before a model call, token → name after
 ├── Retriever ........... pgvector similarity search over school documents
 ├── Feature pipelines ... letters (F1), reports (F2), adapter (F3); drafting model,
 │                         structured outputs validated by Pydantic
 ├── Guardrails .......... no grades, no invented facts, word limits, reading age
 ├── Approval queue ...... draft → edited → approved → exported
 └── Audit log ........... one record per model call and per request
```

| Component | Responsibility | Key constraint |
|---|---|---|
| Router agent | Classify the request, ask for clarification, or refuse. | Refusal of summative judgements is mandatory (hard rule 3). |
| PII redactor | Replace roster names with stable tokens (`PUPIL_001`) and restore them afterwards. | Runs before **every** outbound model call (hard rule 2). |
| Retriever | Return the most relevant chunks of synthetic school documents, with source references. | Retrieved chunks are the only permitted source of facts in letters (hard rule 4). |
| Feature pipelines | Build prompts, call the drafting model, validate the structured output. | Model names come from configuration, never code. Raw model text is never trusted. |
| Guardrails | Deterministic and model-assisted checks on every draft. | Failures are recorded in the audit log and shown to the teacher. |
| Approval queue | Hold every output as a draft until a teacher approves it. | Export requires status `approved` (hard rule 5). |
| Audit log | Record route, documents retrieved, model, tokens, cost, latency, guardrail results and approval status. | Every model call is logged (hard rule 6). |

## Request lifecycle (F1: parent letter)

1. The teacher submits a request, e.g. *"Letter to Year 9 parents about the
   science museum trip on Friday 16 October."*
2. The router classifies it as F1. If it is ambiguous, the teacher is asked a
   clarifying question instead.
3. The retriever finds relevant documents: trips policy, term dates, letter
   templates, contact details.
4. The drafting model receives the request and the retrieved chunks, and
   returns a structured draft: letter body, list of sources, and list of facts
   it could not ground.
5. The output is validated against its Pydantic schema. Guardrails check that
   every date and cost in the letter appears in a cited source; any that do
   not are converted to `[TO CONFIRM: ...]`.
6. The draft is stored with status `draft` and shown to the teacher with its
   sources.
7. The teacher edits (status `edited`) and approves (status `approved`).
8. Only then can the letter be exported. Every step writes to the audit log.

## Model usage

| Purpose | Model (default) | Rationale |
|---|---|---|
| Routing and quick checks | `claude-haiku-4-5-20251001` | Low latency and cost for classification. |
| Drafting | `claude-sonnet-5-5` | Higher quality for teacher-facing prose. |

Model identifiers are read from configuration and environment variables; no
model name is hard-coded in application logic, so models can be changed
without a code change.

## Technology stack

| Layer | Choice | Decision |
|---|---|---|
| Language | Python 3.12 | `SPEC.md` §5 |
| Dependency management | uv | ADR-0002 |
| API | FastAPI + Pydantic v2 | `SPEC.md` §5 |
| LLM | Anthropic Python SDK (Claude API) | `SPEC.md` §5 |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2`, run locally | `SPEC.md` §5 |
| Database | Postgres 16 + pgvector | `SPEC.md` §5 |
| Data access | SQLAlchemy 2.0 (async) + Alembic | ADR-0003 |
| Front end | Jinja2 templates + HTMX | `SPEC.md` §5 |
| Documents | python-docx, pypdf | `SPEC.md` §5 |
| Readability | textstat | `SPEC.md` §5 |
| Testing | pytest | `SPEC.md` §5 |
| Packaging | Docker + docker compose | `SPEC.md` §5 |
| Infrastructure | Terraform | `SPEC.md` §5 |
| CI | GitHub Actions: lint, tests, evals on every PR | `SPEC.md` §5 |
| Documentation | Markdown → pandoc → .docx → LibreOffice → .pdf | ADR-0001 |
