import pytest

from app.league_scrapper import LeagueToolBelt

test_object = LeagueToolBelt()


def test_get():
    """
    Test that get-method returns a good response to a valid endpoint
    """
    result = test_object.get('/lol-platform-config/v1/initial-configuration-complete')
    assert result[0].status_code == 200

def test_get_bad_endpoint():
    """
    Test that get-method returns anything but a good response to an invalid endpoint
    """
    result = test_object.get('')
    assert result[0].status_code != 200
