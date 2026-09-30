# Healthchecks generated project

This directory preserves Voxgig's native `.sdk/` and `py/` structure.
Only Python is generated. See the [assessment README](../README.md) for
installation, live usage, reproduction, and limitations, and the
[report](../REPORT.md) for observed outcomes.

The generated Python documentation remains intact as evidence. Its claim
that `list()` returns dictionaries is inaccurate for the tested version:
it returns entity objects; call `data_get()` on each. The assessment example
uses the verified behavior. Generated links describe the proposed repository
destination and do not prove publication.

Minimal list usage (configure the environment variable locally first):

```python
import os
from healthchecks_sdk import HealthchecksSDK

client = HealthchecksSDK({"apikey": os.environ.get("HEALTHCHECKS_API_KEY")})
checks = client.Check().list()
print(f"Retrieved {len(checks)} checks")
```

For both live reads with safe output and error handling, run
`examples/read_checks.py` from the assessment repository root as documented
in the assessment README.
