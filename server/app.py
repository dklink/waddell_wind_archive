import base64
import io
import os
from datetime import datetime, timezone

from flask import Flask, abort, jsonify, request, send_file
from google.cloud import storage
from sqlalchemy import func

from common.database import SessionLocal
from common.models import Images

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    # Allow requests from your frontend domain (or all origins with *)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/images/nearest", methods=["GET"])
def get_nearest_image():
    """
    Retrieve the image nearest to a given timestamp.

    This endpoint accepts a timestamp as a query parameter and returns metadata
    for the image archived closest to the specified timestamp. If the timestamp
    is missing, invalid, or no images are found, appropriate error messages are returned.

    Query Parameters:
    -----------------
    timestamp : float (required)
        The Unix timestamp (in seconds) to find the nearest image.

    Returns:
        The image file or an appropriate error message
    """
    # Get the 'timestamp' query parameter
    timestamp = request.args.get("timestamp")
    if not timestamp:
        abort(400, "Missing 'timestamp' query parameter")

    try:
        # Convert the input timestamp to a datetime object
        target_time = datetime.fromtimestamp(float(timestamp), tz=timezone.utc)
    except ValueError:
        abort(400, description="Invalid timestamp format. Use a Unix timestamp.")

    nearest_image = get_nearest_image_from_db(target_time=target_time)
    image_archival_timestamp = nearest_image.archived_at.timestamp()
    image_data = read_image_from_gcloud(blob_name=nearest_image.filename)
    encoded_image = base64.b64encode(image_data).decode("utf-8")

    return jsonify(
        {
            "image_archival_timestamp": image_archival_timestamp,
            "image_data_base64": encoded_image,
        }
    )


def get_nearest_image_from_db(target_time: datetime):
    with SessionLocal() as session:
        nearest_image = (
            session.query(Images)
            .order_by(
                func.abs(func.extract("epoch", Images.archived_at - target_time))
            )  # Convert interval to seconds to allow use of ABS
            .first()
        )
        if not nearest_image:
            abort(404, description="No images found in the database.")
        return nearest_image


def read_image_from_gcloud(blob_name: str):
    # Get bucket name from environment variable
    project_id = os.environ["GC_PROJECT_ID"]
    bucket_name = os.environ["GCS_BUCKET_NAME"]

    # Initialize the Google Cloud Storage client and bucket
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    if not blob.exists():
        abort(404, description=f"Image file not found in the bucket.")

    content = blob.download_as_bytes()

    return content


if __name__ == "__main__":
    app.run()
