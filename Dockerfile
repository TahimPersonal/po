# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port for the Flask server (health check)
EXPOSE 5000

# Run the bot when the container starts
CMD ["python", "bot.py"]
