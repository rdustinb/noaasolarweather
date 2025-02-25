# Use Python
FROM python:3.13.2-slim

################################################################################
# Using security best-practices, avoiding using the root user
# 
# Everything after this point will use the regular user 'noaauser' and install
# any needed packages in a python virtual environment
################################################################################
# Create a custom user with UID 1001 and GID 1001
RUN groupadd -g 1001 noaausers && \
    useradd -m -u 1001 -g noaausers noaauser
 
# Switch to the custom user
USER noaauser
 
# Set the workdir
WORKDIR /home/noaauser

# Create a virtual environment for python
RUN python3 -m venv /home/noaauser/.venv_noaa

# Set the virtual environment at the beginning of the PATH
# No more sourcing the activate tool is needed, the path is modified from here on out...
ENV PATH="/home/noaauser/.venv_noaa/bin:$PATH"

# Install dependencies:
COPY docker/requirements.txt /home/noaauser/requirements.txt

RUN pip install --no-cache-dir -r /home/noaauser/requirements.txt

# Copy the source into the Docker container
RUN mkdir -p /home/noaauser/noaasolarweather
COPY src /home/noaauser/noaasolarweather

WORKDIR /home/noaauser/noaasolarweather

CMD ["gunicorn", "-w", "1", "-b", ":8000", "view_agent:server"]
