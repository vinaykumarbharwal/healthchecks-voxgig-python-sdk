# Voxgig developer-experience report

**Exercise 1 only.** Prepared by Vinay Kumar with AI assistance, 30 September
2026. This is a narrow Python SDK assessment, not a claim that both exercises
are complete. No invoice or PyPI release was prepared.

## API choice and provenance

I selected Healthchecks.io Management API v3: listing checks and retrieving
one check. On 30 September 2026 the assistant retrieved all 802 public
repositories from the [Voxgig catalogue](https://github.com/orgs/voxgig-sdk/repositories)
through the paginated GitHub API. Case-insensitive searches of names and
descriptions for `health.?check`, `healthchecks.io`, and `hc-ping` found no match.
The [snapshot](evidence/catalogue.jsonl) and [session notes](evidence/session.md)
record the method. This is a metadata-level absence check, not a source-content
audit of 802 repositories or a statement about private repositories.

No official OpenAPI link was found on the [official API documentation](https://healthchecks.io/docs/api/)
or in a targeted official-repository search. The supplied specification is a
manually authored subset derived from those docs, with two GET operations,
`X-Api-Key` authentication, documented status codes, and a small selection of
response properties. Read-only credentials use `unique_key`, not `uuid`.

## Environment and output

Windows host: Python 3.11.0, Node 24.14.1, npm 11.11.0, Git 2.53.0.windows.2,
GitHub CLI 2.96.0. Successful generation used the official Docker image
`node:24.14.1-bookworm-slim` (digest recorded in scripts/generate.ps1), with
Node 24.14.1 and npm 11.11.0. The Python SDK ran on the Windows host.

Scaffolder 0.30.4; sdkgen 4.32.1; apidef 8.22.1; model 12.0.0; docgen 0.30.0;
aontu 0.76.0; jostraca 0.39.0; TypeScript 7.0.2. Exact dependencies are in the
npm lockfile and [version log](evidence/generator-versions.log).

The actual generator produced one Python package, a `Check` entity with
`list` and `load`, API-key configuration, test transport, offline tests,
types, documentation, and reusable model/templates/components in `.sdk/`.
No handwritten HTTP client was substituted. The separate example calls the
generated entity methods. No generated Python code or upstream template was
edited. The project overlay disables root release output and sets assessment
author and proposed repository/package metadata.

## Verification

| Check | Actual outcome |
| --- | --- |
| Original Windows scaffold | Failed: `Failed to start npm: spawn npm ENOENT` |
| Windows `--no-install` with targets/features | Failed with explicit guidance to install dependencies first |
| Direct dependency install and Python target/test feature setup | Passed |
| Native Windows generation | Failed resolving `api/api-info.aontu`; file exists under `.sdk/model/api/` |
| Linux container generation | Passed, exit 0 |
| Generated Python offline suite | Final: 194 passed, 87 skipped in 1.94 seconds |
| Added API-contract tests | Final: 3 passed in 0.08 seconds |
| Final documented installation and `pip check` | Passed: package installed in `.venv`; no broken requirements |
| `voxgig-sdkgen doctor` | Passed: `.sdk matches the scaffold (0 additive)` |
| Real API call with deliberately invalid key | Passed: `HealthchecksError`, HTTP status 401 |
| Authenticated live list | Not run at this handoff: read-only key not configured |
| Authenticated live retrieval | Not run at this handoff: needs key and suitable check data |

The initial generated run had 191 passes and 90 skips because the generated
project root README was absent. Adding a prose-only README exposed two expected
documentation-gate failures; adding the actual runnable list example made those
checks pass. Final skips: 85 cases for unselected features in test_feature.py,
one unselected cost-feature corpus case, and optional mypy (not installed).
The [final log](evidence/generated-tests-final.log) records each reason. The
materialized offline corpus is versioned so a checkout can run these tests.
Offline tests do not prove authenticated live integration. Initial added tests
failed because the assistant omitted the mock response `body`, assumed the
wrong trailing-slash behavior, and compared a case-sensitive header spelling.
The actual SDK preserves `/checks/` and sends `x-api-key`, correctly. Those
were test-authoring mistakes, not generator bugs; original logs are retained.

## Experience and recommended improvements

Each finding follows **step attempted → expected behavior → observed behavior
→ suggested improvement**. These are observations from recorded assistant
execution, not invented first-hand human interactions.

1. **High: native Windows setup.** Run the documented scaffolder → install
   dependencies and add Python → `spawn npm ENOENT`, despite npm working in
   PowerShell → handle Windows npm invocation explicitly and test Windows CI.
   A second attempt using `--no-install` and targets/features clearly explained
   the missing dependency prerequisite. Make the Windows fallback a complete
   sequence in the quick start. See [original log](evidence/scaffold.log).
2. **High: Windows model resolution.** Run `npm run generate` after successful
   installation → resolve includes relative to the model → `api/api-info.aontu`
   was reported missing even though it exists; diagnostic paths included
   `/Users/.../.sdk/api/` instead of the model location → add a Windows path
   regression case and show the include base clearly. This suggests a path
   resolution issue, but the exact root cause was not patched or proven.
   The same project generated in Linux. See [failure](evidence/generate.log)
   and [successful fallback](evidence/generate-linux.log).
3. **Medium: return-value documentation.** Follow the Python list tutorial →
   receive the described list of dictionaries → actual items are entity
   objects exposing `data_get()`; focused tests confirm this → align prose,
   type annotations and examples with runtime returns, and assert return
   shapes in documentation tests. Printing an object can pass a runnable
   example test while leaving its stated type inaccurate.
4. **Medium: docs currency and scope.** Read website setup and generated docs →
   current model extension and only selected deliverables → website examples
   use `.aon` while current source uses `.aontu`; the Python README refers to
   sibling languages/CLI/MCP that were not selected → version the quick start
   and render scope-dependent prose from active targets. Source guidance was
   more current than the website summary.
5. **Positive: API modelling.** Generate from the small specification → correct
   reads, envelope handling and header auth → `list` unwraps `checks`, the
   documented trailing slash is preserved, and `load` accepts the provided
   identifier; mock contract tests pass → retain this behavior and include
   a read-only identifier example in the tutorial.
6. **Positive: error visibility and reproducibility.** Call with an invalid
   key, run offline tests and doctor → inspect a usable failure and verify
   generated state → live HTTP 401 is available as `error.status`, offline
   suite passes and doctor reports no drift → document safe error summaries
   alongside these useful verification commands.

## Limits, AI assistance, and time

Authenticated success has not been established at this handoff.
Only Python 3.11 on Windows was exercised. Optional features/languages, writes,
filters, full response-schema coverage, and package release were out of scope.
The generation environment reported two moderate npm audit findings; their
impact was not investigated within this narrow assessment. No forced package
upgrade was applied.

Vinay directed the assistant with the API candidate, Python-only/two-operation
scope, official-doc requirements, real generator requirement, secret-handling
rules, human time limit, and honest reporting criteria. The assistant inspected
docs and code, authored the subset spec and example, ran Voxgig and tests,
corrected its own test fixtures, and drafted this report. Automated checks are
not claimed as human review. Human review, credential setup and final time
should be confirmed by Vinay before submission.

Human time: Vinay initially reported zero prior hands-on minutes and subsequently
reported **10 minutes spent**, leaving 20 minutes of the 30-minute allowance.
Specific personal review/run details have not been supplied. Further human time
must be added before submission. Assistant work began approximately 15:10 UTC;
At the 15:29 UTC handoff, assistant execution and waiting elapsed approximately
19 minutes. This is separate from human hands-on time; no claim is made that
the entire assessment took 30 minutes.

Publication: proposed account `vinaykumarbharwal`, destination
`healthchecks-voxgig-python-sdk`; public creation awaits explicit destination
confirmation. Proposed generated links are not evidence of a published repo.
