### Dependencies
- [docker](https://docs.docker.com/get-docker)
- [docker-compose](https://docs.docker.com/compose/install)


### Example usage
```
# clone
git clone git@github.com:kjurek/objectivity.git

# build
cd objectivity/web_app
make build

#run
make run

# create dataset from data.csv file
curl -L -F "dataset=@data.csv" localhost:5057/dataset

# it will return id of created dataset in the response (or return existing one)
{"id":1}

# train new model
curl -XPOST localhost:5057/fit/1

# it will return id of created model in the response (or return existing one)
{"id":1}

# get prediction using model from previous steps, input data is passed as csv file (input.csv in this example)
curl -XGET -L -F "input_data=@input.csv" localhost:5057/predict/1

# endpoint will return prediction
[225.87962962962962]

```


### Build
Project includes Makefile with helper commands for building, runing and testing the application.
There are two docker files, `web_app/docker/Dockerfile` is for local environment and `web_app/docker/DockerfileTests` is for testing, linting and requirements generation.

```
git clone git@github.com:kjurek/objectivity.git
cd objectivity/web_app
make build
```

### Python requirements
Requirements generator generates `requirements.txt` file from `requirements.in` file using proper python version.
It may ask for a sudo password because docker is launching as a root user so generated file owner is root.
To avoid this problem this make step includes `sudo chown $(USER):$(USER) requirements.txt` command.

```
make requirements
```

### Linter
Checks code with flake-8 and bandit

```
make lint
```

### Tests
Runs unit tests

```
make test
```

### Run
Runs main application

```
make run

```

### Environments and configuration
Currently there is only one production-like environment `local` and it's called `web_app` in `docker-compose.yml`.
There is also a testing service which has separate PostgreSQL instance to avoid deleting data from other environments, it's called `web_app_tests`.
Both services are configured using environment variables which are stored in the `web_app/env` folder.

### Docs
When application is running it publish following endpoints:
- Swagger documentation: http://localhost:5057/docs
- Redoc documentation: http://localhost:5057/redoc
