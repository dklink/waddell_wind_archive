# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Copy the necessary directories into the container
COPY ./server /waddell_wind/server
COPY ./common /waddell_wind/common

# Set the working directory inside the container to /waddell_wind
WORKDIR /waddell_wind

# Install any dependencies from the requirements.txt
RUN pip install --no-cache-dir -r server/requirements.txt

# Set environment variables
ENV FLASK_APP=server.app
ENV FLASK_ENV=production

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
