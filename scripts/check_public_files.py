"""Fail if tracked files include local secrets, credentials, or dependency dirs.

This targeted check supports manual review; it is not an exhaustive secret detector.
Only paths/categories are printed, never matching credential text.
"""
import os
from pathlib import Path
import re
import subprocess


root = Path(__file__).resolve().parents[1]
paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
known_key = os.getenv("HEALTHCHECKS_API_KEY", "").encode()
patterns = [
    re.compile(rb"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(rb"github_pat_[A-Za-z0-9_]{50,}"),
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]
failures = []
for name in filter(None, paths):
    path = Path(name)
    if any(part in {"node_modules", ".venv", "__pycache__", ".jostraca"} for part in path.parts):
        failures.append((name, "local/generated cache directory"))
    if path.name == ".env" or (path.name.startswith(".env.") and path.name != ".env.example") or ".local." in path.name:
        failures.append((name, "local environment file"))
    data = (root / path).read_bytes()
    if known_key and known_key in data:
        failures.append((name, "configured API key"))
    if any(pattern.search(data) for pattern in patterns):
        failures.append((name, "credential pattern"))
for name, kind in failures:
    print(f"FAIL: {name}: {kind}")
if failures:
    raise SystemExit(1)
print(f"PASS: scanned {len([p for p in paths if p])} tracked files; no targeted secret or local-file matches")
print("Configured API-key scan: " + ("included" if known_key else "not available"))
