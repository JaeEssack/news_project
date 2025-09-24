# Use an official Python runtime as a parent image
# This is our base image
FROM python:3.11-slim

# Set the working directory in the container
# All subsequent commands will be run from this directory
WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install any dependencies
# The --no-cache-dir flag prevents pip from storing cached wheels, saving space
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your Django project into the working directory
COPY . .

# Expose the port that Django will run on
EXPOSE 8000

# Run the command to start the Django server
# The 0.0.0.0 host allows the app to be accessible outside the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]