import pytest

from dummy import main


@pytest.mark.timeout(5)
def test_dummy():
    assert dummy() == 8