# README

## Installation
The following instructions are for setting up these apps in a Google Cloud environment.
### Requirements
Python 3.13 recommended.  For setup, we'll need to set up a minimal dev environment:
```
python -m venv venv_dev
source venv_dev/bin/activate
pip install -r requirements-dev.txt
```

### Environment Variables
Make a copy of the `.env_sample` file named `.env`, and fill in the fields appropriately.

### Create/migrate Postgres database
We're going to use a Postgres database to store image metadata.  It doesn't really matter where your Postgres server is hosted, so long as you can fill in the public IP and user/password information in the `.env` file.  I have mine hosted in Google Cloud.

To create the initial database, run
```
source .env
python -m common.init_db
```
This will create an new database (idempotently) with the name set in `.env`.

Then, to perform migrations, navigate to `common/migrations` and run
```
alembic upgrade head
```
That's it!

### Google cloud storage
We'll use a GCS bucket for storing image files. You'll need to spin up a google cloud storage bucket, and set your project ID/bucket name in `.env`.

### Docker
You'll need docker to build the application containers.  https://www.docker.com/get-started/

## Local Usage
You can run the archiver and server locally but they'll still connect to the cloud database and bucket.  So, you'll need to be able to authenticate to GCS.  Go ahead and [install the gcloud command line tools](https://cloud.google.com/sdk/docs/install), then set up authentication by running
```
gcloud auth application-default login
```
The keys created by this step will be passed into the docker containers - it's handled in `docker-compose.yml`.


### Image archiver
To archive an image:
```
docker-compose build archiver
docker-compose up archiver
```

You can verify that a new image exists in your GCS bucket, and that your database "images" table has a new row.

### Backend App
The backend app exposes an API with a `/images/nearest?timestamp=<timestamp>` that returns the nearest image to that timestamp in the database.

To start the server locally:
```
docker-compose build server
docker-compose up server
```

Exercise the server by visiting
`http://127.0.0.1:5000/images/nearest?timestamp=1672531200` in a browser.  Insert a recent unix timestamp (e.g. 1731955206), and you should see the nearest archived image!

## Setting up the cloud system
We want to push our images up to a google cloud container registery.  First,
```
gcloud auth configure-docker
```

Then, just run
```
docker-compose build
docker-compose push
```

And that should work!

### Archiver
Create a cloud run function using the container we've just pushed.  Make sure you update the DATABASE_URL, GC_PROJECT_ID, and GCS_BUCKET_NAME env variables.  Also, the DATABASE_URL should be in unix socket format, e.g. `postgresql://<username>:<password>@/dbname?host=/cloudsql/PROJECT_ID:REGION:INSTANCE_NAME`, and you should add your cloud sql database in the "connections" configuration.

Once you've verified the cloud run job works, you can schedule it to run hourly (or as often as you like) via the "triggers" tab.


### Server
The easiest solution is to deploy the container as a cloud run function.  Create a new cloud run service, select the latest `waddell-wind/service` container that you pushed to the artifact registry.  Follow similar setup to the archiver cloud run job (same env variables and set up connection to cloud sql database).  Make sure to allow unauthenticated invocations, and to allow all ingress.

Once deployed, exercise the service by copying the endpoint url and appending the nearest image endpoint URI.  E.g.:
`https://service-name-554112691235.us-central1.run.app/images/nearest?timestamp=173321300`

That completes the backend system!

## Development
If you make changes to the database, you can generate new migrations by navigating to `common/migrations` and running
```
alembic revision --autogenerate
```
