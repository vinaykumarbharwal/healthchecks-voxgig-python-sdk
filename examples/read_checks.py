"""Read two Healthchecks operations through the unmodified generated SDK.

Only counts, test outcomes, and error status are printed. Account records,
identifiers, credentials, and full exception/context objects are never logged.
"""
import argparse
import os

from healthchecks_sdk import HealthchecksSDK
from healthchecks_sdk.core.error import HealthchecksError


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--invalid-key", action="store_true",
                        help="Make one list call using a deliberately invalid key")
    args = parser.parse_args()
    key = "assessment-deliberately-invalid" if args.invalid_key else os.getenv("HEALTHCHECKS_API_KEY")
    if not key:
        parser.error("Set HEALTHCHECKS_API_KEY locally; do not put it in source code")
    client = HealthchecksSDK({"apikey": key})
    try:
        checks = client.Check().list()
        if args.invalid_key:
            print("FAIL: invalid key was unexpectedly accepted")
            return 1
        print(f"PASS: live list returned {len(checks)} checks")
        if not checks:
            print("SKIP: retrieval needs a check; create a harmless test check manually")
            return 0
        record = checks[0].data_get()
        check_id = record.get("unique_key") or record.get("uuid")
        if not check_id:
            print("FAIL: first check lacks a documented retrieval identifier")
            return 1
        loaded = client.Check().load({"id": check_id}).data_get()
        if (loaded.get("unique_key") or loaded.get("uuid")) != check_id:
            print("FAIL: retrieved identifier does not match the listed check")
            return 1
        print("PASS: live retrieval returned the same check")
        return 0
    except HealthchecksError as error:
        status = getattr(error, "status", None)
        print(f"SDK error: {type(error).__name__}; HTTP status={status}")
        if args.invalid_key and status == 401:
            print("PASS: invalid-key list request rejected with HTTP 401")
            return 0
        return 1
    except Exception as error:
        print(f"FAIL: unexpected {type(error).__name__} (details suppressed)")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
