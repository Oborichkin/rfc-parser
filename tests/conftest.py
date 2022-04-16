import pytest


@pytest.fixture
def rfc3261():
    with open("data/rfc3261.txt") as f:
        return f.read()


@pytest.fixture
def rfc2119():
    with open("data/rfc2119.txt") as f:
        return f.read()


@pytest.fixture
def rfc2327():
    with open("data/rfc2327.txt") as f:
        return f.read()
