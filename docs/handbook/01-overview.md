# Overview

## About this handbook

This handbook is the single engineering record for TeachDesk. It explains what
the system does, how it is built, why each significant decision was made, and
how to run, test and operate it. It is written for three readers:

- **The project owner**, who takes every product and technical decision and
  needs a precise record of what was decided and why.
- **Engineers and reviewers** joining or assessing the project.
- **A school's data-protection or IT lead** evaluating whether the tool could
  be used safely (see *Safety and data protection*).

The handbook is maintained as Markdown in the repository (`docs/`) and built
into Word and PDF with `make docs` (see ADR-0001). It is updated in the same
pull request as the change it describes, so the document never drifts from
the code.

### Status labels

Every section that describes behaviour carries one of these labels:

| Label | Meaning |
|---|---|
| **Implemented** | Exists on `main`, covered by tests. |
| **In progress** | Being built on an open `feature/<name>` branch. |
| **Planned** | Designed from `SPEC.md`; not yet built. Details may change and will be recorded as ADRs. |

### Source documents

| Document | Role |
|---|---|
| `SPEC.md` | Product requirements: problem, features, architecture, milestones. |
| `CLAUDE.md` | Engineering rules and hard constraints for everyone (human or AI) working on the code. |
| `docs/adr/` | Architecture Decision Records: one file per decision. |
| This handbook | The assembled, readable view of all of the above plus design detail. |

Where this handbook and `SPEC.md` disagree, `SPEC.md` wins until an ADR
records the change.

## The problem

Teachers in England work around 50 hours a week, and less than half of that is
teaching. The remainder is administration: parent letters, report comments,
adapting resources and email. The Department for Education's position is that
generative AI is most useful, and least risky, when it supports teachers rather
than pupils, and that AI must never make summative judgements about a pupil's
attainment.

TeachDesk removes that administrative load. The teacher asks in plain English,
the system drafts, and the teacher reviews and approves. Nothing leaves the
system without explicit human approval.

## Users

| User | Needs |
|---|---|
| Secondary classroom teacher (primary) | Fast, accurate drafts of letters, report comments and adapted resources that need light editing only. |
| Head of year / admin staff (secondary) | Parent communications that are factually correct and consistent with school policy. |

**Demo context:** a fictional school, *Oakfield Academy* (Years 7–11, around
900 pupils). Every person, document and record in the project is synthetic.

## Scope

### In scope (MVP)

| ID | Feature | Outcome |
|---|---|---|
| F1 | Parent letters and emails | Grounded letter drafts that cite their sources and flag missing facts as `[TO CONFIRM: ...]`. |
| F2 | Report comments | One polished comment per pupil, in school style and within the word limit, from the teacher's own notes, with pupil names never sent to the model. |
| F3 | Resource adapter | Simplified, stretch and EAL-friendly versions of a worksheet, each within a target reading-age band. |
| F4 | Agent router | One chat box that routes to F1–F3, asks clarifying questions, and refuses unsafe or out-of-scope requests. |

### Out of scope

- Real school data or MIS integration (SIMS, Arbor, Bromcom)
- Pupil-facing features
- Marking or grading of pupil work
- Multi-school / multi-tenant accounts
- Mobile app

## Non-negotiable principles

These come from `CLAUDE.md` and apply to every change. A pull request that
breaks any of them is rejected regardless of other merits.

1. **Synthetic data only.** No real names, schools or pupil data, ever.
2. **Redact before every model call.** Pupil names are tokenised before any
   text leaves the system; no roster name may appear in an outbound prompt.
3. **No summative judgements.** No grades, levels, predictions or SEN labels.
   Such requests are refused.
4. **Grounded facts only.** Letters state only facts from retrieved documents;
   anything missing becomes `[TO CONFIRM: ...]`.
5. **Drafts need approval.** Nothing is exported unless its status is
   `approved`.
6. **Every model call is audited:** route, model, tokens, cost, latency and
   guardrail results.
7. **Secrets come from environment variables only.** `.env` files and keys are
   never committed.

## Delivery plan

| Week | Milestone | Status |
|---|---|---|
| 1 | Foundations + F1: repository, Docker, Postgres/pgvector, synthetic documents, ingestion, retrieval, parent letters end to end | **In progress:** project information and documentation pipeline |
| 2 | F2 + F3: report comments with PII redaction; resource adapter with reading-age checks | Planned |
| 3 | Agent + guardrails: router, clarify/refuse, approval queue, audit log | Planned |
| 4 | Evals + observability: golden set, eval runner in CI, cost/latency/guardrail dashboard | Planned |
| 5 | Ship: Terraform deploy, live demo, README with architecture diagram, demo video, write-up | Planned |

## Ways of working

- **Decision ownership.** The project owner takes every decision. Options,
  trade-offs and a recommendation are presented; nothing is implemented until
  the owner approves it. Each decision is recorded as an ADR.
- **Naming.** Every name in the project — branches, files, modules, tables,
  routes, services, environment variables, cloud resources — is proposed,
  approved by the owner, and only then implemented (ADR-0004).
- **Small steps.** One feature or fix per branch and pull request. A step is
  done only when its tests pass and this handbook is updated.
