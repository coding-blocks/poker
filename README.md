# Poker

An application that makes an Http request periodically on the given endpoint. This gives us more control rather than using crontab or agendajs.

## Project explanation

Poker is a django web server that creates and schedules jobs for making HTTP request to some endpoint.
We use python's crontab package for managing cronjobs.

These jobs are created inside crontab as soon as a Job object is created either through admin panel or through django shell. 

## Setting pipenv in python
We use pipenv for packaging and dependency management in the project.

Pipenv is a packaging tool for Python that solves some common problems associated with the typical workflow using pip, virtualenv, and the good old requirements.txt.

In addition to addressing some common issues, it consolidates and simplifies the development process to a single command line tool.

Install pipenv using:
```shell script
pip install pipenv
```
Next, create and activate the virtual python environment:
```shell script
pipenv shell
```
Pipfile contains all the python packages required in the project, which could be installed simply using
```shell script
pipenv install
```
## Setup database
**Install postgres**

We use PostgreSql as database. In order to setup a local PSQL server on your machine, see [this](https://tutorial-extensions.djangogirls.org/en/optional_postgresql_installation/)
 
**Create Database**

Now create a database using `createdb` command with dbname as `poker`
```shell script
createdb poker
```
## Environment variables 
Environment variables are a way to store/pass some sensitive/config information that is required by the software. This can include passwords, secret keys, config variables.

We need to pass database config variable through `.env` file. 
Create a `.env` file in the root directory of the project, with variables : `DB_USER`, `DB_NAME`, `DB_HOST` and `DB_PASSWORD`.

See `.env.example` for reference.

Perform database migration:
```shell script
python manage.py migrate
```
Create a superuser to access admin panel:
```shell script
python manage.py createsuperuser
```
Now run the development server:
```shell script
python manage.py runserver
```

Open `http://localhost:8000/admin` to access admin panel and create jobs with appropriate URLs.

## Project Structure
* `cron`: Django application that stores and handles Cron Jobs in the databases and synchronizes them with the crontab.

* `scripts`: Contains script for making http request to a given URL, request method and authentication token could be specified in the program arguments.

* `services`: Contains services such as `CrontabService`, and allows creation, deletion and refresh of jobs in the crontab.

* `poker`: Contains app settings, server configuration and url routes.

## Using Docker

Alternatively, the application could be run as docker containers, running the API server and one running postgres.

Install docker from [here](https://docs.docker.com/engine/install/ubuntu/) 

Make sure that docker is properly installed in your system.
```shell script
docker run hello-world
```

### Building the Docker container

In order to build the docker container for poker API from `Dockerfile`, use:
```shell script
docker build -t codingblocks/poker .
```
### Running docker container
Since this is a multi-container application, use `docker-compose` to create and start all the services from the configuration.
```shell script
docker-compose up
```