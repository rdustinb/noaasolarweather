# Use Python!
FROM python:3.13.2-slim

# Create a working directory in the docker container's 'home' folder
RUN mkdir -p /home/noaa/noaasolarweather

WORKDIR /home/noaa/noaasolarweather

# Using Layered approach for the installation of requirements
COPY requirements.txt /home/noaa/noaasolarweather/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy files to the container directory
COPY . /home/noaa/noaasolarweather

# Run the initial data fetch
RUN python data_agent_master.py

# Run the app in gunicorn
#CMD gunicorn -b 0.0.0.0:80 view_agent:server
# This is being put in the docker compose file along with nginx. Is nginx required?
# Let's try to build this docker image here and run it without the docker compose file and see what happens...
CMD gunicorn -w 1 -b :8000 view_agent:server
