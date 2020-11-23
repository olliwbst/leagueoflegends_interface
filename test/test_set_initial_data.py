import pytest

from app.league_scrapper import LeagueToolBelt


def test_set_initial_data_complete():
    """
    Test that initial data is set completely
    """
    test_object = LeagueToolBelt()
    assert test_object.install_dir != None
    assert test_object.port != None
    assert test_object.auth != None
    assert test_object.version != None
