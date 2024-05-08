# Web Datenbeschaffung - Premier League Data Extraction

## Overview
This repository is dedicated to the extraction and analysis of football data, specifically focusing on player and match statistics from the Premier League over the past several seasons. Utilizing Python and Selenium, this project aims to gather detailed data to drive insightful analytics and visualization.

The data is sourced from [FBref.com](https://fbref.com), a comprehensive football statistics website, ensuring a rich dataset that encompasses various aspects of player performances and match outcomes.

## Contents
- **src/**: Contains all the source code for the project.
  - `scraper_matches.py`: Python script for scraping match statistics from FBref.com.
  - `scraper_players.py`: Python script for scraping player statistics from FBref.com.
  - `helper.py`: Includes Python functions that assist with data cleaning and plotting for analysis.
  - `eda.ipynb`: Jupyter notebook containing exploratory data analysis that offers initial insights and visualizations of player and match statistics.
- **docs/**: Contains documentation related to the project.
  - `Peer-Review-Concept-FS23.pdf`: Details the objectives of the mini challenge and the criteria that should be followed for peer review.
- **tests/**: Directory for test scripts to verify the functionality of the source code.
  - `test_scrapers.py`: Example test file for testing the scraping scripts.
- **data/**: A directory where scraped data files are stored.
- **Dockerfile**: Configuration file for Docker that sets up the environment and runs the scripts.
- **requirements.txt**: Lists all dependencies required by the project.
- **.gitignore**: Specifies intentionally untracked files that Git should ignore.

---

## Installation
Before running the project, make sure you have Docker installed on your machine. If not, follow the instructions here to install Docker: [Get Docker](https://docs.docker.com/get-docker/).

### Building the Docker Image
Navigate to the project directory and build the Docker image using the following command:
```bash
docker build -t premier-league-data-scraper .
```
This command builds a Docker image named `premier-league-data-scraper` based on the instructions in the `Dockerfile`.

### Running the Docker Container
Once the image is built, run the container using:
```bash
docker run premier-league-data-scraper
```
This command starts the container where the scraping scripts are executed sequentially to collect data on match and player statistics from the Premier League.

## Usage
- **Data Collection**: The `scraper_matches.py` and `scraper_players.py` scripts will run automatically when the Docker container starts, scraping data from FBref.com.
- **Data Analysis**: After data collection, run the Jupyter notebook for exploratory data analysis:
  ```bash
  jupyter notebook eda.ipynb
  ```
  Ensure that you have Jupyter installed, or use JupyterLab within Docker if preferred.
  
---

## Why This is a Useful Project

This project makes it easier to understand football by collecting data about Premier League matches and players using automated tools. It focuses on specific statistics that aren't usually highlighted, providing a different perspective that can be useful for anyone interested in football tactics and player performance.

### Additional Information

**Practical Applications:** The insights from this project are helpful for several areas such as team strategy, scouting, managing fantasy football teams, and writing about football. These insights are designed to help make informed decisions in these areas.

**Future Plans:** There are plans to include cloud technologies to enhance the project. This might allow us to get even more detailed information and provide automated reports.

**Ease of Use:** The project uses scripts that automatically collect and analyze data, which means you don't need to do the heavy lifting. This could be especially handy for people who need regularly updated football data.

**Accessibility:** The project is set up in a way that can be expanded or adapted to other leagues or sports in the future, showing its flexibility.

---
