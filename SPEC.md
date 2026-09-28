# TeachDesk — Project Spec

*Working name. An AI admin assistant for UK secondary school teachers.*

## 1. The problem

Teachers in England work around 50 hours a week, and less than half of that is teaching. The rest goes on admin: parent letters, report comments, adapting resources, emails. The DfE's position is that AI is most useful (and least risky) when it supports teachers rather than pupils, and that AI must never make summative judgements about a pupil's attainment.

TeachDesk takes that admin off the teacher's plate. The teacher asks in plain English, the AI drafts, and the teacher approves. Nothing leaves the system without human approval.

## 2. Who it's for

- **Primary user:** a secondary school classroom teacher
- **Secondary user:** a head of year or admin staff sending letters to parents
- **Demo context:** a fictional school, "Oakfield Academy" (Years 7–11, ~900 pupils)

## 3. Core features (MVP)

### F1 — Parent letters and emails
- Teacher types a request, e.g. *"Letter to Year 9 parents about the science museum trip on Friday 16 October."*
- System retrieves relevant school documents (trips policy, term dates, letter templates, contact details) and drafts the letter.
- Every factual claim (dates, costs, policies) must come from a retrieved document. If a fact is missing, the draft marks it as `[TO CONFIRM: ...]` rather than inventing it.
- Output: letter text + list of sources used.

**Done when:** a teacher can request, edit, approve and export a letter; drafts cite their sources; missing facts are flagged, not made up.

### F2 — Report comments
- Teacher uploads or enters a class list with short notes per pupil (e.g. *"strong effort, essays need structure, 72% in test"*).
- System produces a polished comment per pupil in the school's report style and word limit.
- System **does not** assign or change grades, predict attainment, or add judgements the teacher didn't give.
- Pupil names are replaced with tokens before any model call and restored afterwards (see §6).

**Done when:** a class of 30 produces 30 comments within the word limit, in school style, with no invented judgements and no real names in any outbound prompt.

### F3 — Resource adapter
- Teacher uploads a worksheet (text, .docx or PDF).
- System produces one or more versions: simplified (lower reading age), stretch (harder), EAL-friendly (with key vocabulary glossary).
- Reports the reading age of the original and each version.

**Done when:** each adapted version hits its target reading-age band and keeps the original learning objective.

### F4 — Agent router (ties it together)
- One chat box. The agent decides which feature (F1/F2/F3) the request needs, asks a clarifying question if the request is ambiguous, and refuses out-of-scope or unsafe requests (e.g. "what grade should this pupil get?").

## 4. Architecture

```
Teacher (web UI)
   │
   ▼
FastAPI backend
   ├── Router agent (small, fast model) → picks F1 / F2 / F3 / refuse / clarify
   ├── PII redactor (roster-based name → token, and back)
   ├── Retriever (pgvector over school documents)
   ├── Feature pipelines (drafting model, structured outputs via Pydantic)
   ├── Guardrail checks (no grades, no invented facts, word limits, reading age)
   └── Approval queue (draft → edited → approved → exported)
   │
   ▼
Postgres (documents + embeddings + request logs + approvals)
```

### Model use
- **Router and quick checks:** `claude-haiku-4-5-20251001` (cheap, fast)
- **Drafting:** `claude-sonnet-5-5`
- Model names live in config/env, never hard-coded in logic.

## 5. Tech stack

| Layer | Choice |
|---|---|
| Language | Python 3.12 |
| API | FastAPI + Pydantic v2 |
| LLM | Anthropic Python SDK (Claude API) |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`), runs locally |
| Database | Postgres 16 + pgvector |
| Front end | Jinja2 templates + HTMX (simple, no heavy JS framework) |
| Documents | python-docx, pypdf |
| Readability | textstat |
| Testing | pytest |
| Packaging | Docker + docker compose |
| Infra | Terraform (one small cloud VM or container service) |
| CI | GitHub Actions: lint, tests, evals on every PR |

## 6. Safety and data protection

- **Synthetic data only.** Oakfield Academy, its staff, pupils and documents are all invented. No real school or pupil data, ever.
- **PII redaction.** Pupil names from the class roster are swapped for tokens (`PUPIL_001`) before any model call and swapped back after. A test asserts no roster name appears in any logged outbound prompt.
- **No summative judgements.** The system never assigns grades, levels, predictions or SEN labels. Requests for these are refused with a short explanation.
- **Grounded facts.** Letters only state facts found in retrieved documents; anything else is flagged `[TO CONFIRM]`.
- **Human in the loop.** Every output starts as a draft; only an approved draft can be exported.
- **Audit log.** Every request records: route chosen, documents retrieved, model, tokens, cost, latency, guardrail results, approval status.
- **README includes** a short DPIA-style note explaining how a real school would assess this tool.

## 7. Evaluation

A golden set of 30–50 test requests in `evals/cases.yaml`, run with `make eval`.

| Check | How |
|---|---|
| Correct routing | expected feature vs chosen feature |
| Factual grounding | dates/costs in letter match source docs (exact match) + LLM-as-judge for claims |
| Refusals | grading/prediction requests are refused |
| No PII leak | no roster names in outbound prompts |
| Word limit | report comments within limit |
| Reading age | adapted resources within target band (textstat) |
| Cost & latency | average per request, tracked over time |

Eval results are saved to `evals/results/` and summarised in the README.

## 8. Milestones (~5 weeks)

1. **Week 1 — Foundations + F1:** repo, Docker, Postgres/pgvector, synthetic school documents, ingestion, retrieval, parent letter feature end to end.
2. **Week 2 — F2 + F3:** report comments with PII redaction; resource adapter with reading-age checks.
3. **Week 3 — Agent + guardrails:** router, clarify/refuse behaviour, approval queue, audit log.
4. **Week 4 — Evals + observability:** golden set, eval runner in CI, simple dashboard page for cost/latency/guardrail stats.
5. **Week 5 — Ship:** Terraform deploy, live demo link, README with architecture diagram, 2-minute demo video, LinkedIn write-up.

## 9. Out of scope (for now)

- Real school data or MIS integration (SIMS, Arbor, Bromcom)
- Pupil-facing features
- Marking or grading of pupil work
- Multi-school / multi-tenant accounts
- Mobile app

## 10. Suggested repo layout

```
teachdesk/
├── CLAUDE.md
├── SPEC.md
├── README.md
├── docker-compose.yml
├── Makefile
├── app/
│   ├── main.py
│   ├── config.py
│   ├── agent/          # router
│   ├── features/       # letters.py, reports.py, adapter.py
│   ├── rag/            # ingest.py, retrieve.py
│   ├── safety/         # redact.py, guardrails.py
│   ├── db/             # models, migrations
│   └── web/            # templates, static
├── data/synthetic/     # Oakfield Academy docs + roster
├── evals/              # cases.yaml, runner.py, results/
├── tests/
└── infra/              # terraform
```
