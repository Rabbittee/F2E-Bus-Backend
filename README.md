# F2E-Bus-Backend

## Table Of Contents

- [About the Project](#about-the-project)
- [Requirements](#requirements)
- [Redis](#redis)
- [Local development](#local-development)
- [Docker](#docker)

## About the Project

## Requirements

## Redis

For Local Development

```shell
docker run --name test-redis -d -p 6379:6379 redis
```

Connect Remote Redis

```shell
docker run -it --rm redis redis-cli
    -h ec2-50-19-118-165.compute-1.amazonaws.com \
    -p 24369 \
    -a pb3361052f6a0bdbd5bc124d1b5a523514e7a5757d47847c5d61d575af6299d4b
```

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
