# ADR-0004: Git workflow and naming governance

- **Status:** Accepted
- **Date:** 2026-09-28
- **Decider:** Project owner

## Context

The repository is `Harsh3720-code/TeachDesk` on GitHub. Work proceeds in small,
reviewable steps (`CLAUDE.md`, *How to work*). The project owner requires full
control over naming across the entire project, not only in git.

## Options considered

1. **A default branch plus one short-lived branch and pull request per step**,
   with CI as the merge gate once it exists. Clean history; each step
   reviewable on its own.
2. **A single long-running branch**, merged when convenient. Simpler, but
   large unreviewable merges and little history to show.

## Decision

**Option 1**, with the following rules.

### Branches

- The default branch is **`main`**. It was created with a root commit
  containing only `.gitignore`, so secrets and build output are excluded from
  the first commit onwards.
- Every other branch follows **`feature/<name>`**. The `<name>` is chosen by
  the project owner for each branch.
- Each step is one branch and one pull request into `main`.

### Naming governance

Every name introduced anywhere in the project — branches, files and folders,
Python modules, database tables and columns, API routes, Docker services,
environment variables, cloud and Terraform resources — follows the same
process:

1. **Ask:** the name is proposed together with its purpose.
2. **Tell:** the project owner approves it or supplies a different name.
3. **Implement:** only approved names are used.

No name is introduced on the assumption that it will be approved.

## Consequences

- Every step begins with a list of proposed names for approval, which adds a
  short review round but gives the owner full ownership of the project's
  vocabulary.
- Pull requests are small and each maps to one handbook changelog entry.
- History on `main` is a readable sequence of completed steps.
