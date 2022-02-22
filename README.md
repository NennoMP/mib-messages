# Message In A Bottle - Messages

[![CircleCI](https://circleci.com/gh/NennoMP/mib-messages.svg?style=svg)](https://app.circleci.com/pipelines/github/NennoMP/mib-messages)
[![codecov](https://codecov.io/gh/NennoMP/mib-messages/branch/main/graph/badge.svg?token=7GC2OZW43F)](https://codecov.io/gh/NennoMP/mib-messages)

This is the source code of My Message in a Bottle Messages microservice, project of **Advanced Software Engineering** course of the MSc in Computer Science,
University of Pisa.

#### Members

Mark with *bold* the person(s) that has developed this microservice.

|Name and Surname    | Email                         |
|--------------------|-------------------------------|
|*Laura Norato*      |l.norato@studenti.unipi.it     |
|*Emanuele Albertosi*|20783727@studenti.unipi.it     |
|*Michele Zoncheddu* |m.zoncheddu@studenti.unipi.it  |
|*Alessio Russo*     |a.russo65@studenti.unipi.it    |
|*Matteo Pinna*      |m.pinna10@studenti.unipi.it    |


## Overview
This microservice implements the Messages logic, messages-related backend features, and maintains the corresponding database. Its services are available to the **mib-api-gateway** through APIs, you can test the APIs by running the microservice and then by accessing the Swagger interface with */ui*. In addition, you can find the APIs specifications in the corresponding settings file *mib/specifications/<file-name>.yml*.

## Instructions
The available environments are:

- debug
- development
- testing
- production

If you want to run the appliction with development environment, or you are developing the application and you want to have the debug tools, you can start the application locally (without `docker-compose`) by executing `bash run.sh`.

**Note:** if you use `docker-compose up` you are going to startup a production ready microservice, hence postgres will be used as default database and gunicorn will serve your application.


### Run the project
You can run the entire application by following the instructions on the main repository mib-main. However, if you would like to separately run the User microservice take a look at the steps below.

#### Initialization
First, you need to setup create a virtual environment and to install all requirements. Run these commands inside **mib-messages** root:

1. Create a virtual environment with `virtualenv venv`.
3. Activate it with `source venv/bin/activate` or `source venv/scripts/activate`.
4. Install all requirements needed with `pip install -r requirements.dev.txt`.

#### Run
You can now run the project running the following commands:

1. Run the microservice with `bash run.sh` (environment is automatically set to development).

#### Testing
In order to execute the tests you need, if you haven't already, to install the requirements by following the steps mentioned above. When you're done, you can run the tests:

1. Set Flask environment to testing with `export FLASK_ENV=testing`
2. Run the tests with `pytest`

The tests are set to file when the coverage is below 90%.

You can also specify one or more specific test files, in order to run only those specific tests. In case you also want to see the overall coverage of the tests, execute the following command:

`python -m pytest --cov=mib`

In order to know what are the lines of codes which are not covered by the tests, execute the command:

`python -m pytest --cov-report term-missing`

