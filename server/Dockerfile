# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory inside the container to /waddell_wind
WORKDIR /waddell_wind

# Copy the requirements.txt file into the container
COPY requirements.txt /waddell_wind/

# Install any dependencies from the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container, excluding the ones specified in .dockerignore
COPY . /waddell_wind/

# Set environment variables
ENV FLASK_APP=src.app.server
ENV FLASK_ENV=production

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
