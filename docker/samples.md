## Current default docker-compose for projects

    version: "3.7"

    services:
    web:
        build: .
        command: sh -c 'python manage.py collectstatic --no-input &&
                python manage.py makemigrations &&
                python manage.py migrate &&
                python manage.py runserver 0.0.0.0:8000'
        volumes:
        - .:/usr/src/server/
        ports:
        - "8000:8000"
        env_file:
        - .env
        depends_on:
        - db
    db:
        image: postgres:12.0-alpine
        volumes:
        - postgres_data:/var/lib/postgresql/data/
        environment:
        - POSTGRES_USER=postgres
        - POSTGRES_PASSWORD=postgres
        - POSTGRES_DB=postgres
    volumes:

### If need celery then add this service

    redis:
        image: redis
        ports:
        - "6379:6379"

## Current default Dockerfile

    FROM python:3.9.0

    WORKDIR /usr/src/server

    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1

    RUN pip install --upgrade pip
    COPY requirements.txt .
    RUN pip install -r requirements.txt

    COPY . .

## docker-compose for python script

    version: "3.7"

    services:
    main:
        build: .
        volumes:
        - .:/usr/src/app
        env_file:
        - .env

## Dockerfile for python script

    FROM python:3.9.0

    RUN pip install --upgrade pip

    COPY . ./
    RUN pip install -r requirements.txt

    ENTRYPOINT ["python", "bot.py"]


## Magical image that will find and install everything from requirements.txt.

## Dockerfile

    FROM python:3-onbuild

    COPY . .
    CMD ["python", "main.py"]

## Minimalistic docker-compose for small web apps, flask for example, works w dockerfile above

    version "3"

    services:
        app:
            build: .
            volumes:
                -.: /usr/src/app
            ports:
                - 5001:80
