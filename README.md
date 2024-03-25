# Pyspark test project


---

http://localhost:8000/docs Swagger documentation\
http://localhost:8000/redoc ReDoc documentation

## Project structure

```shell
$ tree .
ns_app
├── __main__.py             # Startup script. Starts uvicorn.
├── db                      # Database module.
│   ├── config.py           # Database configuration.
│   ├── dao                 # Data access objects.
│   │   └── task_dao.py     # Task DAO.
│   ├── helpers.py          # Database helpers.
│   ├── migrations          # Database migrations.
│   │   └── models
│   └── models              # Database models.
│       ├── files_model.py
│       └── task_model.py
├── dto                     # Data transfer objects.
│   ├── base.py
│   └── task.py
├── enum                    # Enumerations.
│   ├── metadata.py
│   └── task.py
├── services                # Services.
│   ├── redis               # Redis service.
│   │   └── lifetime.py
│   ├── s3                  # S3 service.
│   │   └── paginator.py
│   └── spark               # Spark service.
│       ├── client.py
│       ├── reader.py
│       ├── session.py
│       ├── udf.py
│       └── writer.py
├── settings.py             # Main configuration settings for project.
├── web                     # Web module.
│   ├── api                 # API handlers.
│   │   ├── monitoring
│   │   ├── router.py
│   │   └── tasks
│   ├── application.py      # FastAPI application configuration.
│   └── lifetime.py         # Actions to perform on application startup and shutdown.
└── workers                 # Workers.
    ├── broker.py
    ├── helpers.py
    └── tasks.py
```

## Configuration

This application can be configured with environment variables.

All environment variables should start with `NSAPP_` prefix.

For example if you see in your `ns_app/settings.py` a variable named like
`random_parameter`, you should provide the `NS_APP__RANDOM_PARAMETER`
variable to configure the value.

An example of `.env.*` file:

```shell
NSAPP_RELOAD=True
NS_APP_PORT=8000
```

## Initial setup

##### Install Poetry

Follow the official [Poetry Installation Manual](https://python-poetry.org/docs/#installation).

##### Set local Python version

Follow the official [Pyenv Installation Manual](https://github.com/pyenv/pyenv#installation).

```shell
pyenv local <python version>
```

##### Set up virtual environment

```shell
poetry env use $(pyenv which python)
```

##### Install dependencies

```shell
poetry install
```

##### Install pre-commit hooks

```shell
poetry run pre-commit install
```

After that all linters will be run on every `git commit`.


## Developer Tasks

##### Emulate local DB

Spin up a fresh PostgreSQL instance locally:

```shell
make db-up
```

Run database migration in a local PostgreSQL instance:

```shell
make db-migrate
```


Shut down the local PostgreSQL instance:

```shell
make db-down
```

##### Run Python code locally

```shell
make run
```

##### Full local dev environment

Spin up full dev environment emulation (code + db) locally using Docker Compose:

```shell
make compose-dev
```
