# fitsync

An application that automatically syncs non GPS tracked Fitbit activities to Strava

## Run application

1. Poetry install: `poetry install`
1. Run database: `docker-compose up -d --remove-orphans`
1. Ensure contents in .env file. Refer to `.env.example`
1. Run application: `poetry run uvicorn main:app --reload`
1. Create a password hash for your user: `poetry run python ./generate_password.py`
1. Insert users into DB:

    ```bash
        \c fitsync
        insert into users (username, password) values ('<username>', '<brcypt password>');
    ```

1. Make API call: `http POST 'http://127.0.0.1:8000/token' username=<username> password=<password> -f`
