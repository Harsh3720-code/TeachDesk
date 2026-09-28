# Features

**Status: Planned.** Each feature below is specified from `SPEC.md` §3. Design
detail, prompts, schemas and test strategy are added as each feature is built.

## F1 — Parent letters and emails

**Milestone:** Week 1

**User story.** As a teacher, I type a request such as *"Letter to Year 9
parents about the science museum trip on Friday 16 October"* and receive a
draft letter that uses the school's templates and policies, cites its sources,
and flags anything it could not verify.

**Behaviour**

- Retrieve relevant school documents: trips policy, term dates, letter
  templates and contact details.
- Draft the letter from the request and retrieved content only.
- Every factual claim (dates, costs, policies) must come from a retrieved
  document. A missing fact appears as `[TO CONFIRM: ...]` and is never invented.
- Output: letter text plus the list of sources used.

**Acceptance criteria**

- A teacher can request, edit, approve and export a letter.
- Every draft cites its sources.
- Missing facts are flagged, never made up.

**Principal risks and controls**

| Risk | Control |
|---|---|
| Hallucinated date or cost reaches parents | Structured output listing claims with sources; exact-match check of dates and costs against retrieved text; approval required before export. |
| Out-of-date policy retrieved | Documents carry source references shown to the teacher. |

## F2 — Report comments

**Milestone:** Week 2

**User story.** As a teacher, I provide a class list with short notes per pupil
(e.g. *"strong effort, essays need structure, 72% in test"*) and receive one
polished comment per pupil in the school's report style and word limit.

**Behaviour**

- Pupil names are replaced with tokens before any model call and restored
  afterwards.
- The system does **not** assign or change grades, predict attainment, or add
  judgements the teacher did not give.

**Acceptance criteria**

- A class of 30 produces 30 comments, each within the word limit and in school
  style.
- No invented judgements.
- No roster name in any outbound prompt.

**Principal risks and controls**

| Risk | Control |
|---|---|
| Pupil name sent to the model | Roster-based redaction before every call; automated test on logged prompts. |
| Model adds a judgement the teacher did not make | Constrained prompt; guardrail check against the teacher's notes; teacher approval. |
| Word limit exceeded | Deterministic word count check; regenerate or flag. |

## F3 — Resource adapter

**Milestone:** Week 2

**User story.** As a teacher, I upload a worksheet (text, .docx or PDF) and
receive simplified, stretch and EAL-friendly versions, each with its reading
age reported.

**Behaviour**

- Produce one or more versions: simplified (lower reading age), stretch
  (harder), EAL-friendly (with a key-vocabulary glossary).
- Report the reading age of the original and of each version.

**Acceptance criteria**

- Each adapted version hits its target reading-age band.
- Each version keeps the original learning objective.

**Principal risks and controls**

| Risk | Control |
|---|---|
| Adapted version misses its reading-age band | Measured with textstat; regenerate or flag if outside the band. |
| Learning objective lost in simplification | Objective extracted first and checked against each version. |

## F4 — Agent router

**Milestone:** Week 3

**User story.** As a teacher, I use one chat box for everything; the system
decides what I need, asks when it is unclear, and refuses what it must not do.

**Behaviour**

- Route each request to F1, F2 or F3.
- Ask a clarifying question when the request is ambiguous.
- Refuse out-of-scope or unsafe requests (e.g. *"What grade should this pupil
  get?"*) with a short explanation.

**Acceptance criteria**

- Routing accuracy measured against the golden evaluation set.
- All grading, prediction and SEN-labelling requests are refused.
