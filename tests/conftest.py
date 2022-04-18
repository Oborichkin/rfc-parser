import pytest
from RfcParser import RFC


@pytest.fixture
def rfc3261() -> RFC:
    with open("data/rfc3261.txt") as f:
        return RFC(f.read())


@pytest.fixture
def rfc2119() -> RFC:
    with open("data/rfc2119.txt") as f:
        return RFC(f.read())


@pytest.fixture
def rfc2327() -> RFC:
    with open("data/rfc2327.txt") as f:
        return RFC(f.read())
