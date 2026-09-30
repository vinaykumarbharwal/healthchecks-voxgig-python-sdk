# Assessment evidence

Retained files support the claims in [REPORT.md](../REPORT.md). Redundant
installation logs, intermediate test runs and submission housekeeping were
removed during cleanup; they remain available in Git history.

| File | Evidence |
| --- | --- |
| `catalogue.jsonl` | All 802 public Voxgig catalogue repositories checked on 2026-09-30 |
| `generator-versions.log` | Installed generator package versions |
| `scaffold.log` | Original native Windows `spawn npm ENOENT` failure |
| `scaffold-no-install.log` | Missing-toolchain diagnostic for the first fallback |
| `generate.log` | Native Windows model include-resolution failure |
| `generate-linux.log` | Successful generation in the pinned Linux container |
| `generated-tests-final.log` | 194 passed, 87 skipped; individual skip reasons |
| `contract-tests-final.log` | Three passing API-contract tests |
| `live-invalid-key.log` | Actual generated-SDK request rejected with HTTP 401 |
| `doctor.log` | Successful scaffold drift check |

## Catalogue and specification

Retrieved with:

```sh
gh api --paginate 'orgs/voxgig-sdk/repos?per_page=100' --jq '.[] | {name, description, html_url}'
```

Names and descriptions were searched case-insensitively for
`health.?check|healthchecks\.io|hc-ping`: no matches. This is a public metadata
check, not a source-content audit or access to private repositories.

The retained source specification is
[`healthchecks-sdk/.sdk/def/openapi.json`](../healthchecks-sdk/.sdk/def/openapi.json).
It was manually authored from https://healthchecks.io/docs/api/. The original
root copy was identical and was removed during cleanup.

## Original command sequence

The first two commands used the original root copy of `openapi.json`, before
cleanup. They are historical reproductions of the failures, not setup instructions:

```sh
npx --yes @voxgig/create-sdkgen@0.30.4 healthchecks -d ./openapi.json -o ./healthchecks-sdk -t py -f test
npx --yes @voxgig/create-sdkgen@0.30.4 healthchecks -d ./openapi.json -o ./healthchecks-sdk -t py -f test --no-install
```

After those attempts, in `healthchecks-sdk/.sdk/`:

```sh
npm install
npm run add-target -- py
npm run add-feature -- test
npm run generate
```

Native Windows generation failed. The same project generated successfully in
`node:24.14.1-bookworm-slim`; [the pinned script](../scripts/generate.ps1) records
the Docker mounts, image digest and successful `npm ci`, generation and doctor
sequence. The [README](../README.md#reproduce-generation) documents current setup.

## Verification and timing notes

The documented Python installation and `pip check` passed. Two root README
Python examples were also executed with seeded offline data. No authenticated
success is claimed. Initial assistant-authored mock fixtures were corrected;
those fixture mistakes were not SDK defects.

Vinay reported a total of **28 minutes of human hands-on work**, updating earlier
zero- and 10-minute checkpoints. Specific personal review/run details were not
provided. Assistant work is separate: approximately 19 minutes in the initial
session (15:10–15:29 UTC) and 4.5 minutes in the publication follow-up
(15:40–15:44 UTC), excluding time between turns. These are recorded checkpoints,
not a total including every later documentation edit or review.

All recorded work occurred on 30 September 2026. A sandbox proxy failure affected
initial network checks; it was an environment issue, not a Voxgig defect.
