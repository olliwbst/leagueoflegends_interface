import unittest
from app.league_scrapper import LeagueToolBelt


class TestBasic(unittest.TestCase):
    def test_set_initial_data_complete(self):
        """
        Test that initial data is set completely
        """
        test_object = LeagueToolBelt()
        self.assertIsNotNone(test_object.install_dir)
        self.assertIsNotNone(test_object.port)
        self.assertIsNotNone(test_object.auth)
        self.assertIsNotNone(test_object.version)


if __name__ == '__main__':
    unittest.main()
