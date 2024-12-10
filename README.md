# README

This is a project I undertook to better understand deploying cloud applications.  It's a simple image archival / retrieval system.  It's been archiving since late Nov. 2024, and you can view a basic frontend into the archive [here](https://storage.googleapis.com/waddell-wind-misc/basic.html)!

Following are instructions for setting up the system yourself!

## Setting Up Cloud Infrastructure
We can provision resources in an automated and more reproducible way using Terraform - you'll need to install it before proceeding.

### Authentication
Go ahead and [install the gcloud command line tools](https://cloud.google.com/sdk/docs/install), then set up authentication by running
```
gcloud auth application-default login
```

### Environment Variables
Make a copy of the `.env_sample` file named `.env`, and fill in the missing fields appropriately.  Note that some of the variables can't be set until the resources are provisioned, such as the database public IP.  Load the environmental variables with `source .env`.

### Provision Storage Resources
Navigate to the `infrastructure` directiory.  The GCS Image and Frontend buckets and Postgres Configurations are in `main.tf`.  First, iniliatize terraform via
`terraform init`.

Then, review the changes with `terraform plan`, and apply with `terraform apply`.

### Complete .env setup
Now that the resources are provisioned, fill in any remaining variables in .env, such as the database public IP.  You can view that in the cloud console.

## Initialize Database
Navigate back to the project root.
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

### Creating new migrations
If you make changes to the database, you can generate new migrations by navigating to `common/migrations` and running
```
alembic revision --autogenerate
```


## Run Applications Locally
To connect to the database locally, you'll need to go into the cloud console and add your local IP address to the set of authorized networks.  This isn't necessary for running the applications in the cloud.
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
The backend app exposes an API with a single endpoint, which returns the nearest image to a provided timestamp.

To start the server locally:
```
docker-compose build server
docker-compose up server
```

Exercise the server by visiting
`http://127.0.0.1:5000/images/nearest?timestamp=<timestamp>` in a browser.  Insert a somewhat recent unix timestamp (e.g. 1731955206), and you should get a response that includes the image data and the time of archival.

### Frontend
You will need to replace `{{API_URL}}` in `frontend/basic.html` with `http://127.0.0.1:5000`.  Then, launch a local http server using `python -m http.server 8000`, then navigate to `127.0.0.1:8000` in a browser.  Navigate to and open `frontend/basic.html`, and try it out!

## Set up applications in the cloud
First we'll want to push our images up to a google cloud container registery.  First,
```
gcloud auth configure-docker
```

Then, just run
```
docker-compose build
docker-compose push
```

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
Just run
```
source .env
bash infrastructure/deploy_server.sh
```
Same as archiver, this only needs to be done once, as it's pinned to the 'latest' tagged server Docker image - update via pushing a new one.

Once deployed, exercise the service by copying the endpoint url and appending the nearest image endpoint URI.  E.g.:
`https://service-name-554112691235.us-central1.run.app/images/nearest?timestamp=173321300`

Or, replace `{{API_URL}}` in the frontend with the base url and give that a try.

### Frontend
To deploy the frontend, just run
```
bash infrastructure/deploy_frontend.sh <API_URL>
```
Where <API_URL> is the url of the deployed cloud run server.  This script will inject the url into the html, then upload the file to the public frontend bucket.  Make sure you haven't modified the html file and removed the {{API_URL}} tag, which is used for the injection.

# Thanks
That's all!  Thanks for checking out this project.  Hope you find out Waddell was glassy last week and you totally missed out.  Now if only this thing could tell us the conditions tommorrow...
