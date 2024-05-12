# Use an official Python runtime as a parent image
FROM selenium/standalone-firefox:latest

# Set the working directory in the container
WORKDIR /wdb

# Copy the current directory contents into the container at /usr/src/app
COPY . /wdb

RUN sudo apt-get update && sudo apt-get install -y python3-pip

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r /wdb/requirements.txt

# Navigate to the src folder
WORKDIR /wdb/src

# Run scraper scripts to download the data when the container launches
CMD python3 ./scraper_matches.py && python3 ./scraper_players.py && \
    jupyter nbconvert --execute /wdb/src/eda.ipynb --to notebook --output /wdb/src/eda_output.ipynb --ExecutePreprocessor.timeout=-1