# Use Python!
FROM python:3.13.2-slim

# Using Layered approach for the installation of requirements
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copy files to your container
COPY . ./

# Run the app in gunicorn
CMD gunicorn -b 0.0.0.0:80 view_agent:server
