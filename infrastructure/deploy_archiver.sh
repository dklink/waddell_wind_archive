#!/bin/bash

# Variables
REGION="us-central1"
JOB_NAME="image-archiver"
TRIGGER_NAME="image-archiver-trigger"
CONTAINER_IMAGE="gcr.io/$GC_PROJECT_ID/archiver:latest"
CLOUD_SQL_CONNECTION="$GC_PROJECT_ID:$REGION:$DB_INSTANCE_NAME"
DATABASE_URL="postgresql://$DB_USERNAME:$DB_PASSWORD@/$DB_NAME?host=/cloudsql/$CLOUD_SQL_CONNECTION"


# Create Cloud Run Job
if gcloud run jobs describe $JOB_NAME --region=$REGION &>/dev/null; then
  echo "Cloud Run job '$JOB_NAME' already exists. Skipping creation."
else
  echo "Creating Cloud Run job '$JOB_NAME'..."
  gcloud run jobs create $JOB_NAME \
    --image $CONTAINER_IMAGE \
    --region $REGION \
    --set-env-vars="DATABASE_URL=$DATABASE_URL,GC_PROJECT_ID=$GC_PROJECT_ID,GCS_BUCKET_NAME=$GCS_BUCKET_NAME" \
    --set-cloudsql-instances $CLOUD_SQL_CONNECTION
fi


# Schedule Cloud Run Job (half-hourly trigger)
if gcloud scheduler jobs describe $TRIGGER_NAME --location=$REGION &>/dev/null; then
  echo "Cloud Scheduler job '$TRIGGER_NAME' already exists. Skipping creation."
else
  echo "Creating Cloud Scheduler job '$TRIGGER_NAME'..."
  # Get the default Compute Engine service account
  DEFAULT_COMPUTE_SA=$(gcloud iam service-accounts list \
    --filter="displayName:Compute Engine default service account" \
    --format="value(email)")
  gcloud scheduler jobs create http $TRIGGER_NAME \
    --schedule="*/30 * * * *" \
    --uri="https://$REGION-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/$GC_PROJECT_ID/jobs/$JOB_NAME:run" \
    --http-method POST \
    --oauth-service-account-email $DEFAULT_COMPUTE_SA \
    --location=$REGION
fi
