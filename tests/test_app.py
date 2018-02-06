import pytest
from pibackup import app


def test_imports():
    assert app.HOME_FOLDER == "/home/pi/"
    assert app.config_data['system']['type'] == 'fhem' == app.SMART_HOME_SYSTEM

