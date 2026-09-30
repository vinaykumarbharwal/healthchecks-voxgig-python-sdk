# Healthchecks SDK utility: make_context

from projectname_sdk.core.context import HealthchecksContext


def make_context_util(ctxmap, basectx):
    return HealthchecksContext(ctxmap, basectx)
