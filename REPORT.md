# Voxgig SDK assessment report

Exercise 1, Vinay Kumar, 30 September 2026. Built with AI assistance using the
actual Voxgig generator; no handwritten HTTP client replaced its output.

Public repository: [healthchecks-voxgig-python-sdk](https://github.com/vinaykumarbharwal/healthchecks-voxgig-python-sdk).
Publication and the remote commit were verified on 30 September 2026.

## API and output

Healthchecks.io Management API v3 was selected for two reads: list checks and
retrieve one. The assistant checked all **802 public repositories** in the
[Voxgig catalogue](https://github.com/orgs/voxgig-sdk/repositories) on 30 September.
Name/description searches for Healthchecks, health-check, health check,
Healthchecks.io and hc-ping found no match. The [snapshot](evidence/catalogue.jsonl)
is evidence of metadata-level absence, not a source audit or private-repository check.

No official OpenAPI download was found in the documentation or targeted
repository search. [openapi.json](openapi.json) is a clearly labelled, manually
authored subset of the [official API docs](https://healthchecks.io/docs/api/).
It describes two GET operations, header authentication and partial response
schemas. Read-only keys return `unique_key` for retrieval.

Voxgig generated the Python package, `Check().list()` and `Check().load()`,
authentication, test transport, types, tests and documentation. Native `.sdk/`
model/template structure is preserved. The [example](examples/read_checks.py)
uses those generated methods. Generated Python code and templates are unpatched.
Original contributions are MIT-licensed to Vinay Kumar; upstream notices remain.

## Environment and verification

Windows: Python 3.11.0, Node 24.14.1, npm 11.11.0, Git 2.53.0.windows.2,
GitHub CLI 2.96.0. Successful generation used pinned Linux Node 24.14.1 in Docker.
Scaffolder **0.30.4**, sdkgen **4.32.1**, apidef **8.22.1**, model **12.0.0**,
docgen **0.30.0**. Lockfiles, [versions](evidence/generator-versions.log), exact
[reproduction instructions](README.md#reproduce-generation) and attempt logs are included.

| Verification | Actual result |
| --- | --- |
| Windows scaffold | Failed: `spawn npm ENOENT` |
| Separate install and target setup | Passed |
| Windows generation | Failed resolving an existing model include |
| Linux generation and regeneration | Passed |
| Generated offline tests | **194 passed, 87 skipped** |
| Added offline contract tests | **3 passed** |
| Installation, pip dependency check, generator doctor | Passed; no scaffold drift |
| Live deliberately invalid-key request | Passed: `HealthchecksError.status == 401` |
| Authenticated list/retrieval | Not run: key unavailable at publication handoff |

Skips cover unselected features and optional mypy. Offline success does not prove
live integration. Initial assistant-written fixtures had missing response bodies
and incorrect URL/header expectations; these were corrected, not reported as
SDK bugs. Adding a runnable README example satisfied the generated documentation
gate. [Logs](evidence) retain the attempts and final results.

## Developer experience

These findings describe recorded assistant execution, not invented human observations.

1. **High - Windows setup:** documented scaffold → install dependencies →
   `spawn npm ENOENT` despite working npm in PowerShell → support Windows npm
   invocation and publish a tested fallback. The `--no-install` error usefully
   explained that targets/features need installed dependencies first.
2. **High - model paths:** generate on Windows → resolve local includes →
   existing `api/api-info.aontu` reported missing; the same project worked in
   Linux → add Windows include-resolution regression coverage. Exact root
   cause remains unproven; the container avoided patching the generator.
3. **Medium - Python docs:** follow list tutorial → dictionaries as described →
   actual items are entities with `data_get()` → align prose and annotations
   with runtime returns, and test return shapes rather than only executable snippets.
4. **Medium - docs consistency:** follow current setup → matching extensions and
   selected scope → website shows `.aon`, source uses `.aontu`; Python docs mention
   unselected sibling products → version the quick start and condition scope prose.
5. **Positive - mapping and errors:** generate the subset and verify requests →
   useful read operations and inspectable failures → correct envelope extraction,
   trailing slash and API-key header in mocks; HTTP 401 exposed in a real request →
   retain these behaviors and document safe error summaries and read-only identifiers.

## Limits, assistance and time

Only Python 3.11 on Windows was exercised. Writes, filters, full schema coverage,
other languages and package publication are outside scope. npm reported two
moderate audit findings; their impact was not investigated. No forced upgrade
was applied. The targeted tracked-file secret scan passed; it is not an exhaustive
security audit. No private API response is stored.

Vinay directed API choice, scope, official-source verification, actual generation,
secret handling and the time limit. AI authored the subset/example, inspected
output, ran tools and tests, corrected its fixtures, and drafted this report.
Specific human code-review or test-run details have not been supplied, so automated
verification is not presented as personal verification.

**Human time last reported: 10 minutes**, leaving 20 of the 30-minute allowance;
additional human work must be included before submission. Assistant execution
and waiting took approximately 19 minutes in the first work session. Follow-up
execution is recorded separately in [session notes](evidence/session.md); time
between turns is not counted as assistant execution. No claim is made that the
entire assessment took 30 minutes. This is exercise 1 only; no invoice was prepared.
