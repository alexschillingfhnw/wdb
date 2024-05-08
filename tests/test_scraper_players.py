import unittest
from unittest.mock import MagicMock, patch
from src.scraper_players import initialize_driver, scrape_multiple_seasons


class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.driver = initialize_driver()
        self.base_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

    def tearDown(self):
        self.driver.quit()

    def test_scrape_multiple_seasons(self):
        # Mocking dependent functions
        with patch('src.scraper_players.get_season') as mock_get_season, \
             patch('src.scraper_players.extract_teams') as mock_extract_teams, \
             patch('src.scraper_players.process_team_data') as mock_process_team_data, \
             patch('src.scraper_players.navigate_to_page') as mock_navigate_to_page, \
             patch('src.scraper_players.click_previous_season_button') as mock_click_previous_season_button:

            # Mocking return values of dependent functions
            mock_get_season.return_value = "2023/2024"
            mock_extract_teams.return_value = [("Team1", "url1"), ("Team2", "url2")]
            mock_process_team_data.side_effect = [("Team1", ["header1", "header2"], [["data1", "data2"]]),
                                                  ("Team2", ["header1", "header2"], [["data3", "data4"]])]
            scrape_multiple_seasons(self.driver, num_seasons=1)

            # Asserting that dependent functions were called
            mock_navigate_to_page.assert_called_once()
            mock_get_season.assert_called_once()
            mock_extract_teams.assert_called_once()
            mock_process_team_data.assert_any_call(self.driver, "2023/2024", "Team1", "url1")
            mock_process_team_data.assert_any_call(self.driver, "2023/2024", "Team2", "url2")
            mock_click_previous_season_button.assert_called_once()


if __name__ == '__main__':
    unittest.main()