from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time 
import pandas as pd


def initialize_driver():
    driver = webdriver.Firefox()
    return driver


def navigate_to_page(driver, url):
    """
    Navigates to the given url page on FBref.
    """
    driver.get(url)


def click_accept_cookies_button(driver):
    """
    Clicks the decline cookies button on the page.
    """
    try:
        decline_cookies_button = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/button[2]'))
        )
        decline_cookies_button.click()

    except Exception as e:
        print("Error clicking decline cookies button: \n", e)


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


def extract_match_reports(season, driver):
    """
    Extracts all the match report URLs from the scores and fixtures page, excluding links containing "Head to Head."
    """
    match_report_urls = []

    fictures_table = WebDriverWait(driver, 5).until(  
        EC.presence_of_element_located((By.XPATH, f'//*[@id="sched_{season}_9_1"]/tbody'))
    )

    fictures_table_rows = fictures_table.find_elements(By.TAG_NAME, 'tr')

    # Extract match report url from each table row
    for row in fictures_table_rows: 
        try:
            link_element = row.find_element(By.CSS_SELECTOR, 'td[data-stat="match_report"] a')

            # Check if the link text contains "Head to Head" -> skip
            if "Head-to-Head" not in link_element.text:
                match_report_url = link_element.get_attribute('href')
                match_report_urls.append(match_report_url)
        except Exception as e:
            pass  # No match report link in this row

    print(f"Extracted {len(match_report_urls)} match reports.")

    return match_report_urls


def extract_match_data(driver, url, season):
    """
    Extracts the two team names, score, xG, date, and officials from the match report's scorebox using Selenium.
    """

    driver.get(url)

    try:
        scorebox = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]'))
        )
        stats_table = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="team_stats"]/table'))
        )
        extra_stats_div = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="team_stats_extra"]'))
        )
        stat_divs = extra_stats_div.find_elements(By.XPATH, './div')

        date = scorebox.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[3]/div[1]/strong/a').text.split(',')[0].strip()
        time_str = scorebox.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[3]/div[1]/span[1]').text.strip()
        team1 = scorebox.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div[1]/strong/a').text.strip()
        team2 = scorebox.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div[1]/strong/a').text.strip()
        score_team1 = scorebox.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div[2]/div[1]').text
        score_team2 = scorebox.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div[2]/div[1]').text
        xg_team1 = scorebox.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div[2]/div[2]').text
        xg_team2 = scorebox.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div[2]/div[2]').text

        try:
            officials_xpath = '//*[@id="content"]/div[2]/div[3]/div[7]/small'
            officials_text = scorebox.find_element(By.XPATH, officials_xpath).text.strip()
            officials = [official.strip() for official in officials_text.split('·')]
        except:
            officials_xpath = '//*[@id="content"]/div[2]/div[3]/div[6]/small'
            officials_text = scorebox.find_element(By.XPATH, officials_xpath).text.strip()
            officials = [official.strip() for official in officials_text.split('·')]

        possession_team1 = stats_table.find_element(By.XPATH, '//*[@id="team_stats"]/table/tbody/tr[3]/td[1]/div/div[1]/strong').text
        possession_team2 = stats_table.find_element(By.XPATH, '//*[@id="team_stats"]/table/tbody/tr[3]/td[2]/div/div[1]/strong').text
        passing_acc_team1 = stats_table.find_element(By.XPATH, '//*[@id="team_stats"]/table/tbody/tr[5]/td[1]/div/div[1]/strong').text
        passing_acc_team2 = stats_table.find_element(By.XPATH, '//*[@id="team_stats"]/table/tbody/tr[5]/td[2]/div/div[1]/strong').text
        shots_target_team1 = stats_table.find_element(By.XPATH, '//*[@id="team_stats"]/table/tbody/tr[7]/td[1]/div/div[1]/strong').text
        shots_target_team2 = stats_table.find_element(By.XPATH, '//*[@id="team_stats"]/table/tbody/tr[7]/td[2]/div/div[1]/strong').text
        saves_team1 = stats_table.find_element(By.XPATH, '//*[@id="team_stats"]/table/tbody/tr[9]/td[1]/div/div[1]/strong').text
        saves_team2 = stats_table.find_element(By.XPATH, '//*[@id="team_stats"]/table/tbody/tr[9]/td[2]/div/div[1]/strong').text

        data = [season, date, time_str, team1, team2, score_team1, score_team2, xg_team1, xg_team2, officials, possession_team1, 
                possession_team2, passing_acc_team1, passing_acc_team2, shots_target_team1, shots_target_team2, saves_team1, saves_team2
        ]
        keys = ['season', 'date', 'time', 'team1', 'team2', 'score_team1', 'score_team2', 'xg_team1', 'xg_team2', 'officials', 'possession_team1', 
                'possession_team2', 'passing_acc_team1', 'passing_acc_team2', 'shots_target_team1', 'shots_target_team2', 'saves_team1', 'saves_team2'
        ]
        match_data = dict(zip(keys, data))

        for div in stat_divs:
            stats = div.find_elements(By.XPATH, './/div')
            for i in range(0, len(stats), 3):  # Adjust loop to ensure correct indexing
                stat_name = stats[i + 1].text.lower().replace(' ', '_')  # Central element for stat name
                match_data[f'{stat_name}_team1'] = stats[i].text
                match_data[f'{stat_name}_team2'] = stats[i + 2].text

        return match_data

    except Exception as e:
        print("Error: Match data elements not found on the page.\n", e)
        return {}  # Empty dictionary if data not found


def click_previous_season_button(driver):
    try:
        prev_season_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="meta"]/div[2]/div/a'))
        )
        prev_season_button.click()

    except Exception as e:
        print("Error clicking previous season button: \n", e)


def scrape_matches(driver, num_seasons=4):
    """
    Main function to scrape match reports from FBref.
    """
    data_directory = "data"
    csv_filename = f"Premier_League_Match_Stats_Last_{num_seasons}_Seasons.csv"

    for _ in range(num_seasons):
        current_season = driver.current_url
        season = get_season(driver)
        match_report_urls = extract_match_reports(season, driver)

        # Loop through the match report URLs to extract data from each match
        for url in match_report_urls:
            match_data = extract_match_data(driver, url, season)

            print(f"Extracted data for {match_data.get('team1')} vs {match_data.get('team2')}.")

            # Check if data was extracted successfully
            if match_data:
                # Convert to DataFrame and save to CSV
                csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", data_directory, csv_filename)
                pd.DataFrame([match_data.values()], columns=match_data.keys()) \
                    .to_csv(csv_path, mode='a', index=False, header=not os.path.exists(csv_path))

        navigate_to_page(driver, current_season)
        click_previous_season_button(driver)

        time.sleep(3)

    print(f"Collected head to head matches for the last {num_seasons} seasons.")


# -------- Main Execution ---------
if __name__ == "__main__":
    base_url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
    driver = initialize_driver()
    navigate_to_page(driver, base_url)
    click_accept_cookies_button(driver)
    scrape_matches(driver, num_seasons=6)
    driver.quit()
