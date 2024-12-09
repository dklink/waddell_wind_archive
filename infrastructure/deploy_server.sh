#!/bin/bash

# Variables
REGION="us-central1"
SERVICE_NAME="image-server"
CONTAINER_IMAGE="gcr.io/$GC_PROJECT_ID/server:latest"
CLOUD_SQL_CONNECTION="$GC_PROJECT_ID:$REGION:$DB_INSTANCE_NAME"
DATABASE_URL="postgresql://$DB_USERNAME:$DB_PASSWORD@/$DB_NAME?host=/cloudsql/$CLOUD_SQL_CONNECTION"

# Check if the Cloud Run service exists
if gcloud run services describe $SERVICE_NAME --region=$REGION &>/dev/null; then
  echo "Cloud Run service '$SERVICE_NAME' already exists. Skipping creation."
else
  # Deploy Cloud Run service
  echo "Creating Cloud Run service '$SERVICE_NAME'..."
  gcloud run deploy $SERVICE_NAME \
    --image $CONTAINER_IMAGE \
    --region $REGION \
    --set-env-vars="DATABASE_URL=$DATABASE_URL,GC_PROJECT_ID=$GC_PROJECT_ID,GCS_BUCKET_NAME=$GCS_BUCKET_NAME" \
    --set-cloudsql-instances $CLOUD_SQL_CONNECTION \
    --allow-unauthenticated \
    --ingress all
  echo "Server deployment completed."
fi