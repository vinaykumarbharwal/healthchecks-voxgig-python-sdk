# Healthchecks Python SDK

A Python client for listing and retrieving monitoring checks from the
[Healthchecks.io Management API](https://healthchecks.io/docs/api/), generated
with [Voxgig SDK tools](https://voxgig.com/sdk).

This is an unofficial SDK, unaffiliated with Healthchecks.io. It is a small,
MIT-licensed assessment project with two read operations. The input is a
manually authored OpenAPI subset of the official API documentation.

**For reviewers:** [mini-task report](REPORT.md) ·
[test evidence](evidence) · [submission files](submission-files.txt) ·
[license](LICENSE) · [attribution](NOTICE)

## Submission status

| Check | Result |
| --- | --- |
| Actual Voxgig generation | Passed in a pinned Linux container |
| Generated offline tests | 194 passed, 87 skipped |
| Focused contract tests | 3 passed |
| Live invalid-key request | HTTP 401 exposed as `HealthchecksError` |
| Authenticated list and retrieval | Not run; local key unavailable at handoff |

The SDK is published as source for assessment. See the report for Windows
generation failures and Python documentation limitations.

## Package

| Language | Package | Installation |
| --- | --- | --- |
| Python | `healthchecks-voxgig-python-sdk` | From source; not published to PyPI |

## Entities and operations

The generated `Check` entity provides both operations. A list returns entity
objects; call `data_get()` to access each record.

| Entity call | API operation | Return value |
| --- | --- | --- |
| `client.Check().list()` | `GET /api/v3/checks/` | List of check entities |
| `client.Check().load({"id": identifier})` | `GET /api/v3/checks/{id}` | One check entity |

Use the listed record's `unique_key` with a read-only API key, or `uuid` with
a read-write key. Only the two read operations are included in this model.

## Install and verify

Tested with Python 3.11.0 on Windows. From the repository root in PowerShell:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-test.txt -e ./healthchecks-sdk/py
.venv/Scripts/python.exe -m pytest healthchecks-sdk/py/test/ -q
.venv/Scripts/python.exe -m pytest tests/ -q
```

On Linux/macOS use `.venv/bin/python` instead. The locked test requirements
capture the tested environment; the generated package declares its own runtime
dependency. The generated package's Python >=3.8 claim was not tested beyond
Python 3.11.0 in this assessment.

## Quickstart

Configure `HEALTHCHECKS_API_KEY` locally as shown below, then:

```python
import os
from healthchecks_sdk import HealthchecksSDK

client = HealthchecksSDK({"apikey": os.environ["HEALTHCHECKS_API_KEY"]})
checks = client.Check().list()
print(f"Retrieved {len(checks)} checks")

if checks:
    record = checks[0].data_get()
    identifier = record.get("unique_key") or record.get("uuid")
    check = client.Check().load({"id": identifier})
    print("Retrieved one check successfully")
```

The [runnable example](examples/read_checks.py) adds error handling, validates
that the retrieved identifier matches, and avoids printing private records.

## Offline example

The opt-in test feature uses a mock transport and needs no credentials. Seed
the records before calling it:

```python
from healthchecks_sdk import HealthchecksSDK

client = HealthchecksSDK.test({
    "entity": {
        "check": {
            "demo": {"id": "demo", "name": "Synthetic check", "status": "new"}
        }
    }
})
checks = client.Check().list()
assert len(checks) == 1
assert checks[0].data_get()["name"] == "Synthetic check"
assert client.Check().load({"id": "demo"}).data_get()["status"] == "new"
```

## Run the example

Create a **read-only** project API key in Healthchecks.io → Project Settings.
Enter it locally without putting it in shell history or this repository:

```powershell
$key = Read-Host 'Healthchecks read-only API key' -AsSecureString
$env:HEALTHCHECKS_API_KEY = [System.Net.NetworkCredential]::new('', $key).Password
.venv/Scripts/python.exe examples/read_checks.py
Remove-Item Env:HEALTHCHECKS_API_KEY
```

For a key already stored in your Windows user environment, load it in the
terminal with `$env:HEALTHCHECKS_API_KEY = [Environment]::GetEnvironmentVariable('HEALTHCHECKS_API_KEY', 'User')`.
To remove that persistent setting later, use
`[Environment]::SetEnvironmentVariable('HEALTHCHECKS_API_KEY', $null, 'User')`.
The example does not load `.env` files.

The example lists checks, takes the first record's `unique_key` (read-only key)
or `uuid`, then retrieves that same check. An empty list is a successful list
call but leaves retrieval skipped. Create a harmless check manually if needed;
the example never creates or pings one. It prints counts and outcomes, not
account data. It uses `HealthchecksSDK({"apikey": key})`, `Check().list()`,
and `Check().load({"id": identifier})`; returned entities expose `data_get()`.

One deliberately invalid-key request requires no account key:

```powershell
.venv/Scripts/python.exe examples/read_checks.py --invalid-key
```

Do not print complete SDK exception/context objects: they may include account
information. The example prints only exception class and HTTP status.

## Repository layout

| Path | Contents |
| --- | --- |
| [`healthchecks-sdk/py/`](healthchecks-sdk/py/) | Generated Python package, tests and language documentation |
| [`healthchecks-sdk/.sdk/`](healthchecks-sdk/.sdk/) | Native generator model, templates, components and lockfile |
| [`openapi.json`](openapi.json) | Original two-operation specification |
| [`examples/read_checks.py`](examples/read_checks.py) | Runnable live example with safe output |
| [`tests/`](tests/) | Focused offline API-contract verification |
| [`REPORT.md`](REPORT.md) | Assessment findings, results, AI assistance and time |
| [`evidence/`](evidence/) | Catalogue snapshot and recorded tool/test outcomes |

## Reproduce generation

Sources: [Voxgig setup](https://voxgig.com/sdk/docs/create-sdkgen) and the
[current source guide](https://github.com/voxgig/create-sdkgen/blob/main/AGENTS.md).
Node >=24 is required. Versions are pinned by
`healthchecks-sdk/.sdk/package-lock.json`; the scaffolder used was
`@voxgig/create-sdkgen@0.30.4` and SDK generator `4.32.1`.

On Windows with Docker Desktop running, from this repository root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/generate.ps1
```

This uses a pinned official Linux Node image and an isolated dependency volume.
It runs `npm ci`, `npm run generate`, and `voxgig-sdkgen doctor` in `.sdk/`.
On Linux with Node 24.14.1 installed, the equivalent is:

```sh
cd healthchecks-sdk/.sdk
npm ci
npm run generate
npx --no-install voxgig-sdkgen doctor
```

The authoritative regeneration input is
`healthchecks-sdk/.sdk/def/openapi.json`; `openapi.json` at repository root is
an identical copy of the original source for easy inspection. Keep them in
sync if deliberately changing the API scope. The specification is a
**manually authored subset**, based on the
[official Healthchecks Management API v3 docs](https://healthchecks.io/docs/api/),
not an official OpenAPI download. Filters and most response properties are
intentionally out of scope; unspecified response fields are not forbidden.

The original clean-scaffold command was:

```sh
npx --yes @voxgig/create-sdkgen@0.30.4 healthchecks -d ./openapi.json -o ./healthchecks-sdk -t py -f test
```

That command failed natively on Windows with `spawn npm ENOENT`. The documented
`--no-install` retry also failed when targets/features were supplied before
dependencies existed. To scaffold afresh, use a **new empty output folder**:
run the same pinned scaffolder with `--no-install` and without `-t`/`-f`,
then install in `.sdk/`, run `npm run add-target -- py` and
`npm run add-feature -- test`, and generate in Linux. A clean fresh scaffold
may resolve newer transitive versions; use the committed lockfile to reproduce
this assessment. Full attempt logs are in [evidence](evidence).

Project decisions live in `.sdk/model/project.aontu`. The top generation phase
is disabled to preserve assessment documentation and avoid top-level release
workflows. Templates and generated Python code have not been patched.

## Customization and Python reference

Use [`project.aontu`](healthchecks-sdk/.sdk/model/project.aontu) for project
settings, then regenerate. API operations come from the specification and
entity model. Changes to generated Python files will not reliably survive
regeneration; template or component changes belong in `.sdk/`.

The generated [Python README](healthchecks-sdk/py/README.md) and
[reference](healthchecks-sdk/py/REFERENCE.md) describe the wider client surface.
Their list-return prose is inconsistent with the verified entity behavior;
the quickstart above and assessment example use the observed interface.

## Limitations and publication

This is a narrow assessment artifact, not a production SDK release. Read the
[report](REPORT.md) for actual live-test status, Windows blockers, skipped tests,
and documentation inconsistencies. Generated READMEs remain intact as evidence;
use this README and `examples/read_checks.py` for the assessed workflow.

Public source repository:
[vinaykumarbharwal/healthchecks-voxgig-python-sdk](https://github.com/vinaykumarbharwal/healthchecks-voxgig-python-sdk).
Publication succeeded on 30 September 2026. No package was published to PyPI.

Original assessment contributions: Copyright 2026 Vinay Kumar, MIT.
Upstream notices and the generated SDK's license are preserved.
