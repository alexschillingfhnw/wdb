# Web Datenbeschaffung - Premier League Data Extraction

## Overview
This repository is dedicated to the extraction and analysis of football data, specifically focusing on player and match statistics from the Premier League over the past several seasons. Utilizing Python and Selenium, this project aims to gather detailed data to drive insightful analytics and visualization.

The data is sourced from [FBref.com](https://fbref.com), a comprehensive football statistics website, ensuring a rich dataset that encompasses various aspects of player performances and match outcomes.

## Contents
- **data/**: A directory where scraped data files are stored.
- **.gitignore**: Specifies intentionally untracked files that Git should ignore.
- **Peer-Review-Concept-FS23.pdf**: Details the objectives of the mini challenge and the criteria that should be followed for peer review.
- **README.md**: Provides an overview of the project, setup instructions, and additional information.
- **eda.ipynb**: Contains exploratory data analysis on the collected Premier League data, offering initial insights and visualizations of player and match statistics.
- **helper.py**: Includes Python functions that assist with data cleaning and plotting for analysis.
- **scraper_matches.py**: Python script for scraping match statistics from FBref.com.
- **scraper_players.py**: Python script for scraping player statistics from FBref.com.
- **requirements.txt**: Includes all dependencies used for the scripts.
- **dockerfile**: Docker configuration for setting up the environment and running the scripts.

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

This README includes comprehensive setup and running instructions, making it easy for others to get the project up and running on their machines. It integrates the Docker setup into the project workflow, simplifying the process of data collection and analysis.



