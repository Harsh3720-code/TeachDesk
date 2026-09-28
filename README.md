# TeachDesk

An AI admin assistant for UK secondary school teachers. Teachers ask in plain
English, TeachDesk drafts, and the teacher approves; nothing leaves the system
without human approval.

| Feature | What it does |
|---|---|
| **F1** Parent letters | Grounded letter drafts that cite school documents and flag missing facts as `[TO CONFIRM: ...]` |
| **F2** Report comments | Per-pupil comments in school style and word limit; pupil names never sent to the model |
| **F3** Resource adapter | Simplified, stretch and EAL-friendly worksheet versions with reading-age checks |
| **F4** Agent router | One chat box that routes, clarifies, and refuses unsafe requests (e.g. grading) |

> **Synthetic data only.** Oakfield Academy, its staff, pupils and documents
> are fictional. The project never uses real school or pupil data.

## Status

Portfolio project in active development. Current milestone: **Week 1 —
Foundations + F1**. See the changelog in the handbook for progress.

## Documentation

| Document | Contents |
|---|---|
| [`SPEC.md`](SPEC.md) | Product requirements |
| [`CLAUDE.md`](CLAUDE.md) | Engineering rules and hard constraints |
| [`docs/handbook/`](docs/handbook/) | Engineering Handbook (Markdown source) |
| [`docs/adr/`](docs/adr/) | Architecture Decision Records |

Build the handbook as Word and PDF:

```bash
uv sync --locked
make docs        # → docs/build/TeachDesk-Engineering-Handbook.{docx,pdf}
```

PDF output requires LibreOffice. See the *Developer guide* chapter for details.
