# An archive script for a web image link.
# Pulls the latest image, persists it in local filesystem,
#  and writes metadata to a postgresql database.
from launch_db import launch_postgres

# 1. launch the Postgres app, to start the db if not running
launch_postgres()

# 2. download image to local filesystem

# 3. write metadata into DB
