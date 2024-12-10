#!/bin/bash

# Check if the API_URL argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <API_URL>"
  exit 1
fi

API_URL=$1
FRONTEND_PATH="frontend/basic.html"

# Replace the placeholder {{API_URL}} with the actual URL
echo "Injecting API URL into the HTML..."
sed "s|{{API_URL}}|$API_URL|" $FRONTEND_PATH > frontend/url_injected.html

echo "Uploading to GCS bucket..."
gcloud storage cp frontend/url_injected.html gs://$FRONTEND_BUCKET_NAME/basic.html
rm frontend/url_injected.html
echo "Upload complete."
