# Use Python 3.13 slim image
FROM python:3.13-slim

# Copy the necessary directories into the container
COPY ./archiver /waddell_wind/archiver
COPY ./common /waddell_wind/common

# Set the working directory inside the container
WORKDIR /waddell_wind

# Install Python dependencies
RUN pip install --no-cache-dir -r archiver/requirements.txt

# Set the default command to run the archive_image.py script
CMD ["python", "-m", "archiver.archive_image"]
