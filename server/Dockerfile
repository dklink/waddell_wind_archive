# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Install requirements
COPY ./server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the necessary directories into the container
COPY ./server /waddell_wind/server
COPY ./common /waddell_wind/common

# Set the working directory inside the container to /waddell_wind
WORKDIR /waddell_wind

# Set environment variables
ENV FLASK_APP=server.app
ENV FLASK_ENV=production

# Run the Flask application
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=$PORT"]
