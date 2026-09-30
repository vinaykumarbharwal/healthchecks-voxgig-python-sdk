# Healthchecks Python SDK — Voxgig assessment

An unofficial, MIT-licensed Python SDK generated with the actual Voxgig
toolchain. Scope: list monitoring checks and retrieve one check. No API writes,
other language SDKs, frontend, or PyPI publication.

The generated SDK is in [`healthchecks-sdk/py`](healthchecks-sdk/py).
The [report](REPORT.md) separates offline verification from live API results.

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

## Limitations and publication

This is a narrow assessment artifact, not a production SDK release. Read the
[report](REPORT.md) for actual live-test status, Windows blockers, skipped tests,
and documentation inconsistencies. Generated READMEs remain intact as evidence;
use this README and `examples/read_checks.py` for the assessed workflow.

Public source publication requires confirmation of the proposed account
`vinaykumarbharwal` and repository name `healthchecks-voxgig-python-sdk`.
No PyPI publication is needed. If publication has not completed, after reviewing
the files, confirming the account, and verifying the name is unused:

```powershell
gh api user --jq .login
gh repo create vinaykumarbharwal/healthchecks-voxgig-python-sdk --public --source . --remote origin --push
```

The command assumes a local commit exists. Do not run it against an existing
repository or treat proposed links in generated metadata as published links.

Original assessment contributions: Copyright 2026 Vinay Kumar, MIT.
Upstream notices and the generated SDK's license are preserved.
