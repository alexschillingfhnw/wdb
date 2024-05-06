import pandas as pd
import numpy as np
import re

def clean_minutes(min_str):
    """
    Removes commas, converts to integer, and handles NaN values.
    """
    if pd.isna(min_str):  # Check for NaN
        return min_str  # Return NaN as is
    return int(min_str.replace(',', ''))

def remove_lowercase(text):
    for i in range(len(text)):
        if text[i].isupper():  # Find the first uppercase letter
            return text[i:]  # Return the string from that point onwards
    return np.NaN  # If no uppercase letters are found, return NA

def extract_year(age_str):
    """
    Extracts the year from the age string, handling NaN values.
    """
    if pd.isna(age_str):  # Check for NaN
        return age_str  # Return NaN as is
    return int(age_str.split('-')[0])

def determine_year(row):
    """
    Determine the year of the match based on the month and the season.
    """
    season_start, season_end = row['season'].split('-')
    month = row['date'].split(" ")[1]
    if month in ["January", "February", "March", "April", "May"]:
        year = season_end
    else:
        year = season_start
    return year

def str_to_list(officials_str):
    """
    Converts a string representation of a list to an actual list.
    """
    try:
        officials_list = eval(officials_str)
    except:
        officials_list = []
    return officials_list

def extract_officials(officials_str):
    """
    Extracts the officials from the string representation and assigns them to separate columns.
    """
    officials_list = str_to_list(officials_str)
    officials_dict = {'Referee': None, 'AR1': None, 'AR2': None, '4th': None, 'VAR': None}
    for official in officials_list:
        match = re.match(r"(.*) \((.*?)\)", official)
        if match:
            name, role = match.groups()
            if role in officials_dict:
                officials_dict[role] = name
    return pd.Series(officials_dict)

def convert_percentage_to_float(df, columns):
    """
    Converts percentage strings to floats in the specified columns.
    """
    for column in columns:
        # Remove the percentage sign and convert to float
        df[column] = df[column].str.replace('%', '', regex=False).str.strip()
        # Convert to numeric, setting errors to 'coerce' to handle non-numeric values gracefully
        df[column] = pd.to_numeric(df[column], errors='coerce') / 100