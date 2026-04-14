import pytest

from main import dummy


@pytest.mark.timeout(5)
def test_dummy():
    assert dummy() == 8
