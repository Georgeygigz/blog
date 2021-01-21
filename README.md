# My blog
- This is a web that allows users to:
    - Create Articles,
    - List Articles,
    - Update Articles, 
    - Delete Articles,

## Requirements
- [Python 3.8](https://www.python.org/)
- [Pipenv](https://pypi.org/project/pipenv/)
- [Postgres](https://www.postgresql.org/)

## How to set this manualy

- `git clone https://github.com/Georgeygigz/blog`
- `cd blog` to navigate to the project folder
- `pipenv shell` to create and activate virtual env
- `pipenv install` to insall the dependencies
- `touch .env` to create a new env file
- `source .env` to source env variables
- copy and paste the sample env and replace with your actual credentials
- `python manage.py migrate` to apply all the migrations
- `python manage.py runserver` to start the server
- Navigate to `http://127.0.0.1:8000` to visit the site

## Sample env 
- export DB_NAME=<your_db_name>
- export DB_USER=<your_db_user>
- export DB_PASS=<your_db_pass>
- export DB_HOST=<your_db_host>
- export DB_PORT=<your_db_port>
- Note: There is no space next to '='
