$ErrorActionPreference = 'Stop'
$workspace = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$image = 'node:24.14.1-bookworm-slim@sha256:b506e7321f176aae77317f99d67a24b272c1f09f1d10f1761f2773447d8da26c'
# A Linux dependency volume avoids mixing Windows and Linux native npm packages.
docker run --rm --mount "type=bind,source=$workspace,target=/work" --mount 'type=volume,source=voxgig-healthchecks-node-deps,target=/work/healthchecks-sdk/.sdk/node_modules' -w /work/healthchecks-sdk/.sdk $image sh -c 'npm ci && npm run generate && npx --no-install voxgig-sdkgen doctor'
if ($LASTEXITCODE -ne 0) { throw "Generation failed with exit code $LASTEXITCODE" }
