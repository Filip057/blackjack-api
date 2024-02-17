# Use an official Python runtime as a parent image
FROM python:3.10

# Ensures Python output is sent straight to terminal without being buffered
ENV PYTHONUNBUFFERED=1

# Sets the container's working directory to /app
WORKDIR /app

# Install system dependencies required by mysqlclient and other packages
RUN apt-get update \
  && apt-get install python3-dev default-libmysqlclient-dev gcc -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install pipenv
RUN pip install --upgrade pip \
  && pip install pipenv

# Copy the Pipfile and Pipfile.lock into the image
COPY Pipfile Pipfile.lock /app/

# Install application dependencies with pipenv
# The --system flag installs dependencies system-wide; --deploy fails the build if the lockfile is out of date
# --ignore-pipfile ignores the Pipfile for installation and uses the lock file
RUN pipenv install --system --deploy --ignore-pipfile

# Copy the rest of your application's code into the image
COPY . /app/

# Expose port 8000 to be accessible from the host
EXPOSE 8000
