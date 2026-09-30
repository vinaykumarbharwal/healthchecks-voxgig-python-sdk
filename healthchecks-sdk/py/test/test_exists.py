# Healthchecks SDK exists test

import pytest
from healthchecks_sdk import HealthchecksSDK


class TestExists:

    def test_should_create_test_sdk(self):
        testsdk = HealthchecksSDK.test(None, None)
        assert testsdk is not None
