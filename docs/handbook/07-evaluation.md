# Evaluation

**Status: Planned (Week 4).**

## Approach

Quality is measured, not asserted. A golden set of 30–50 representative
teacher requests, each with its expected behaviour, is run against the system
with `make eval`. Results are saved with every run so quality, cost and latency
can be tracked over time, and the suite runs in CI on every pull request.

## Metrics

| Check | Method | Target |
|---|---|---|
| Correct routing | Expected feature vs chosen feature | To be set when the baseline is measured |
| Factual grounding | Dates and costs in letters match source documents exactly; LLM-as-judge for other claims | No ungrounded date or cost |
| Refusals | Grading and prediction requests are refused | 100% |
| No PII leak | No roster names in outbound prompts | 100% |
| Word limit | Report comments within the limit | 100% |
| Reading age | Adapted resources within the target band (textstat) | To be set per band |
| Cost and latency | Average per request, tracked across runs | Tracked; budgets to be agreed |

Targets marked *to be set* will be agreed with the project owner once a
baseline exists, and recorded as an ADR.

## Reporting

Each run writes its results to the repository's eval results location; a
summary table is published in the README and in this chapter.
