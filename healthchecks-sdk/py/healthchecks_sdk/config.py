# Healthchecks SDK configuration


# The sekreto plugin DEFINITIONS the model selected per feature, imported
# above by name from the modules the catalogue's active `plugin.def`
# entries declare. Handed to each feature (secrets builds its Sekreto
# with them): a provider kind not listed here is unknown to that SDK.
FEATURE_PLUGINS = {
}


_shared_config = None


def shared_config():
    """Return the process-wide config, built once on first use.

    The SDK reads the config on every request and never writes to it, so one
    instance is shared by every client rather than rebuilt per client.

    The returned dict is shared: treat it as read-only. Callers that need to
    mutate should use make_config, which always returns a fresh copy.
    """
    global _shared_config
    if _shared_config is None:
        _shared_config = make_config()
    return _shared_config


def make_config():
    """Build a fresh, fully materialised config dict.

    Every call rebuilds the whole structure, so prefer shared_config unless
    you need a private copy you intend to mutate.
    """
    return {
        "main": {
            "name": "Healthchecks",
            "slug": "healthchecks",
            "version": "0.0.1",
            "target": "py",
        },
        "feature": {
            "test": {
        "options": {
          "active": False,
        },
        "optspec": {
          "entity": "`$MAP`",
          "net": "`$MAP`",
        },
        "strict": False,
        "transport": "base",
      },
        },
        "options": {
            "base": "https://healthchecks.io/api/v3",
            "auth": {
                "prefix": "",
                "name": "X-Api-Key",
            },
            "headers": {
        "content-type": "application/json",
      },
            "entity": {
                "check": {},
            },
        },
        "entity": {
      "check": {
        "fields": [
          {
            "name": "desc",
            "title": "Desc",
            "type": "`$STRING`",
          },
          {
            "name": "id",
            "title": "Id",
            "type": "`$STRING`",
          },
          {
            "name": "name",
            "title": "Name",
            "type": "`$STRING`",
          },
          {
            "name": "slug",
            "title": "Slug",
            "type": "`$STRING`",
          },
          {
            "name": "status",
            "title": "Status",
            "type": "`$STRING`",
          },
          {
            "name": "tags",
            "title": "Tags",
            "type": "`$STRING`",
          },
          {
            "name": "unique_key",
            "title": "Unique Key",
            "type": "`$STRING`",
            "short": "Returned with a read-only key",
          },
          {
            "name": "uuid",
            "title": "Uuid",
            "type": "`$STRING`",
            "short": "Omitted with a read-only key",
          },
        ],
        "id": {
          "field": "id",
          "name": "id",
        },
        "name": "check",
        "op": {
          "list": {
            "input": "data",
            "name": "list",
            "points": [
              {
                "kind": "http",
                "method": "GET",
                "orig": "/checks/",
                "segments": [
                  {
                    "lit": "checks",
                  },
                ],
                "parts": [
                  "checks",
                ],
                "rename": {},
                "transform": {
                  "req": "`reqdata`",
                  "res": "`body.checks`",
                },
                "args": {},
                "select": {},
              },
            ],
          },
          "load": {
            "input": "data",
            "name": "load",
            "points": [
              {
                "kind": "http",
                "method": "GET",
                "orig": "/checks/{id}",
                "segments": [
                  {
                    "lit": "checks",
                  },
                  {
                    "var": "id",
                  },
                ],
                "parts": [
                  "checks",
                  "{id}",
                ],
                "rename": {},
                "transform": {
                  "req": "`reqdata`",
                  "res": "`body`",
                },
                "args": {
                  "params": [
                    {
                      "name": "id",
                      "orig": "id",
                      "type": "`$STRING`",
                      "kind": "param",
                      "reqd": True,
                    },
                  ],
                },
                "select": {
                  "exist": [
                    "id",
                  ],
                },
              },
            ],
          },
        },
        "relations": {
          "ancestors": [],
        },
      },
    },
    }
