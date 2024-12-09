# README

## Setting Up Cloud Infrastructure
We can provision resources in an automated and more reproducible way using Terraform.  Install terraform and navigate to the `infrastructure` directory.

### Authentication
Go ahead and [install the gcloud command line tools](https://cloud.google.com/sdk/docs/install), then set up authentication by running
```
gcloud auth application-default login
```

### Environment Variables
Make a copy of the `.env_sample` file named `.env`, and fill in the missing fields appropriately.  Note that some of the variables can't be set until the resources are provisioned, such as the database public IP.  Load the environmental variables with `source .env`.

### Provision Storage Resources
The GCS Bucket and Postgres Configurations are in `main.tf`.  First, iniliatize terraform via
`terraform init`.

Then, review the changes with `terraform plan`, and apply with `terraform apply`.

### Complete .env setup
Now that the resources are provisioned, fill in any remaining variables in .env, such as the database public IP.  You can view that in the cloud console.

## Initialize Database

### Requirements
Python 3.13 recommended.  For setup, we'll need to set up a minimal dev environment:
```
python -m venv venv_dev
source venv_dev/bin/activate
pip install -r requirements-dev.txt
```

### Create/migrate Postgres database
To create the initial database, run
```
source .env
python -m common.init_db
```
This will (idempotently) create a new database (on the instance that the DATABASE_URL env variable points to) with the name set in `.env`.

Then, to perform migrations, navigate to `common/migrations` and run
```
alembic upgrade head
```
That's it!

## Run Applications Locally
### Docker
You'll need docker to build the application containers.  https://www.docker.com/get-started/

## Authentication
You should have already set up GCP application default credentials when setting up infrastructure.  The keys created by that step will be passed into the docker containers - it's handled in `docker-compose.yml`.

### Image archiver
To archive an image:
```
docker-compose build archiver
docker-compose up archiver
```

You can verify that a new image exists in your GCS bucket, and that your database's "images" table has a new row.

### Backend App
The backend app exposes an API with a `/images/nearest?timestamp=<timestamp>` that returns the nearest image to that timestamp in the database.

To start the server locally:
```
docker-compose build server
docker-compose up server
```

Exercise the server by visiting
`http://127.0.0.1:5000/images/nearest?timestamp=<timsestamp>` in a browser.  Insert a somewhat recent unix timestamp (e.g. 1731955206), and you should get a response that includes the image data and the time of archival.

### Frontend
You will need to modify the `apiURL` in `frontend/basic.html`, to point to `http://127.0.0.1:5000/...` rather than a public URL.  Then, launch a local http server using `python -m http.server 8000`, then navigate to `127.0.0.1:8000` in a browser.  Navigate to and open `frontend/basic.html`, and try it out!

## Set up applications in the cloud
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
We'll need to enable a few gcloud cli services:
```
gcloud services enable run.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
```
Then run
```
source .env
bash infrastructure/deploy_archiver.sh
```
This only needs to be done once.  The job points to the 'latest' tagged archiver Docker image, so to update the job with a newly built image, simply push the image to the Google Container registry with `docker-compose push`.

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
