# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /wdb

# Copy the current directory contents into the container at /usr/src/app
COPY . /wdb

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Firefox
RUN apt-get update \
    && apt-get install -y firefox-esr wget

# Install GeckoDriver
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz" \
    && tar -xzf geckodriver-v0.30.0-linux64.tar.gz -C /usr/local/bin \
    && rm geckodriver-v0.30.0-linux64.tar.gz

# Run scraper scripts to download the data when the container launches
CMD python ./scraper_matches.py && python ./scraper_players.py