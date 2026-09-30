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
