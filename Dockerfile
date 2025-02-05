# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port (since it is not directly interacting with a web server, port selection doesn't matter much)
# We are just running the bot and not serving anything over HTTP
EXPOSE 8080

# Run the bot when the container starts
CMD ["python", "bot.py"]
