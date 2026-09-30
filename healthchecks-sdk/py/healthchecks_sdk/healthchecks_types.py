# Typed models for the Healthchecks SDK.
#
# GENERATED from the API model: main.kit.entity.<e>.fields{} and per-op
# params (op.<name>.points[].g.params[]). Field/param types come from the
# canonical type sentinels via @voxgig/sdkgen canonToType (source of truth:
# @voxgig/apidef VALID_CANON). Do not edit by hand.
#
# These are TypedDicts, not dataclasses: the SDK ops return/accept plain dicts
# at runtime, and a TypedDict IS a dict shape, so the types match the runtime.
# Optional (req:false) keys are modelled as TypedDict key-optionality
# (total=False), split into a required base + total=False subclass when a type
# has both required and optional keys.

from __future__ import annotations

from typing import TypedDict, Any


class Check(TypedDict, total=False):
    desc: str
    id: str
    name: str
    slug: str
    status: str
    tags: str
    unique_key: str
    uuid: str


class CheckLoadMatch(TypedDict):
    id: str


class CheckListMatch(TypedDict, total=False):
    desc: str
    id: str
    name: str
    slug: str
    status: str
    tags: str
    unique_key: str
    uuid: str
