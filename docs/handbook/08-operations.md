# Operations

**Status: Planned (Weeks 1, 4 and 5).**

## Environments

| Environment | Purpose | How it runs |
|---|---|---|
| Local | Development and testing | docker compose: application + Postgres 16 with pgvector |
| CI | Lint, tests and evals on every pull request | GitHub Actions |
| Demo | Public demonstration | One small cloud VM or container service, provisioned with Terraform |

## Configuration and secrets

- All configuration comes from environment variables, including model names
  and the Anthropic API key.
- A committed example file will list every variable with a safe placeholder;
  real values are never committed.
- In CI and the demo environment, secrets come from the platform's secret
  store (GitHub Actions secrets; the cloud provider's secret manager).

## Continuous integration (planned)

Every pull request into `main` will run:

1. Lint and type checks (ruff, mypy)
2. Unit and integration tests (pytest, against a real Postgres + pgvector)
3. The evaluation suite
4. Documentation build

## Runbook

To be written alongside deployment in Week 5: start/stop, rotating the API key,
restoring the database, reading the audit log and responding to a guardrail
failure.
