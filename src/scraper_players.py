from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import os
import pandas as pd

def initialize_driver():
    driver = webdriver.Firefox()
    return driver


def navigate_to_page(driver, url):
    """
    Navigates to a given page on FBref.
    """
    driver.get(url)


def click_accept_cookies_button(driver):
    """
    Clicks the accept cookies button on the page.
    """
    try:
        accept_cookies_button = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]'))
        )
        accept_cookies_button.click()

    except Exception as e:
        print("Error clicking accept cookies button: \n", e)


def get_season(driver):
    """
    Extracts the season from the page and saves it as a string.
    """
    try:
        h1_element = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="meta"]/div[2]/h1'))
        )

        season_text = h1_element.text
        season = season_text.split(" ")[0]
        print("------\nSeason:", season)
        
        return season
    
    except Exception as e:
        print("Error extracting season: \n", e)
        return None


def extract_player_stats(driver, team_name):
    """
    Extracts player statistics from a given table.
    """
    player_data = []

    try:
        stats_table = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="stats_standard_9"]/tbody' ))
        )

        header_row  = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="stats_standard_9"]/thead/tr[2]')) 
        )

        headers = [th.text for th in header_row.find_elements(By.TAG_NAME, 'th')]
        player_rows = stats_table.find_elements(By.TAG_NAME, 'tr')

        # Gather player data from each table row
        for row in player_rows:
            player_name = row.find_element(By.TAG_NAME, 'th').text
            player_stats = row.find_elements(By.TAG_NAME, 'td')
            player_data.append([player_name] + [cell.text for cell in player_stats]) 

        print(team_name, "player stats extracted.")

    except Exception as e:
        print("Error extracting player stats: \n", e)   

    return headers, player_data


def extract_teams(driver, season):
    """
    Extracts team names and urls from the Premier League table.
    """
    teams = []

    try:
        league_table_body = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, f'//*[@id="results{season}91_overall"]/tbody'))
        )
        team_rows = league_table_body.find_elements(By.TAG_NAME, 'tr')

        # Gather team names and urls from each table row
        for row in team_rows:
            url_element = row.find_element(By.CSS_SELECTOR, 'td[data-stat="team"] a')
            team_url = url_element.get_attribute('href')
            team_name = url_element.text
            teams.append([team_name, team_url])

        print("Found all team names and urls from league table.")

    except Exception as e:
        print("Error extracting team names and urls from league table: \n", e)

    return teams


def process_team_data(driver, season, team_name, team_url):
    """
    Processes player data for a given team. Collects player stats for the given season and adds season and team as columns.
    """
    driver.get(team_url)
    headers, player_data = extract_player_stats(driver, team_name)

    # Add season and team as a column
    headers.insert(0, 'Season')
    headers.insert(1, 'Team')

    # Add corresponding season and team name to the new columns
    for data in player_data:
        data.insert(0, season)
        data.insert(1, team_name)

    return team_name, headers, player_data


def click_previous_season_button(driver):
    """
    Clicks the previous season button to navigate to the previous season's data to continue data extraction.
    """
    passed = False

    try:
        prev_season_button = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[1]/div[2]/div/a'))
        )
        prev_season_button.click()
        passed = True

    except Exception:
        print("Error clicking previous season button")

    if not passed:
        try:
            prev_season_button = WebDriverWait(driver, 2).until( 
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[1]/div[2]/div/a[1]'))
            )
            prev_season_button.click()

        except Exception:
            print("Error clicking previous season button")


def scrape_multiple_seasons(driver, num_seasons=4):
    """
    Scrapes player data for n=num_seasons seasons and saves all the data to a csv file.
    """
    all_seasons_data = pd.DataFrame()

    for _ in range(num_seasons):
        current_season_page = driver.current_url
        season = get_season(driver)
        teams = extract_teams(driver, season)

        for team_name, team_url in teams:
            team_name, headers, player_data = process_team_data(driver, season, team_name, team_url)
            all_seasons_data = pd.concat([all_seasons_data, pd.DataFrame(player_data, columns=headers)])
        
        navigate_to_page(driver, current_season_page)
        click_previous_season_button(driver)

        time.sleep(1)

    # After all seasons are processed, save the combined data
    csv_filename = f"Premier_League_Player_Stats_Last_{num_seasons}_Seasons.csv"

    data_directory = "data"  # Change this to the name of your data directory if it's different
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "..", data_directory, csv_filename)
    all_seasons_data.to_csv(csv_path, index=False)
    print(f"Player stats for the last {num_seasons} seasons saved to {csv_path}")

# -------- Main Execution ---------
if __name__ == "__main__":
    base_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    driver = initialize_driver()
    navigate_to_page(driver, base_url)
    click_accept_cookies_button(driver)
    scrape_multiple_seasons(driver, num_seasons=6)
    driver.quit()
