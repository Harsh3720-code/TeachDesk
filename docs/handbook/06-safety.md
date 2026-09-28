# Safety and data protection

**Status: Planned.** Controls below are specified from `SPEC.md` §6 and
`CLAUDE.md`. Each will be marked **Implemented** with a reference to its
automated test when built.

## Control matrix

| Hard rule | Control | Verification |
|---|---|---|
| 1. Synthetic data only | All data lives in a single synthetic-data directory; Oakfield Academy and its people are invented. | Code review; no data import paths from external systems. |
| 2. Redact before every model call | Roster-based redactor replaces pupil names with tokens (`PUPIL_001`) before any outbound call and restores them after. | Automated test asserting no roster name appears in any logged outbound prompt. |
| 3. No summative judgements | Router refuses grade, level, prediction and SEN-label requests; output guardrails reject such content. | Refusal cases in the golden evaluation set. |
| 4. Grounded facts only | Letters may state only facts found in retrieved documents; anything else becomes `[TO CONFIRM: ...]`. | Exact-match checks on dates and costs plus LLM-as-judge on claims. |
| 5. Drafts need approval | Status workflow: draft → edited → approved → exported. Export rejects anything not `approved`. | Tests on the export path. |
| 6. Log every model call | Audit record: route, documents retrieved, model, tokens, cost, latency, guardrail results, approval status. | Tests assert one audit record per model call. |
| 7. Secrets from environment only | Configuration reads secrets from environment variables; `.env` and key files are git-ignored. | `.gitignore` (in place since the first commit); secret scanning in CI (planned). |

## Personal data flow

The only personal data the system handles is (synthetic) pupil names and
teacher-written notes about pupils. The design ensures:

- **Names never leave the system.** Redaction happens before every model call.
- **Embeddings are local.** School documents are embedded on the application
  host; no document text is sent to a third-party embedding service.
- **Minimum content to the model.** Only the redacted request and the
  retrieved chunks needed for the task are sent.

## DPIA-style assessment (outline)

A school considering a tool like TeachDesk would complete a Data Protection
Impact Assessment under UK GDPR before use. This outline records how the design
answers the questions such an assessment asks; it will be expanded for the
README in Week 5.

| Question | Position |
|---|---|
| What personal data is processed? | Pupil names and teacher notes (in this project, synthetic only). |
| Is it necessary and minimised? | Names are tokenised before model calls; only task-relevant text is sent. |
| Who are the processors? | The LLM provider (Anthropic) receives redacted prompts only. A real deployment would require a data processing agreement and a review of the provider's retention terms. |
| Are there automated decisions about individuals? | No. The system never makes summative judgements, and every output requires teacher approval. |
| How is accountability maintained? | Full audit log of requests, model calls, guardrail results and approvals. |
| What are the residual risks? | Unredacted identifiers in free-text notes (e.g. nicknames); model errors surviving teacher review. Mitigations will be recorded as they are designed. |
