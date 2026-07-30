# GeoProspect Stage 0 Review and Merge Policy

**Effective:** 30 July 2026  
**Owner:** Lachlan McDonald  
**Status:** ACTIVE

## 1. Purpose

GeoProspect uses branches and pull requests to preserve an auditable implementation history. Pull requests are not intended to create routine manual-review obligations for the project owner.

The owner has stated that they are unlikely to manually review GeoProspect pull requests. Therefore, routine implementation work must not remain open indefinitely awaiting owner review.

## 2. Default Operating Rule

For routine Stage 0 work, the implementing AI assistant may:

1. Create a narrowly scoped branch and pull request.
2. Inspect the complete diff and relevant repository state.
3. Run or verify all applicable automated checks.
4. Correct identified defects.
5. Merge the pull request when the acceptance conditions are satisfied.
6. Record the checks, evidence produced, risks and next action.

The owner is not a required code reviewer for routine changes.

## 3. Review Standard

Before merging routine work, the implementing assistant must verify:

- The change is limited to the authorised Stage 0 work unit.
- No unrelated files or user changes are included.
- The diff matches the issue and acceptance criteria.
- Relevant tests, validation commands or document checks pass.
- No credentials, restricted raw data or large unintended artefacts are committed.
- Stage 1 or later work has not been introduced.
- Mandatory Stage 0 thresholds and evidence rules have not been weakened.
- Risks, assumptions and unresolved questions are visible.

A pull request may not be merged merely because it was created successfully.

## 4. Optional Independent AI Review

Where useful, a second AI system such as Claude or another ChatGPT review session may perform an independent review.

Independent AI review is recommended for:

- Acquisition and pagination logic.
- Geospatial transformations and CRS choices.
- Deduplication algorithms.
- Gate-evaluation logic.
- Licensing interpretations.
- Major scientific assumptions.
- Security-sensitive or destructive repository changes.

Independent AI review is optional unless a later governance decision makes it mandatory for a named class of change.

## 5. Decisions That Still Require Owner Input

The owner is not expected to review implementation details, but explicit owner input is required when a change involves a genuine project decision, including:

- Changing the business or portfolio objective of GeoProspect.
- Weakening or replacing a mandatory feasibility threshold.
- Accepting a material scientific-validity exception.
- Choosing between materially different commodity or region strategies when evidence does not determine the answer.
- Accepting unresolved licensing or redistribution risk.
- Publishing restricted or potentially sensitive data.
- Incurring paid services or material expenditure.
- Making irreversible or destructive changes outside the approved work unit.
- Issuing the final GO, SWITCH or STOP decision when owner sign-off is explicitly required by the final gate package.

These decisions must be presented concisely with evidence, consequences and a recommended option. The owner should not be asked to perform a line-by-line code review.

## 6. Merge Behaviour

- Routine, low-risk documentation and implementation pull requests should be reviewed and merged during the same execution session when checks pass.
- A pull request should remain open only when there is a real blocker, failed check, unresolved high-risk finding or owner decision required.
- Draft pull requests may be used while work is incomplete, but must not be left open merely to wait for routine owner review.
- The Stage 0 master issue remains open until the final GO, SWITCH or STOP outcome; merging routine pull requests does not close the master gate.

## 7. Review Evidence

Each merged pull request must record, as applicable:

- What changed.
- Which Stage 0 objective, gate and step it advances.
- Tests or validation performed.
- Diff-review result.
- Evidence artefacts produced.
- Risks, assumptions and unresolved questions.
- Whether independent AI review occurred.
- Exact next action.

## 8. Current Policy Summary

Pull requests remain the default implementation and audit mechanism. They are not a queue of work for Lachlan McDonald to manually review. Routine pull requests will be checked and merged by the implementing assistant. Lachlan will be consulted only for material decisions, exceptions and risks that cannot properly be resolved from the governing documents and measured evidence.
