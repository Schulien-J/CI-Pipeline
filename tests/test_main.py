import pytest

from main import main

def test_main():
    assert main() == 6
