import unittest
from app.league_scrapper import LeagueToolBelt

test_object = LeagueToolBelt()


class TestBasic(unittest.TestCase):
    def test_get(self):
        """
        Test that get-method returns a good response to a valid endpoint
        """
        result = test_object.get('/lol-platform-config/v1/initial-configuration-complete')
        self.assertEqual(result[0].status_code, 200)

    def test_get_bad_endpoint(self):
        """
        Test that get-method returns anything but a good response to an invalid endpoint
        """
        result = test_object.get('')
        self.assertNotEqual(result[0].status_code, 200)

    def test_get_no_endpoint(self):
        """
        Test that get-method throws a TypeError Exception when given no endpoint
        """
        with self.assertRaises(TypeError):
            test_object.get()


if __name__ == '__main__':
    unittest.main()
