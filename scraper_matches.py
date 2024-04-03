from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time 
import pandas as pd
import threading

base_url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"

def initialize_driver():
    driver = webdriver.Firefox()
    return driver

def navigate_to_page(driver, url):
    """
    Navigates to the given url page on FBref.
    """
    driver.get(url)

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
        print("Season:", season)
        
        return season
    
    except Exception as e:
        print("Error extracting season: \n", e)
        return None


def extract_match_reports(season, driver):
    """
    Extracts all the match report URLs from the scores and fixtures page,
    excluding links containing "Head to Head."
    """
    match_report_urls = []

    fictures_table = WebDriverWait(driver, 5).until(  
        EC.presence_of_element_located((By.XPATH, f'//*[@id="sched_{season}_9_1"]/tbody'))
    )

    fictures_table_rows = fictures_table.find_elements(By.TAG_NAME, 'tr')

    for row in fictures_table_rows: 
        try:
            link_element = row.find_element(By.CSS_SELECTOR, 'td[data-stat="match_report"] a')

            # Check if the link text contains "Head to Head"
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

    Args:
        driver (WebDriver): An instance of a WebDriver (e.g., Firefox driver).

    Returns:
        dict: A dictionary containing the extracted match data.
    """

    driver.get(url)

    match_data = {}

    try:
        scorebox = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]'))
        )
        stats_table = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="team_stats"]/table'))
        )
        extra_stats_div = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="team_stats_extra"]'))
        )
        stat_groups = extra_stats_div.find_elements(By.XPATH, './div')

        # Team Names
        team1_xpath = '//*[@id="content"]/div[2]/div[1]/div[1]/strong/a'
        team2_xpath = '//*[@id="content"]/div[2]/div[2]/div[1]/strong/a'
        team1 = scorebox.find_element(By.XPATH, team1_xpath).text.strip()
        team2 = scorebox.find_element(By.XPATH, team2_xpath).text.strip()

        # Score and xG
        score_team1_xpath = '//*[@id="content"]/div[2]/div[1]/div[2]/div[1]'
        score_team2_xpath = '//*[@id="content"]/div[2]/div[2]/div[2]/div[1]'
        xg_team1_xpath = '//*[@id="content"]/div[2]/div[1]/div[2]/div[2]'
        xg_team2_xpath = '//*[@id="content"]/div[2]/div[2]/div[2]/div[2]'
        score_team1 = scorebox.find_element(By.XPATH, score_team1_xpath).text
        score_team2 = scorebox.find_element(By.XPATH, score_team2_xpath).text
        xg_team1 = scorebox.find_element(By.XPATH, xg_team1_xpath).text
        xg_team2 = scorebox.find_element(By.XPATH, xg_team2_xpath).text

        # Date
        date_xpath = '//*[@id="content"]/div[2]/div[3]/div[1]/strong/a'
        date = scorebox.find_element(By.XPATH, date_xpath).text.split(',')[0].strip()

        time_xpath = '//*[@id="content"]/div[2]/div[3]/div[1]/span[1]'
        time_str = scorebox.find_element(By.XPATH, time_xpath).text.strip()

        try:
            # Officials
            officials_xpath = '//*[@id="content"]/div[2]/div[3]/div[7]/small'
            officials_text = scorebox.find_element(By.XPATH, officials_xpath).text.strip()
            officials = [official.strip() for official in officials_text.split('·')]
        except:
            # for season 2020/2021
            officials_xpath = '//*[@id="content"]/div[2]/div[3]/div[6]/small'
            officials_text = scorebox.find_element(By.XPATH, officials_xpath).text.strip()
            officials = [official.strip() for official in officials_text.split('·')]

        # Possession
        possession_team1_xpath = '//*[@id="team_stats"]/table/tbody/tr[3]/td[1]/div/div[1]/strong'
        possession_team2_xpath = '//*[@id="team_stats"]/table/tbody/tr[3]/td[2]/div/div[1]/strong'

        # Passing Accuracy
        passing_acc_team1_xpath = '//*[@id="team_stats"]/table/tbody/tr[5]/td[1]/div/div[1]/strong'
        passing_acc_team2_xpath = '//*[@id="team_stats"]/table/tbody/tr[5]/td[2]/div/div[1]/strong'

        # Shots on Target
        shots_target_team1_xpath = '//*[@id="team_stats"]/table/tbody/tr[7]/td[1]/div/div[1]/strong'
        shots_target_team2_xpath = '//*[@id="team_stats"]/table/tbody/tr[7]/td[2]/div/div[1]/strong'

        # Saves
        saves_team1_xpath = '//*[@id="team_stats"]/table/tbody/tr[9]/td[1]/div/div[1]/strong'
        saves_team2_xpath = '//*[@id="team_stats"]/table/tbody/tr[9]/td[2]/div/div[1]/strong'

        # Extract the data
        possession_team1 = stats_table.find_element(By.XPATH, possession_team1_xpath).text
        possession_team2 = stats_table.find_element(By.XPATH, possession_team2_xpath).text
        passing_acc_team1 = stats_table.find_element(By.XPATH, passing_acc_team1_xpath).text
        passing_acc_team2 = stats_table.find_element(By.XPATH, passing_acc_team2_xpath).text
        shots_target_team1 = stats_table.find_element(By.XPATH, shots_target_team1_xpath).text
        shots_target_team2 = stats_table.find_element(By.XPATH, shots_target_team2_xpath).text
        saves_team1 = stats_table.find_element(By.XPATH, saves_team1_xpath).text
        saves_team2 = stats_table.find_element(By.XPATH, saves_team2_xpath).text

        # Update the returned dictionary
        match_data['season'] = season
        match_data['date'] = date
        match_data['time'] = time_str
        match_data['team1'] = team1
        match_data['team2'] = team2
        match_data['score_team1'] = score_team1
        match_data['score_team2'] = score_team2
        match_data['xg_team1'] = xg_team1
        match_data['xg_team2'] = xg_team2
        match_data['officials'] = officials
        match_data['possession_team1'] = possession_team1
        match_data['possession_team2'] = possession_team2
        match_data['passing_acc_team1'] = passing_acc_team1
        match_data['passing_acc_team2'] = passing_acc_team2
        match_data['shots_target_team1'] = shots_target_team1
        match_data['shots_target_team2'] = shots_target_team2
        match_data['saves_team1'] = saves_team1
        match_data['saves_team2'] = saves_team2

        # Add additional stats to the dictionary
        for group in stat_groups:
            stats = group.find_elements(By.XPATH, './/div')

            for i in range(0, len(stats), 3): 
                # Ignore header elements
                if stats[i].text in [team1, team2] or stats[i].text.strip() in [' _team1', ' _team2']: 
                    continue   # Skip to the next iteration

                stat_name = stats[i + 1].text.lower()
                stat_team1 = stats[i].text  
                stat_team2 = stats[i + 2].text 

                match_data[f'{stat_name}_team1'] = stat_team1
                match_data[f'{stat_name}_team2'] = stat_team2

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


def scrape_matches(driver, base_url, num_seasons=4):
    """
    Main function to scrape match reports from FBref.
    """
    navigate_to_page(driver, base_url)
    csv_filename = f"Premier_League_Match_Stats_Last_{num_seasons}_Seasons.csv"

    for _ in range(num_seasons):
        current_season = driver.current_url
        season = get_season(driver)
        match_report_urls = extract_match_reports(season, driver)

        # Loop through the match report URLs
        for url in match_report_urls:
            match_data = extract_match_data(driver, url, season)

            print(f"Extracted data for {match_data.get('team1')} vs {match_data.get('team2')}.")

            # Check if data was extracted successfully
            if match_data:
                # Convert to DataFrame and save to CSV (appending)
                pd.DataFrame([match_data.values()], columns=match_data.keys()) \
                    .to_csv(csv_filename, mode='a', index=False, header=not os.path.exists(csv_filename))

        navigate_to_page(driver, current_season)
        click_previous_season_button(driver)

        time.sleep(2)

    print(f"Collected head to head matches for the last {num_seasons} seasons.")

# -------- Main Execution ---------

if __name__ == "__main__":
    driver = initialize_driver()
    scrape_matches(driver, base_url, num_seasons=4)
    driver.quit()
