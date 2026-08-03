# Security Policy

## Supported project state

GeoProspect is currently in Stage 0. Only the latest commit on `main` is supported for security fixes. No model, production API, PostGIS service, frontend or agent is authorised or supported during Stage 0.

## Reporting a vulnerability

Do not disclose suspected vulnerabilities, credentials, private endpoints or exploitable data-access details in a public issue or pull request.

Use GitHub's **Report a vulnerability** function for this repository when it is available. When that function is unavailable, contact the repository owner privately through the contact method shown on the owner's GitHub profile and include:

- A concise description of the issue.
- Reproduction steps or a minimal proof of concept.
- The affected commit, file or workflow.
- Potential impact.
- Any suggested mitigation.

Do not include real credentials, restricted datasets or personal information in the report.

## Response expectations

A report will be assessed for reproducibility, severity and Stage 0 relevance. Confirmed issues will be corrected through a traceable change. Public disclosure should wait until the issue is fixed or the repository owner explicitly approves disclosure.

## Repository safeguards

The repository uses automated formatting, linting, typing, tests, secret detection, private-key detection and large-file checks. These controls reduce risk but do not replace source licensing, provenance review or the Stage 0 GO/SWITCH/STOP gate.
