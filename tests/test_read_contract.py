"""Offline contract checks with synthetic records, never a live account."""
import json
import pytest
from healthchecks_sdk import HealthchecksSDK
from healthchecks_sdk.core.error import HealthchecksError


def mock_client(body, status=200):
    calls = []

    def fetch(url, init):
        calls.append((url, init))
        return {"status": status, "statusText": "OK" if status == 200 else "Unauthorized",
                "headers": {"content-type": "application/json"},
                "body": json.dumps(body), "json": lambda: body}, None

    return HealthchecksSDK({"apikey": "synthetic-test-key", "system": {"fetch": fetch}}), calls


def test_list_unwraps_checks_and_returns_entities():
    record = {"name": "Synthetic check", "unique_key": "synthetic-id", "status": "new"}
    client, calls = mock_client({"checks": [record]})
    checks = client.Check().list()
    assert len(checks) == 1
    assert checks[0].data_get() == record
    assert calls[0][0] == "https://healthchecks.io/api/v3/checks/"
    assert calls[0][1]["method"] == "GET"
    assert calls[0][1]["headers"]["x-api-key"] == "synthetic-test-key"


def test_load_accepts_read_only_identifier():
    record = {"name": "Synthetic check", "unique_key": "synthetic-id", "status": "new"}
    client, calls = mock_client(record)
    assert client.Check().load({"id": "synthetic-id"}).data_get() == record
    assert calls[0][0] == "https://healthchecks.io/api/v3/checks/synthetic-id"
    assert calls[0][1]["method"] == "GET"
    assert calls[0][1]["headers"]["x-api-key"] == "synthetic-test-key"


def test_unauthorized_is_a_typed_error_with_status():
    client, calls = mock_client({}, status=401)
    with pytest.raises(HealthchecksError) as caught:
        client.Check().list()
    assert caught.value.status == 401
    assert len(calls) == 1
