# CLAUDE.md — TeachDesk

TeachDesk is an AI admin assistant for UK secondary school teachers: parent letters, report comments and resource adaptation. It is a portfolio project. Full requirements are in `SPEC.md` — read it before starting any feature.

## Stack
- Python 3.12, FastAPI, Pydantic v2
- Anthropic Python SDK (Claude API). Model names come from `app/config.py` / env vars, never hard-coded.
- Postgres 16 + pgvector; sentence-transformers for embeddings
- Jinja2 + HTMX front end
- pytest; Docker + docker compose; Terraform in `infra/`

## Commands
- `make up` — start app + database with docker compose
- `make test` — run pytest
- `make eval` — run the eval suite in `evals/`
- `make lint` — ruff + mypy
- `make ingest` — load synthetic school documents into the vector store

(Create these Makefile targets if they don't exist yet.)

## Hard rules (never break these)
1. **Synthetic data only.** Never add real names, schools or pupil data. All data lives in `data/synthetic/`.
2. **Redact before every model call.** Any text containing pupil information goes through `app/safety/redact.py` first. No roster name may appear in an outbound prompt.
3. **No summative judgements.** The system never generates grades, levels, predictions or SEN labels. Refuse these requests.
4. **Grounded facts only.** Letters state only facts from retrieved documents. Missing facts become `[TO CONFIRM: ...]`.
5. **Drafts need approval.** Nothing is exported unless its status is `approved`.
6. **Log every model call** (route, model, tokens, cost, latency, guardrail results) to the audit log.
7. **Secrets** come from environment variables only. Never commit `.env` or API keys.

## How to work
- Use plan mode for any new feature: propose the approach and files to touch, then wait for approval.
- Work in small steps. One feature or fix per change.
- Write or update tests with every change. A feature isn't done until `make test` passes.
- Use Pydantic models for all LLM structured outputs; validate, don't trust raw text.
- Keep functions small and typed. Prefer clear code over clever code.
- After finishing a step, summarise what changed and why in plain English, so I can explain it in interviews.
- If a requirement in SPEC.md is unclear or seems wrong, ask rather than guess.

## Current milestone
Week 1 — Foundations + F1 (parent letters). See SPEC.md §8.
