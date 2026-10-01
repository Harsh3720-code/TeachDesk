# Operations

**Status: Planned (Weeks 1, 4 and 5)**, except where a section says otherwise.

## Environments

| Environment | Purpose | How it runs |
|---|---|---|
| Local | Development and testing | docker compose: application + Postgres 16 with pgvector |
| CI | Lint, tests and evals on every pull request | GitHub Actions |
| Demo | Public demonstration | One small cloud VM or container service, provisioned with Terraform |

## Configuration and secrets

- All configuration comes from environment variables with the prefix
  `TEACHDESK_`, read and validated by `Settings` in `app/config.py`
  (**In progress**). The model names are already configured this way; the
  Anthropic API key will be added the same way with the first model call.
- `.env.example` is committed and lists every variable with a safe value. Real
  values go in `.env`, which is git-ignored and never committed. The variables
  are listed in the *Developer guide*.
- The app checks every value when it starts and refuses to start if one is
  invalid.
- In CI and the demo environment, secrets come from the platform's secret
  store (GitHub Actions secrets; the cloud provider's secret manager).

## Continuous integration

**Status: In progress.** The workflow `.github/workflows/ci.yml` (workflow
`ci`, job `lint-and-test`) runs on every pull request into `main` and every
push to `main`, on `ubuntu-24.04`:

| Step | Command | Status |
|---|---|---|
| Install dependencies | `uv sync --locked`: fails if `uv.lock` is out of date; uv installs Python 3.12 from `.python-version` | **In progress** |
| Lint and type checks | `make lint` (ruff check, ruff format check, mypy --strict) | **In progress** |
| Unit tests | `make test` (pytest) | **In progress** |
| Handbook build | `scripts/build_docs.py --no-pdf`: Word only, because the runner has no LibreOffice | **In progress** |
| Integration tests against a real Postgres + pgvector | — | Planned (with the data layer) |
| Evaluation suite | — | Planned (Week 4) |

CI calls the same `make` targets developers run locally, so the two cannot
drift apart. Other properties:

- The job has read-only access to the repository (`permissions: contents:
  read`) and a 10-minute timeout.
- A new push to a pull request cancels that pull request's previous run. Runs
  on `main` are never cancelled, so every commit on `main` gets a result.
- Actions are referenced by version tag. Pinning them to commit SHAs is an open
  question (*Decision log*).
- Until the job is a required status check in GitHub's branch protection for
  `main`, it reports results but does not block a merge.

## Runbook

To be written alongside deployment in Week 5: start/stop, rotating the API key,
restoring the database, reading the audit log and responding to a guardrail
failure.
