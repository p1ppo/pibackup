import pytest
from pibackup import config


def test_imports():
    assert config.HOME_DIR == "/home/pi/"
