# F2E-Bus-Backend

## Table Of Contents

- [About the Project](#about-the-project)
- [Local development](#local-development)
- [Docker](#docker)

## About the Project

## Local development

Create the virtual environment and install dependencies with:

```sh
poetry install
```

See the [poetry docs](https://python-poetry.org/docs/) for information on how to add/update dependencies.

Run commands inside the virtual environment with:

```shell
poetry run start
```

Run Redis for local development

```shell
docker run --name test-redis -d -p 6379:6379 redis
```

## Docker

Build image with:

```shell
docker build --tag f2e-bus-backend .
```

Run image with:

```shell
docker run \
    -p 8000:80 \
    --env-file .env \
    -d \
    f2e-bus-backend
```
