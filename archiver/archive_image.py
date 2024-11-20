# An archive script for a web image link.
# Pulls the latest image, persists it in local filesystem,
#  and writes metadata to a postgresql database.
# Assumes database has already been initialized and migrated.

import os
import sys
from datetime import datetime, timezone
from multiprocessing import Value
from pathlib import Path

import requests

sys.path.append("../common")

from common.database import SessionLocal
from common.models import Images

LIVE_WADDELL_WIND_URL = "https://mapper.weatherflow.com/cgi-bin/tinyGv2Wap.gif?t=213&d=t&c=0&cb=41741&wid=1&width=900&height=220&sh=0&eh=23"


def archive_image():
    # 1. download image to local filesystem
    img_data = requests.get(LIVE_WADDELL_WIND_URL).content
    archived_at = datetime.now(timezone.utc)
    print(f"Image successfully downloaded at timestamp {archived_at.timestamp()}")

    filename = f"{int(archived_at.timestamp())}.gif"
    save_image(img_data=img_data, filename=filename)

    # 2. write metadata into DB
    with SessionLocal() as session:
        new_image = Images(
            archived_at=archived_at,
            filename=filename,
        )
        session.add(new_image)
        session.commit()

        print(f"New image metadata added to DB with ID: {new_image.id}")


def save_image(img_data, filename):
    storage_type = os.environ["IMAGE_STORE_TYPE"]
    if storage_type == "gcs":
        save_image_to_gcloud(img_data=img_data, filename=filename)
    elif storage_type == "local":
        save_image_to_local_store(img_data=img_data, filename=filename)
    else:
        raise ValueError(f"Unsupported IMAGE_STORE_TYPE: {storage_type}")


def save_image_to_gcloud(img_data, blob_name):
    # Get bucket name from environment variable
    bucket_name = os.getenv("IMAGE_STORE")

    # Initialize the Google Cloud Storage client and bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Upload image data directly to Google Cloud Storage
    blob.upload_from_string(img_data, content_type="image/gif")

    print(f"File uploaded to {bucket_name}/{blob_name}")


def save_image_to_local_store(img_data, filename):
    IMAGE_STORE_PATH = Path(os.environ["IMAGE_STORE_PATH"])
    if not IMAGE_STORE_PATH.exists():
        IMAGE_STORE_PATH.mkdir(parents=True)
    img_path = IMAGE_STORE_PATH / filename
    with open(img_path, "wb") as handler:
        handler.write(img_data)
    print(f"Image successfully written to disk at {img_path}")


if __name__ == "__main__":
    archive_image()
