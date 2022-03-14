# QuickCheck Python Developer Case Study

This repository houses the code for the QuickCheck Python Developer Case Study - A Django application for indexing items from Hackernews and exposing them through an API with CRUD functionalities e.t.c.

Case study can be found [here](https://form.jotform.com/211856214308452) 

## Retrieve code

-   `$ git clone https://github.com/madewithkode/quickcheck_test.git`

## Requrements

This project requires the following system dependencies:


*   Python 3.9

*   PostgreSQL

*   RabbitMQ

*   Virtualenv(Recommended)

## Setup

#### Database

Create a PostgresSQL database following the configurations on `src/qc_interview_test/settings/dev.py`

`$ sudo -u postgres psql`

`postgres=# create database <database_name>;`

`postgres=# create user <user_name> with encrypted password '<password>';`

`postgres=# grant all privileges on database <database_name> to <user_name>;`

#### Environment Variables

This project requires a `.env` file with the following variables, please create one in the project's root folder and supply the relevant credentials according to your local setup.

*   DEBUG
*   SECRET_KEY
*   DATABASE_HOST
*   DATABASE_NAME
*   DATABASE_USERNAME
*   DATABASE_PASSWORD
*   BROKER_URL

## Running


-   `$ virtualenv -p /usr/bin/python3.9 virtualenv`  - While in the project root, run this to create a virtual environment named virtualenv.(This assumes you've installed virtualenv earlier.)
-   `$ pip install requirements.txt` - While in the project root, run this to install all external packages required to run project.
-   Cd into `src` folder and run `$ python manage.py migrate` This applies the project's migration(if any)
-   While still in `src` folder, run `$ python manage.py ingest_first_time` This initially ingests the latest 100 items from Hackernews into the local DB according to requirements.
-   While still in `src` folder, run `$ python manage.py collectstatic` This collects static files from around the app and puts into the `STATIC_ROOT` configuration defined in `qc_interview_test.settings.base` in order to be able to serve them. Note: This is not recommended for production.
-   While still in `src` folder, run `$ python manage.py runserver` This should now start the django app at the default localhost:8000
-   In a new terminal, cd into `src` and run `celery -A qc_interview_test.settings.celery.CELERY beat -l info` to start celery beat for periodic(5 minutes interval) indexing of new content.


## Front End

This app contains a simple frontend for listing, searching and filtering indexed items. It is located in the `hackernews_frontend` directory. It is recommended to access this frontend over http, to do this, using your preferred http local server tool(e.g Liveserver for VSCode), start the server in the `hackernews_frontend` root. Once this is started, take note of the port, and add it to the `CORS_ORIGIN_WHITELIST` configuration  located at `qc_interview_test.settings.dev`. This is to allow Cross-Origin Resource Sharing(CORS) between the frontend and backend services.


## Endpoints

The full documentation can be found at `/api/docs`, the following is a rundown of available endpoints:

-  GET `/api/v1/hackernews/items/`  - This endpoint fetches paginated results of all indexed and locally created items. It also supports filtering items by type(e.g story, job, poll e.t.c) using a query parameter `type`.

-  POST `/api/v1/hackernews/add/` - This endpoint is used to create a new item locally as against fetching from Hackernews.

-  GET `/api/v1/hackernews/search/` - This endpoint is used to search for items by title/content. It requires a `search` query parameter with the search keyword being its value.

-  DELETE `/api/v1/hackernews/delete/<item_id>/` - This endpoint deletes a given item, provided it wasn't indexed externally from Hackernews, i.e it was locally created.

-  PUT `/api/v1/hackernews/update/` - This endpoint updates a given item, provided it wasn't indexed externally from Hackernews, i.e it was locally created.
