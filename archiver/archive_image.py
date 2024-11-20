# An archive script for a web image link.
# Pulls the latest image, persists it in local filesystem,
#  and writes metadata to a postgresql database.
# Assumes database has already been initialized and migrated.

import os
import sys
from datetime import datetime, timezone

import requests
from google.cloud import storage

sys.path.append("../common")

from common.database import SessionLocal
from common.models import Images

LIVE_WADDELL_WIND_URL = "https://mapper.weatherflow.com/cgi-bin/tinyGv2Wap.gif?t=213&d=t&c=0&cb=41741&wid=1&width=900&height=220&sh=0&eh=23"


def archive_image():
    # 1. download image data to local variable
    img_data = requests.get(LIVE_WADDELL_WIND_URL).content
    archived_at = datetime.now(timezone.utc)
    print(f"Image successfully downloaded at timestamp {archived_at.timestamp()}")

    # 2. upload image to google cloud storage
    filename = f"{int(archived_at.timestamp())}.gif"
    save_image_to_gcloud(img_data=img_data, blob_name=filename)

    # 3. write metadata into DB
    with SessionLocal() as session:
        new_image = Images(
            archived_at=archived_at,
            filename=filename,
        )
        session.add(new_image)
        session.commit()

        print(f"New image metadata added to DB with ID: {new_image.id}")


def save_image_to_gcloud(img_data, blob_name):
    # Get bucket name from environment variable
    project_id = os.environ["GC_PROJECT_ID"]
    bucket_name = os.environ["GCS_BUCKET_NAME"]

    # Initialize the Google Cloud Storage client and bucket
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Upload image data directly to Google Cloud Storage
    blob.upload_from_string(img_data, content_type="image/gif")

    print(f"File uploaded to {bucket_name}/{blob_name}")


if __name__ == "__main__":
    archive_image()
